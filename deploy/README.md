# 部署指南

## 服务器环境要求

- Ubuntu 20.04+ / CentOS 7+
- Python 3.10+
- Node.js 20+
- Nginx
- MySQL 8.0+
- Systemd

## 一键部署步骤

### 1. 服务器初始化

```bash
# 安装依赖
sudo apt update
sudo apt install -y python3 python3-pip nginx mysql-server

# 创建目录
sudo mkdir -p /opt/ams
sudo chown -R www-data:www-data /opt/ams
```

### 2. 配置数据库

```sql
CREATE DATABASE ams_config CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER 'ams_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ams_config.* TO 'ams_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 配置后端服务

```bash
sudo cp deploy/ams-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ams-backend
sudo systemctl start ams-backend
```

### 4. 配置 Nginx

```bash
sudo cp deploy/nginx-ams.conf /etc/nginx/sites-available/ams
sudo ln -s /etc/nginx/sites-available/ams /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 修改后端数据库配置

编辑 `backend/app/core/config.py`，将 `DATABASE_URL` 改为 MySQL 地址：

```python
DATABASE_URL = "mysql+pymysql://ams_user:your_password@localhost:3306/ams_config"
```

### 6. 初始化管理员

```bash
curl -X POST http://localhost:8000/api/auth/init-admin
```

## CI/CD 自动部署

已在 `.github/workflows/deploy.yml` 中配置好 GitHub Actions。

需要在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加以下 Secrets：

| Secret 名称 | 说明 |
|---|---|
| `DEPLOY_HOST` | 服务器 IP 或域名 |
| `DEPLOY_USER` | SSH 用户名 |
| `DEPLOY_SSH_KEY` | SSH 私钥 |
| `DEPLOY_PATH` | 部署路径，如 `/opt/ams` |
| `DEPLOY_PORT` | SSH 端口，默认 22（可选） |
