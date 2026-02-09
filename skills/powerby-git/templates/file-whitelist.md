# 文件白名单规范

## 合法文件类型

### 1. 业务代码和测试用例

```
src/                           # 源代码
lib/                           # 库代码
tests/                         # 测试目录
__tests__/                     # 测试目录（深层次）
*.test.{js,ts,py}              # 测试文件
*.spec.{js,ts,py}              # 测试规格文件
```

### 2. PowerBy 流程文档

```
docs/
├── iterations/{id}/
│   ├── prd.md                 # 产品需求文档
│   ├── task.md                # 任务分解文档
│   ├── architecture.md        # 架构设计文档
│   ├── technical-research.md  # 技术调研报告
│   ├── clarifications.md      # 需求澄清记录
│   └── function-points.md     # 功能点清单
├── bugs/{id}/
│   ├── diagnosis.md           # 诊断报告
│   └── resolution.md          # 解决方案
├── proposals/                 # 方案提案
└── references/                # 参考资料
```

### 3. 项目配置文件

```
package.json                  # Node.js 依赖
pyproject.toml                # Python 项目
go.mod                        # Go 模块
pom.xml / build.gradle        # Java 项目
requirements.txt              # Python 依赖
Cargo.toml                    # Rust 项目
```

### 4. 项目说明文件

```
README.md                     # 项目说明
CONTRIBUTING.md               # 贡献指南
LICENSE                       # 许可证
.gitignore                    # Git 忽略规则
```

## 临时文件（会被标记删除）

```
*.tmp / *.temp                # 临时文件
*.log                         # 日志文件
*.debug                       # 调试文件
*.bak / *.backup              # 备份文件
*.swp / *.swo                 # 编辑器交换文件
.DS_Store                     # macOS 系统文件
__pycache__/                  # Python 缓存
node_modules/                 # 依赖目录（通常在 .gitignore）
.dist/ / .build/              # 构建输出
coverage/                     # 测试覆盖率报告
.env                          # 环境变量（应加入 .gitignore）
```

## 检查流程

1. 提交时：检查变更文件是否在白名单
2. 合并前：全量扫描工作区
3. 清理时：识别临时文件并提示删除
