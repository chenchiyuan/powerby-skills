/**
 * Git 操作封装
 */

const simpleGit = require('simple-git');
const path = require('path');

/**
 * 获取 Git 实例
 * @param {string} [cwd] - 工作目录
 * @returns {SimpleGit}
 */
function getGit(cwd = process.cwd()) {
  return simpleGit(cwd);
}

/**
 * 获取当前分支名
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<string>}
 */
async function getCurrentBranch(cwd = process.cwd()) {
  const git = getGit(cwd);
  const summary = await git.branch();
  return summary.current;
}

/**
 * 获取所有本地分支
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<string[]>}
 */
async function getAllBranches(cwd = process.cwd()) {
  const git = getGit(cwd);
  const summary = await git.branch();
  return summary.all;
}

/**
 * 获取本地分支（不包含远程分支）
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<string[]>}
 */
async function getLocalBranches(cwd = process.cwd()) {
  const git = getGit(cwd);
  const summary = await git.branch();
  return summary.branches;
}

/**
 * 检查分支是否存在
 * @param {string} branchName - 分支名
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<boolean>}
 */
async function branchExists(branchName, cwd = process.cwd()) {
  const git = getGit(cwd);
  const summary = await git.branch();
  return summary.all.includes(branchName) || Object.keys(summary.branches).includes(branchName);
}

/**
 * 创建并切换分支
 * @param {string} branchName - 分支名
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<void>}
 */
async function createBranch(branchName, cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.checkoutLocalBranch(branchName);
}

/**
 * 删除分支
 * @param {string} branchName - 分支名
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<void>}
 */
async function deleteBranch(branchName, cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.deleteLocalBranch(branchName);
}

/**
 * 检查分支是否已合并到主分支
 * @param {string} branchName - 分支名
 * @param {string} [mainBranch='main'] - 主分支名
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<boolean>}
 */
async function isBranchMerged(branchName, mainBranch = 'main', cwd = process.cwd()) {
  const git = getGit(cwd);

  try {
    // 尝试合并到主分支来检查
    await git.mergeBase('--is-ancestor', branchName, mainBranch);
    return true;
  } catch {
    return false;
  }
}

/**
 * 获取分支状态
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function getBranchStatus(cwd = process.cwd()) {
  const git = getGit(cwd);
  const [status, branchSummary] = await Promise.all([
    git.status(),
    git.branch()
  ]);

  return {
    current: branchSummary.current,
    branches: branchSummary.all,
    isClean: status.isClean(),
    staged: status.staged,
    unstaged: status.unstaged,
    not_tracked: status.not_tracked
  };
}

/**
 * 获取文件的变更状态
 * @param {string[]} [files] - 文件列表
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function getFileStatus(files = [], cwd = process.cwd()) {
  const git = getGit(cwd);
  const status = await git.status();

  const result = {
    staged: [],
    unstaged: [],
    not_tracked: []
  };

  for (const file of files) {
    if (status.staged.includes(file)) {
      result.staged.push(file);
    } else if (status.removed.includes(file)) {
      result.staged.push(file);
    } else if (status.modified.includes(file)) {
      result.unstaged.push(file);
    } else if (status.not_tracked.includes(file)) {
      result.not_tracked.push(file);
    }
  }

  return result;
}

/**
 * 获取最后一次提交的提交信息
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function getLastCommit(cwd = process.cwd()) {
  const git = getGit(cwd);
  const log = await git.log({ maxCount: 1 });
  return log.latest;
}

/**
 * 获取已合并到主分支的分支列表
 * @param {string} [mainBranch='main'] - 主分支名
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<string[]>}
 */
async function getMergedBranches(mainBranch = 'main', cwd = process.cwd()) {
  const git = getGit(cwd);
  const summary = await git.branch();

  const mergedBranches = [];

  for (const branch of summary.all) {
    if (branch === mainBranch) continue;
    if (branch.startsWith('HEAD')) continue;

    try {
      const isMerged = await git.mergeBase('--is-ancestor', branch, mainBranch);
      if (isMerged) {
        mergedBranches.push(branch);
      }
    } catch {
      // 分支可能已删除，忽略
    }
  }

  return mergedBranches;
}

/**
 * 检查是否是 Git 仓库
 * @param {string} [cwd] - 工作目录
 * @returns {Promise<boolean>}
 */
async function isGitRepository(cwd = process.cwd()) {
  try {
    const git = getGit(cwd);
    await git.revparse(['--git-dir']);
    return true;
  } catch {
    return false;
  }
}

module.exports = {
  getGit,
  getCurrentBranch,
  getAllBranches,
  getLocalBranches,
  branchExists,
  createBranch,
  deleteBranch,
  isBranchMerged,
  getBranchStatus,
  getFileStatus,
  getLastCommit,
  getMergedBranches,
  isGitRepository
};
