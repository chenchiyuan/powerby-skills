/**
 * 文件白名单验证器测试
 */

const {
  isTemporaryFile,
  isTemporaryDir,
  isPowerByDoc,
  isProjectConfig,
  isSourceFile,
  isTestFile,
  validateFile,
  validateFileList
} = require('../../src/core/file-whitelist');

describe('File Whitelist Validator', () => {
  describe('isTemporaryFile', () => {
    test('应该识别临时文件扩展名', () => {
      expect(isTemporaryFile('debug.tmp')).toBe(true);
      expect(isTemporaryFile('test.temp')).toBe(true);
      expect(isTemporaryFile('debug.log')).toBe(true);
    });

    test('应该识别临时文件名', () => {
      expect(isTemporaryFile('.DS_Store')).toBe(true);
      expect(isTemporaryFile('.env')).toBe(true);
      expect(isTemporaryFile('data.bak')).toBe(true);
    });

    test('应该拒绝普通文件', () => {
      expect(isTemporaryFile('src/index.js')).toBe(false);
      expect(isTemporaryFile('README.md')).toBe(false);
    });
  });

  describe('isTemporaryDir', () => {
    test('应该识别临时目录', () => {
      expect(isTemporaryDir('node_modules')).toBe(true);
      expect(isTemporaryDir('__pycache__')).toBe(true);
      expect(isTemporaryDir('.dist')).toBe(true);
    });

    test('应该拒绝普通目录', () => {
      expect(isTemporaryDir('src')).toBe(false);
      expect(isTemporaryDir('docs')).toBe(false);
    });
  });

  describe('isPowerByDoc', () => {
    test('应该识别 PowerBy 项目文档', () => {
      expect(isPowerByDoc('docs/demo-project/prd.md')).toBe(true);
      expect(isPowerByDoc('docs/demo-project/tasks.md')).toBe(true);
      expect(isPowerByDoc('docs/demo-project/architecture.md')).toBe(true);
    });

    test('应该识别 PowerBy Bug 文档', () => {
      expect(isPowerByDoc('docs/bugs/001-login-bug/diagnosis.md')).toBe(true);
      expect(isPowerByDoc('docs/bugs/001-login-bug/resolution.md')).toBe(true);
    });

    test('应该识别方案提案目录', () => {
      expect(isPowerByDoc('docs/proposals/new-feature.md')).toBe(true);
    });

    test('应该拒绝普通文档', () => {
      expect(isPowerByDoc('docs/readme.md')).toBe(false);
    });
  });

  describe('isProjectConfig', () => {
    test('应该识别项目配置文件', () => {
      expect(isProjectConfig('package.json')).toBe(true);
      expect(isProjectConfig('pyproject.toml')).toBe(true);
      expect(isProjectConfig('go.mod')).toBe(true);
      expect(isProjectConfig('tsconfig.json')).toBe(true);
    });
  });

  describe('isSourceFile', () => {
    test('应该识别源代码文件', () => {
      expect(isSourceFile('src/index.js')).toBe(true);
      expect(isSourceFile('lib/utils.ts')).toBe(true);
      expect(isSourceFile('tests/example.test.js')).toBe(true);
    });
  });

  describe('isTestFile', () => {
    test('应该识别测试文件', () => {
      expect(isTestFile('src/index.test.js')).toBe(true);
      expect(isTestFile('src/index.spec.ts')).toBe(true);
      expect(isTestFile('tests/example_test.go')).toBe(true);
    });
  });

  describe('validateFile', () => {
    test('应该验证源代码文件为合法', () => {
      const result = validateFile('src/index.js');
      expect(result.valid).toBe(true);
      expect(result.category).toBe('source');
    });

    test('应该验证测试文件为合法', () => {
      const result = validateFile('tests/example.test.js');
      expect(result.valid).toBe(true);
      expect(result.category).toBe('test');
    });

    test('应该验证 PowerBy 文档为合法', () => {
      const result = validateFile('docs/demo-project/prd.md');
      expect(result.valid).toBe(true);
      expect(result.category).toBe('powerby-doc');
    });

    test('应该验证临时文件为不合法', () => {
      const result = validateFile('debug.log');
      expect(result.valid).toBe(false);
      expect(result.category).toBe('temporary');
    });
  });

  describe('validateFileList', () => {
    test('应该批量验证文件', () => {
      const files = [
        'src/index.js',
        'tests/example.test.js',
        'debug.log',
        'docs/demo-project/prd.md'
      ];

      const result = validateFileList(files);

      expect(result.summary.total).toBe(4);
      expect(result.summary.valid).toBe(3);
      expect(result.summary.invalid).toBe(1);
      expect(result.invalidFiles.length).toBe(1);
      expect(result.invalidFiles[0].path).toBe('debug.log');
    });
  });
});
