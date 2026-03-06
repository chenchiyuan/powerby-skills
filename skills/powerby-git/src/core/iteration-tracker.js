/**
 * 迭代元数据追踪器
 */

const fs = require('fs');
const path = require('path');
const { createError } = require('./errors');
const { buildIterationFolderName, validateIterationId } = require('./iteration-branch');

const DEFAULT_ITERATIONS_DATA = {
  iterations: [],
  current_iteration: null,
  completed_iterations: 0,
  total_iterations: 0
};

/**
 * 获取迭代元数据文件路径。
 * @param {string} cwd - 项目根目录。
 * @returns {string} `.powerby/iterations.json` 绝对路径。
 */
function getIterationsFilePath(cwd = process.cwd()) {
  return path.join(cwd, '.powerby', 'iterations.json');
}

/**
 * 读取迭代元数据。
 * @param {string} cwd - 项目根目录。
 * @throws {Error} 当文件缺失或 JSON 非法时抛出异常。
 * @returns {Object} 迭代元数据对象。
 */
function readIterationsData(cwd = process.cwd()) {
  const iterationsFilePath = getIterationsFilePath(cwd);

  if (!fs.existsSync(iterationsFilePath)) {
    throw createError('E009', `缺少迭代元数据文件: expected="${iterationsFilePath}"`);
  }

  try {
    const rawContent = fs.readFileSync(iterationsFilePath, 'utf-8');
    const parsed = JSON.parse(rawContent);

    if (!Array.isArray(parsed.iterations)) {
      throw createError('E009', 'iterations.json 必须包含 iterations 数组');
    }

    return parsed;
  } catch (error) {
    if (error.code === 'E009') {
      throw error;
    }

    throw createError('E009', `解析 iterations.json 失败: ${error.message}`);
  }
}

/**
 * 持久化迭代元数据。
 * @param {Object} data - 待写入的元数据。
 * @param {string} cwd - 项目根目录。
 * @throws {Error} 当结构非法或写入失败时抛出异常。
 */
function writeIterationsData(data, cwd = process.cwd()) {
  if (!data || !Array.isArray(data.iterations)) {
    throw createError('E016', 'iterations 数据结构非法，缺少 iterations 数组');
  }

  const normalizedData = {
    ...DEFAULT_ITERATIONS_DATA,
    ...data,
    total_iterations: data.iterations.length,
    completed_iterations: data.completed_iterations ?? DEFAULT_ITERATIONS_DATA.completed_iterations
  };

  const iterationsFilePath = getIterationsFilePath(cwd);
  const powerbyDir = path.dirname(iterationsFilePath);

  try {
    fs.mkdirSync(powerbyDir, { recursive: true });
    fs.writeFileSync(iterationsFilePath, `${JSON.stringify(normalizedData, null, 2)}\n`, 'utf-8');
  } catch (error) {
    throw createError('E016', `写入 iterations.json 失败: ${error.message}`);
  }
}

/**
 * 从标准迭代目录构建已存在的文档索引。
 * @param {string} iterationId - 迭代编号。
 * @param {string} iterationName - 迭代名称。
 * @param {string} cwd - 项目根目录。
 * @returns {Object} 文档路径映射。
 */
function buildIterationDocuments(iterationId, iterationName, cwd = process.cwd()) {
  const folderName = buildIterationFolderName(iterationId, iterationName);
  const iterationDirectory = path.join(cwd, 'docs', 'iterations', folderName);

  if (!fs.existsSync(iterationDirectory)) {
    return {};
  }

  const candidates = {
    proposal: 'proposal.md',
    spec: 'spec.md',
    function_points: 'function-points.md',
    product_map: 'product-map.md',
    architecture: 'architecture.md',
    tasks: 'tasks.md',
    implementation_report: path.join('implementation', 'implementation-report.md')
  };

  return Object.entries(candidates).reduce((documents, [key, relativePath]) => {
    const absolutePath = path.join(iterationDirectory, relativePath);

    if (fs.existsSync(absolutePath)) {
      documents[key] = path.join('docs', 'iterations', folderName, relativePath).replace(/\\/g, '/');
    }

    return documents;
  }, {});
}

/**
 * 创建新的迭代记录骨架。
 * @param {Object} options - 创建选项。
 * @param {string} options.iterationId - 迭代编号。
 * @param {string} options.iterationName - 迭代名称。
 * @param {string} options.phase - 当前阶段。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Object} 新的迭代记录。
 */
function createIterationRecord({ iterationId, iterationName, phase, cwd }) {
  const now = new Date().toISOString();
  const folderName = buildIterationFolderName(iterationId, iterationName);

  return {
    id: iterationId,
    name: folderName.slice(4),
    full_name: folderName,
    status: 'in_progress',
    phase,
    created_at: now,
    branch: null,
    documents: buildIterationDocuments(iterationId, iterationName, cwd)
  };
}

/**
 * 获取指定迭代记录。
 * @param {string} iterationId - 迭代编号。
 * @param {string} cwd - 项目根目录。
 * @throws {Error} 当迭代不存在时抛出异常。
 * @returns {Object} 迭代记录。
 */
function getIterationRecord(iterationId, cwd = process.cwd()) {
  validateIterationId(iterationId);
  const data = readIterationsData(cwd);
  const iteration = data.iterations.find((item) => item.id === iterationId);

  if (!iteration) {
    throw createError('E010', `未找到迭代记录: iterationId="${iterationId}"`);
  }

  return iteration;
}

/**
 * 确保迭代记录存在，不存在时自动创建基础记录。
 * @param {Object} options - 选项。
 * @param {string} options.iterationId - 迭代编号。
 * @param {string} options.iterationName - 迭代名称。
 * @param {string} options.phase - 生命周期阶段。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Object} 已存在或新建的迭代记录。
 */
function ensureIterationRecord({ iterationId, iterationName, phase = 'P1', cwd = process.cwd() }) {
  validateIterationId(iterationId);
  const data = readIterationsData(cwd);
  let iteration = data.iterations.find((item) => item.id === iterationId);

  if (!iteration) {
    iteration = createIterationRecord({ iterationId, iterationName, phase, cwd });
    data.iterations.push(iteration);
  } else if (iterationName && iteration.name && iteration.name !== buildIterationFolderName(iterationId, iterationName).slice(4)) {
    throw createError(
      'E010',
      `迭代名称不一致: expected="${iteration.name}" actual="${iterationName}"`
    );
  }

  if (iterationName) {
    const folderName = buildIterationFolderName(iterationId, iterationName);
    iteration.name = folderName.slice(4);
    iteration.full_name = folderName;
    iteration.documents = {
      ...iteration.documents,
      ...buildIterationDocuments(iterationId, iterationName, cwd)
    };
  }

  iteration.phase = phase;
  data.current_iteration = iterationId;
  writeIterationsData(data, cwd);

  return getIterationRecord(iterationId, cwd);
}

/**
 * 更新迭代记录中的分支信息。
 * @param {Object} options - 选项。
 * @param {string} options.iterationId - 迭代编号。
 * @param {string} options.iterationName - 迭代名称。
 * @param {Object} options.branchInfo - 分支信息补丁。
 * @param {string} options.phase - 生命周期阶段。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Object} 更新后的迭代记录。
 */
function updateIterationBranchInfo({
  iterationId,
  iterationName,
  branchInfo,
  phase,
  cwd = process.cwd()
}) {
  if (!branchInfo || typeof branchInfo !== 'object') {
    throw createError('E008', 'branchInfo 必须是对象');
  }

  const iteration = ensureIterationRecord({ iterationId, iterationName, phase, cwd });
  const storedData = readIterationsData(cwd);
  const storedIteration = storedData.iterations.find((item) => item.id === iteration.id);

  storedIteration.branch_info = {
    ...(storedIteration.branch_info || {}),
    ...branchInfo
  };

  if (storedIteration.branch_info.branch_name) {
    storedIteration.branch = storedIteration.branch_info.branch_name;
  }

  if (iterationName) {
    storedIteration.documents = {
      ...storedIteration.documents,
      ...buildIterationDocuments(iterationId, iterationName, cwd)
    };
  }

  storedIteration.phase = phase || storedIteration.phase;
  storedData.current_iteration = iterationId;
  writeIterationsData(storedData, cwd);

  return getIterationRecord(iterationId, cwd);
}

/**
 * 更新迭代记录中的文档索引。
 * @param {Object} options - 选项。
 * @param {string} options.iterationId - 迭代编号。
 * @param {Object} options.documents - 文档路径补丁。
 * @param {string} options.cwd - 项目根目录。
 * @returns {Object} 更新后的迭代记录。
 */
function updateIterationDocuments({ iterationId, documents, cwd = process.cwd() }) {
  if (!documents || typeof documents !== 'object') {
    throw createError('E008', 'documents 必须是对象');
  }

  const data = readIterationsData(cwd);
  const iteration = data.iterations.find((item) => item.id === iterationId);

  if (!iteration) {
    throw createError('E010', `未找到迭代记录: iterationId="${iterationId}"`);
  }

  iteration.documents = {
    ...(iteration.documents || {}),
    ...documents
  };

  writeIterationsData(data, cwd);
  return getIterationRecord(iterationId, cwd);
}

module.exports = {
  getIterationsFilePath,
  readIterationsData,
  writeIterationsData,
  buildIterationDocuments,
  getIterationRecord,
  ensureIterationRecord,
  updateIterationBranchInfo,
  updateIterationDocuments
};
