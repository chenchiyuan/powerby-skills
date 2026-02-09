/**
 * 分支命名验证器
 * 验证分支名称是否符合规范
 */

const { createError } = require('./errors');

/**
 * 分支类型定义
 */
const BRANCH_TYPES = {
  FEATURE: 'feature',
  BUGFIX: 'bugfix',
  HOTFIX: 'hotfix',
  RELEASE: 'release'
};

/**
 * 分支类型模式映射
 */
const BRANCH_PATTERNS = {
  [BRANCH_TYPES.FEATURE]: /^feature\/[a-z0-9]+(-[a-z0-9]+)*$/,
  [BRANCH_TYPES.BUGFIX]: /^bugfix\/[a-z0-9]+(-[a-z0-9]+)*$/,
  [BRANCH_TYPES.HOTFIX]: /^hotfix\/v\d+\.\d+\.\d+(-[a-z0-9]+)*$/,
  [BRANCH_TYPES.RELEASE]: /^release\/v\d+\.\d+\.\d+$/
};

/**
 * 验证分支类型
 * @param {string} type - 分支类型
 * @returns {boolean}
 */
function validateBranchType(type) {
  const validTypes = Object.values(BRANCH_TYPES);
  if (!validTypes.includes(type)) {
    throw createError('E002', `无效的分支类型: ${type}。支持类型: ${validTypes.join(', ')}`);
  }
  return true;
}

/**
 * 规范化分支名称
 * @param {string} name - 分支名称
 * @returns {string} 规范化后的名称
 */
function normalizeBranchName(name) {
  // 转换为小写
  let normalized = name.toLowerCase();
  // 替换空格为连字符
  normalized = normalized.replace(/\s+/g, '-');
  // 保留版本号中的点和斜杠 (v1.2.3 -> v1.2.3, feature/xxx -> feature/xxx)
  normalized = normalized.replace(/[^a-z0-9\-./]/g, '');
  // 移除连续连字符
  normalized = normalized.replace(/-+/g, '-');
  // 移除首尾连字符和点
  normalized = normalized.replace(/^-+|^[.]+|[.-]+$|[.-]+$/g, '');

  return normalized;
}

/**
 * 验证分支名称
 * @param {string} branchName - 分支名称
 * @param {string} [expectedType] - 期望的分支类型
 * @returns {{valid: boolean, type: string|null, normalizedName: string, errors: string[]}}
 */
function validateBranchName(branchName, expectedType = null) {
  const result = {
    valid: true,
    type: null,
    normalizedName: branchName,
    errors: []
  };

  if (!branchName || branchName.trim() === '') {
    result.valid = false;
    result.errors.push('分支名称不能为空');
    return result;
  }

  // 规范化名称
  const normalized = normalizeBranchName(branchName);
  result.normalizedName = normalized;

  // 检查是否匹配任何分支类型
  for (const [type, pattern] of Object.entries(BRANCH_PATTERNS)) {
    if (pattern.test(normalized)) {
      result.type = type;

      if (expectedType && type !== expectedType) {
        result.valid = false;
        result.errors.push(`期望分支类型为 ${expectedType}，但检测到 ${type}`);
      }

      return result;
    }
  }

  // 如果有期望类型但未匹配
  if (expectedType) {
    result.valid = false;
    result.errors.push(`分支名称不符合 ${expectedType} 格式`);
  } else {
    result.valid = false;
    result.errors.push('分支名称不符合任何标准格式 (feature/, bugfix/, hotfix/, release/)');
  }

  return result;
}

/**
 * 生成完整分支名
 * @param {string} type - 分支类型
 * @param {string} name - 分支名称
 * @returns {string}
 */
function generateBranchName(type, name) {
  validateBranchType(type);
  const normalized = normalizeBranchName(name);
  return `${type}/${normalized}`;
}

/**
 * 获取分支类型
 * @param {string} branchName - 分支名称
 * @returns {string|null}
 */
function getBranchType(branchName) {
  const result = validateBranchName(branchName);
  return result.type;
}

module.exports = {
  BRANCH_TYPES,
  BRANCH_PATTERNS,
  validateBranchType,
  normalizeBranchName,
  validateBranchName,
  generateBranchName,
  getBranchType
};
