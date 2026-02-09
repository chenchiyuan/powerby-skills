/**
 * Cleanup Command - 清理已合并的分支
 */

const chalk = require('chalk');
const { getMergedBranches, deleteBranch, getCurrentBranch, branchExists } = require('../utils/git');
const { createError } = require('../core/errors');

/**
 * 执行 cleanup 命令
 * @param {Object} options - 命令选项
 * @param {boolean} [options.dryRun] - 预览模式
 * @param {boolean} [options.force] - 强制执行
 * @param {string} [options.mainBranch] - 主分支名
 * @param {string} [options.cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function executeCleanup(options) {
  const { dryRun = false, force = false, mainBranch = 'main', cwd = process.cwd() } = options;

  // 获取当前分支
  const currentBranch = await getCurrentBranch(cwd);

  // 获取已合并分支
  const mergedBranches = await getMergedBranches(mainBranch, cwd);

  // 排除当前分支
  const branchesToDelete = mergedBranches.filter(b => b !== currentBranch);

  if (branchesToDelete.length === 0) {
    return {
      success: true,
      message: '没有需要清理的分支',
      branchesToDelete: [],
      deletedBranches: []
    };
  }

  // 如果是预览模式，直接返回
  if (dryRun) {
    return {
      success: true,
      message: '预览模式',
      branchesToDelete,
      deletedBranches: [],
      dryRun: true
    };
  }

  // 如果不是强制模式，需要用户确认
  if (!force) {
    // 返回待确认的信息
    return {
      success: true,
      message: '需要确认',
      branchesToDelete,
      deletedBranches: [],
      needConfirm: true
    };
  }

  // 执行删除
  const deletedBranches = [];
  const failedBranches = [];

  for (const branch of branchesToDelete) {
    try {
      // 检查分支是否还存在
      if (await branchExists(branch, cwd)) {
        await deleteBranch(branch, cwd);
        deletedBranches.push(branch);
      }
    } catch (error) {
      failedBranches.push({
        branch,
        error: error.message
      });
    }
  }

  return {
    success: true,
    message: '清理完成',
    branchesToDelete,
    deletedBranches,
    failedBranches,
    dryRun: false
  };
}

/**
 * 格式化清理报告
 * @param {Object} result - 执行结果
 * @returns {string}
 */
function formatCleanupReport(result) {
  let output = '\n';
  const separator = '-'.repeat(40);

  if (result.dryRun) {
    output += chalk.cyan('Preview - Branches to Cleanup\n');
    output += chalk.gray(separator) + '\n\n';
  } else {
    output += chalk.cyan('Branch Cleanup Report\n');
    output += chalk.gray(separator) + '\n\n';
  }

  if (result.branchesToDelete.length === 0) {
    output += chalk.green('✅ 没有需要清理的分支\n');
    return output;
  }

  output += `待清理分支数: ${result.branchesToDelete.length}\n\n`;

  for (const branch of result.branchesToDelete) {
    output += `   ${chalk.yellow('○')} ${branch}\n`;
  }

  if (result.dryRun) {
    output += chalk.cyan('\n💡 提示:\n');
    output += `   运行 ${chalk.cyan('powerby-git cleanup --force')} 执行清理\n`;
  } else if (result.deletedBranches.length > 0) {
    output += chalk.green('\n✅ 已删除分支:\n');
    for (const branch of result.deletedBranches) {
      output += `   ${chalk.green('✓')} ${branch}\n`;
    }
  }

  if (result.failedBranches && result.failedBranches.length > 0) {
    output += chalk.red('\n❌ 删除失败:\n');
    for (const { branch, error } of result.failedBranches) {
      output += `   - ${branch}: ${error}\n`;
    }
  }

  return output;
}

/**
 * 命令配置
 */
function configureCleanupCommand(program) {
  program
    .command('cleanup')
    .description('清理已合并到主分支的分支')
    .option('--dry-run', '预览模式，不实际删除')
    .option('--force', '强制执行，不询问确认')
    .option('--main-branch <name>', '主分支名', 'main')
    .action(async (options) => {
      try {
        const result = await executeCleanup(options);
        console.log(formatCleanupReport(result));

        // 如果需要确认，提示用户
        if (result.needConfirm) {
          console.log(chalk.cyan('\n⚠️  确认删除这些分支？'));
          console.log(`   运行 ${chalk.cyan('powerby-git cleanup --force')} 确认执行`);
          process.exit(0);
        }
      } catch (error) {
        console.error('\n' + chalk.red('❌ ' + error.message));
        process.exit(1);
      }
    });
}

module.exports = {
  executeCleanup,
  formatCleanupReport,
  configureCleanupCommand
};
