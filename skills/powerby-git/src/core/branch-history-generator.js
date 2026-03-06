/**
 * 分支历史报告生成器
 */

const fs = require('fs');
const path = require('path');
const { createError } = require('./errors');
const {
  getIterationRecord,
  updateIterationDocuments
} = require('./iteration-tracker');
const {
  getDetailedCommitHistory,
  getGitUser
} = require('../utils/git');

/**
 * 转义 Mermaid 文本。
 * @param {string} value - 原始字符串。
 * @returns {string} 转义后的字符串。
 */
function escapeMermaidText(value) {
  return String(value || '').replace(/"/g, '\\"');
}

/**
 * 构建 Mermaid gitGraph 内容。
 * @param {string} branchName - 分支名。
 * @param {string} targetBranch - 目标分支。
 * @param {Object[]} commits - 提交历史。
 * @param {Object|null} mergeRecord - 合并记录。
 * @returns {string} Mermaid 内容。
 */
function buildGitGraph(branchName, targetBranch, commits, mergeRecord) {
  const lines = ['gitGraph', '  commit id: "base"', `  branch ${branchName}`];

  for (const commit of commits.slice(0, 20).reverse()) {
    lines.push(`  commit id: "${escapeMermaidText(commit.message)}"`);
  }

  if (mergeRecord) {
    lines.push(`  checkout ${targetBranch}`);
    lines.push(`  merge ${branchName}`);
  }

  return lines.join('\n');
}

/**
 * 构建提交历史表格。
 * @param {Object[]} commits - 提交历史。
 * @returns {string} Markdown 表格。
 */
function buildCommitTable(commits) {
  const header = [
    '| Commit Hash | Author | Date | Message |',
    '|-------------|--------|------|---------|'
  ];

  const rows = commits.map((commit) => {
    return `| ${commit.hash.slice(0, 7)} | ${commit.author_name} | ${commit.timestamp} | ${commit.message.replace(/\|/g, '\\|')} |`;
  });

  return [...header, ...rows].join('\n');
}

/**
 * 组装完整分支历史报告。
 * @param {Object} options - 组装参数。
 * @param {Object} options.iteration - 迭代记录。
 * @param {Object[]} options.commits - 提交历史。
 * @param {Object|null} options.mergeRecord - 合并记录。
 * @returns {string} Markdown 报告内容。
 */
function buildHistoryReport({ iteration, commits, mergeRecord }) {
  const branchName = iteration.branch_info.branch_name;
  const targetBranch = iteration.branch_info.target_branch || 'develop';
  const mergeSection = mergeRecord
    ? [
        `- **源分支**: ${mergeRecord.source_branch}`,
        `- **目标分支**: ${mergeRecord.target_branch}`,
        `- **合并时间**: ${mergeRecord.merged_at}`,
        `- **合并者**: ${mergeRecord.merger}`,
        `- **合并邮箱**: ${mergeRecord.merger_email}`,
        `- **合并提交**: ${mergeRecord.merge_commit_hash}`,
        '- **合并策略**: --no-ff'
      ].join('\n')
    : '- 尚未合并，当前报告为预生成版本';

  return [
    `# Branch History: ${branchName}`,
    '',
    '## 提交历史',
    buildCommitTable(commits),
    '',
    '## 分支图',
    '```mermaid',
    buildGitGraph(branchName, targetBranch, commits, mergeRecord),
    '```',
    '',
    '## 合并记录',
    mergeSection,
    '',
    `---`,
    `- **迭代编号**: ${iteration.id}`,
    `- **报告生成时间**: ${new Date().toISOString()}`
  ].join('\n');
}

/**
 * 写入分支历史报告并更新文档索引。
 * @param {string} iterationId - 迭代编号。
 * @param {Object|null} mergeRecord - 合并记录。
 * @param {Object} options - 运行选项。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Promise<{success:boolean, reportPath:string, message:string}>}
 */
async function writeBranchHistoryReport(iterationId, mergeRecord = null, options = {}) {
  const cwd = options.cwd || process.cwd();
  const iteration = getIterationRecord(iterationId, cwd);

  if (!iteration.branch_info || !iteration.branch_info.branch_name) {
    throw createError('E020', `迭代缺少 branch_info: iterationId="${iterationId}"`);
  }

  const commits = await getDetailedCommitHistory(
    iteration.branch_info.branch_name,
    iteration.branch_info.source_branch || 'develop',
    cwd
  );
  const report = buildHistoryReport({ iteration, commits, mergeRecord });
  const reportPath = path.join(cwd, 'docs', 'iterations', iteration.full_name, 'branch-history.md');

  try {
    fs.mkdirSync(path.dirname(reportPath), { recursive: true });
    fs.writeFileSync(reportPath, `${report}\n`, 'utf-8');
  } catch (error) {
    throw createError('E020', `写入分支历史报告失败: ${error.message}`);
  }

  updateIterationDocuments({
    iterationId,
    documents: {
      branch_history: path.join('docs', 'iterations', iteration.full_name, 'branch-history.md').replace(/\\/g, '/')
    },
    cwd
  });

  return {
    success: true,
    reportPath,
    message: mergeRecord ? '已更新分支历史报告' : '已生成分支历史报告'
  };
}

/**
 * 生成初始分支历史报告。
 * @param {string} iterationId - 迭代编号。
 * @param {Object} options - 运行选项。
 * @returns {Promise<{success:boolean, reportPath:string, message:string}>}
 */
async function generateBranchHistoryReport(iterationId, options = {}) {
  return writeBranchHistoryReport(iterationId, null, options);
}

/**
 * 更新分支历史报告中的合并记录。
 * @param {string} iterationId - 迭代编号。
 * @param {Object} mergeRecord - 合并记录。
 * @param {Object} options - 运行选项。
 * @returns {Promise<{success:boolean, reportPath:string, message:string}>}
 */
async function updateBranchHistoryReport(iterationId, mergeRecord, options = {}) {
  if (!mergeRecord || typeof mergeRecord !== 'object') {
    throw createError('E020', 'mergeRecord 必须是对象');
  }

  return writeBranchHistoryReport(iterationId, mergeRecord, options);
}

/**
 * 使用当前 Git 用户信息补齐合并者信息。
 * @param {Object} mergeRecord - 原始合并记录。
 * @param {string} [cwd] - 工作目录。
 * @returns {Promise<Object>} 补齐后的合并记录。
 */
async function enrichMergeRecord(mergeRecord, cwd = process.cwd()) {
  const gitUser = await getGitUser(cwd);
  return {
    ...mergeRecord,
    merger: mergeRecord.merger || gitUser.name,
    merger_email: mergeRecord.merger_email || gitUser.email
  };
}

module.exports = {
  escapeMermaidText,
  buildGitGraph,
  buildCommitTable,
  buildHistoryReport,
  generateBranchHistoryReport,
  updateBranchHistoryReport,
  enrichMergeRecord
};
