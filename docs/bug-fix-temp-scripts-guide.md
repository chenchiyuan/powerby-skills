# Bug-Fix临时脚本使用指南

## 概述

本文档详细说明如何在Bug修复过程中使用 `temp_scripts/` 目录管理临时代码、验证脚本和测试数据，确保项目目录整洁有序。

## 核心原则

### 1. 优先复用现有代码
在创建临时脚本前，优先考虑：
- 调用项目中现有的工具模块
- 使用已有的测试框架
- 复用现有的数据处理脚本

### 2. 分类管理
临时文件按用途分类存储：
- `analysis/` - 分析和诊断脚本
- `validation/` - 验证和测试脚本
- `mock/` - 模拟数据和场景
- `logs/` - 临时日志文件

### 3. 及时清理
修复完成后立即清理所有临时文件，确保工作目录整洁。

## 使用场景示例

### 场景1：认证模块Bug修复

#### 问题描述
用户登录后token验证失败，返回401错误。

#### 步骤1：创建分析脚本

```bash
# 创建临时目录
mkdir -p temp_scripts/analysis
mkdir -p temp_scripts/logs

# 创建代码分析脚本
cat > temp_scripts/analysis/bug-001-token-analyzer.py << 'EOF'
#!/usr/bin/env python3
"""
Bug-001 Token验证分析脚本
分析token生成和验证逻辑
"""
import json
import jwt
from datetime import datetime, timedelta

def analyze_token_logic():
    """分析token逻辑"""
    print("=== Bug-001 Token验证分析 ===")

    # 读取项目配置（调用现有代码）
    try:
        from src.config import JWT_SECRET, JWT_ALGORITHM
        print(f"✅ 成功导入配置: 算法={JWT_ALGORITHM}")
    except ImportError as e:
        print(f"❌ 配置导入失败: {e}")
        return

    # 分析token生成逻辑
    print("\n--- Token生成分析 ---")
    try:
        # 创建测试token
        payload = {
            'user_id': 123,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        print(f"✅ Token生成成功: {token[:20]}...")

        # 分析token验证逻辑
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f"✅ Token验证成功: 用户ID={decoded['user_id']}")

    except Exception as e:
        print(f"❌ Token验证失败: {e}")
        with open('temp_scripts/logs/bug-001-analysis.log', 'w') as f:
            f.write(f"Token验证错误: {e}\n")

if __name__ == "__main__":
    analyze_token_logic()
EOF

chmod +x temp_scripts/analysis/bug-001-token-analyzer.py
```

#### 步骤2：创建验证脚本

```bash
mkdir -p temp_scripts/validation

cat > temp_scripts/validation/bug-001-test-auth.py << 'EOF'
#!/usr/bin/env python3
"""
Bug-001 认证验证脚本
测试修复后的认证逻辑
"""
import sys
import os

# 添加项目根目录到路径（调用现有模块）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_authentication():
    """测试认证功能"""
    print("=== Bug-001 认证验证测试 ===")

    try:
        # 调用现有的认证模块
        from src.auth import verify_token, generate_token
        print("✅ 成功导入认证模块")

        # 测试token生成
        token = generate_token(user_id=123)
        print(f"✅ Token生成: {token[:20]}...")

        # 测试token验证
        result = verify_token(token)
        if result['valid']:
            print(f"✅ Token验证成功: 用户ID={result['user_id']}")
            return True
        else:
            print(f"❌ Token验证失败: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ 认证测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_authentication()
    sys.exit(0 if success else 1)
EOF

chmod +x temp_scripts/validation/bug-001-test-auth.py
```

#### 步骤3：执行分析和验证

```bash
# 运行分析脚本
echo "🔍 执行代码分析..."
python3 temp_scripts/analysis/bug-001-token-analyzer.py

# 运行验证脚本
echo "✅ 执行验证测试..."
python3 temp_scripts/validation/bug-001-test-auth.py
```

#### 步骤4：清理临时文件

```bash
echo "🧹 清理临时文件..."

# 删除所有bug-001相关的临时文件
find temp_scripts -name "*bug-001*" -type f -delete

# 清理空的子目录
find temp_scripts -type d -empty -delete

# 如果temp_scripts目录为空，则删除它
if [ -d "temp_scripts" ] && [ -z "$(ls -A temp_scripts)" ]; then
    rmdir temp_scripts
    echo "✅ temp_scripts目录已删除"
else
    echo "✅ 临时文件已清理，目录保留"
fi

# 验证清理结果
if [ ! -d "temp_scripts" ]; then
    echo "✅ 清理完成：工作目录整洁"
else
    echo "⚠️ 仍有临时文件残留"
    ls -la temp_scripts/
fi
```

### 场景2：数据库连接Bug修复

#### 问题描述
数据库连接池耗尽，导致查询失败。

#### 步骤1：创建数据库分析脚本

```bash
mkdir -p temp_scripts/analysis
mkdir -p temp_scripts/mock

cat > temp_scripts/analysis/bug-002-db-connection-analyzer.py << 'EOF'
#!/usr/bin/env python3
"""
Bug-002 数据库连接分析脚本
分析连接池配置和使用情况
"""
import psycopg2
from psycopg2 import pool as pg_pool
import time

def analyze_db_pool():
    """分析数据库连接池"""
    print("=== Bug-002 数据库连接池分析 ===")

    try:
        # 读取数据库配置（调用现有配置）
        from src.config import DB_CONFIG
        print(f"✅ 数据库配置: {DB_CONFIG}")

        # 创建连接池（使用现有代码）
        connection_pool = pg_pool.ThreadedConnectionPool(
            1, 20, **DB_CONFIG
        )
        print("✅ 连接池创建成功")

        # 分析连接池状态
        print(f"📊 连接池状态:")
        print(f"   空闲连接: {connection_pool._pool}")
        print(f"   占用连接: {connection_pool._used}")

        # 模拟高并发场景
        print("\n--- 高并发测试 ---")
        connections = []
        for i in range(25):
            try:
                conn = connection_pool.getconn()
                connections.append(conn)
                print(f"✅ 获取连接 {i+1}/25")
            except Exception as e:
                print(f"❌ 获取连接失败 {i+1}: {e}")
                break

        # 归还连接
        for conn in connections:
            connection_pool.putconn(conn)

        print("✅ 连接已归还")

    except Exception as e:
        print(f"❌ 数据库分析失败: {e}")

    finally:
        if 'connection_pool' in locals():
            connection_pool.closeall()
            print("✅ 连接池已关闭")
EOF

chmod +x temp_scripts/analysis/bug-002-db-connection-analyzer.py
```

#### 步骤2：创建模拟数据

```bash
cat > temp_scripts/mock/bug-002-test-data.json << 'EOF'
{
  "test_scenarios": [
    {
      "name": "normal_load",
      "concurrent_requests": 10,
      "expected_result": "success"
    },
    {
      "name": "high_load",
      "concurrent_requests": 50,
      "expected_result": "some_failures"
    },
    {
      "name": "overload",
      "concurrent_requests": 100,
      "expected_result": "connection_exhausted"
    }
  ]
}
EOF
```

#### 步骤3：清理临时文件

```bash
echo "🧹 清理Bug-002临时文件..."
find temp_scripts -name "*bug-002*" -type f -delete
find temp_scripts -type d -empty -delete
[ -d temp_scripts ] && [ -z "$(ls -A temp_scripts)" ] && rmdir temp_scripts
echo "✅ 清理完成"
```

## 最佳实践

### 1. 脚本编写规范

#### 头部注释
每个临时脚本必须包含：
```python
#!/usr/bin/env python3
"""
Bug-{ID} {脚本名称}
{简要描述}
作者: {姓名}
日期: {日期}
"""
```

#### 错误处理
```python
try:
    # 调用现有代码
    result = existing_function()
except Exception as e:
    print(f"❌ 错误: {e}")
    # 记录到日志
    with open(f'temp_scripts/logs/bug-{id}.log', 'a') as f:
        f.write(f"{datetime.now()}: {e}\n")
    raise
```

### 2. 文件命名规范

- 分析脚本: `bug-{id}-analyzer.{py|js|sh}`
- 验证脚本: `bug-{id}-test-{component}.{py|js|sh}`
- 模拟数据: `bug-{id}-{data|scenario}.{json|csv|yaml}`
- 日志文件: `bug-{id}-{analysis|debug}.log`

### 3. 日志记录

```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'temp_scripts/logs/bug-{id}.log'),
        logging.StreamHandler()
    ]
)

# 使用日志
logging.info("开始分析...")
logging.error(f"分析失败: {error}")
```

### 4. 清理验证

```bash
#!/bin/bash
# verify-cleanup.sh

echo "🔍 验证临时文件清理..."

BUG_ID=$1
if [ -z "$BUG_ID" ]; then
    echo "❌ 请提供Bug ID"
    exit 1
fi

# 检查是否还有残留文件
REMAINING=$(find . -name "*bug-${BUG_ID}*" 2>/dev/null)

if [ -z "$REMAINING" ]; then
    echo "✅ 清理验证通过：无残留文件"
    exit 0
else
    echo "❌ 清理验证失败：发现残留文件"
    echo "$REMAINING"
    exit 1
fi
```

## 安全注意事项

### 1. 永远不清理
- ❌ `.powerby/` 目录
- ❌ `src/` 目录
- ❌ `docs/` 目录
- ❌ `tests/` 目录
- ❌ `.git/` 目录

### 2. 清理范围
- ✅ `temp_scripts/` 目录及其子目录
- ✅ 与当前bug相关的所有临时文件

### 3. 备份策略
```bash
# 如需备份重要临时文件
tar -czf "backup_bug_${BUG_ID}_$(date +%Y%m%d).tar.gz" temp_scripts/

# 清理前确认
read -p "确认清理临时文件？(y/N): " confirm
[ "$confirm" = "y" ] || exit 1
```

## 常见问题

### Q: 如何处理跨平台的临时脚本？
A: 使用通用的shebang和库，避免使用平台特定的命令。

### Q: 临时脚本需要提交到版本控制吗？
A: 不需要。临时脚本仅用于bug修复过程，修复完成后应立即删除。

### Q: 如何处理大型的临时数据文件？
A: 使用压缩格式，或在清理前确认用户是否需要保留。

### Q: 临时脚本可以调用生产环境的API吗？
A: 不推荐。临时脚本应使用测试数据或模拟环境。

## 总结

通过遵循本指南，您可以：
- ✅ 保持项目目录整洁
- ✅ 高效管理临时文件
- ✅ 避免遗留垃圾文件
- ✅ 提升bug修复效率
- ✅ 确保修复过程可追溯

记住：**修复完成后立即清理临时文件！**
