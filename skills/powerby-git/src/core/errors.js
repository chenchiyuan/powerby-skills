/**
 * PowerBy Git 错误码体系
 * @constant {Object.<string, {code: string, message: string, hint: string}>}
 */
const ERRORS = {
  E001: {
    code: 'E001',
    message: '分支已存在',
    hint: '请使用新名称或切换到现有分支: git checkout {分支名}'
  },
  E002: {
    code: 'E002',
    message: '无效的分支名称',
    hint: '请使用小写字母和连字符，例如: user-authentication'
  },
  E003: {
    code: 'E003',
    message: '不在分支上',
    hint: '请先创建或切换到分支'
  },
  E004: {
    code: 'E004',
    message: '临时文件未清理',
    hint: '请删除临时文件后再提交: rm {文件列表}'
  },
  E005: {
    code: 'E005',
    message: '文档不完整',
    hint: '请检查 PowerBy 文档是否齐全'
  },
  E006: {
    code: 'E006',
    message: '合并冲突',
    hint: '请先解决冲突再合并'
  },
  E007: {
    code: 'E007',
    message: 'Git 操作失败',
    hint: '请检查 Git 仓库状态'
  },
  E008: {
    code: 'E008',
    message: '无效的参数',
    hint: '请检查命令参数是否正确'
  }
};

/**
 * 创建自定义错误
 * @param {string} errorCode - 错误码
 * @param {string} [details] - 详细错误信息
 * @returns {Error}
 */
function createError(errorCode, details = '') {
  const error = ERRORS[errorCode];
  if (!error) {
    return new Error(`未知错误: ${errorCode}`);
  }

  const message = details
    ? `${error.message}: ${details}`
    : error.message;

  const err = new Error(message);
  err.code = error.code;
  err.hint = error.hint;
  return err;
}

module.exports = {
  ERRORS,
  createError
};
