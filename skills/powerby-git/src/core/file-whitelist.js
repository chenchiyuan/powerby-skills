/**
 * 文件白名单验证器
 * 验证文件是否符合合规性要求
 */

const path = require('path');
const fs = require('fs');

/**
 * 临时文件模式
 */
const TEMPORARY_PATTERNS = [
  /\.(tmp|temp)$/,
  /\.log$/,
  /\.debug$/,
  /\.bak$/,
  /\.backup$/,
  /\.swp$/,
  /\.swo$/,
  /\.pyc$/,
  /\.pyo$/,
  /\.class$/,
  /\.o$/,
  /\.exe$/,
  /\.dll$/,
  /\.so$/,
  /\.dylib$/
];

/**
 * 临时目录模式
 */
const TEMPORARY_DIRS = [
  '__pycache__',
  'node_modules',
  '.dist',
  '.build',
  'dist',
  'build',
  'coverage',
  '.nyc_output',
  '.tox',
  '.venv',
  'venv'
];

/**
 * PowerBy 流程文档模式
 */
const POWERBY_DOC_PATTERNS = [
  /^docs\/constitution\.md$/,
  /^docs\/[\w-]+\/(prd|function-points|clarifications|technical-research|architecture|tasks|data-model)\.md$/,
  /^docs\/[\w-]+\/contracts\//,
  /^docs\/[\w-]+\/checklists\/(requirements|architecture|testing|security)\.md$/,
  /^docs\/[\w-]+\/implementation\/(implementation-report|decisions|work-log|blockers-[\w-]+)\.md$/,
  /^docs\/[\w-]+\/reviews\/(code-review-report|acceptance-test)\.md$/,
  /^docs\/[\w-]+\/(project-retrospective)\.md$/,
  /^docs\/[\w-]+\/releases\/.*\.md$/,
  /^docs\/[\w-]+\/operations\/.*\.md$/,
  /^docs\/bugs\/[\w-]+\/(diagnosis|resolution)\.md$/,
  /^docs\/proposals\//,
  /^docs\/references\//,
  /^docs\/.*workflow.*\.md$/i
];

/**
 * 项目配置文件模式
 */
const PROJECT_CONFIG_PATTERNS = [
  /^package\.json$/,
  /^pyproject\.toml$/,
  /^requirements\.txt$/,
  /^go\.mod$/,
  /^Cargo\.toml$/,
  /^pom\.xml$/,
  /^build\.gradle$/,
  /^Makefile$/,
  /^tsconfig\.json$/,
  /\.config\.(js|ts|mjs|cjs)$/,
  /^\.eslintrc/,
  /^\.prettierrc/,
  /\.eslintrc/,
  /\.prettierrc/
];

/**
 * 项目说明文件模式
 */
const PROJECT_DOC_PATTERNS = [
  /^README\.md$/i,
  /^CONTRIBUTING\.md$/i,
  /^LICENSE$/i,
  /^COPYING$/i,
  /\.md$/i
];

/**
 * 源代码目录模式
 */
const SOURCE_DIR_PATTERNS = [
  /^src\//,
  /^lib\//,
  /^tests?\//,
  /^__tests__\//,
  /^[a-z]+\/(src|lib)$/
];

/**
 * 检查文件是否为临时文件
 * @param {string} filePath - 文件路径
 * @returns {boolean}
 */
function isTemporaryFile(filePath) {
  const fileName = path.basename(filePath);
  const ext = path.extname(filePath);

  // 检查扩展名
  for (const pattern of TEMPORARY_PATTERNS) {
    if (pattern.test(fileName) || pattern.test(ext)) {
      return true;
    }
  }

  // 检查文件名
  if (fileName === '.DS_Store' || fileName === '.env') {
    return true;
  }

  return false;
}

/**
 * 检查路径是否为临时目录
 * @param {string} dirPath - 目录路径
 * @returns {boolean}
 */
function isTemporaryDir(dirPath) {
  const dirName = path.basename(dirPath);
  return TEMPORARY_DIRS.includes(dirName);
}

/**
 * 检查文件是否为 PowerBy 流程文档
 * @param {string} filePath - 文件路径
 * @returns {boolean}
 */
function isPowerByDoc(filePath) {
  for (const pattern of POWERBY_DOC_PATTERNS) {
    if (pattern.test(filePath)) {
      return true;
    }
  }
  return false;
}

/**
 * 检查文件是否为项目配置文件
 * @param {string} filePath - 文件路径
 * @returns {boolean}
 */
function isProjectConfig(filePath) {
  for (const pattern of PROJECT_CONFIG_PATTERNS) {
    if (pattern.test(filePath)) {
      return true;
    }
  }
  return false;
}

/**
 * 检查文件是否为项目说明文件
 * @param {string} filePath - 文件路径
 * @returns {boolean}
 */
function isProjectDoc(filePath) {
  const fileName = path.basename(filePath);
  // 只检查根目录的项目文档
  const dirName = path.dirname(filePath);

  if (dirName === '.' || dirName === '/') {
    for (const pattern of PROJECT_DOC_PATTERNS) {
      if (pattern.test(fileName)) {
        return true;
      }
    }
  }
  return false;
}

/**
 * 检查文件是否在源代码目录中
 * @param {string} filePath - 文件路径
 * @returns {boolean}
 */
function isSourceFile(filePath) {
  const dirName = path.dirname(filePath);

  for (const pattern of SOURCE_DIR_PATTERNS) {
    if (pattern.test(filePath) || pattern.test(dirName)) {
      return true;
    }
  }
  return false;
}

/**
 * 检查文件是否为测试用例
 * @param {string} filePath - 文件路径
 * @returns {boolean}
 */
function isTestFile(filePath) {
  const fileName = path.basename(filePath);
  const ext = path.extname(filePath);

  // 测试文件模式
  const testPatterns = [
    /\.test\.(js|ts|py|go|java)$/,
    /\.spec\.(js|ts|py|go|java)$/,
    /_test\.(go|java)$/,
    /-test\.(js|ts)$/,
    /Test\.(java|py)$/
  ];

  for (const pattern of testPatterns) {
    if (pattern.test(fileName)) {
      return true;
    }
  }

  // 测试目录
  const dirName = path.dirname(filePath);
  if (dirName.match(/tests?|__tests__|test|spec/)) {
    return true;
  }

  return false;
}

/**
 * 验证文件是否在白名单内
 * @param {string} filePath - 文件路径
 * @returns {{valid: boolean, category: string, message: string}}
 */
function validateFile(filePath) {
  // 标准化路径
  const normalizedPath = filePath.replace(/\\/g, '/');

  // 先检查是否为测试文件（优先级高于源代码）
  if (isTestFile(normalizedPath)) {
    return {
      valid: true,
      category: 'test',
      message: '测试用例文件'
    };
  }

  // 检查是否在白名单内
  if (isSourceFile(normalizedPath)) {
    return {
      valid: true,
      category: 'source',
      message: '源代码文件'
    };
  }

  if (isPowerByDoc(normalizedPath)) {
    return {
      valid: true,
      category: 'powerby-doc',
      message: 'PowerBy 流程文档'
    };
  }

  if (isProjectConfig(normalizedPath)) {
    return {
      valid: true,
      category: 'config',
      message: '项目配置文件'
    };
  }

  if (isProjectDoc(normalizedPath)) {
    return {
      valid: true,
      category: 'doc',
      message: '项目说明文件'
    };
  }

  // 检查是否为临时文件
  if (isTemporaryFile(normalizedPath)) {
    return {
      valid: false,
      category: 'temporary',
      message: '临时文件'
    };
  }

  // 检查临时目录中的文件
  const dirName = path.dirname(normalizedPath);
  for (const tempDir of TEMPORARY_DIRS) {
    if (dirName.includes(tempDir)) {
      return {
        valid: false,
        category: 'temporary',
        message: `临时目录中的文件 (${tempDir})`
      };
    }
  }

  // 其他文件默认不通过
  return {
    valid: false,
    category: 'unknown',
    message: '未分类文件'
  };
}

/**
 * 验证文件列表
 * @param {string[]} files - 文件路径数组
 * @returns {{validFiles: Array, invalidFiles: Array, summary: Object}}
 */
function validateFileList(files) {
  const validFiles = [];
  const invalidFiles = [];

  for (const file of files) {
    const result = validateFile(file);
    if (result.valid) {
      validFiles.push({
        path: file,
        ...result
      });
    } else {
      invalidFiles.push({
        path: file,
        ...result
      });
    }
  }

  const summary = {
    total: files.length,
    valid: validFiles.length,
    invalid: invalidFiles.length,
    byCategory: {}
  };

  // 按类别统计
  for (const file of validFiles) {
    summary.byCategory[file.category] = (summary.byCategory[file.category] || 0) + 1;
  }

  return {
    validFiles,
    invalidFiles,
    summary
  };
}

/**
 * 扫描目录获取所有文件
 * @param {string} dir - 目录路径
 * @param {string[]} [ignorePatterns] - 忽略模式
 * @returns {string[]}
 */
function scanDirectory(dir, ignorePatterns = []) {
  const files = [];

  function scan(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      // 检查是否在忽略列表中
      const shouldIgnore = ignorePatterns.some(pattern => {
        if (typeof pattern === 'string') {
          return fullPath.includes(pattern);
        }
        return pattern.test(fullPath);
      });

      if (shouldIgnore) continue;

      if (entry.isDirectory()) {
        scan(fullPath);
      } else if (entry.isFile()) {
        files.push(fullPath);
      }
    }
  }

  scan(dir);
  return files;
}

module.exports = {
  TEMPORARY_PATTERNS,
  TEMPORARY_DIRS,
  POWERBY_DOC_PATTERNS,
  PROJECT_CONFIG_PATTERNS,
  SOURCE_DIR_PATTERNS,
  isTemporaryFile,
  isTemporaryDir,
  isPowerByDoc,
  isProjectConfig,
  isProjectDoc,
  isSourceFile,
  isTestFile,
  validateFile,
  validateFileList,
  scanDirectory
};
