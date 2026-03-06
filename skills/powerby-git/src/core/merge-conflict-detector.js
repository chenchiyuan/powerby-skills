/**
 * 合并冲突预检测器
 */

const { createError } = require('./errors');
const {
  getCurrentBranch,
  checkoutBranch,
  previewMerge,
  abortMerge,
  getConflictedFiles
} = require('../utils/git');

/**
 * 对 feature -> target 的合并执行预检测。
 * @param {Object} options - 检测参数。
 * @param {string} options.sourceBranch - 源分支。
 * @param {string} options.targetBranch - 目标分支。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<{hasConflict:boolean, conflictFiles:string[], message:string}>}
 */
async function detectMergeConflicts({ sourceBranch, targetBranch, cwd = process.cwd() }) {
  if (!sourceBranch || !targetBranch) {
    throw createError('E008', `sourceBranch/targetBranch 不能为空: source="${sourceBranch}" target="${targetBranch}"`);
  }

  const originalBranch = await getCurrentBranch(cwd);

  try {
    await previewMerge(sourceBranch, targetBranch, cwd);

    try {
      await abortMerge(cwd);
    } catch (error) {
      throw createError('E017', `无冲突预检测后回滚失败: ${error.message}`);
    }

    return {
      hasConflict: false,
      conflictFiles: [],
      message: `分支 ${sourceBranch} 可安全合并到 ${targetBranch}`
    };
  } catch (error) {
    const conflictFiles = await getConflictedFiles(cwd);

    if (conflictFiles.length === 0) {
      throw createError('E007', `合并预检测失败: ${error.message}`);
    }

    try {
      await abortMerge(cwd);
    } catch (abortError) {
      throw createError('E017', `冲突预检测后回滚失败: ${abortError.message}`);
    }

    return {
      hasConflict: true,
      conflictFiles,
      message: `检测到 ${conflictFiles.length} 个冲突文件，请先手动解决后再重试合并`
    };
  } finally {
    await checkoutBranch(originalBranch, cwd);
  }
}

module.exports = {
  detectMergeConflicts
};
