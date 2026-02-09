/**
 * 提交信息验证器
 * 验证 Git 提交信息是否符合规范
 */

const { createError } = require('./errors');

/**
 * 标准提交类型
 */
const COMMIT_TYPES = {
  FEAT: 'feat',
  FIX: 'fix',
  DOCS: 'docs',
  STYLE: 'style',
  REFACTOR: 'refactor',
  TEST: 'test',
  CHORE: 'chore',
  BUILD: 'build',
  CI: 'ci',
  PERF: 'perf',
  REVERT: 'revert'
};

/**
 * 提交类型描述
 */
const COMMIT_TYPE_DESCRIPTIONS = {
  [COMMIT_TYPES.FEAT]: '新功能',
  [COMMIT_TYPES.FIX]: 'Bug 修复',
  [COMMIT_TYPES.DOCS]: '文档更新',
  [COMMIT_TYPES.STYLE]: '代码格式（不影响含义）',
  [COMMIT_TYPES.REFACTOR]: '重构（既不是新功能也不是 Bug 修复）',
  [COMMIT_TYPES.TEST]: '添加或修改测试',
  [COMMIT_TYPES.CHORE]: '构建过程或辅助工具的变动',
  [COMMIT_TYPES.BUILD]: '构建系统或外部依赖的变动',
  [COMMIT_TYPES.CI]: 'CI 配置文件和脚本的变动',
  [COMMIT_TYPES.PERF]: '性能优化',
  [COMMIT_TYPES.REVERT]: '回滚提交'
};

/**
 * 提交信息正则表达式
 * 格式: {type}({scope}): {description}
 */
const COMMIT_MESSAGE_REGEX = /^([a-z]+)(?:\(([^)]+)\))?: (.+)$/;

/**
 * 最大行长度
 */
const MAX_HEADER_LENGTH = 50;
const MAX_BODY_LINE_LENGTH = 72;

/**
 * 验证提交类型
 * @param {string} type - 提交类型
 * @returns {boolean}
 */
function validateCommitType(type) {
  const validTypes = Object.values(COMMIT_TYPES);
  if (!validTypes.includes(type)) {
    throw createError('E008', `无效的提交类型: ${type}。支持类型: ${validTypes.join(', ')}`);
  }
  return true;
}

/**
 * 解析提交信息
 * @param {string} message - 提交信息
 * @returns {{type: string|null, scope: string|null, description: string, body: string, breakingChanges: Array, issues: Array}|null}
 */
function parseCommitMessage(message) {
  const lines = message.trim().split('\n');
  const header = lines[0];

  const headerMatch = header.match(COMMIT_MESSAGE_REGEX);

  if (!headerMatch) {
    return null;
  }

  const [, type, scope, description] = headerMatch;

  // 解析正文
  const body = lines.slice(1).join('\n').trim();

  // 解析 Breaking Changes
  const breakingChanges = [];
  // 解析 Issues
  const issues = [];

  if (body) {
    const bodyLines = body.split('\n');
    for (const line of bodyLines) {
      const trimmedLine = line.trim();

      if (trimmedLine.startsWith('BREAKING CHANGE:')) {
        breakingChanges.push(trimmedLine.replace('BREAKING CHANGE:', '').trim());
      } else if (trimmedLine.startsWith('Closes #') || trimmedLine.startsWith('Fixes #')) {
        const issueMatch = trimmedLine.match(/#(\d+)/);
        if (issueMatch) {
          issues.push(issueMatch[1]);
        }
      } else if (trimmedLine.startsWith('Refs #')) {
        const issueMatch = trimmedLine.match(/#(\d+)/);
        if (issueMatch) {
          issues.push(issueMatch[1]);
        }
      }
    }
  }

  return {
    type,
    scope: scope || null,
    description,
    body,
    breakingChanges,
    issues
  };
}

/**
 * 验证提交信息
 * @param {string} message - 提交信息
 * @returns {{valid: boolean, parsed: Object|null, errors: string[], warnings: string[]}}
 */
function validateCommitMessage(message) {
  const result = {
    valid: true,
    parsed: null,
    errors: [],
    warnings: []
  };

  if (!message || message.trim() === '') {
    result.valid = false;
    result.errors.push('提交信息不能为空');
    return result;
  }

  const parsed = parseCommitMessage(message);
  result.parsed = parsed;

  if (!parsed) {
    result.valid = false;
    result.errors.push('提交信息格式不正确');
    result.errors.push(`期望格式: type(scope): description`);
    result.errors.push(`例如: feat(auth): add login functionality`);
    return result;
  }

  // 验证类型
  const validTypes = Object.values(COMMIT_TYPES);
  if (!validTypes.includes(parsed.type)) {
    result.valid = false;
    result.errors.push(`无效的提交类型: ${parsed.type}`);
    result.errors.push(`支持类型: ${validTypes.join(', ')}`);
  }

  // 验证 scope 格式
  if (parsed.scope) {
    if (!/^[a-z0-9-]+$/.test(parsed.scope)) {
      result.warnings.push('scope 建议使用小写字母和连字符');
    }
  }

  // 验证描述长度
  if (parsed.description.length > MAX_HEADER_LENGTH) {
    result.warnings.push(`标题建议不超过 ${MAX_HEADER_LENGTH} 字符，当前: ${parsed.description.length}`);
  }

  // 验证描述首字母
  if (/^[A-Z]/.test(parsed.description)) {
    result.warnings.push('描述建议使用小写字母开头');
  }

  // 验证 body 行长度
  if (parsed.body) {
    const bodyLines = parsed.body.split('\n');
    for (const line of bodyLines) {
      if (line.length > MAX_BODY_LINE_LENGTH) {
        result.warnings.push(`正文行建议不超过 ${MAX_BODY_LINE_LENGTH} 字符`);
        break;
      }
    }
  }

  return result;
}

/**
 * 获取提交类型列表
 * @returns {string[]}
 */
function getCommitTypes() {
  return Object.entries(COMMIT_TYPES).map(([key, value]) => ({
    type: value,
    description: COMMIT_TYPE_DESCRIPTIONS[value]
  }));
}

module.exports = {
  COMMIT_TYPES,
  COMMIT_TYPE_DESCRIPTIONS,
  COMMIT_MESSAGE_REGEX,
  validateCommitType,
  parseCommitMessage,
  validateCommitMessage,
  getCommitTypes
};
