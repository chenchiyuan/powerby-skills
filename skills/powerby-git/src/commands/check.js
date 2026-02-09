/**
 * Check Command - 执行合规性检查
 */

const chalk = require('chalk');
const path = require('path');
const {
  validateFile,
  validateFileList,
  scanDirectory
} = require('../core/file-whitelist');
const { validateCommitMessage, getCommitTypes } = require('../core/commit-validator');
const { getFileStatus, getBranchStatus } = require('../utils/git');

/**
 * 执行提交检查
 * @param {Object} options - 命令选项
 * @returns {Promise<Object>}
 */
async function executeCommitCheck(options) {
  const { cwd = process.cwd() } = options;

  const gitStatus = await getBranchStatus(cwd);

  // 获取待提交文件
  const filesToCheck = [
    ...gitStatus.staged,
    ...gitStatus.unstaged,
    ...gitStatus.not_tracked
  ];

  const result = validateFileList(filesToCheck);

  return {
    type: 'commit',
    staged: gitStatus.staged,
    unstaged: gitStatus.unstaged,
    not_tracked: gitStatus.not_tracked,
    ...result
  };
}

/**
 * 执行合并检查
 * @param {Object} options - 命令选项
 * @returns {Promise<Object>}
 */
async function executeMergeCheck(options) {
  const { cwd = process.cwd() } = options;

  // 全量扫描工作区
  const files = scanDirectory(cwd, [
    /node_modules/,
    /\.git/,
    /\.dist/,
    /dist$/,
    /build$/
  ]);

  // 转换为相对路径
  const relativeFiles = files.map(f => path.relative(cwd, f));

  const result = validateFileList(relativeFiles);

  return {
    type: 'merge',
    ...result
  };
}

/**
 * 执行 full 检查
 * @param {Object} options - 命令选项
 * @returns {Promise<Object>}
 */
async function executeFullCheck(options) {
  const [commitResult, mergeResult] = await Promise.all([
    executeCommitCheck(options),
    executeMergeCheck(options)
  ]);

  return {
    type: 'full',
    commitCheck: commitResult,
    mergeCheck: mergeResult
  };
}

/**
 * 执行 check 命令
 * @param {Object} options - 命令选项
 * @param {string} [options.type] - 检查类型 (commit|merge|full)
 * @param {string} [options.message] - 提交信息（用于验证）
 * @param {string} [options.cwd] - 工作目录
 * @returns {Promise<Object>}
 */
async function executeCheck(options) {
  const { type = 'commit', message = null, cwd = process.cwd() } = options;

  let result;

  switch (type) {
    case 'commit':
      result = await executeCommitCheck({ cwd });
      break;
    case 'merge':
      result = await executeMergeCheck({ cwd });
      break;
    case 'full':
      result = await executeFullCheck({ cwd });
      break;
    default:
      throw new Error(`未知的检查类型: ${type}`);
  }

  // 如果提供了提交信息，也验证提交格式
  if (message) {
    const commitValidation = validateCommitMessage(message);
    result.commitMessageValidation = commitValidation;
  }

  return result;
}

/**
 * 格式化检查报告
 * @param {Object} result - 检查结果
 * @returns {string}
 */
function formatCheckReport(result) {
  let output = '\n';

  if (result.type === 'full') {
    output += chalk.cyan('🔍 全量检查报告\n');
    output += chalk.gray('---'.repeat(40)) + '\n\n';

    output += chalk.yellow('📝 提交检查:\n');
    output += formatCommitCheckResult(result.commitCheck) + '\n';

    output += chalk.yellow('📁 全量文件检查:\n');
    output += formatMergeCheckResult(result.mergeCheck) + '\n';
  } else if (result.type === 'commit') {
    output += chalk.cyan('🔍 提交检查\n');
    output += formatCommitCheckResult(result) + '\n';
  } else {
    output += chalk.cyan('🔍 合并检查\n');
    output += formatMergeCheckResult(result) + '\n';
  }

  return output;
}

/**
 * 格式化提交检查结果
 * @param {Object} result - 检查结果
 * @returns {string}
 */
function formatCommitCheckResult(result) {
  let output = '';

  const fileCount = result.staged.length + result.unstaged.length + result.not_tracked.length;
  output += `   文件数: ${fileCount}\n`;

  if (result.invalidFiles.length === 0) {
    output += chalk.green('   ✅ 所有文件合规\n');
  } else {
    output += chalk.red(`   ❌ 发现 ${result.invalidFiles.length} 个问题文件\n`);

    for (const file of result.invalidFiles) {
      output += `      - ${file.path} (${file.message})\n`;
    }

    output += chalk.cyan('\n   💡 建议删除临时文件后重新提交\n');
  }

  // 提交信息验证
  if (result.commitMessageValidation) {
    output += '\n   📝 提交信息:\n';
    if (result.commitMessageValidation.valid) {
      output += chalk.green('   ✅ 格式正确\n');
    } else {
      output += chalk.red('   ❌ 格式错误\n');
      for (const error of result.commitMessageValidation.errors) {
        output += `      - ${error}\n`;
      }
    }
  }

  return output;
}

/**
 * 格式化合并检查结果
 * @param {Object} result - 检查结果
 * @returns {string}
 */
function formatMergeCheckResult(result) {
  let output = '';

  output += `   总文件: ${result.summary.total}\n`;
  output += `   合法文件: ${chalk.green(result.summary.valid)}\n`;
  output += `   问题文件: ${chalk.red(result.summary.invalid)}\n\n`;

  if (result.invalidFiles.length === 0) {
    output += chalk.green('   ✅ 所有文件合规，可以合并\n');
  } else {
    output += chalk.red('   ⚠️ 发现以下问题文件:\n');

    // 按类别分组
    const byCategory = {};
    for (const file of result.invalidFiles) {
      if (!byCategory[file.category]) {
        byCategory[file.category] = [];
      }
      byCategory[file.category].push(file.path);
    }

    for (const [category, files] of Object.entries(byCategory)) {
      output += `\n   [${category}]:\n`;
      for (const file of files.slice(0, 10)) {
        output += `      - ${file}\n`;
      }
      if (files.length > 10) {
        output += `      ... 还有 ${files.length - 10} 个\n`;
      }
    }

    output += chalk.cyan('\n   💡 请清理问题文件后再合并\n');
  }

  return output;
}

/**
 * 命令配置
 */
function configureCheckCommand(program) {
  program
    .command('check')
    .description('执行合规性检查')
    .option('--type <type>', '检查类型 (commit|merge|full)', 'commit')
    .option('--message <message>', '提交信息（用于验证格式）')
    .action(async (options) => {
      try {
        const result = await executeCheck(options);
        console.log(formatCheckReport(result));

        // 根据结果决定退出码
        let hasError = false;
        if (result.type === 'full') {
          hasError = result.commitCheck.invalidFiles.length > 0 || result.mergeCheck.invalidFiles.length > 0;
        } else if (result.type === 'commit') {
          hasError = result.invalidFiles.length > 0;
        } else {
          hasError = result.invalidFiles.length > 0;
        }

        if (hasError) {
          process.exit(1);
        }
      } catch (error) {
        console.error('\n' + chalk.red('❌ ' + error.message));
        process.exit(1);
      }
    });
}

module.exports = {
  executeCheck,
  executeCommitCheck,
  executeMergeCheck,
  executeFullCheck,
  formatCheckReport,
  configureCheckCommand
};
