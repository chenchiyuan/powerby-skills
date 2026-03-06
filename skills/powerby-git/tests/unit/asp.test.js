/**
 * ASP Git 分支集成测试
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

jest.mock('../../src/utils/git', () => ({
  branchExists: jest.fn(),
  createBranchFromSource: jest.fn(),
  mergeBranch: jest.fn(),
  deleteBranch: jest.fn(),
  deleteRemoteBranch: jest.fn(),
  remoteBranchExists: jest.fn(),
  getCurrentBranch: jest.fn(),
  getBranchStatus: jest.fn(),
  getLastCommit: jest.fn(),
  getGitUser: jest.fn(),
  checkoutBranch: jest.fn(),
  isWorkingTreeClean: jest.fn()
}));

jest.mock('../../src/core/merge-conflict-detector', () => ({
  detectMergeConflicts: jest.fn()
}));

jest.mock('../../src/core/branch-history-generator', () => ({
  generateBranchHistoryReport: jest.fn(),
  updateBranchHistoryReport: jest.fn(),
  enrichMergeRecord: jest.fn(async (record) => record)
}));

const gitUtils = require('../../src/utils/git');
const { detectMergeConflicts } = require('../../src/core/merge-conflict-detector');
const historyGenerator = require('../../src/core/branch-history-generator');
const {
  createIterationBranch,
  checkIterationBranchCompliance,
  switchIterationBranch,
  detectIterationMergeConflicts,
  mergeIterationBranch,
  deleteIterationBranch
} = require('../../src/integrations/asp');

function createTempProject() {
  const tempDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'powerby-git-asp-'));
  const powerbyDirectory = path.join(tempDirectory, '.powerby');

  fs.mkdirSync(powerbyDirectory, { recursive: true });
  fs.writeFileSync(
    path.join(powerbyDirectory, 'iterations.json'),
    JSON.stringify({ iterations: [], current_iteration: null, completed_iterations: 0, total_iterations: 0 }, null, 2)
  );

  return tempDirectory;
}

describe('ASP Integration', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    detectMergeConflicts.mockResolvedValue({ hasConflict: false, conflictFiles: [], message: 'ok' });
    historyGenerator.generateBranchHistoryReport.mockResolvedValue({ success: true, reportPath: 'x', message: 'ok' });
    historyGenerator.updateBranchHistoryReport.mockResolvedValue({ success: true, reportPath: 'x', message: 'ok' });
    historyGenerator.enrichMergeRecord.mockImplementation(async (record) => record);
    gitUtils.getGitUser.mockResolvedValue({ name: 'Bob', email: 'bob@example.com' });
    gitUtils.remoteBranchExists.mockResolvedValue(false);
  });

  test('应创建迭代分支并写入 branch_info', async () => {
    gitUtils.branchExists
      .mockResolvedValueOnce(true)
      .mockResolvedValueOnce(false);

    const cwd = createTempProject();
    const result = await createIterationBranch('008', 'git-branch-automation', 'develop', { cwd });
    const metadata = JSON.parse(fs.readFileSync(path.join(cwd, '.powerby', 'iterations.json'), 'utf-8'));

    expect(result.branchName).toBe('feature/008-git-branch-automation');
    expect(gitUtils.createBranchFromSource).toHaveBeenCalledWith(
      'feature/008-git-branch-automation',
      'develop',
      cwd
    );
    expect(metadata.iterations[0].branch_info.status).toBe('active');
  });

  test('应在源分支不存在时快速失败', async () => {
    gitUtils.branchExists.mockResolvedValue(false);
    const cwd = createTempProject();

    await expect(createIterationBranch('008', 'git-branch-automation', 'develop', { cwd }))
      .rejects
      .toThrow('源分支不存在');
  });

  test('应在工作区干净时合并并更新状态', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
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
              status: 'active',
              source_branch: 'develop',
              target_branch: 'develop'
            }
          }
        ],
        current_iteration: '008',
        completed_iterations: 0,
        total_iterations: 1
      }, null, 2)
    );

    gitUtils.isWorkingTreeClean.mockResolvedValue(true);
    gitUtils.branchExists.mockResolvedValue(true);
    gitUtils.getLastCommit.mockResolvedValue({ hash: 'abc123' });

    const result = await mergeIterationBranch('008', 'develop', { cwd });
    const metadata = JSON.parse(fs.readFileSync(path.join(cwd, '.powerby', 'iterations.json'), 'utf-8'));

    expect(result.mergeCommitHash).toBe('abc123');
    expect(gitUtils.mergeBranch).toHaveBeenCalled();
    expect(historyGenerator.generateBranchHistoryReport).toHaveBeenCalled();
    expect(metadata.iterations[0].branch_info.status).toBe('merged');
  });

  test('应在冲突检测失败时返回冲突结果而不是抛错', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
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
              status: 'active',
              source_branch: 'develop',
              target_branch: 'develop'
            }
          }
        ],
        current_iteration: '008',
        completed_iterations: 0,
        total_iterations: 1
      }, null, 2)
    );

    gitUtils.isWorkingTreeClean.mockResolvedValue(true);
    gitUtils.branchExists.mockResolvedValue(true);
    detectMergeConflicts.mockResolvedValue({ hasConflict: true, conflictFiles: ['src/a.js'], message: 'conflict' });

    const result = await mergeIterationBranch('008', 'develop', { cwd });
    expect(result.hasConflict).toBe(true);
    expect(result.conflictFiles).toEqual(['src/a.js']);
  });

  test('应在工作区不干净时拒绝合并', async () => {
    gitUtils.isWorkingTreeClean.mockResolvedValue(false);
    gitUtils.getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');
    const cwd = createTempProject();

    await expect(mergeIterationBranch('008', 'develop', { cwd }))
      .rejects
      .toThrow('工作区不干净');
  });

  test('应在已合并状态下删除本地分支', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
      JSON.stringify({
        iterations: [
          {
            id: '008',
            name: 'git-branch-automation',
            full_name: '008-git-branch-automation',
            status: 'in_progress',
            phase: 'P8',
            branch: 'feature/008-git-branch-automation',
            branch_info: {
              branch_name: 'feature/008-git-branch-automation',
              status: 'merged',
              source_branch: 'develop',
              target_branch: 'develop'
            }
          }
        ],
        current_iteration: '008',
        completed_iterations: 0,
        total_iterations: 1
      }, null, 2)
    );

    gitUtils.getCurrentBranch.mockResolvedValue('develop');
    gitUtils.branchExists.mockResolvedValue(true);

    const result = await deleteIterationBranch('008', { cwd });
    const metadata = JSON.parse(fs.readFileSync(path.join(cwd, '.powerby', 'iterations.json'), 'utf-8'));

    expect(result.success).toBe(true);
    expect(gitUtils.deleteBranch).toHaveBeenCalledWith('feature/008-git-branch-automation', cwd);
    expect(metadata.iterations[0].branch_info.status).toBe('deleted');
  });

  test('应在远程删除失败时标记 deleted_local_only', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
      JSON.stringify({
        iterations: [
          {
            id: '008',
            name: 'git-branch-automation',
            full_name: '008-git-branch-automation',
            status: 'in_progress',
            phase: 'P8',
            branch: 'feature/008-git-branch-automation',
            branch_info: {
              branch_name: 'feature/008-git-branch-automation',
              status: 'merged',
              source_branch: 'develop',
              target_branch: 'develop'
            }
          }
        ],
        current_iteration: '008',
        completed_iterations: 0,
        total_iterations: 1
      }, null, 2)
    );

    gitUtils.getCurrentBranch.mockResolvedValue('develop');
    gitUtils.branchExists.mockResolvedValue(true);
    gitUtils.remoteBranchExists.mockResolvedValue(true);
    gitUtils.deleteRemoteBranch.mockRejectedValue(new Error('remote failed'));

    const result = await deleteIterationBranch('008', { cwd });
    const metadata = JSON.parse(fs.readFileSync(path.join(cwd, '.powerby', 'iterations.json'), 'utf-8'));

    expect(result.message).toContain('远程分支删除失败');
    expect(metadata.iterations[0].branch_info.status).toBe('deleted_local_only');
  });

  test('应支持一键切换到期望分支', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
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

    gitUtils.getCurrentBranch.mockResolvedValue('main');
    gitUtils.branchExists.mockResolvedValue(true);
    gitUtils.isWorkingTreeClean.mockResolvedValue(true);

    const result = await switchIterationBranch('008', { cwd });
    expect(result.success).toBe(true);
    expect(gitUtils.checkoutBranch).toHaveBeenCalledWith('feature/008-git-branch-automation', cwd);
  });

  test('应支持单独执行冲突预检测', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
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

    detectMergeConflicts.mockResolvedValue({ hasConflict: false, conflictFiles: [], message: 'ok' });
    const result = await detectIterationMergeConflicts('008', 'develop', { cwd });
    expect(result.hasConflict).toBe(false);
  });

  test('应透传分支合规检查', async () => {
    const cwd = createTempProject();

    fs.writeFileSync(
      path.join(cwd, '.powerby', 'iterations.json'),
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

    gitUtils.getCurrentBranch.mockResolvedValue('feature/008-git-branch-automation');

    const report = await checkIterationBranchCompliance('008', 'P1', { cwd });
    expect(report.compliant).toBe(true);
  });
});
