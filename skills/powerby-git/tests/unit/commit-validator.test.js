/**
 * 提交信息验证器测试
 */

const {
  COMMIT_TYPES,
  validateCommitType,
  parseCommitMessage,
  validateCommitMessage,
  getCommitTypes
} = require('../../src/core/commit-validator');

describe('Commit Validator', () => {
  describe('validateCommitType', () => {
    test('应该接受有效的提交类型', () => {
      expect(() => validateCommitType('feat')).not.toThrow();
      expect(() => validateCommitType('fix')).not.toThrow();
      expect(() => validateCommitType('docs')).not.toThrow();
      expect(() => validateCommitType('style')).not.toThrow();
    });

    test('应该拒绝无效的提交类型', () => {
      expect(() => validateCommitType('invalid')).toThrow();
      expect(() => validateCommitType('')).toThrow();
    });
  });

  describe('parseCommitMessage', () => {
    test('应该解析有效的提交信息', () => {
      const result = parseCommitMessage('feat(auth): add login functionality');

      expect(result).not.toBeNull();
      expect(result.type).toBe('feat');
      expect(result.scope).toBe('auth');
      expect(result.description).toBe('add login functionality');
    });

    test('应该解析没有 scope 的提交信息', () => {
      const result = parseCommitMessage('chore: update dependencies');

      expect(result).not.toBeNull();
      expect(result.type).toBe('chore');
      expect(result.scope).toBeNull();
      expect(result.description).toBe('update dependencies');
    });

    test('应该解析带有正文的提交信息', () => {
      const message = `feat(auth): add login functionality

This adds the login functionality with JWT tokens.

Closes #123`;

      const result = parseCommitMessage(message);

      expect(result).not.toBeNull();
      expect(result.body).toContain('This adds the login functionality');
      expect(result.issues).toContain('123');
    });

    test('应该返回 null 表示无效格式', () => {
      expect(parseCommitMessage('invalid commit message')).toBeNull();
      expect(parseCommitMessage('')).toBeNull();
    });
  });

  describe('validateCommitMessage', () => {
    test('应该验证有效的提交信息', () => {
      const result = validateCommitMessage('feat(auth): add login');

      expect(result.valid).toBe(true);
      expect(result.errors.length).toBe(0);
      expect(result.parsed.type).toBe('feat');
    });

    test('应该验证无效的提交信息', () => {
      const result = validateCommitMessage('invalid message');

      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    test('应该验证空提交信息', () => {
      const result = validateCommitMessage('');

      expect(result.valid).toBe(false);
    });

    test('应该生成大写开头的警告', () => {
      const result = validateCommitMessage('feat(auth): Add login');

      expect(result.valid).toBe(true);
      expect(result.warnings.some(w => w.includes('小写字母'))).toBe(true);
    });
  });

  describe('getCommitTypes', () => {
    test('应该返回所有提交类型', () => {
      const types = getCommitTypes();

      expect(types.length).toBeGreaterThan(0);
      expect(types.find(t => t.type === 'feat')).toBeDefined();
      expect(types.find(t => t.type === 'fix')).toBeDefined();
    });
  });
});
