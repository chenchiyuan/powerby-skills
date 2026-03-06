/**
 * 迭代分支命名工具
 */

const { normalizeBranchName, generateBranchName } = require('./branch-validator');
const { createError } = require('./errors');

/**
 * 验证三位迭代编号。
 * @param {string} iterationId - 迭代编号。
 * @throws {Error} 当编号为空或非三位数字时抛出异常。
 * @returns {string} 原始迭代编号。
 */
function validateIterationId(iterationId) {
  if (typeof iterationId !== 'string' || !/^\d{3}$/.test(iterationId)) {
    throw createError('E008', `迭代编号必须是三位数字: actual="${iterationId}"`);
  }

  return iterationId;
}

/**
 * 规范化迭代名称，并去除可能重复的编号前缀。
 * @param {string} iterationId - 迭代编号。
 * @param {string} iterationName - 迭代名称。
 * @throws {Error} 当名称为空时抛出异常。
 * @returns {string} 规范化后的迭代名称。
 */
function normalizeIterationName(iterationId, iterationName) {
  validateIterationId(iterationId);

  if (typeof iterationName !== 'string' || iterationName.trim() === '') {
    throw createError('E008', `迭代名称不能为空: actual="${iterationName}"`);
  }

  const normalizedName = normalizeBranchName(iterationName);
  const duplicatedPrefix = `${iterationId}-`;

  if (normalizedName.startsWith(duplicatedPrefix)) {
    return normalizedName.slice(duplicatedPrefix.length);
  }

  return normalizedName;
}

/**
 * 构建标准迭代目录名。
 * @param {string} iterationId - 迭代编号。
 * @param {string} iterationName - 迭代名称。
 * @returns {string} 目录名，如 `008-git-branch-automation`。
 */
function buildIterationFolderName(iterationId, iterationName) {
  const normalizedName = normalizeIterationName(iterationId, iterationName);
  return `${validateIterationId(iterationId)}-${normalizedName}`;
}

/**
 * 构建标准 feature 分支名。
 * @param {string} iterationId - 迭代编号。
 * @param {string} iterationName - 迭代名称。
 * @returns {string} 分支名，如 `feature/008-git-branch-automation`。
 */
function buildIterationBranchName(iterationId, iterationName) {
  return generateBranchName('feature', buildIterationFolderName(iterationId, iterationName));
}

module.exports = {
  validateIterationId,
  normalizeIterationName,
  buildIterationFolderName,
  buildIterationBranchName
};
