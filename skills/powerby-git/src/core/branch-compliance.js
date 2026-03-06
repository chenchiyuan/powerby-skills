/**
 * 迭代分支合规检查器
 */

const {
  getCurrentBranch,
  getBranchStatus,
  remoteBranchExists,
  getBranchSyncStatus
} = require('../utils/git');
const { createError } = require('./errors');
const { getIterationRecord } = require('./iteration-tracker');
const { buildIterationBranchName, validateIterationId } = require('./iteration-branch');

const DIRTY_PHASES = new Set(['P6', 'P8']);

/**
 * 构建期望分支名。
 * @param {Object} iteration - 迭代记录。
 * @returns {string} 期望分支名。
 */
function resolveExpectedBranch(iteration) {
  if (iteration.branch_info && iteration.branch_info.branch_name) {
    return iteration.branch_info.branch_name;
  }

  if (!iteration.name) {
    throw createError('E010', `迭代缺少名称，无法推导期望分支: iterationId="${iteration.id}"`);
  }

  return buildIterationBranchName(iteration.id, iteration.name);
}

/**
 * 生成工作区脏状态警告。
 * @param {Object} status - Git 状态。
 * @param {string} phase - 生命周期阶段。
 * @returns {Object|null} 警告对象。
 */
function buildWorkingTreeWarning(status, phase) {
  if (status.isClean) {
    return null;
  }

  const changedFiles = [
    ...status.staged,
    ...status.unstaged,
    ...status.not_tracked
  ].length;

  return {
    level: phase === 'P8' ? 'error' : 'warning',
    message: `阶段 ${phase} 要求工作区干净: changedFiles=${changedFiles}`,
    suggestion: '请先执行 git status，随后提交、暂存或清理未提交改动'
  };
}

/**
 * 检查当前分支是否符合迭代约束。
 * @param {Object} options - 检查参数。
 * @param {string} options.iterationId - 迭代编号。
 * @param {string} options.phase - 生命周期阶段，如 P1/P6/P8。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<Object>} 合规检查结果。
 */
async function checkBranchCompliance({ iterationId, phase, cwd = process.cwd() }) {
  validateIterationId(iterationId);

  if (typeof phase !== 'string' || phase.trim() === '') {
    throw createError('E008', `phase 不能为空: actual="${phase}"`);
  }

  const iteration = getIterationRecord(iterationId, cwd);
  const expectedBranch = resolveExpectedBranch(iteration);
  const currentBranch = await getCurrentBranch(cwd);
  const warnings = [];
  let compliant = true;

  if (currentBranch !== expectedBranch) {
    compliant = false;
    warnings.push({
      level: 'warning',
      message: `当前分支与迭代不匹配: current="${currentBranch}" expected="${expectedBranch}"`,
      suggestion: `请执行 git checkout ${expectedBranch}`
    });
  }

  if (DIRTY_PHASES.has(phase)) {
    const branchStatus = await getBranchStatus(cwd);
    const dirtyWarning = buildWorkingTreeWarning(branchStatus, phase);

    if (dirtyWarning) {
      compliant = false;
      warnings.push(dirtyWarning);
    }
  }

  if (phase === 'P8') {
    const hasRemoteBranch = await remoteBranchExists(expectedBranch, 'origin', cwd);

    if (hasRemoteBranch) {
      const syncStatus = await getBranchSyncStatus(expectedBranch, 'origin', cwd);

      if (syncStatus.behind > 0) {
        compliant = false;
        warnings.push({
          level: 'error',
          message: `本地分支落后远程: branch="${expectedBranch}" behind=${syncStatus.behind}`,
          suggestion: `请先执行 git pull --rebase origin ${expectedBranch}`
        });
      }
    } else {
      warnings.push({
        level: 'info',
        message: `远程分支不存在: branch="origin/${expectedBranch}"`,
        suggestion: `如需保留远程协作记录，可执行 git push -u origin ${expectedBranch}`
      });
    }
  }

  return {
    compliant,
    currentBranch,
    expectedBranch,
    warnings
  };
}

module.exports = {
  checkBranchCompliance
};
