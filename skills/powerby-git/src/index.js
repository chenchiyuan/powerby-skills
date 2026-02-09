#!/usr/bin/env node

/**
 * PowerBy Git - Git 分支管理 CLI
 */

const { Command } = require('commander');
const chalk = require('chalk');
const path = require('path');
const fs = require('fs');

// 版本号
const VERSION = '1.0.0';

// 导入命令
const { configureStartCommand } = require('./commands/start');
const { configureListCommand } = require('./commands/list');
const { configureCheckCommand } = require('./commands/check');
const { configureCleanupCommand } = require('./commands/cleanup');
const { configureStatusCommand } = require('./commands/status');

/**
 * 创建 CLI 程序
 * @returns {Command}
 */
function createProgram() {
  const program = new Command();

  program
    .name('powerby-git')
    .description('PowerBy Git 分支管理工具 - 确保每次迭代都在规范分支上进行')
    .version(VERSION, '-v, --version');

  // 添加命令
  configureStartCommand(program);
  configureListCommand(program);
  configureCheckCommand(program);
  configureCleanupCommand(program);
  configureStatusCommand(program);

  // 默认命令
  program.action(() => {
    program.help();
  });

  return program;
}

/**
 * 检查是否是 Git 仓库
 * @returns {boolean}
 */
function checkGitRepository() {
  const gitDir = path.join(process.cwd(), '.git');
  return fs.existsSync(gitDir);
}

/**
 * 显示欢迎信息
 */
function showWelcome() {
  console.log(chalk.cyan('\nPowerBy Git - Branch Manager'));
  console.log(chalk.gray('-'.repeat(40)));
  console.log('');
  console.log('Ensure every iteration follows branch standards');
  console.log('');
}

/**
 * 主入口
 */
async function main() {
  showWelcome();

  // 检查是否是 Git 仓库
  if (!checkGitRepository()) {
    console.error(chalk.red('❌ 当前目录不是 Git 仓库'));
    console.log(chalk.gray('💡 请在 Git 仓库目录下运行此命令'));
    process.exit(1);
  }

  // 创建并解析 CLI
  const program = createProgram();
  program.parse(process.argv);
}

// 导出供测试使用
module.exports = {
  createProgram,
  main,
  VERSION
};

// 如果直接运行
if (require.main === module) {
  main().catch(error => {
    console.error(chalk.red('\n❌ 发生错误:'), error.message);
    process.exit(1);
  });
}
