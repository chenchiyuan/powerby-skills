/**
 * List Command - 列出分支
 */

const chalk = require('chalk');
const { getAllBranches, isBranchMerged, getLastCommitForBranch } = require('../utils/git');

/**
 * 获取分支信息
 * @param {string} branchName - 分支名
 * @param {string} mainBranch - 主分支名
 * @returns {Promise<Object>}
 */
async function getBranchInfo(branchName, mainBranch, cwd = process.cwd()) {
  const [lastCommit, merged] = await Promise.all([
    getLastCommitForBranch(branchName, cwd),
    isBranchMerged(branchName, mainBranch, cwd)
  ]);

  return {
    name: branchName,
    lastCommit: lastCommit ? {
      hash: lastCommit.hash.substring(0, 7),
      message: lastCommit.message,
      date: lastCommit.date
    } : null,
    isMerged: merged
  };
}

/**
 * 执行 list 命令
 * @param {Object} options - 命令选项
 * @param {boolean} [options.merged] - 只显示已合并的分支
 * @param {boolean} [options.unmerged] - 只显示未合并的分支
 * @param {string} [options.mainBranch] - 主分支名
 * @param {string} [options.cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function executeList(options) {
  const { merged = false, unmerged = false, mainBranch = 'main', cwd = process.cwd() } = options;

  const branches = await getAllBranches(cwd);
  const mainBranches = [mainBranch, 'master', 'develop'];

  // 过滤主分支
  const filteredBranches = branches.filter(b => !mainBranches.includes(b));

  const branchInfos = await Promise.all(
    filteredBranches.map(b => getBranchInfo(b, mainBranch, cwd))
  );

  // 按已合并状态过滤
  let displayBranches = branchInfos;
  if (merged) {
    displayBranches = branchInfos.filter(b => b.isMerged);
  } else if (unmerged) {
    displayBranches = branchInfos.filter(b => !b.isMerged);
  }

  // 排序：未合并的在前，已合并的在后
  displayBranches.sort((a, b) => {
    if (a.isMerged === b.isMerged) return 0;
    return a.isMerged ? 1 : -1;
  });

  return {
    success: true,
    branches: displayBranches,
    count: displayBranches.length,
    mergedCount: displayBranches.filter(b => b.isMerged).length,
    unmergedCount: displayBranches.filter(b => !b.isMerged).length
  };
}

/**
 * 格式化输出分支列表
 * @param {Object} result - 执行结果
 * @returns {string}
 */
function formatBranchList(result) {
  let output = '\n';

  // 统计信息
  output += chalk.cyan('📊 分支统计\n');
  output += `   总数: ${result.count} | `;
  output += chalk.green(`已合并: ${result.mergedCount}`) + ' | ';
  output += chalk.yellow(`未合并: ${result.unmergedCount}\n`);
  output += '\n';

  if (result.branches.length === 0) {
    output += chalk.gray('   没有符合条件分支\n');
    return output;
  }

  // 分支列表
  output += chalk.cyan('📋 分支列表\n');

  for (const branch of result.branches) {
    const statusIcon = branch.isMerged ? chalk.green('✓') : chalk.yellow('○');
    const mergedLabel = branch.isMerged ? chalk.gray(' [已合并]') : '';

    output += `   ${statusIcon} ${branch.name}${mergedLabel}\n`;

    if (branch.lastCommit) {
      const hash = chalk.gray(branch.lastCommit.hash);
      const message = branch.lastCommit.message.length > 40
        ? branch.lastCommit.message.substring(0, 40) + '...'
        : branch.lastCommit.message;
      output += `      ${hash} ${message}\n`;
    }
  }

  return output;
}

/**
 * 命令配置
 */
function configureListCommand(program) {
  program
    .command('list')
    .description('列出所有本地分支')
    .option('--merged', '只显示已合并的分支')
    .option('--unmerged', '只显示未合并的分支')
    .option('--main-branch <name>', '主分支名', 'main')
    .action(async (options) => {
      try {
        const result = await executeList(options);
        console.log(formatBranchList(result));

        // 提示清理
        if (result.mergedCount > 0) {
          console.log(chalk.cyan('\n💡 提示:'));
          console.log(`   运行 ${chalk.cyan('powerby-git cleanup --dry-run')} 预览待清理分支`);
        }
      } catch (error) {
        console.error('\n' + chalk.red('❌ ' + error.message));
        process.exit(1);
      }
    });
}

module.exports = {
  executeList,
  formatBranchList,
  configureListCommand
};
