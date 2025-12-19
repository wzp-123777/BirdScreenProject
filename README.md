# 🐦 机场鸟情监测与预警系统

基于Django开发的航空鸟情监测系统，提供鸟类活动监测、风险评估和可视化展示功能。

## 🚀 快速开始

### 环境要求
- Python 3.12+
- Django 6.0
- SQLite

### 启动步骤

1. **激活虚拟环境**
   ```bash
   venv\Scripts\activate
   ```

2. **运行数据库迁移**
   ```bash
   python manage.py migrate
   ```

3. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

4. **访问系统**
   - 主界面: http://127.0.0.1:8000/
   - 管理后台: http://127.0.0.1:8000/admin/

### 初始化数据（可选）

```bash
# 初始化鸟类种类
python init_data.py

# 生成示例数据
python update_coords.py
```

## 🎯 核心功能

- 🏠 **鸟情态势仪表盘** - 统计概览和数据可视化
- 📋 **记录管理** - 鸟情记录的增删改查
- 🗺️ **ArcGIS地图视图** - 鸟情分布可视化
- 📤 **数据导入导出** - 支持XLS/CSV批量导入
- 🔧 **管理后台** - 系统管理和数据维护

## 🛠️ 技术栈

- **后端**: Django 6.0
- **数据库**: SQLite
- **前端**: Bootstrap 5, Chart.js
- **地图**: ArcGIS API for JavaScript
- **部署**: WSGI/ASGI

## 📁 项目结构

```
BirdScreenProject/
├── bird_system/          # Django主项目
├── monitor/             # 鸟情监测应用
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图逻辑
│   ├── templates/       # HTML模板
│   └── static/          # 静态资源
├── venv/               # Python虚拟环境
├── manage.py           # Django管理脚本
└── db.sqlite          # 数据库文件
```

## 📞 使用说明

1. 访问主页查看鸟情概况
2. 通过管理后台添加鸟类种类
3. 录入鸟情记录并自动风险评估
4. 在地图上查看鸟情分布
5. 导出数据进行分析

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目仅供学习和研究使用。
