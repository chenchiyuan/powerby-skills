/**
 * ASP 生命周期与 Git 分支自动化集成层
 */

const { createError } = require('../core/errors');
const { checkBranchCompliance: runComplianceCheck } = require('../core/branch-compliance');
const { detectMergeConflicts } = require('../core/merge-conflict-detector');
const {
  generateBranchHistoryReport,
  updateBranchHistoryReport,
  enrichMergeRecord
} = require('../core/branch-history-generator');
const {
  ensureIterationRecord,
  getIterationRecord,
  updateIterationBranchInfo
} = require('../core/iteration-tracker');
const { buildIterationBranchName, validateIterationId } = require('../core/iteration-branch');
const {
  branchExists,
  createBranchFromSource,
  mergeBranch,
  deleteBranch,
  deleteRemoteBranch,
  remoteBranchExists,
  getCurrentBranch,
  getLastCommit,
  getGitUser,
  checkoutBranch,
  isWorkingTreeClean
} = require('../utils/git');

/**
 * 获取已记录的分支信息，并验证分支状态。
 * @param {string} iterationId - 迭代编号。
 * @param {string} expectedStatus - 期望状态。
 * @param {string} cwd - 项目根目录。
 * @returns {{iteration: Object, branchInfo: Object}} 当前迭代与分支信息。
 */
function requireBranchInfo(iterationId, expectedStatus, cwd = process.cwd()) {
  const iteration = getIterationRecord(iterationId, cwd);
  const branchInfo = iteration.branch_info;

  if (!branchInfo || !branchInfo.branch_name) {
    throw createError('E010', `迭代缺少 branch_info: iterationId="${iterationId}"`);
  }

  if (expectedStatus && branchInfo.status !== expectedStatus) {
    throw createError(
      'E013',
      `迭代分支状态不满足要求: expected="${expectedStatus}" actual="${branchInfo.status}"`
    );
  }

  return { iteration, branchInfo };
}

/**
 * 创建标准分支信息对象。
 * @param {string} branchName - feature 分支名。
 * @param {string} sourceBranch - 源分支。
 * @param {string} targetBranch - 目标分支。
 * @returns {Object} 分支状态对象。
 */
function buildActiveBranchInfo(branchName, sourceBranch, targetBranch) {
  return {
    branch_name: branchName,
    status: 'active',
    created_at: new Date().toISOString(),
    merged_at: null,
    deleted_at: null,
    source_branch: sourceBranch,
    target_branch: targetBranch,
    merge_commit_hash: null,
    remote_status: 'not_pushed'
  };
}

/**
 * 创建并切换到标准迭代 feature 分支。
 * @param {string} iterationId - 迭代编号。
 * @param {string} iterationName - 迭代名称。
 * @param {string} sourceBranch - 源分支，默认 `develop`。
 * @param {Object} options - 运行选项。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<Object>} 分支创建结果。
 */
async function createIterationBranch(
  iterationId,
  iterationName,
  sourceBranch = 'develop',
  options = {}
) {
  const cwd = options.cwd || process.cwd();
  validateIterationId(iterationId);

  if (typeof sourceBranch !== 'string' || sourceBranch.trim() === '') {
    throw createError('E008', `sourceBranch 不能为空: actual="${sourceBranch}"`);
  }

  const branchName = buildIterationBranchName(iterationId, iterationName);

  ensureIterationRecord({ iterationId, iterationName, phase: 'P1', cwd });

  if (!(await branchExists(sourceBranch, cwd))) {
    throw createError('E015', `源分支不存在: sourceBranch="${sourceBranch}"`);
  }

  if (await branchExists(branchName, cwd)) {
    throw createError('E001', `branch="${branchName}"`);
  }

  await createBranchFromSource(branchName, sourceBranch, cwd);

  updateIterationBranchInfo({
    iterationId,
    iterationName,
    phase: 'P1',
    branchInfo: buildActiveBranchInfo(branchName, sourceBranch, sourceBranch),
    cwd
  });

  return {
    success: true,
    branchName,
    message: `已从 ${sourceBranch} 创建并切换到 ${branchName}`
  };
}

/**
 * 执行迭代分支规范检查。
 * @param {string} iterationId - 迭代编号。
 * @param {string} phase - 生命周期阶段。
 * @param {Object} options - 运行选项。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<Object>} 合规检查报告。
 */
async function checkIterationBranchCompliance(iterationId, phase, options = {}) {
  return runComplianceCheck({ iterationId, phase, cwd: options.cwd || process.cwd() });
}

/**
 * 切换到迭代 feature 分支。
 * @param {string} iterationId - 迭代编号。
 * @param {Object} options - 运行选项。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<Object>} 切换结果。
 */
async function switchIterationBranch(iterationId, options = {}) {
  const cwd = options.cwd || process.cwd();
  const { iteration, branchInfo } = requireBranchInfo(iterationId, null, cwd);
  const currentBranch = await getCurrentBranch(cwd);

  if (currentBranch === branchInfo.branch_name) {
    return {
      success: true,
      branchName: branchInfo.branch_name,
      message: `当前已在目标分支 ${branchInfo.branch_name}`
    };
  }

  if (!(await branchExists(branchInfo.branch_name, cwd))) {
    throw createError('E014', `目标分支不存在: branch="${branchInfo.branch_name}"`);
  }

  if (!(await isWorkingTreeClean(cwd))) {
    throw createError('E011', `切换前工作区必须干净: currentBranch="${currentBranch}"`);
  }

  await checkoutBranch(branchInfo.branch_name, cwd);

  return {
    success: true,
    branchName: branchInfo.branch_name,
    message: `已切换到 ${branchInfo.branch_name}`,
    iteration: iteration.full_name
  };
}

/**
 * 执行迭代合并冲突预检测。
 * @param {string} iterationId - 迭代编号。
 * @param {string} targetBranch - 目标分支。
 * @param {Object} options - 运行选项。
 * @returns {Promise<Object>} 冲突检测结果。
 */
async function detectIterationMergeConflicts(iterationId, targetBranch = 'develop', options = {}) {
  const cwd = options.cwd || process.cwd();
  const { branchInfo } = requireBranchInfo(iterationId, 'active', cwd);
  return detectMergeConflicts({
    sourceBranch: branchInfo.branch_name,
    targetBranch,
    cwd
  });
}

/**
 * 将当前迭代分支合并到目标分支。
 * @param {string} iterationId - 迭代编号。
 * @param {string} targetBranch - 目标分支，默认 `develop`。
 * @param {Object} options - 运行选项。
 * @param {string} options.cwd - 项目根目录。
 * @param {string} options.commitMessage - 自定义合并提交信息。
 * @returns {Promise<Object>} 合并结果。
 */
async function mergeIterationBranch(iterationId, targetBranch = 'develop', options = {}) {
  const cwd = options.cwd || process.cwd();
  validateIterationId(iterationId);

  if (!(await isWorkingTreeClean(cwd))) {
    const currentBranch = await getCurrentBranch(cwd);
    throw createError('E011', `合并前工作区必须干净: currentBranch="${currentBranch}"`);
  }

  const { iteration, branchInfo } = requireBranchInfo(iterationId, 'active', cwd);

  if (!(await branchExists(branchInfo.branch_name, cwd))) {
    throw createError('E014', `待合并分支不存在: branch="${branchInfo.branch_name}"`);
  }

  if (!(await branchExists(targetBranch, cwd))) {
    throw createError('E015', `目标分支不存在: targetBranch="${targetBranch}"`);
  }

  const conflictResult = await detectIterationMergeConflicts(iterationId, targetBranch, { cwd });
  if (conflictResult.hasConflict) {
    return {
      success: false,
      hasConflict: true,
      conflictFiles: conflictResult.conflictFiles,
      message: conflictResult.message
    };
  }

  await generateBranchHistoryReport(iterationId, { cwd });

  await mergeBranch(branchInfo.branch_name, targetBranch, {
    noFF: true,
    commitMessage: options.commitMessage || `merge(iteration): ${branchInfo.branch_name} into ${targetBranch}`
  }, cwd);

  const [latestCommit, gitUser] = await Promise.all([
    getLastCommit(cwd),
    getGitUser(cwd)
  ]);

  const mergeRecord = await enrichMergeRecord({
    merge_commit_hash: latestCommit ? latestCommit.hash : null,
    merger: gitUser.name,
    merger_email: gitUser.email,
    merged_at: new Date().toISOString(),
    source_branch: branchInfo.branch_name,
    target_branch: targetBranch
  }, cwd);

  await updateBranchHistoryReport(iterationId, mergeRecord, { cwd });

  updateIterationBranchInfo({
    iterationId,
    iterationName: iteration.name,
    phase: 'P8',
    branchInfo: {
      ...branchInfo,
      status: 'merged',
      target_branch: targetBranch,
      merged_at: mergeRecord.merged_at,
      merge_commit_hash: latestCommit ? latestCommit.hash : null
    },
    cwd
  });

  return {
    success: true,
    hasConflict: false,
    branchName: branchInfo.branch_name,
    message: `已将 ${branchInfo.branch_name} 合并到 ${targetBranch}`,
    mergeCommitHash: latestCommit ? latestCommit.hash : null
  };
}

/**
 * 删除已合并的本地迭代分支。
 * @param {string} iterationId - 迭代编号。
 * @param {Object} options - 运行选项。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<Object>} 删除结果。
 */
async function deleteIterationBranch(iterationId, options = {}) {
  const cwd = options.cwd || process.cwd();
  validateIterationId(iterationId);

  const { iteration, branchInfo } = requireBranchInfo(iterationId, 'merged', cwd);
  const currentBranch = await getCurrentBranch(cwd);

  if (currentBranch === branchInfo.branch_name) {
    throw createError('E013', `不能删除当前分支: branch="${branchInfo.branch_name}"`);
  }

  if (!(await branchExists(branchInfo.branch_name, cwd))) {
    throw createError('E014', `待删除分支不存在: branch="${branchInfo.branch_name}"`);
  }

  await deleteBranch(branchInfo.branch_name, cwd);

  let nextStatus = 'deleted';
  let remoteDeleted = false;

  if (await remoteBranchExists(branchInfo.branch_name, 'origin', cwd)) {
    try {
      await deleteRemoteBranch(branchInfo.branch_name, 'origin', cwd);
      remoteDeleted = true;
    } catch (error) {
      nextStatus = 'deleted_local_only';
    }
  }

  updateIterationBranchInfo({
    iterationId,
    iterationName: iteration.name,
    phase: 'P8',
    branchInfo: {
      ...branchInfo,
      status: nextStatus,
      deleted_at: new Date().toISOString()
    },
    cwd
  });

  return {
    success: true,
    branchName: branchInfo.branch_name,
    remoteDeleted,
    message: nextStatus === 'deleted_local_only'
      ? `已删除本地分支 ${branchInfo.branch_name}，但远程分支删除失败`
      : `已删除本地分支 ${branchInfo.branch_name}`
  };
}

module.exports = {
  createIterationBranch,
  checkIterationBranchCompliance,
  switchIterationBranch,
  detectIterationMergeConflicts,
  mergeIterationBranch,
  deleteIterationBranch,
  generateBranchHistoryReport,
  updateBranchHistoryReport
};
