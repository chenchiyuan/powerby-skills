/**
 * status 命令测试
 */

jest.mock('../../src/utils/git', () => ({
  getBranchStatus: jest.fn(),
  getCurrentBranch: jest.fn()
}));

jest.mock('../../src/core/file-whitelist', () => ({
  validateFileList: jest.fn()
}));

const gitUtils = require('../../src/utils/git');
const whitelist = require('../../src/core/file-whitelist');
const { executeStatus, generateSuggestions } = require('../../src/commands/status');

describe('Status Command', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    gitUtils.getBranchStatus.mockResolvedValue({
      isClean: true,
      staged: [],
      unstaged: [],
      not_tracked: []
    });
    gitUtils.getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');
    whitelist.validateFileList.mockReturnValue({
      summary: { valid: 0, invalid: 0 },
      invalidFiles: []
    });
  });

  test('应在工作区干净时给出可提交建议', async () => {
    const result = await executeStatus({});
    expect(result.suggestions).toContain('工作区很干净，可以提交了');
  });

  test('应在存在临时文件时给出清理建议', () => {
    const suggestions = generateSuggestions(
      { summary: { invalid: 1 }, invalidFiles: [{ path: 'temp.log' }] },
      [{ path: 'temp.log', message: '临时文件' }]
    );

    expect(suggestions[0]).toContain('临时文件');
  });
});
