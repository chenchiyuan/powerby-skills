/**
 * 分支历史报告生成器测试
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

jest.mock('../../src/utils/git', () => ({
  getDetailedCommitHistory: jest.fn(),
  getGitUser: jest.fn()
}));

const gitUtils = require('../../src/utils/git');
const {
  buildGitGraph,
  generateBranchHistoryReport,
  updateBranchHistoryReport,
  enrichMergeRecord
} = require('../../src/core/branch-history-generator');

function createTempProject() {
  const tempDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'powerby-git-history-'));
  const powerbyDirectory = path.join(tempDirectory, '.powerby');
  const docsDirectory = path.join(tempDirectory, 'docs', 'iterations', '008-git-branch-automation');

  fs.mkdirSync(powerbyDirectory, { recursive: true });
  fs.mkdirSync(docsDirectory, { recursive: true });
  fs.writeFileSync(
    path.join(powerbyDirectory, 'iterations.json'),
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
            status: 'active',
            source_branch: 'develop',
            target_branch: 'develop'
          },
          documents: {}
        }
      ],
      current_iteration: '008',
      completed_iterations: 0,
      total_iterations: 1
    }, null, 2)
  );

  return tempDirectory;
}

describe('Branch History Generator', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    gitUtils.getDetailedCommitHistory.mockResolvedValue([
      {
        hash: 'abc1234567',
        author_name: 'Alice',
        author_email: 'alice@example.com',
        timestamp: '2026-03-06T10:00:00Z',
        message: 'feat: add automation'
      }
    ]);
    gitUtils.getGitUser.mockResolvedValue({ name: 'Bob', email: 'bob@example.com' });
  });

  test('应构建带 merge 行的 mermaid 图', () => {
    const graph = buildGitGraph('feature/008-git-branch-automation', 'develop', [{ message: 'feat' }], {
      merge_commit_hash: 'abc'
    });

    expect(graph).toContain('branch feature/008-git-branch-automation');
    expect(graph).toContain('merge feature/008-git-branch-automation');
  });

  test('应生成分支历史报告文件', async () => {
    const cwd = createTempProject();
    const result = await generateBranchHistoryReport('008', { cwd });
    const content = fs.readFileSync(result.reportPath, 'utf-8');

    expect(content).toContain('# Branch History: feature/008-git-branch-automation');
    expect(content).toContain('feat: add automation');
  });

  test('应更新合并记录', async () => {
    const cwd = createTempProject();
    await updateBranchHistoryReport('008', {
      merge_commit_hash: 'merge123',
      merger: 'Bob',
      merger_email: 'bob@example.com',
      merged_at: '2026-03-06T12:00:00Z',
      source_branch: 'feature/008-git-branch-automation',
      target_branch: 'develop'
    }, { cwd });

    const content = fs.readFileSync(path.join(cwd, 'docs', 'iterations', '008-git-branch-automation', 'branch-history.md'), 'utf-8');
    expect(content).toContain('merge123');
    expect(content).toContain('Bob');
  });

  test('应使用当前 git 用户补齐合并者信息', async () => {
    const result = await enrichMergeRecord({ merge_commit_hash: 'abc' });

    expect(result.merger).toBe('Bob');
    expect(result.merger_email).toBe('bob@example.com');
  });
});
