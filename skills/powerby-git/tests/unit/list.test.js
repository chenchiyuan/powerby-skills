/**
 * list 命令测试
 */

jest.mock('../../src/utils/git', () => ({
  getAllBranches: jest.fn(),
  isBranchMerged: jest.fn(),
  getLastCommitForBranch: jest.fn()
}));

const gitUtils = require('../../src/utils/git');
const { executeList } = require('../../src/commands/list');

describe('List Command', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    gitUtils.getAllBranches.mockResolvedValue(['main', 'develop', 'feature/a', 'feature/b']);
    gitUtils.getLastCommitForBranch.mockImplementation(async (branch) => ({
      hash: `${branch}-hash`,
      message: `${branch} message`,
      date: '2026-03-06T00:00:00Z'
    }));
    gitUtils.isBranchMerged.mockImplementation(async (branch) => branch === 'feature/a');
  });

  test('应正确过滤已合并分支', async () => {
    const result = await executeList({ merged: true, mainBranch: 'main' });
    expect(result.branches).toHaveLength(1);
    expect(result.branches[0].name).toBe('feature/a');
  });

  test('应正确过滤未合并分支', async () => {
    const result = await executeList({ unmerged: true, mainBranch: 'main' });
    expect(result.branches).toHaveLength(1);
    expect(result.branches[0].name).toBe('feature/b');
  });
});
