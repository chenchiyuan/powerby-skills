#!/usr/bin/env node

/**
 * Pre-merge Hook
 * 在 git merge 时自动检查
 */

const chalk = require('chalk');
const path = require('path');
const { scanDirectory } = require('../core/file-whitelist');
const { validateFileList } = require('../core/file-whitelist');

/**
 * 执行合并前检查
 */
async function runMergeCheck() {
  console.log(chalk.cyan('\n🔍 powerby-git: 合并前检查\n'));

  try {
    const cwd = process.cwd();

    // 全量扫描工作区
    const ignorePatterns = [
      /node_modules/,
      /\.git/,
      /\.dist/,
      /dist$/,
      /build$/
    ];

    const files = scanDirectory(cwd, ignorePatterns);
    const relativeFiles = files.map(f => path.relative(cwd, f));

    // 检查文件合规性
    const result = validateFileList(relativeFiles);

    let hasError = false;

    if (result.invalidFiles.length > 0) {
      hasError = true;
      console.log(chalk.red('❌ 发现不合规文件:\n'));

      // 按类别分组显示
      const byCategory = {};
      for (const file of result.invalidFiles) {
        if (!byCategory[file.category]) {
          byCategory[file.category] = [];
        }
        byCategory[file.category].push(file);
      }

      for (const [category, files] of Object.entries(byCategory)) {
        console.log(`\n   [${category}]:`);
        for (const file of files.slice(0, 5)) {
          console.log(`   - ${file.path}`);
        }
        if (files.length > 5) {
          console.log(`   ... 还有 ${files.length - 5} 个`);
        }
      }

      console.log('');
    } else {
      console.log(chalk.green('✅ 文件检查通过'));
    }

    // 显示统计信息
    console.log(chalk.cyan('\n📊 文件统计:'));
    console.log(`   总文件: ${result.summary.total}`);
    console.log(`   合法文件: ${chalk.green(result.summary.valid)}`);
    console.log(`   问题文件: ${chalk.red(result.summary.invalid)}`);

    if (hasError) {
      console.log(chalk.cyan('\n💡 提示:'));
      console.log('   请清理问题文件后再合并');
      console.log('   运行 powerby-git check --type=merge 查看详细信息');
      process.exit(1);
    }

    console.log(chalk.green('\n✅ 所有检查通过，可以合并！\n'));
    process.exit(0);

  } catch (error) {
    console.error(chalk.red('\n❌ 检查失败:'), error.message);
    process.exit(1);
  }
}

// 跳过检查标记
if (process.env.POWERBY_GIT_SKIP_HOOK === 'true') {
  console.log(chalk.gray('⏭️  跳过 pre-merge 检查'));
  process.exit(0);
}

runMergeCheck();
