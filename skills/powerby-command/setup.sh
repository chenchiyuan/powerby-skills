#!/bin/bash
# PowerBy CLI 安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查操作系统
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        print_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
    print_info "检测到操作系统: $OS"
}

# 检查Python
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "未找到 Python3，请先安装 Python 3.7 或更高版本"
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_info "Python 版本: $PYTHON_VERSION"
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_SCRIPT="$SCRIPT_DIR/powerby-cli.py"

# 检查CLI脚本是否存在
if [ ! -f "$CLI_SCRIPT" ]; then
    print_error "未找到 powerby-cli.py 脚本: $CLI_SCRIPT"
    exit 1
fi

# 打印欢迎信息
echo "=========================================="
echo "   PowerBy CLI 安装程序"
echo "=========================================="
echo ""

# 检查环境
print_info "检查运行环境..."
check_os
check_python
print_success "环境检查通过"
echo ""

# 安装位置
INSTALL_DIR="/usr/local/bin"
BIN_NAME="powerby"

# 检查权限
if [ "$EUID" -ne 0 ]; then
    print_warning "需要 sudo 权限来安装到 $INSTALL_DIR"
    print_info "请输入您的密码..."
    SUDO="sudo"
else
    SUDO=""
fi

# 创建启动脚本
print_info "创建启动脚本..."

cat > /tmp/powerby << EOF
#!/bin/bash
# PowerBy CLI 启动脚本

SCRIPT_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
CLI_SCRIPT="$CLI_SCRIPT"

exec python3 "\$CLI_SCRIPT" "\$@"
EOF

# 复制启动脚本
print_info "安装到 $INSTALL_DIR/$BIN_NAME..."
$SUDO cp /tmp/powerby "$INSTALL_DIR/$BIN_NAME"
$SUDO chmod +x "$INSTALL_DIR/$BIN_NAME"
rm /tmp/powerby

# 验证安装
print_info "验证安装..."
if command -v $BIN_NAME &> /dev/null; then
    print_success "PowerBy CLI 安装成功！"
else
    print_error "安装失败"
    exit 1
fi

# 显示帮助信息
echo ""
echo "=========================================="
print_success "PowerBy CLI 安装完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  powerby init [项目名称]   - 初始化PowerBy项目"
echo "  powerby update           - 更新PowerBy命令"
echo "  powerby status           - 检查项目状态"
echo "  powerby clean            - 清理PowerBy命令"
echo ""
echo "示例:"
echo "  powerby init my-project"
echo "  powerby status"
echo ""
echo "在Claude中使用:"
echo "  /powerby.init"
echo "  /powerby.initialize"
echo "  /powerby.define"
echo ""
