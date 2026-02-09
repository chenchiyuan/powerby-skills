/**
 * Status Command - 查看当前状态
 */

const chalk = require('chalk');
const { getBranchStatus, getCurrentBranch } = require('../utils/git');
const { validateFileList } = require('../core/file-whitelist');

/**
 * 执行 status 命令
 * @param {Object} options - 命令选项
 * @param {string} [options.cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function executeStatus(options) {
  const { cwd = process.cwd() } = options;

  const [branchStatus, currentBranch] = await Promise.all([
    getBranchStatus(cwd),
    getCurrentBranch(cwd)
  ]);

  // 获取所有变更文件
  const allFiles = [
    ...branchStatus.staged,
    ...branchStatus.unstaged,
    ...branchStatus.not_tracked
  ];

  // 检查文件合规性
  const validation = validateFileList(allFiles);

  // 识别临时文件
  const tempFiles = validation.invalidFiles.filter(f =>
    f.category === 'temporary' || f.category === 'unknown'
  );

  return {
    success: true,
    currentBranch,
    branchStatus,
    fileValidation: validation,
    tempFiles,
    suggestions: generateSuggestions(validation, tempFiles)
  };
}

/**
 * 生成建议
 * @param {Object} validation - 验证结果
 * @param {Array} tempFiles - 临时文件
 * @returns {string[]}
 */
function generateSuggestions(validation, tempFiles) {
  const suggestions = [];

  if (tempFiles.length > 0) {
    suggestions.push(`发现 ${tempFiles.length} 个临时文件，建议删除`);
  }

  if (validation.invalidFiles.length > 0) {
    suggestions.push('运行 powerby-git check --type=commit 检查详情');
  }

  if (branchStatus.isClean && tempFiles.length === 0) {
    suggestions.push('工作区很干净，可以提交了');
  }

  return suggestions;
}

/**
 * 格式化状态报告
 * @param {Object} result - 执行结果
 * @returns {string}
 */
function formatStatusReport(result) {
  let output = '\n';

  // 分支信息
  output += chalk.cyan('🔀 分支状态\n');
  output += chalk.gray('---'.repeat(40)) + '\n';
  output += `   当前分支: ${chalk.green(result.currentBranch)}\n`;
  output += '\n';

  // 变更统计
  output += chalk.cyan('📊 变更统计\n');
  output += chalk.gray('---'.repeat(40)) + '\n';
  output += `   已暂存: ${result.branchStatus.staged.length}\n`;
  output += `   已修改: ${result.branchStatus.unstaged.length}\n`;
  output += `   未跟踪: ${result.branchStatus.not_tracked.length}\n`;
  output += '\n';

  // 文件合规性
  output += chalk.cyan('✅ 文件合规性\n');
  output += chalk.gray('---'.repeat(40)) + '\n';
  output += `   合法文件: ${chalk.green(result.fileValidation.summary.valid)}\n`;
  output += `   问题文件: ${chalk.red(result.fileValidation.summary.invalid)}\n`;
  output += '\n';

  // 临时文件
  if (result.tempFiles.length > 0) {
    output += chalk.yellow('⚠️  临时文件:\n');
    for (const file of result.tempFiles) {
      output += `   - ${file.path} (${file.message})\n`;
    }
    output += '\n';
  }

  // 建议
  if (result.suggestions.length > 0) {
    output += chalk.cyan('💡 建议:\n');
    for (const suggestion of result.suggestions) {
      output += `   - ${suggestion}\n`;
    }
    output += '\n';
  }

  return output;
}

/**
 * 命令配置
 */
function configureStatusCommand(program) {
  program
    .command('status')
    .description('查看当前分支和工作区状态')
    .action(async (options) => {
      try {
        const result = await executeStatus(options);
        console.log(formatStatusReport(result));
      } catch (error) {
        console.error('\n' + chalk.red('❌ ' + error.message));
        process.exit(1);
      }
    });
}

module.exports = {
  executeStatus,
  formatStatusReport,
  configureStatusCommand
};
