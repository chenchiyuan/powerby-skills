/**
 * Git 操作封装
 */

const simpleGit = require('simple-git');

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
 * 切换到指定分支。
 * @param {string} branchName - 分支名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function checkoutBranch(branchName, cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.checkout(branchName);
}

/**
 * 基于源分支创建并切换到新分支。
 * @param {string} branchName - 新分支名。
 * @param {string} sourceBranch - 源分支名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function createBranchFromSource(branchName, sourceBranch, cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.checkout(sourceBranch);
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
 * 执行 no-ff 分支合并。
 * @param {string} sourceBranch - 待合并分支。
 * @param {string} targetBranch - 目标分支。
 * @param {Object} [options] - 合并选项。
 * @param {boolean} [options.noFF=true] - 是否使用 `--no-ff`。
 * @param {string} [options.commitMessage] - 自定义提交信息。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function mergeBranch(
  sourceBranch,
  targetBranch,
  options = { noFF: true },
  cwd = process.cwd()
) {
  const git = getGit(cwd);
  const mergeArguments = ['merge'];

  if (options.noFF !== false) {
    mergeArguments.push('--no-ff');
  }

  if (options.commitMessage) {
    mergeArguments.push('-m', options.commitMessage);
  }

  mergeArguments.push(sourceBranch);

  await git.checkout(targetBranch);
  await git.raw(mergeArguments);
}

/**
 * 预执行合并以检测冲突。
 * @param {string} sourceBranch - 待合并分支。
 * @param {string} targetBranch - 目标分支。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function previewMerge(sourceBranch, targetBranch, cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.checkout(targetBranch);
  await git.raw(['merge', '--no-commit', '--no-ff', sourceBranch]);
}

/**
 * 中止当前合并。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function abortMerge(cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.raw(['merge', '--abort']);
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
 * 获取指定分支的最后一次提交。
 * @param {string} branchName - 分支名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<Object|null>}
 */
async function getLastCommitForBranch(branchName, cwd = process.cwd()) {
  const git = getGit(cwd);
  const output = await git.raw(['log', '-1', branchName, '--format=%H%x1f%an%x1f%ae%x1f%aI%x1f%s']);
  const trimmed = output.trim();

  if (!trimmed) {
    return null;
  }

  const [hash, authorName, authorEmail, date, message] = trimmed.split('\x1f');
  return {
    hash,
    author_name: authorName,
    author_email: authorEmail,
    date,
    message
  };
}

/**
 * 获取分支相对于基线分支的提交历史。
 * @param {string} branchName - 目标分支名。
 * @param {string} [baseBranch='develop'] - 基线分支名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<Object[]>} 提交列表。
 */
async function getCommitHistory(branchName, baseBranch = 'develop', cwd = process.cwd()) {
  const git = getGit(cwd);
  const log = await git.log({ from: baseBranch, to: branchName });
  return log.all;
}

/**
 * 获取详细提交历史。
 * @param {string} branchName - 分支名。
 * @param {string} [baseBranch='develop'] - 基线分支。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<Object[]>}
 */
async function getDetailedCommitHistory(branchName, baseBranch = 'develop', cwd = process.cwd()) {
  const git = getGit(cwd);
  const output = await git.raw([
    'log',
    `${baseBranch}..${branchName}`,
    '--format=%H%x1f%an%x1f%ae%x1f%aI%x1f%s'
  ]);

  const trimmed = output.trim();
  if (!trimmed) {
    return [];
  }

  return trimmed.split('\n').map((line) => {
    const [hash, authorName, authorEmail, timestamp, message] = line.split('\x1f');
    return {
      hash,
      author_name: authorName,
      author_email: authorEmail,
      timestamp,
      message
    };
  });
}

/**
 * 获取当前冲突文件列表。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<string[]>}
 */
async function getConflictedFiles(cwd = process.cwd()) {
  const git = getGit(cwd);
  const status = await git.status();

  if (Array.isArray(status.conflicted) && status.conflicted.length > 0) {
    return status.conflicted;
  }

  const output = await git.raw(['diff', '--name-only', '--diff-filter=U']);
  return output.trim() ? output.trim().split('\n') : [];
}

/**
 * 检查远程分支是否存在。
 * @param {string} branchName - 本地分支名。
 * @param {string} [remote='origin'] - 远程名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<boolean>}
 */
async function remoteBranchExists(branchName, remote = 'origin', cwd = process.cwd()) {
  const git = getGit(cwd);
  const output = await git.listRemote(['--heads', remote, branchName]);
  return output.trim() !== '';
}

/**
 * 获取本地分支相对远程分支的同步状态。
 * @param {string} branchName - 本地分支名。
 * @param {string} [remote='origin'] - 远程名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<{ahead:number,behind:number}>}
 */
async function getBranchSyncStatus(branchName, remote = 'origin', cwd = process.cwd()) {
  const git = getGit(cwd);
  const output = await git.raw(['rev-list', '--left-right', '--count', `${branchName}...${remote}/${branchName}`]);
  const [ahead, behind] = output.trim().split(/\s+/).map((value) => Number(value));
  return {
    ahead: Number.isNaN(ahead) ? 0 : ahead,
    behind: Number.isNaN(behind) ? 0 : behind
  };
}

/**
 * 推送本地分支到远程。
 * @param {string} branchName - 分支名。
 * @param {Object} [options] - 推送选项。
 * @param {string} [options.remote='origin'] - 远程名。
 * @param {boolean} [options.setUpstream=true] - 是否设置上游。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function pushBranch(branchName, options = { remote: 'origin', setUpstream: true }, cwd = process.cwd()) {
  const git = getGit(cwd);
  const remote = options.remote || 'origin';

  if (options.setUpstream === false) {
    await git.push(remote, branchName);
    return;
  }

  await git.push(remote, branchName, { '--set-upstream': null });
}

/**
 * 删除远程分支。
 * @param {string} branchName - 分支名。
 * @param {string} [remote='origin'] - 远程名。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<void>}
 */
async function deleteRemoteBranch(branchName, remote = 'origin', cwd = process.cwd()) {
  const git = getGit(cwd);
  await git.push(remote, `:${branchName}`);
}

/**
 * 获取 Git 用户配置。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<{name:string,email:string}>}
 */
async function getGitUser(cwd = process.cwd()) {
  const git = getGit(cwd);
  const [name, email] = await Promise.all([
    git.raw(['config', 'user.name']),
    git.raw(['config', 'user.email'])
  ]);

  return {
    name: name.trim(),
    email: email.trim()
  };
}

/**
 * 检查工作区是否干净。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<boolean>}
 */
async function isWorkingTreeClean(cwd = process.cwd()) {
  const git = getGit(cwd);
  const status = await git.status();
  return status.isClean();
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
  checkoutBranch,
  createBranchFromSource,
  deleteBranch,
  mergeBranch,
  previewMerge,
  abortMerge,
  isBranchMerged,
  getBranchStatus,
  getFileStatus,
  getLastCommit,
  getLastCommitForBranch,
  getCommitHistory,
  getDetailedCommitHistory,
  getConflictedFiles,
  getMergedBranches,
  remoteBranchExists,
  getBranchSyncStatus,
  pushBranch,
  deleteRemoteBranch,
  getGitUser,
  isWorkingTreeClean,
  isGitRepository
};
