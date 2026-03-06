/**
 * 迭代元数据追踪器测试
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  readIterationsData,
  ensureIterationRecord,
  getIterationRecord,
  updateIterationBranchInfo
} = require('../../src/core/iteration-tracker');

function createTempProject() {
  const tempDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'powerby-git-iteration-tracker-'));
  const powerbyDirectory = path.join(tempDirectory, '.powerby');

  fs.mkdirSync(powerbyDirectory, { recursive: true });
  fs.writeFileSync(
    path.join(powerbyDirectory, 'iterations.json'),
    JSON.stringify({ iterations: [], current_iteration: null, completed_iterations: 0, total_iterations: 0 }, null, 2)
  );

  return tempDirectory;
}

describe('Iteration Tracker', () => {
  test('应为缺失的迭代自动创建记录', () => {
    const cwd = createTempProject();

    ensureIterationRecord({
      iterationId: '008',
      iterationName: 'git-branch-automation',
      phase: 'P5',
      cwd
    });

    const record = getIterationRecord('008', cwd);

    expect(record.id).toBe('008');
    expect(record.name).toBe('git-branch-automation');
    expect(record.phase).toBe('P5');
  });

  test('应更新 branch_info 并同步 current_iteration', () => {
    const cwd = createTempProject();

    updateIterationBranchInfo({
      iterationId: '008',
      iterationName: 'git-branch-automation',
      phase: 'P6',
      branchInfo: {
        branch_name: 'feature/008-git-branch-automation',
        status: 'active',
        created_at: '2026-03-06T00:00:00.000Z'
      },
      cwd
    });

    const data = readIterationsData(cwd);
    const iteration = data.iterations[0];

    expect(data.current_iteration).toBe('008');
    expect(iteration.branch).toBe('feature/008-git-branch-automation');
    expect(iteration.branch_info.status).toBe('active');
    expect(iteration.phase).toBe('P6');
  });

  test('应在名称不一致时快速失败', () => {
    const cwd = createTempProject();

    ensureIterationRecord({
      iterationId: '008',
      iterationName: 'git-branch-automation',
      phase: 'P5',
      cwd
    });

    expect(() => ensureIterationRecord({
      iterationId: '008',
      iterationName: 'another-name',
      phase: 'P5',
      cwd
    })).toThrow('迭代名称不一致');
  });
});
