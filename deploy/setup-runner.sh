#!/bin/bash
set -e

# ============================================
# 服务器初始化脚本 — 在目标服务器上以 root 执行
# 用法: bash setup-runner.sh
# ============================================

echo "=== 1. 安装基础依赖 ==="
apt update
apt install -y python3 python3-pip python3-venv nodejs npm nginx git curl

echo "=== 2. 配置国内镜像加速 ==="
# npm 镜像
npm config set registry https://registry.npmmirror.com
# pip 镜像
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

echo "=== 3. 创建部署目录 ==="
mkdir -p /opt/ams
mkdir -p /opt/ams-runner

echo "=== 4. 安装 GitHub Actions Runner ==="
cd /opt/ams-runner

# 下载最新的 runner（Linux x64）
RUNNER_VERSION="2.322.0"
curl -o actions-runner-linux-x64.tar.gz -L \
  "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"

tar xzf actions-runner-linux-x64.tar.gz

echo ""
echo "=============================================="
echo "  下一步：在 GitHub 上注册 Runner"
echo "=============================================="
echo ""
echo "请访问以下页面，获取注册 Token："
echo "  https://github.com/xugegegong/ams-config-manager/settings/actions/runners/new"
echo ""
echo "选择操作系统: Linux  架构: x64"
echo "然后复制页面上 'Configure' 部分的 token，运行下面命令："
echo ""
echo "  cd /opt/ams-runner && sudo ./config.sh --url https://github.com/xugegegong/ams-config-manager --token 你的TOKEN"
echo ""
echo "注册完成后，运行："
echo "  sudo ./svc.sh install && sudo ./svc.sh start"
echo ""
echo "然后回到 GitHub 页面，确认 Runner 状态为 🟢 Idle"
echo "=============================================="
