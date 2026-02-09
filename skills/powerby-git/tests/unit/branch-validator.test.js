/**
 * 分支命名验证器测试
 */

const {
  BRANCH_TYPES,
  validateBranchType,
  normalizeBranchName,
  validateBranchName,
  generateBranchName,
  getBranchType
} = require('../../src/core/branch-validator');

describe('Branch Validator', () => {
  describe('validateBranchType', () => {
    test('应该接受有效的分支类型', () => {
      expect(() => validateBranchType('feature')).not.toThrow();
      expect(() => validateBranchType('bugfix')).not.toThrow();
      expect(() => validateBranchType('hotfix')).not.toThrow();
      expect(() => validateBranchType('release')).not.toThrow();
    });

    test('应该拒绝无效的分支类型', () => {
      expect(() => validateBranchType('invalid')).toThrow();
      expect(() => validateBranchType('')).toThrow();
    });
  });

  describe('normalizeBranchName', () => {
    test('应该转换为小写', () => {
      expect(normalizeBranchName('USER-NAME')).toBe('user-name');
    });

    test('应该将空格替换为连字符', () => {
      expect(normalizeBranchName('user name')).toBe('user-name');
    });

    test('应该移除特殊字符', () => {
      expect(normalizeBranchName('user@name!')).toBe('username');
    });

    test('应该移除连续连字符', () => {
      expect(normalizeBranchName('user---name')).toBe('user-name');
    });

    test('应该移除首尾连字符', () => {
      expect(normalizeBranchName('-user-name-')).toBe('user-name');
    });
  });

  describe('validateBranchName', () => {
    test('应该验证有效的 feature 分支名', () => {
      const result = validateBranchName('feature/user-auth');
      expect(result.valid).toBe(true);
      expect(result.type).toBe('feature');
    });

    test('应该验证有效的 bugfix 分支名', () => {
      const result = validateBranchName('bugfix/login-timeout');
      expect(result.valid).toBe(true);
      expect(result.type).toBe('bugfix');
    });

    test('应该验证有效的 hotfix 分支名', () => {
      const result = validateBranchName('hotfix/v1.2.3-security');
      expect(result.valid).toBe(true);
      expect(result.type).toBe('hotfix');
    });

    test('应该验证有效的 release 分支名', () => {
      const result = validateBranchName('release/v2.0.0');
      expect(result.valid).toBe(true);
      expect(result.type).toBe('release');
    });

    test('应该拒绝空名称', () => {
      const result = validateBranchName('');
      expect(result.valid).toBe(false);
    });

    test('应该拒绝无效格式', () => {
      const result = validateBranchName('invalid-name');
      expect(result.valid).toBe(false);
    });

    test('应该验证期望的类型', () => {
      const result = validateBranchName('feature/user-auth', 'feature');
      expect(result.valid).toBe(true);

      const wrongType = validateBranchName('feature/user-auth', 'bugfix');
      expect(wrongType.valid).toBe(false);
    });
  });

  describe('generateBranchName', () => {
    test('应该生成完整的 feature 分支名', () => {
      expect(generateBranchName('feature', 'user auth')).toBe('feature/user-auth');
    });

    test('应该生成完整的 bugfix 分支名', () => {
      expect(generateBranchName('bugfix', 'login timeout')).toBe('bugfix/login-timeout');
    });

    test('应该生成完整的 hotfix 分支名', () => {
      expect(generateBranchName('hotfix', 'v1.2.3')).toBe('hotfix/v1.2.3');
    });
  });

  describe('getBranchType', () => {
    test('应该返回正确的分支类型', () => {
      expect(getBranchType('feature/test')).toBe('feature');
      expect(getBranchType('bugfix/test')).toBe('bugfix');
    });

    test('应该返回 null 表示无效分支', () => {
      expect(getBranchType('invalid')).toBeNull();
    });
  });
});
