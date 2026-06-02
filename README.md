# AMS 配置管理系统

船舶机舱 AMS（Alarm Monitoring System）配置管理工具，替代原有 HldAssistant 桌面程序的配置功能。

## 功能概览

| 功能 | 说明 |
|---|---|
| 📡 数据库连接 | MySQL 连接配置与测试 |
| ⚙️ 机舱设备配置 | Modbus 通讯参数 + 寄存器 + 工况点管理 |
| 📥 Excel 智能导入 | 支持不同 AMS 厂商格式，列映射可配置 |
| 🔄 版本比对 | 自动发现增/删/改的工况点，逐条审批 |
| 📄 配置生成 | 生成与原系统兼容的 JSON + TXT 配置文件 |
| 🗄️ 配置入库 (cfg2DB) | 将配置写入目标数据库 |

## 技术栈

- **前端**: Vue 3 + Element Plus（深色主题）
- **后端**: Python FastAPI
- **数据库**: SQLite（开发）/ MySQL（生产）
- **部署**: Systemd + Nginx + GitHub Actions

## 快速开始

详见 [部署指南](deploy/README.md) 和 [设计文档](docs/设计文档.md)
