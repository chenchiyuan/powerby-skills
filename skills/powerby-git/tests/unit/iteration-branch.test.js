/**
 * 迭代分支命名工具测试
 */

const {
  validateIterationId,
  normalizeIterationName,
  buildIterationFolderName,
  buildIterationBranchName
} = require('../../src/core/iteration-branch');

describe('Iteration Branch Helpers', () => {
  test('应接受合法三位迭代编号', () => {
    expect(validateIterationId('008')).toBe('008');
  });

  test('应拒绝非法迭代编号', () => {
    expect(() => validateIterationId('8')).toThrow('三位数字');
    expect(() => validateIterationId('abc')).toThrow('三位数字');
  });

  test('应规范化迭代名称并去重编号前缀', () => {
    expect(normalizeIterationName('008', 'Git Branch Automation')).toBe('git-branch-automation');
    expect(normalizeIterationName('008', '008-git-branch-automation')).toBe('git-branch-automation');
  });

  test('应生成标准目录名与 feature 分支名', () => {
    expect(buildIterationFolderName('008', 'git-branch-automation')).toBe('008-git-branch-automation');
    expect(buildIterationBranchName('008', 'git-branch-automation')).toBe('feature/008-git-branch-automation');
  });
});
