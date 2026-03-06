/**
 * Iteration Command - 迭代分支自动化命令
 */

const chalk = require('chalk');
const {
  createIterationBranch,
  checkIterationBranchCompliance,
  switchIterationBranch,
  detectIterationMergeConflicts,
  mergeIterationBranch,
  deleteIterationBranch,
  generateBranchHistoryReport
} = require('../integrations/asp');

/**
 * 格式化分支合规检查结果。
 * @param {Object} result - 检查结果。
 * @returns {string} 终端输出。
 */
function formatComplianceResult(result) {
  let output = '\n';
  output += chalk.cyan('Iteration Branch Compliance\n');
  output += `${result.compliant ? chalk.green('✅') : chalk.yellow('⚠️')} 当前分支: ${result.currentBranch}\n`;
  output += `${chalk.cyan('🎯')} 期望分支: ${result.expectedBranch}\n`;

  if (result.warnings.length > 0) {
    output += '\n';
    for (const warning of result.warnings) {
      const icon = warning.level === 'error' ? chalk.red('✗') : chalk.yellow('!');
      output += `${icon} ${warning.message}\n`;
      output += `  ${chalk.gray(warning.suggestion)}\n`;
    }
  }

  return output;
}

/**
 * 配置迭代命令。
 * @param {import('commander').Command} program - CLI 程序。
 */
function configureIterationCommand(program) {
  const iteration = program
    .command('iteration')
    .description('迭代分支自动化管理');

  iteration
    .command('create')
    .requiredOption('--id <id>', '迭代编号')
    .requiredOption('--name <name>', '迭代名称')
    .option('--source-branch <branch>', '源分支', 'develop')
    .action(async (options) => {
      try {
        const result = await createIterationBranch(options.id, options.name, options.sourceBranch);
        console.log(`\n${chalk.green('✅')} ${result.message}`);
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });

  iteration
    .command('check')
    .requiredOption('--id <id>', '迭代编号')
    .requiredOption('--phase <phase>', '阶段，如 P1/P6/P8')
    .option('--switch', '检查失败时自动切换到目标分支')
    .action(async (options) => {
      try {
        const result = await checkIterationBranchCompliance(options.id, options.phase);
        console.log(formatComplianceResult(result));

        if (options.switch && result.currentBranch !== result.expectedBranch) {
          const switchResult = await switchIterationBranch(options.id);
          console.log(chalk.green(`✅ ${switchResult.message}`));
        }

        if (!result.compliant) {
          process.exit(1);
        }
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });

  iteration
    .command('switch')
    .requiredOption('--id <id>', '迭代编号')
    .action(async (options) => {
      try {
        const result = await switchIterationBranch(options.id);
        console.log(`\n${chalk.green('✅')} ${result.message}`);
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });

  iteration
    .command('conflicts')
    .requiredOption('--id <id>', '迭代编号')
    .option('--target-branch <branch>', '目标分支', 'develop')
    .action(async (options) => {
      try {
        const result = await detectIterationMergeConflicts(options.id, options.targetBranch);
        if (result.hasConflict) {
          console.log(`\n${chalk.yellow('⚠️')} ${result.message}`);
          for (const file of result.conflictFiles) {
            console.log(` - ${file}`);
          }
          process.exit(1);
        }

        console.log(`\n${chalk.green('✅')} ${result.message}`);
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });

  iteration
    .command('merge')
    .requiredOption('--id <id>', '迭代编号')
    .option('--target-branch <branch>', '目标分支', 'develop')
    .option('--confirm', '确认执行合并')
    .action(async (options) => {
      try {
        if (!options.confirm) {
          console.log(chalk.yellow('\n⚠️  合并是破坏性操作，请追加 --confirm 后重试'));
          process.exit(1);
        }

        const result = await mergeIterationBranch(options.id, options.targetBranch);
        if (result.hasConflict) {
          console.log(`\n${chalk.yellow('⚠️')} ${result.message}`);
          for (const file of result.conflictFiles || []) {
            console.log(` - ${file}`);
          }
          process.exit(1);
        }

        console.log(`\n${chalk.green('✅')} ${result.message}`);
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });

  iteration
    .command('delete')
    .requiredOption('--id <id>', '迭代编号')
    .option('--confirm', '确认执行删除')
    .action(async (options) => {
      try {
        if (!options.confirm) {
          console.log(chalk.yellow('\n⚠️  删除分支是破坏性操作，请追加 --confirm 后重试'));
          process.exit(1);
        }

        const result = await deleteIterationBranch(options.id);
        console.log(`\n${chalk.green('✅')} ${result.message}`);
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });

  iteration
    .command('history')
    .requiredOption('--id <id>', '迭代编号')
    .action(async (options) => {
      try {
        const result = await generateBranchHistoryReport(options.id);
        console.log(`\n${chalk.green('✅')} ${result.message}: ${result.reportPath}`);
      } catch (error) {
        console.error(`\n${chalk.red('❌')} ${error.message}`);
        process.exit(1);
      }
    });
}

module.exports = {
  formatComplianceResult,
  configureIterationCommand
};
