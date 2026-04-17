#!/usr/bin/env node

const { program } = require('commander');
const fs = require('fs');
const path = require('path');
const yaml = require('yaml');
const chalk = require('chalk');

const POWERBY_HOME = path.join(process.env.HOME, '.powerby');
const EXP_DIR = path.join(POWERBY_HOME, 'experiences');
const TEMPLATE_PATH = path.join(EXP_DIR, '.template.md');

// 确保目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// 解析 Markdown Front Matter
function parseFrontMatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    return { frontMatter: {}, body: content };
  }
  const frontMatter = yaml.parse(match[1]);
  const body = match[2];
  return { frontMatter, body };
}

// 生成 Markdown 文件
function generateMarkdown(frontMatter, body) {
  return `---\n${yaml.stringify(frontMatter)}---\n${body}`;
}

// 获取下一个经验 ID
function getNextExpId() {
  ensureDir(EXP_DIR);
  const files = fs.readdirSync(EXP_DIR)
    .filter(f => f.startsWith('exp-') && f.endsWith('.md') && f !== '.template.md');

  if (files.length === 0) return 'exp-001';

  const ids = files.map(f => {
    const match = f.match(/^exp-(\d+)/);
    return match ? parseInt(match[1]) : 0;
  });

  const maxId = Math.max(...ids);
  return `exp-${String(maxId + 1).padStart(3, '0')}`;
}

// 列出所有经验
function listExperiences(options) {
  ensureDir(EXP_DIR);
  const files = fs.readdirSync(EXP_DIR)
    .filter(f => f.startsWith('exp-') && f.endsWith('.md') && f !== '.template.md')
    .sort();

  if (files.length === 0) {
    console.log(chalk.yellow('暂无经验记录'));
    return;
  }

  console.log(chalk.bold.cyan(`\n共 ${files.length} 条经验记录：\n`));

  files.forEach(file => {
    const filePath = path.join(EXP_DIR, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    const { frontMatter } = parseFrontMatter(content);

    // 过滤状态
    if (options.status && frontMatter.status !== options.status) {
      return;
    }

    const statusColor = frontMatter.status === 'active' ? 'green' :
                       frontMatter.status === 'deprecated' ? 'gray' : 'yellow';

    console.log(chalk.bold(`[${frontMatter.id}]`) + ` ${frontMatter.title}`);
    console.log(`  类型: ${chalk.blue(frontMatter.type)} | 阶段: ${chalk.blue(frontMatter.stage)} | 级别: ${chalk.red(frontMatter.level)}`);
    console.log(`  状态: ${chalk[statusColor](frontMatter.status)} | 创建: ${frontMatter.created}`);
    if (frontMatter.projects && frontMatter.projects.length > 0) {
      console.log(`  项目: ${frontMatter.projects.join(', ')}`);
    }
    console.log('');
  });
}

// 显示经验详情
function showExperience(expId) {
  ensureDir(EXP_DIR);
  const files = fs.readdirSync(EXP_DIR)
    .filter(f => f.startsWith(`${expId}-`) && f.endsWith('.md'));

  if (files.length === 0) {
    console.log(chalk.red(`错误: 未找到经验 ${expId}`));
    return;
  }

  const filePath = path.join(EXP_DIR, files[0]);
  const content = fs.readFileSync(filePath, 'utf-8');
  console.log(content);
}

// 添加经验（交互式）
function addExperience() {
  const templatePath = TEMPLATE_PATH;
  if (!fs.existsSync(templatePath)) {
    console.log(chalk.red('错误: 模板文件不存在'));
    return;
  }

  const nextId = getNextExpId();
  console.log(chalk.cyan(`\n创建新经验: ${nextId}\n`));
  console.log(chalk.yellow('请按照模板填写经验内容，然后保存文件。'));
  console.log(chalk.yellow(`模板路径: ${templatePath}`));
  console.log(chalk.yellow(`\n提示: 你可以复制模板内容，填写后使用 'powerby-exp save' 命令保存。\n`));
}

program
  .name('powerby-exp')
  .description('PowerBy 全局经验库管理工具')
  .version('1.0.0');

program
  .command('list')
  .description('列出所有经验记录')
  .option('-s, --status <status>', '按状态过滤 (active|deprecated|merged)')
  .action(listExperiences);

program
  .command('show <exp-id>')
  .description('显示经验详情')
  .action(showExperience);

program
  .command('add')
  .description('添加新经验（交互式）')
  .action(addExperience);

program.parse();
