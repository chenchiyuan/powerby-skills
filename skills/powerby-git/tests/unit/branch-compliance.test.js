/**
 * 迭代分支合规检查测试
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

jest.mock('../../src/utils/git', () => ({
  getCurrentBranch: jest.fn(),
  getBranchStatus: jest.fn(),
  remoteBranchExists: jest.fn(),
  getBranchSyncStatus: jest.fn()
}));

const { getCurrentBranch, getBranchStatus, remoteBranchExists, getBranchSyncStatus } = require('../../src/utils/git');
const { checkBranchCompliance } = require('../../src/core/branch-compliance');

function createTempProject() {
  const tempDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'powerby-git-branch-compliance-'));
  const powerbyDirectory = path.join(tempDirectory, '.powerby');

  fs.mkdirSync(powerbyDirectory, { recursive: true });
  fs.writeFileSync(
    path.join(powerbyDirectory, 'iterations.json'),
    JSON.stringify({
      iterations: [
        {
          id: '008',
          name: 'git-branch-automation',
          full_name: '008-git-branch-automation',
          status: 'in_progress',
          phase: 'P6',
          branch: 'feature/008-git-branch-automation',
          branch_info: {
            branch_name: 'feature/008-git-branch-automation',
            status: 'active'
          }
        }
      ],
      current_iteration: '008',
      completed_iterations: 0,
      total_iterations: 1
    }, null, 2)
  );

  return tempDirectory;
}

describe('Branch Compliance Checker', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('应在分支正确且工作区干净时通过检查', async () => {
    getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');
    getBranchStatus.mockResolvedValue({ isClean: true, staged: [], unstaged: [], not_tracked: [] });
    remoteBranchExists.mockResolvedValue(false);
    const cwd = createTempProject();

    const result = await checkBranchCompliance({ iterationId: '008', phase: 'P6', cwd });

    expect(result.compliant).toBe(true);
    expect(result.warnings).toHaveLength(0);
  });

  test('应在当前分支不匹配时返回切换建议', async () => {
    getCurrentBranch.mockResolvedValue('v2');
    getBranchStatus.mockResolvedValue({ isClean: true, staged: [], unstaged: [], not_tracked: [] });
    remoteBranchExists.mockResolvedValue(false);
    const cwd = createTempProject();

    const result = await checkBranchCompliance({ iterationId: '008', phase: 'P1', cwd });

    expect(result.compliant).toBe(false);
    expect(result.warnings[0].suggestion).toContain('git checkout feature/008-git-branch-automation');
  });

  test('应在 P8 阶段工作区不干净时返回错误级警告', async () => {
    getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');
    getBranchStatus.mockResolvedValue({
      isClean: false,
      staged: ['a.js'],
      unstaged: ['b.js'],
      not_tracked: ['c.js']
    });
    remoteBranchExists.mockResolvedValue(false);
    const cwd = createTempProject();

    const result = await checkBranchCompliance({ iterationId: '008', phase: 'P8', cwd });

    expect(result.compliant).toBe(false);
    expect(result.warnings[0].level).toBe('error');
    expect(result.warnings[0].message).toContain('changedFiles=3');
  });

  test('应在 P8 阶段远程落后时返回同步错误', async () => {
    getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');
    getBranchStatus.mockResolvedValue({ isClean: true, staged: [], unstaged: [], not_tracked: [] });
    remoteBranchExists.mockResolvedValue(true);
    getBranchSyncStatus.mockResolvedValue({ ahead: 0, behind: 2 });
    const cwd = createTempProject();

    const result = await checkBranchCompliance({ iterationId: '008', phase: 'P8', cwd });

    expect(result.compliant).toBe(false);
    expect(result.warnings.some((item) => item.message.includes('落后远程'))).toBe(true);
  });
});
