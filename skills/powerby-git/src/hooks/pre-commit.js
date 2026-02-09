#!/usr/bin/env node

/**
 * Pre-commit Hook
 * 在 git commit 时自动检查
 */

const chalk = require('chalk');
const path = require('path');
const { getBranchStatus, getLastCommit } = require('../utils/git');
const { validateFileList } = require('../core/file-whitelist');
const { validateCommitMessage } = require('../core/commit-validator');

/**
 * 获取提交信息
 * @returns {string|null}
 */
function getCommitMessage() {
  const commitMsgFile = process.env.GIT_PARAMS ||
                        process.env.GIT_INDEX_FILE ||
                        path.join(process.cwd(), '.git', 'COMMIT_EDITMSG');

  if (fs.existsSync(commitMsgFile)) {
    return fs.readFileSync(commitMsgFile, 'utf-8');
  }
  return null;
}

// 引入 fs（如果上面使用）
const fs = require('fs');

/**
 * 执行检查
 */
async function runCheck() {
  console.log(chalk.cyan('\n🔍 powerby-git: 提交前检查\n'));

  try {
    const cwd = process.cwd();
    const gitStatus = await getBranchStatus(cwd);

    // 获取待提交文件
    const filesToCheck = [
      ...gitStatus.staged,
      ...gitStatus.unstaged
    ];

    if (filesToCheck.length === 0) {
      console.log(chalk.green('✅ 没有待提交文件，跳过检查'));
      process.exit(0);
    }

    // 检查文件合规性
    const fileResult = validateFileList(filesToCheck);

    // 获取提交信息并验证
    const commitMessage = getCommitMessage();
    let commitValid = true;
    let commitResult = null;

    if (commitMessage) {
      commitResult = validateCommitMessage(commitMessage);
      commitValid = commitResult.valid;
    }

    // 输出结果
    let hasError = false;

    // 文件检查结果
    if (fileResult.invalidFiles.length > 0) {
      hasError = true;
      console.log(chalk.red('❌ 发现不合规文件:\n'));
      for (const file of fileResult.invalidFiles) {
        console.log(`   - ${file.path} (${file.message})`);
      }
      console.log('');
    } else {
      console.log(chalk.green('✅ 文件检查通过'));
    }

    // 提交信息检查结果
    if (commitResult && !commitValid) {
      hasError = true;
      console.log(chalk.red('\n❌ 提交信息格式错误:\n'));
      for (const error of commitResult.errors) {
        console.log(`   - ${error}`);
      }
      console.log('');
    } else if (commitResult && commitValid) {
      console.log(chalk.green('✅ 提交信息格式正确'));
    }

    if (hasError) {
      console.log(chalk.cyan('\n💡 提示:'));
      console.log('   请修复以上问题后重新提交');
      process.exit(1);
    }

    console.log(chalk.green('\n✅ 所有检查通过，提交成功！\n'));
    process.exit(0);

  } catch (error) {
    console.error(chalk.red('\n❌ 检查失败:'), error.message);
    process.exit(1);
  }
}

// 跳过检查标记
if (process.env.POWERBY_GIT_SKIP_HOOK === 'true') {
  console.log(chalk.gray('⏭️  跳过 pre-commit 检查'));
  process.exit(0);
}

runCheck();
