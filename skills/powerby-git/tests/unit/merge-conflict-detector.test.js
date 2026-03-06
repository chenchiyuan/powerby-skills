/**
 * 合并冲突预检测器测试
 */

jest.mock('../../src/utils/git', () => ({
  getCurrentBranch: jest.fn(),
  checkoutBranch: jest.fn(),
  previewMerge: jest.fn(),
  abortMerge: jest.fn(),
  getConflictedFiles: jest.fn()
}));

const gitUtils = require('../../src/utils/git');
const { detectMergeConflicts } = require('../../src/core/merge-conflict-detector');

describe('Merge Conflict Detector', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    gitUtils.getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');
  });

  test('应在无冲突时返回可安全合并', async () => {
    gitUtils.previewMerge.mockResolvedValue(undefined);
    gitUtils.abortMerge.mockResolvedValue(undefined);

    const result = await detectMergeConflicts({
      sourceBranch: 'feature/008-git-branch-automation',
      targetBranch: 'develop'
    });

    expect(result.hasConflict).toBe(false);
    expect(gitUtils.abortMerge).toHaveBeenCalledTimes(1);
    expect(gitUtils.checkoutBranch).toHaveBeenCalledWith('feature/008-git-branch-automation', process.cwd());
  });

  test('应在有冲突时返回冲突文件列表', async () => {
    gitUtils.previewMerge.mockRejectedValue(new Error('conflict'));
    gitUtils.getConflictedFiles.mockResolvedValue(['src/a.js', 'src/b.js']);
    gitUtils.abortMerge.mockResolvedValue(undefined);

    const result = await detectMergeConflicts({
      sourceBranch: 'feature/008-git-branch-automation',
      targetBranch: 'develop'
    });

    expect(result.hasConflict).toBe(true);
    expect(result.conflictFiles).toEqual(['src/a.js', 'src/b.js']);
  });

  test('应在回滚失败时快速失败', async () => {
    gitUtils.previewMerge.mockResolvedValue(undefined);
    gitUtils.getConflictedFiles.mockResolvedValue(['src/a.js']);
    gitUtils.abortMerge.mockRejectedValue(new Error('abort failed'));

    await expect(detectMergeConflicts({
      sourceBranch: 'feature/008-git-branch-automation',
      targetBranch: 'develop'
    })).rejects.toThrow('合并预检测回滚失败');
  });

  test('应在非冲突型预检测失败时抛出 git 操作错误', async () => {
    gitUtils.previewMerge.mockRejectedValue(new Error('checkout failed'));
    gitUtils.getConflictedFiles.mockResolvedValue([]);

    await expect(detectMergeConflicts({
      sourceBranch: 'feature/008-git-branch-automation',
      targetBranch: 'develop'
    })).rejects.toThrow('Git 操作失败');
  });
});
