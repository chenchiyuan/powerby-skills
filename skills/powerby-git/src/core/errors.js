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
  },
  E009: {
    code: 'E009',
    message: 'PowerBy 元数据缺失',
    hint: '请先初始化 .powerby/iterations.json，再执行分支自动化流程'
  },
  E010: {
    code: 'E010',
    message: '迭代记录不存在',
    hint: '请确认迭代编号、名称与 docs/iterations 目录一致'
  },
  E011: {
    code: 'E011',
    message: '工作区不干净',
    hint: '请先提交、暂存或清理未提交变更后重试'
  },
  E012: {
    code: 'E012',
    message: '分支不符合迭代约束',
    hint: '请切换到期望的 feature 分支后继续'
  },
  E013: {
    code: 'E013',
    message: '分支状态非法',
    hint: '请检查分支状态是否满足当前生命周期动作要求'
  },
  E014: {
    code: 'E014',
    message: '分支不存在',
    hint: '请确认目标分支已经创建，或先同步本地 Git 状态'
  },
  E015: {
    code: 'E015',
    message: '源分支不存在',
    hint: '请确认源分支已经存在，例如 develop 分支'
  },
  E016: {
    code: 'E016',
    message: '迭代元数据写入失败',
    hint: '请检查 .powerby 目录权限与 JSON 文件格式'
  },
  E017: {
    code: 'E017',
    message: '合并预检测回滚失败',
    hint: '请先执行 git merge --abort 清理现场，再重新触发流程'
  },
  E018: {
    code: 'E018',
    message: '远程分支操作失败',
    hint: '请检查远程仓库配置、权限和网络状态后重试'
  },
  E019: {
    code: 'E019',
    message: '分支保护规则不满足',
    hint: '请先满足分支保护规则约束后再执行合并'
  },
  E020: {
    code: 'E020',
    message: '分支历史报告生成失败',
    hint: '请检查 docs/iterations 目录权限以及 Git 历史是否可读取'
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
