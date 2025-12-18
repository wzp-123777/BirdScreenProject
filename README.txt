# 🐦 机场鸟情分析与预警系统 (Bird Monitoring System)
# =================================================

## 📋 项目简介

这是一个基于Django开发的航空鸟情监测系统，用于监测和记录机场周边鸟类活动，对航空安全可能造成的威胁进行风险评估和预警。该系统提供直观的Web界面，支持鸟情数据的录入、查询、统计分析和可视化展示。

## 🚀 快速开始

### 环境要求
- Python 3.12+
- Django 6.0
- SQLite (内置，无需额外配置)

### ArcGIS地图服务要求

#### 选项1: ArcGIS Online (推荐 - 默认)
- 互联网连接
- 可选: ArcGIS开发者账户 (获得更高使用配额)
- 无需本地ArcGIS软件安装

#### 选项2: ArcGIS Enterprise (企业级 - 本地部署)
- 本地ArcGIS Enterprise服务器
- 支持内网环境，无需互联网
- 企业级安全性和定制化
- 路径示例: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\ArcGIS`

#### 选项3: ArcGIS Desktop + Server (专业级)
- 本地ArcGIS Desktop安装
- ArcGIS Server用于发布地图服务
- 完全离线的GIS解决方案

### 一键部署（推荐）

1. **双击运行批处理脚本**：
   ```
   run_server.bat
   ```
   这个脚本会自动：
   - 激活虚拟环境
   - 启动Django开发服务器
   - 在浏览器中打开系统主页

2. **访问系统**：
   - 主界面：http://127.0.0.1:8000/
   - 管理后台：http://127.0.0.1:8000/admin/

### 手动部署步骤

#### 1. 激活虚拟环境
```bash
venv\Scripts\activate
```

#### 2. 运行数据库迁移
```bash
python manage.py migrate
```

#### 3. 初始化基础数据（可选）
```bash
# 初始化鸟类种类数据
python init_data.py

# 生成示例记录和坐标数据
python update_coords.py
```

#### 4. 创建超级管理员账户
```bash
# 方法1：使用批处理脚本
create_superuser.bat

# 方法2：手动创建
python manage.py createsuperuser
```

#### 5. 启动开发服务器
```bash
python manage.py runserver
```

#### 6. 访问系统
打开浏览器访问：http://127.0.0.1:8000/

## 🎯 系统功能

### 核心功能模块

#### 1. 🏠 鸟情态势仪表盘
- **统计概览**：总记录数、高风险记录数、今日新增
- **鸟种分布图**：饼图展示各类鸟种数量占比（Top 5）
- **活动趋势图**：近7日鸟情活动趋势线图
- **实时数据**：通过API接口动态更新图表数据

#### 2. 📋 记录管理
- **记录列表**：查看所有鸟情记录，按时间倒序排列
- **风险等级显示**：低风险/中风险/高风险的颜色标识
- **详细信息**：鸟种、数量、位置、记录时间、入侵原因等

#### 3. ➕ 新增记录
- **鸟种选择**：下拉选择已录入的鸟类种类
- **信息录入**：数量、发现位置、入侵原因
- **自动风险评估**：系统根据鸟类危险等级×数量自动计算风险等级

#### 4. 🗺️ ArcGIS地图视图
- **鸟情分布地图**：基于ArcGIS API的可视化地图
- **风险等级标识**：不同颜色标记不同风险等级的鸟情点
- **交互式弹窗**：点击标记查看详细信息
- **卫星底图**：高清卫星影像作为地图底图
- **图例说明**：风险等级颜色对照表

#### 5. 🔧 管理后台
- **鸟类种类管理**：添加、编辑、删除鸟类信息和危险等级
- **记录数据管理**：完整的数据CRUD操作
- **用户权限管理**：超级管理员权限控制

### 智能功能

#### 自动风险评估算法
```python
# 风险计算逻辑
score = bird_species.danger_level * quantity
if score > 50:
    risk_level = 'high'      # 高风险
elif score > 20:
    risk_level = 'medium'    # 中风险
else:
    risk_level = 'low'       # 低风险
```

## 📁 项目结构

```
BirdScreenProject/
├── bird_system/              # Django主项目配置
│   ├── settings.py          # 项目设置
│   ├── urls.py             # 主URL路由
│   ├── wsgi.py             # WSGI部署配置
│   └── asgi.py             # ASGI异步配置
├── monitor/                 # 鸟情监测应用
│   ├── models.py           # 数据模型
│   ├── views.py            # 视图逻辑
│   ├── urls.py             # 应用路由
│   ├── admin.py            # 管理后台配置
│   ├── templates/          # HTML模板
│   │   └── monitor/
│   │       ├── base.html   # 基础模板
│   │       ├── index.html  # 仪表盘页面
│   │       ├── record_list.html  # 记录列表
│   │       └── record_form.html  # 添加记录表单
│   ├── static/             # 静态资源
│   │   └── monitor/images/ # 鸟类图片
│   └── migrations/         # 数据库迁移文件
├── venv/                   # Python虚拟环境
├── db.sqlite              # SQLite数据库文件
├── manage.py              # Django管理脚本
├── init_data.py           # 初始化鸟类数据脚本
├── update_coords.py       # 更新坐标数据脚本
├── export_csv.py          # 数据导出脚本
├── run_server.bat        # 一键启动脚本
├── create_superuser.bat   # 创建管理员脚本
└── README.txt             # 项目说明文档
```

## 🗃️ 数据模型

### BirdSpecies（鸟类种类）
- **name**：鸟类名称
- **danger_level**：危险等级（1-10）
- **description**：描述信息

### BirdRecord（鸟情记录）
- **species**：关联的鸟类种类（外键）
- **quantity**：鸟类数量
- **location**：发现位置
- **latitude/longitude**：经纬度坐标
- **intrusion_reason**：入侵原因
- **record_time**：记录时间
- **risk_level**：风险等级（low/medium/high）
- **notes**：备注信息

## 🗺️ ArcGIS地图集成

### 地图功能特性

#### 1. 实时鸟情分布
- **卫星底图**：使用ArcGIS卫星影像作为底图
- **风险等级可视化**：
  - 🔴 **红色圆点**：高风险鸟情（直径随鸟类数量变化）
  - 🟡 **黄色圆点**：中风险鸟情
  - 🟢 **绿色圆点**：低风险鸟情
- **交互式弹窗**：点击任意鸟情点查看详细信息

### ArcGIS部署模式

#### 🖥️ **模式1: ArcGIS Online (默认)**
```javascript
// 使用公共ArcGIS服务
esriConfig.portalUrl = "https://www.arcgis.com";
```
- ✅ **优点**: 无需本地安装，立即可用
- ❌ **缺点**: 需要互联网连接
- 🔧 **适用场景**: 互联网环境，快速原型开发

#### 🏢 **模式2: ArcGIS Enterprise (企业推荐)**
```javascript
// 使用本地ArcGIS Enterprise
esriConfig.portalUrl = "https://your-portal-server.com/portal";
```
- ✅ **优点**: 内网部署，安全可控，企业级功能
- ✅ **支持**: 自定义底图，高级分析，离线使用
- 🔧 **适用场景**: 企业内网，政府部门，安全要求高的环境

#### 💻 **模式3: ArcGIS Desktop + Server**
```javascript
// 使用本地发布的地图服务
// 配置自定义底图服务URL
```
- ✅ **优点**: 完全离线，完全定制化
- ✅ **支持**: 本地数据，高精度地图，专业GIS功能
- 🔧 **适用场景**: 离线环境，专业GIS应用

#### 2. 数据集成方式
```javascript
// ArcGIS API集成示例
require([
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/GraphicsLayer"
], function(Map, MapView, GraphicsLayer) {
    // 创建地图实例
    const map = new Map({ basemap: "satellite" });
    const view = new MapView({
        container: "mapView",
        map: map,
        center: [116.4074, 39.9042], // 默认中心点
        zoom: 10
    });
});
```

#### 3. API数据接口
- **数据源**：`/api/bird-records/` - 返回所有有坐标的鸟情记录
- **数据格式**：JSON数组，包含经纬度、鸟种、风险等级等信息
- **实时更新**：支持动态刷新地图数据

#### 4. ArcGIS配置步骤

##### 配置本地ArcGIS Enterprise
```bash
# 运行配置工具
python arcgis_config.py

# 选择选项2配置Enterprise
# 输入您的Portal服务器地址，例如:
# https://your-arcgis-portal.company.com/portal
```

##### 修改地图模板配置
```javascript
// 在 monitor/templates/monitor/map_view.html 中修改:

// 选项1: 使用本地Portal
esriConfig.portalUrl = "https://your-portal-server.com/portal";

// 选项2: 添加API密钥 (如果需要)
esriConfig.apiKey = "your-api-key-here";

// 选项3: 使用本地地图服务
const map = new Map({
    basemap: "your-custom-basemap" // 使用本地发布的底图
});
```

##### 测试配置
```bash
# 运行测试脚本验证配置
python test_arcgis_integration.py
```

#### 5. 日志查看
- **导入历史**: 查看所有导入操作的详细记录
- **错误追踪**: 显示具体的错误信息和处理步骤
- **状态监控**: 实时显示导入进度和结果
- **筛选查询**: 按类型、状态筛选日志记录

#### 6. 扩展功能
- **热力图**：可扩展为鸟情密度热力图
- **轨迹分析**：显示鸟类迁徙路径
- **缓冲区分析**：机场周边安全缓冲区
- **时空分析**：鸟情活动的时间空间分布

### ArcGIS卫星影像数据说明

#### 🛰️ **影像时间特性**
- **非实时影像**: ArcGIS Online的卫星影像通常是历史影像，不是实时的"Google Earth那种动态地图"
- **数据来源**: 主要来自商业卫星公司（Maxar、Planet Labs、Airbus等）
- **更新机制**: 不定期更新，没有固定周期

#### 📅 **中国地区影像时效性**
- **主要城市**（北京、上海、深圳等）: 2019-2023年
- **一般城市**: 2017-2022年
- **郊区/农村**: 2015-2020年
- **偏远山区**: 可能2010-2015年或更早

#### 🔍 **如何查看影像时间**
1. **在地图上右键** → 查看"影像属性"或"About"
2. **使用浏览器开发者工具**检查网络请求
3. **访问ArcGIS服务元数据**:
   ```
   https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer
   ```

#### ⚠️ **重要提醒**
- **不是实时卫星图像** - 不能用于实时监控
- **仅用于地理参考** - 适合鸟情位置标注和历史分析
- **时效性因地区而异** - 城市地区更新较频繁
- **数据更新不保证** - Esri会根据新影像可用性进行更新

### ArcGIS集成优势

1. **专业GIS功能**：完整的地理信息系统能力
2. **高性能渲染**：支持大量数据点的快速渲染
3. **多种底图选择**：卫星、街道、地形等多种底图
4. **离线部署**：支持ArcGIS Enterprise私有化部署
5. **扩展性强**：可集成更多GIS分析功能

## 📤 数据导入导出

### 支持的文件格式
- **XLS/XLSX**: Excel格式文件
- **CSV**: 逗号分隔值文件（兼容airports.csv标准）

### 支持的数据类型
1. **鸟情数据**: 鸟类观测记录
2. **机场数据**: 机场地理信息（基于OurAirports数据库标准）

### 文件格式规范

#### 鸟情数据格式
**必需列：**
- **鸟种** (文本) - 鸟类名称，如"老鹰"、"海鸥"、"麻雀"
- **数量** (整数) - 鸟类数量，如3、5、10
- **位置** (文本) - 发现位置描述，如"跑道北侧"、"湖边区域"
- **纬度** (数值) - 纬度坐标，范围-90到90
- **经度** (数值) - 经度坐标，范围-180到180

**可选列：**
- **记录时间** (文本) - 格式：YYYY-MM-DD HH:MM:SS
- **入侵原因** (文本) - 鸟类出现的原因
- **备注** (文本) - 其他说明信息

#### 机场数据格式（兼容airports.csv标准）
**必需列：**
- **ident** (文本) - 机场标识符，如"ZBAA"、"PEK"
- **name** (文本) - 机场全称
- **latitude_deg** (数值) - 纬度坐标
- **longitude_deg** (数值) - 经度坐标

**可选列：**
- **type** (文本) - 机场类型：large_airport、medium_airport、small_airport等
- **elevation_ft** (数值) - 海拔高度（英尺）
- **iso_country** (文本) - 国家代码，如"CN"、"US"
- **municipality** (文本) - 城市名称
- **icao_code** (文本) - ICAO代码
- **iata_code** (文本) - IATA代码

### Web界面导入步骤

1. **访问导入页面**：http://127.0.0.1:8000/import-xls/
2. **选择导入类型**：鸟情数据或机场数据
3. **下载示例文件**：点击相应的示例文件下载链接
4. **准备数据**：按照示例格式准备XLS/CSV文件
5. **上传文件**：选择文件并点击"开始导入"
6. **实时监控**：系统自动打开实时日志监控窗口
7. **查看结果**：实时日志显示导入进度和结果

### 数据验证规则

- **鸟种名称**：不能为空，不存在的鸟种会自动创建（危险等级默认为3）
- **坐标范围**：纬度-90到90，经度-180到180
- **数量**：必须为正整数
- **时间格式**：支持YYYY-MM-DD或YYYY-MM-DD HH:MM:SS格式
- **重复数据**：系统会直接插入，不会检查重复

## 🛠️ 数据导入导出

### 导入数据

#### 方法1：通过管理后台
1. 访问 http://127.0.0.1:8000/admin/
2. 登录超级管理员账户
3. 在"BirdSpecies"和"BirdRecord"中添加数据

#### 方法2：使用脚本
```bash
# 初始化鸟类种类
python init_data.py

# 生成示例数据
python update_coords.py
```

#### 方法3：Web界面导入（推荐）
通过浏览器上传文件批量导入数据
- 访问：http://127.0.0.1:8000/import-xls/
- 支持XLS、XLSX和CSV格式
- 支持鸟情数据和机场数据导入
- 自动数据验证和错误提示
- 可下载示例文件作为模板

#### 方法4：自定义导入脚本
创建Python脚本使用Django ORM批量导入数据

### 导出数据
```bash
# 导出为CSV格式
python export_csv.py
```

## 🎨 前端界面

### 技术栈
- **Bootstrap 5.1.3**：响应式CSS框架
- **Chart.js**：图表可视化库
- **ArcGIS API for JavaScript 4.28**：专业地图可视化
- **Font Awesome**：图标库
- **自定义CSS**：毛玻璃效果、渐变背景

### 界面特点
- 📱 **响应式设计**：支持桌面端和移动端
- ✨ **现代化UI**：毛玻璃效果、渐变色彩
- 🎭 **交互动画**：悬停效果和平滑过渡
- 📊 **数据可视化**：饼图和线图展示统计数据

## 🔧 开发和部署

### 开发环境配置

#### 1. 克隆项目
```bash
git clone <repository-url>
cd BirdScreenProject
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

#### 3. 安装依赖
```bash
pip install django
```

#### 4. 运行迁移
```bash
python manage.py migrate
```

### 生产环境部署

#### 使用WSGI（推荐）
- 安装Gunicorn：`pip install gunicorn`
- 运行：`gunicorn bird_system.wsgi:application`
- 配置Nginx反向代理

#### 使用ASGI（支持异步）
- 安装Uvicorn：`pip install uvicorn`
- 运行：`uvicorn bird_system.asgi:application`

## 📞 使用说明

### 日常操作流程

1. **登录系统**：访问主页查看鸟情概况
2. **添加记录**：发现鸟情时及时录入信息
3. **查看统计**：通过仪表盘了解鸟情趋势
4. **数据管理**：定期导出数据进行分析

### 维护建议

- **定期备份**：备份 `db.sqlite` 数据库文件
- **数据清理**：定期清理过期记录
- **性能监控**：监控数据库查询性能
- **安全更新**：及时更新Django和依赖包

## 🐛 常见问题

### Q: 启动时提示端口被占用
A: 修改启动命令：`python manage.py runserver 8001`

### Q: 无法访问管理后台
A: 确认已创建超级用户账户并正确登录

### Q: 图表不显示数据
A: 检查数据库是否有数据，运行 `update_coords.py` 生成示例数据

### Q: ArcGIS地图无法加载
A: 检查网络连接，确认ArcGIS服务是否可访问。尝试使用离线模式或配置本地ArcGIS Enterprise

### Q: 如何使用本地ArcGIS Desktop提供地图服务
A:
1. 确保ArcGIS Desktop和ArcGIS Server已安装
2. 在ArcGIS Server中发布地图服务
3. 在Django项目中配置本地服务URL
4. 使用 `python arcgis_config.py` 进行配置

### Q: 导入数据后地图上什么都没有显示怎么办
A: 请查看 `IMPORT_TROUBLESHOOTING.md` 文件，里面有详细的故障排除指南

### Q: 如何查看导入过程的详细日志
A: 访问 http://127.0.0.1:8000/import-logs/ 查看所有导入日志记录

### Q: 样式显示异常
A: 确认网络连接正常，CDN资源能正常加载

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

## 👥 技术支持

如有问题或建议，请联系开发团队。

---

**最后更新时间**: 2025年12月17日
**系统版本**: v1.0
**Django版本**: 6.0
