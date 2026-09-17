
# PROATHLETE · 个人多生态运动数据中枢

> 一个纯前端 + 本地代理后端的个人运动数据看板。支持 Garmin 中国区一键同步，多主题液态玻璃 UI，FIT / GPX / TCX / XLSX / CSV 多格式导入，以及完整的运动科学分析。

![status](https://img.shields.io/badge/status-active-brightgreen)
![license](https://img.shields.io/badge/license-MIT-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![storage](https://img.shields.io/badge/storage-IndexedDB-orange)
![icons](https://img.shields.io/badge/icons-inline%20SVG-purple)

---

## 📖 项目简介

PROATHLETE 是一个自托管的运动数据中枢，包含：

- **前端**：单文件 `index.html`，纯静态，无需构建。液态玻璃设计，9 款精美主题，全站线性 SVG 图标，支持拖拽导入、数据可视化、ACWR 分析、心率区间、心率漂移、分段 PB、年度热力图等。
- **后端**：`garmin_server.py`，一个本地 Flask 服务，作为 Garmin Connect 的代理，解决纯前端无法直连 Garmin 的问题。特别适配 **Garmin 中国区（[garmin.cn](https://garmin.cn)）** 账号。

整个项目无需数据库服务器，**数据保存在浏览器 IndexedDB**，后端仅负责同步中转，不存储任何账号信息。

---

## ✨ 功能特性

### 前端

#### 🎨 界面与主题

- **9 款主题**：深空、Dracula、Nord、Mocha、Latte、Rosé Pine、Tokyo Night、Gruvbox、One Dark。全部适配液态玻璃，切换平滑。
- **液态玻璃 UI**：可调节**透明度**、**模糊强度**、**饱和度**，类似 Apple 的毛玻璃质感。
- **自定义背景图**：上传任意图片作为最底层背景，自动压缩并叠加遮罩保证可读性。
- **卡片自定义图标**：每张功能卡片支持上传 PNG/SVG 图标（自动压缩到 512px 内），通过 CSS Mask 渲染为主题色。
- **全站线性 SVG 图标系统**：导航、按钮、标签页、表头、状态提示、卡片图标统一使用 Lucide 风格**描边（线性）SVG**（24×24 viewBox、1.7px 描边、圆角端点），描边走 `currentColor`，自动跟随主题、hover、active 变色。
  - `ICONS` 注册表：`name → SVG innerHTML` 映射，50+ 图标。
  - `ic(name, size)`：动态 HTML 中生成 `<svg class="ic-svg">`。
  - 静态 HTML 用 `<span data-ic="xxx" data-size="yy">` 占位，`init()` 开头调用 `materializeIcons()` 批量物化。
  - CSS `.ic-svg { stroke:currentColor; fill:none; stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round; }`。
  - **清零文字符号图标**：原先充当图标的 `☰ ↑ ↓ → +` 等字符已全部替换为 SVG，并新增 `all / menu / plus / arrowRight / arrowDown` 等图标。
  - **全站零 Emoji**，视觉重量一致、无外部依赖、无渲染差异。
- **响应式布局**：侧边栏在鼠标悬停时展开，移动端自动折叠为汉堡菜单。

#### 📊 数据总览

- **总览卡片**：总用时（含天数/周数折算）、总运动次数、分类次数分布。
- **跑步统计**：当日 / 总累计 / 室外 / 室内 分列显示。
- **骑行统计**：当日 / 总累计 / 室外 / 室内 分列显示。
- **步行与徒步**：当日步行 / 总步行 / 室外步行 / 徒步累计。
- **年度热力图**：GitHub 风格 53×7 网格，按运动类型着色（跟随主题 CSS 变量），按当日总时长分 5 档强度；**打破个人纪录的日期带金色脉冲光环 + 星标**。

#### 📈 周期详情

- 点击任一卡片进入周 / 月 / 年 / 全部周期对比。
- 每个周期卡片含：6 项核心指标（带同比涨跌）、可切换柱状/折线图（距离、配速、速度、心率、爬升、时长、步数）、心率区间或速度区间甜甜圈图、星期分布柱状图、最近活动列表。
- 支持**拖拽切换周期**、左右箭头键盘操作、底部圆点快速跳转。

#### 🔢 总次数详情页

- 与「总用时」详情页**完全去重**：共用渲染框架，但通过 `mode: 'time' | 'count'` 拆分两种视图，各自呈现对应维度的指标与图表。
- 5 张「次数向」图表（替换原先与总用时重复的内容）：
  - **月度频次柱状图**：按月统计运动次数。
  - **星期 × 小时时段热力图**：展示一周内各时段的运动频次分布。
  - **12 月玫瑰图**：极坐标展示一年 12 个月的运动频次节律。
  - **运动类型累计条形图**：各类型累计次数排名。
  - **累计增长折线图**：运动次数随时间的累计增长曲线。
- 全部采用**次数 / 时间**维度（而非距离 / 时长），与总用时页、周期详情页、分析页图表零重复。

#### 🏆 个人最佳（PB）与分段最佳

- **PB 网格**：按运动类型自动计算最长距离、最快配速、最长时长、最大爬升、最大消耗、最快均速、最大功率、最大步数等。
- **分段最佳时间**：采用**双指针 + 边界线性插值**算法，精确计算每段覆盖目标距离的最短耗时。支持：
  - 跑步：1km / 5km / 10km / 半马 / 全马
  - 骑行：10 / 20 / 40 / 60 / 80 / 100 km
  - 游泳：400m / 800m / 1500m / 3000m
  - 徒步：10 / 20 / 30 / 40 / 50 / 100 km
- 分段卡片附**该段均速**（如 `5km → 21:35 · 均速 4:19/km`）。
- 命中 PB 的活动在列表中以 🏆 SVG 图标标记，单次详情弹窗中显示全部命中徽章。

#### 🗺️ 轨迹与图表

- 单次活动详情弹窗显示：GPS 轨迹（带起终点标记）、海拔、配速/速度、心率、步频、功率曲线、心率区间分布、完整统计信息。
- 轨迹图为活动点云自动缩放 + 保持宽高比绘制。

#### ❤️ 运动科学指标

**真实派生指标**（从轨迹点计算，具备生理学意义）：

- **心率漂移 (HR Drift)**：`(后半段 HR/Speed − 前半段 HR/Speed) / 前半段 HR/Speed × 100%`，运动科学中公认的有氧耐力指标。判读：`< 5%` 优秀，`5–10%` 良好，`> 10%` 提示有氧耐力待提高或疲劳。活动详情与当日详情中均展示，超 ±10% 红色高亮。
- **心率-速度比**：逐点图表 `HR (bpm) / Speed (m/s)`，反映单位速度下所需心率。该值随时间上升代表有氧效率下降，是心率漂移的时序可视化。
- **ACWR 急慢性负荷比**：7 天急性负荷 / 28 天慢性负荷，安全区间 0.8–1.3，超出则用红/绿虚线提示。
- **心率区间分布**：基于最大心率百分比划分 Z1–Z5，可自定义最大心率。

**Garmin Running Dynamics 活动级字段**（从 Garmin 官方 CSV 读取的真实平均值，非伪造时序）：

- 垂直步幅比 (%)、平均步长 (m)、垂直摆动 (cm)、平均触地时间 (ms)

#### 🚀 进步可视化（数据分析页）

- 数据分析页新增「进步可视化」专区，共 **4 张专业图表**，直观展示运动能力的进步过程：
  - **耐力表现趋势**：散点图 + OLS 线性回归拟合线，展示配速 / 速度随时间的趋势。
  - **阶段能力雷达**：六维雷达图，对比早期 vs 近期能力画像。
  - **稳定性演变**：季度 KDE 脊线图，展示配速分布的收敛 / 离散演变。
  - **心肺效率 EF**：月均 EF（Efficiency Factor，距离 / 心率）面积折线。
- 每张卡片配**方法学引言**与**逐卡数据讲解**，说明指标含义与判读方式；图表维度与其它页面零重复。

#### 📁 多格式导入

- **`.fit`**：Garmin 二进制，手写解析器（正确处理压缩时间戳、developer fields、多 local message 定义）。
- **`.gpx`**：标准 XML 轨迹。
- **`.tcx`**：Garmin Training Center XML。
- **`.zip`**：自动解压内部 FIT/GPX/TCX。
- **`.xlsx`**：Keep / 悦跑圈等导出表，手写 XLSX 解析器（无需 SheetJS）。
- **`.csv`**：**Garmin 官方导出**，两种格式均支持：
  - `Activities.csv`：活动汇总表（活动类型、日期、标题、距离、热量、时间、心率、步频、爬升、功率、温度、垂直步幅比等）。
  - `activity_*.csv`：单次活动的分圈数据，含"摘要信息"行。
- **自动去重**：按运动类型分层容差（见下文），时间窗 + 距离或时长接近的活动会被识别为重复，导入时跳过并提示。
- 支持拖拽整个文件夹/多文件、拖拽 ZIP 自动展开。

#### 📤 导出

- 一键导出 CSV（含日期、名称、类型、距离、时长、心率、爬升、卡路里、训练负荷、来源、命中 PB）。使用 UTF-8 BOM + CRLF 换行，Windows Excel 直接双击打开不乱码不串行。

#### ✨ 演示数据

- 内置生成器，400 天随机生成约 200 条多类型活动，含完整轨迹点、心率、步频、功率、温度序列、Running Dynamics 字段，方便立即体验。

#### ⚙️ 生理阈值与数据设置

- **最大心率**（140–220 bpm）：用于心率区间计算。
- **静息心率**（35–90 bpm）：用于心率储备与训练负荷计算。
- **体重**（30–150 kg）：用于卡路里估算。
- **距离单位**：公里 / 英里一键切换，所有显示自动换算。
- 修改以上参数会触发全量重算（区间 + 负荷）并持久化。

---

### 后端（`garmin_server.py`）

- 🔐 **Garmin 中国区登录**：强制 `is_cn=True`，适配 `sso.garmin.cn`。
- ☁️ **Cloudflare 绕过**：依赖 `curl_cffi` 模拟浏览器 TLS 指纹。
- 📦 **FIT 下载与解压**：自动从 ZIP 中提取 `.fit`，Base64 返回前端。
- 🧵 **异步任务**：线程处理同步，前端轮询进度，不阻塞。
- 🩺 **健康检查**：`/api/garmin/health` 用于测试后端连通性。

---

## 📂 目录结构

```text
.
├── index.html            # 前端单文件应用（所有 CSS/JS 内联）
├── garmin_server.py      # Garmin 同步后端（Flask）
├── requirements.txt      # Python 依赖（可选）
└── README.md
````

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- 现代浏览器（Chrome / Edge / Safari / Firefox，需支持 IndexedDB 与 DecompressionStream）
- Garmin 中国区账号（[garmin.cn](https://garmin.cn)）

### 2. 安装后端依赖

```bash
pip install --upgrade "garminconnect>=0.3.4" curl_cffi ua-generator flask flask-cors
```

> ⚠️ **版本非常重要**：
>
> - `garminconnect` 必须 ≥ 0.3.4，否则中国区登录会失败。
> - `curl_cffi` 和 `ua-generator` 用于绕过 Cloudflare，中国区必需。

### 3. 启动后端

```bash
python garmin_server.py
```

看到以下输出即成功：

```text
==============================================================
  PROATHLETE Garmin Sync Server  ·  中国区 (garmin.cn)
==============================================================
  garminconnect : 可用 0.3.4
  curl_cffi     : 可用
  区域模式      : is_cn=True (强制)

  监听: http://0.0.0.0:5000
  前端填写: http://localhost:5000
  按 Ctrl+C 停止
==============================================================
```

### 4. 打开前端

直接用浏览器打开 `index.html` 即可。
如果使用 `file://` 打开，Garmin 同步可能因 CORS 失败，建议用本地服务器：

```bash
# Python 内置
python -m http.server 8080

# 或 Node
npx serve .
```

然后访问 `http://localhost:8080`。

### 5. 配置 Garmin 同步

1. 前端进入「数据导入」→「Garmin Connect 同步」。
2. 点击「配置账号」，填写：
   - **Garmin 邮箱**：你的 [garmin.cn](https://garmin.cn) 登录邮箱
   - **后端地址**：`http://localhost:5000`
   - **首次拉取天数**：建议 30
3. 点击「保存配置」，然后「测试连接」。
4. 连接正常后，**在同步面板手动输入 Garmin 密码**（密码不保存），点击「同步新活动」，等待进度条完成。

### 6. 非 Garmin 用户

无需启动后端，直接在「数据导入」页拖入 FIT / GPX / TCX / XLSX / CSV 文件即可：

- **手环 / 手表用户**：导出 FIT 或 GPX。
- **Keep / 悦跑圈用户**：导出 XLSX。
- **Garmin Connect 网页用户**：设置 → 数据管理 → 导出 CSV，可选「活动」汇总或单次活动分圈。

---

## 🔒 密码安全说明

**本应用不保存 Garmin 密码**。前后端均遵守此规则：

- **前端**：配置面板仅保存邮箱、后端地址、拉取天数到 `localStorage`。密码输入框仅在同步时短暂存在于内存中（`sessionPassword`），同步完成立即清空。
- **后端**：密码仅用于当次登录，登录流程结束后即丢弃，不落盘、不写日志。
- 首次启动会自动清理旧版本可能残留的密码字段（`load()` 中检测 `config.password` 并重写为安全版本）。

---

## 🕳️ 踩坑记录（重点）

以下是我在开发和使用过程中真实遇到并解决的问题，按出现频率排序。

### 坑 1：纯前端无法直连 Garmin Connect

**现象**：想在 `index.html` 里直接 `fetch('https://connect.garmin.com/...')`，结果全部失败。

**原因**：Garmin 的 API 需要 OAuth 认证、Cookie 会话、CSRF Token，且浏览器同源策略和 CORS 不允许。Cloudflare 也会拦截浏览器发起的非官方请求。

**解决**：必须有一个本地后端做代理。后端用 `garminconnect` 库登录并保持会话，前端只与本地后端通信。这就是 `garmin_server.py` 存在的原因。

---

### 坑 2：Garmin 中国区登录 401 Unauthorized（最坑）

**现象**：账号密码完全正确，在 [garmin.cn](https://garmin.cn) 网页能正常登录，但 `garminconnect` 始终报：

```text
GarminConnectAuthenticationError: 401 Unauthorized (Invalid Username or Password)
```

**原因**：旧版 `garminconnect` 的 `is_cn=True` 参数**没有完全生效**。虽然 `domain` 被设为 `garmin.cn`，但认证流程中的 SSO URL 仍被硬编码为 `.com`，导致中国区账号在登录阶段就被拒绝。这是 `python-garminconnect` 的已知 Bug，在 PR #366 中修复，随后 v0.3.4 进一步修复了中国区令牌刷新路由问题。

**解决**：

```bash
pip install --upgrade "garminconnect>=0.3.4"
```

并在代码中强制传入 `is_cn=True`：

```python
client = Garmin(email, password, is_cn=True)
```

`garmin_server.py` 中已强制启用，并加入了版本检查。

---

### 坑 3：Cloudflare 拦截导致 403 / 401

**现象**：升级库后仍然登录失败，终端可能没有明显 Cloudflare 报错，但请求就是不通。

**原因**：Garmin 中国区使用 `sso.garmin.cn`，前面有 Cloudflare 防护。普通 `requests` 的 TLS 指纹会被识别为机器人，直接拦截。

**解决**：安装 `curl_cffi` 和 `ua-generator`，它们能模拟真实浏览器（Safari/Chrome）的 TLS 指纹。

```bash
pip install curl_cffi ua-generator
```

`garminconnect` 会自动检测并优先使用 `curl_cffi`。`garmin_server.py` 启动时会检查是否安装，未安装会打印警告。

---

### 坑 4：MFA（多因素认证）导致登录失败

**现象**：报错包含 `MFA`、`multi-factor`、`verification` 等关键词。

**原因**：Garmin 账号启用了两步验证，`garminconnect` 无法在非交互环境下完成 MFA。

**解决**：

- 临时关闭 Garmin 账号的 MFA（登录 [garmin.cn](https://garmin.cn) → 账户设置 → 安全）。
- 或使用 Garmin 应用专用密码（如果支持）。
- 同步完成后可以重新开启 MFA。

---

### 坑 5：请求限流 429

**现象**：短时间内多次登录或下载，报错 `429 Too Many Requests`。

**原因**：Garmin 对频繁请求有速率限制，尤其是登录和活动下载。

**解决**：

- 等待数小时或一天后再试。
- 切换网络（如手机热点），更换公网 IP。
- 代码中每次下载后 `sleep(0.35)` 秒，避免触发风控。

---

### 坑 6：本地令牌缓存损坏

**现象**：之前能登录，突然不行了，报认证错误。

**原因**：`garminconnect` 会在用户目录缓存令牌（通常在 `~/.garth` 或类似文件夹），缓存过期或损坏会导致认证异常。

**解决**：

- 删除缓存目录：`rm -rf ~/.garth`（Windows：`C:\Users\你的用户名\.garth`）。
- 重新运行同步。

---

### 坑 7：VPN / 代理干扰

**现象**：开了 VPN 后 Garmin 登录失败。

**原因**：部分 VPN 节点被 Garmin 标记或网络环境异常，导致登录请求被拒。

**解决**：关闭 VPN，或切换到其他节点。中国区账号最好在中国大陆网络环境下使用。

---

### 坑 8：端口 5000 被占用

**现象**：启动 `garmin_server.py` 时报 `Address already in use`。

**原因**：5000 端口被其他程序（如 macOS 的 AirPlay）占用。

**解决**：

- 修改 `garmin_server.py` 最后一行：`app.run(host="0.0.0.0", port=5001, ...)`
- 前端配置中的后端地址改为 `http://localhost:5001`。

---

### 坑 9：前端用 file:// 打开导致 CORS 失败

**现象**：Garmin 同步时前端报 `Failed to fetch` 或 CORS 错误。

**原因**：浏览器对 `file://` 协议发起的跨域请求限制严格。

**解决**：用本地 HTTP 服务器打开前端：

```bash
python -m http.server 8080
# 访问 http://localhost:8080
```

后端已配置 `CORS(app)`，允许跨域。

---

### 坑 10：局域网其他设备无法访问后端

**现象**：手机或另一台电脑填 `http://localhost:5000` 连不上。

**原因**：`localhost` 只指向本机。后端默认监听 `0.0.0.0` 时，其他设备需要用本机的局域网 IP。

**解决**：

1. 查本机局域网 IP：
   - Windows：`ipconfig`，找 IPv4 地址
   - macOS：`ipconfig getifaddr en0`
   - Linux：`hostname -I`
2. 前端后端地址填 `http://192.168.x.x:5000`。
3. 确保防火墙放行 5000 端口。

---

### 坑 11：同步大量活动时前端卡顿

**现象**：活动很多时，同步完成后页面卡顿。

**原因**：每个 FIT 文件 Base64 后体积膨胀约 33%，大量文件同时传输和解析会占用内存。

**解决**：

- 首次同步天数不要设太大（建议 30 天）。
- 后续同步会自动只拉新数据。
- 代码已对活动点做降采样（最多 800 点），减少存储压力。

---

### 坑 12：garminconnect 版本检查误报

**现象**：启动时提示版本过低，但实际已安装新版。

**原因**：`__version__` 属性在某些安装方式下可能缺失或格式异常。

**解决**：代码中做了容错，版本无法解析时会跳过检查，让实际登录暴露问题。如果确认版本正确但仍报错，可以临时注释版本检查。

---

### 坑 13：分段 PB 全部显示为空

**现象**：导入活动后，「数据分析 → 分段最佳时间」所有分段（1km、5km、10km…）都显示"暂无记录"。

**原因**：早期版本的滑动窗口算法存在边界判断缺陷：

```js
// ❌ 错误写法
while (left < right && pts[right].d - pts[left].d > target) left++;
if (pts[right].d - pts[left].d >= target) { ... }
```

循环会把 `left` 推到让差值 **≤ target** 的位置，而 `if` 又要求 **≥ target**——只有当差值**恰好等于**目标距离（浮点精确相等）时才会命中。实际采样点离散分布，几乎永远不成立。

**解决**：改用**双指针 + 边界线性插值**：

1. 过滤非法点、距离回退点，保证 `d` 单调非递减。
2. 对每个左端点 `l`，推进右端点 `r` 直到覆盖 `target` 距离。
3. 在 `[r-1, r]` 两点之间做**线性插值**，求出恰好 `target` 距离对应的精确时刻。
4. 取全局最小的 `endT - pts[l].t`。

同时引入 `State.segPBCache` 缓存，避免每次切页面都重算。

---

### 坑 14：数据存储从 localStorage 迁移到 IndexedDB

**现象**：早期版本用 `localStorage` 存活动数据，几百条后接近 5MB 上限，写入开始失败。

**原因**：`localStorage` 单域名通常限制 5–10MB，且同步 API 会阻塞主线程。

**解决**：

- 迁移到 **IndexedDB**（数据库名 `proathlete_db`），配额通常几百 MB 到数 GB。
- 保留一次性迁移逻辑：首次启动检测旧版 `proathlete_v20_*` 键，自动导入 IndexedDB 并清除旧数据。
- 后续持久化使用 `putActivities`（增量写入）替代全量重写，性能显著提升。

---

### 坑 15：XLSX 解析不依赖第三方库

**现象**：不想引入 SheetJS（体积大、CDN 依赖），但需要解析 Keep / 悦跑圈导出的 `.xlsx`。

**原因**：`.xlsx` 本质上是一个 ZIP，内部是 XML。

**解决**：手写解析器：

1. 用 `DataView` 手动定位 ZIP 的 EOCD 记录和中央目录。
2. 用原生 `DecompressionStream('deflate-raw')` 解压（现代浏览器已支持）。
3. 正则解析 `sharedStrings.xml` 和 `sheet*.xml`，还原单元格值。
4. 智能识别表头（`运动类型`、`开始时间`、`运动距离` 等），多工作表遍历。

---

### 坑 16：FIT 文件二进制解析

**现象**：`fit-file-parser` 之类的库要么体积大，要么不支持所有字段。

**解决**：手写 FIT 解析器：

1. 校验头 12 字节的 `.FIT` 签名。
2. 逐条读记录头，区分**定义消息**（0x40）和**数据消息**。
3. 处理**压缩时间戳**（5 位偏移 + 上次时间戳拼合）。
4. 提取 File ID（0）、Session（18）、Record（20）三类消息。
5. 坐标按 `180/2^31` 缩放，高度按 `v/5 - 500` 解码。
6. **正确跳过 Developer Fields**：FIT 协议中，当 Definition Message 设置了 `developer_data_flag` (0x20)，Data Message 内除了普通字段数据外，还会追加 developer field 的原始数据。早期实现只跳过了 definition 里的 3 字节描述，没有在 data message 里跳过对应数据字节，导致指针错位、后续记录解析全乱。修复后从 Definition 保存 `devFields:[{size}]`，Data 时按 size 累加指针。

---

### 坑 17：Garmin 官方 CSV 解析的单位陷阱

**现象**：直接把 `Activities.csv` 拖进来看板，距离显示为 `0.005 km`，时长显示为 `0`，步数变成 `4`。

**原因**：Garmin 官方 CSV 的字段与直觉不符：

- **距离列单位是公里**（`5.01`），而非米。直接 `parseFloat` 后当作米存储会少 1000 倍。
- **时长列是 `HH:MM:SS` 字符串**（`00:25:57`），`parseFloat` 会截断为 `0`。
- **步数等大数字带千分位逗号**（`"4,774"`），`parseFloat("4,774")` = `4`。
- **空值占位符是 `--`**，`parseFloat("--")` = `NaN`。
- **温度可能是 `'-2`**（带前导单引号），需要清洗引号。
- **中文活动类型"跑步机"** 应映射为 `run + indoor: true`，而不是 `other`。

**解决**：为 Garmin CSV 专门写了 6 个宽容解析工具函数：

```js
parseNumLoose(v)      // 去逗号、去引号、处理 --，返回数字或 null
parseDurationStr(s)   // 支持 HH:MM:SS / MM:SS.s / 纯秒数
parsePaceStr(s)       // M:SS → 秒
normalizeGarminType(s)// 中文类型 → {type, indoor}
parseGarminDate(s)    // "2026-09-15 20:02:20" → ISO
parseCSV(text)        // 处理引号转义、CRLF/LF、BOM
```

并对 `Activities.csv`（汇总）与 `activity_*.csv`（分圈）分别实现解析路径，通过表头正则 `detectGarminCSV` 自动识别。

---

### 坑 18：活动去重的容差不能"一刀切"

**现象**：早期统一用"时间差 < 3 分钟 + 距离差 < 500m"判断重复。结果：

- **游泳**：800m 的游泳与 1300m 的游泳被判为重复（500m 差异对游泳来说是一整趟）。
- **骑行**：100km 骑行的两次记录差 400m（GPS 漂移）被判为不同活动。
- **力量训练**：没有距离和时长数据时永远不判重。

**解决**：按运动类型分层容差：

```js
const DUP_TOLERANCE = {
  run:   { timeMs: 3*60*1000, absDist: 300, relDist: 0.08, absDur: 120, relDur: 0.08 },
  walk:  { timeMs: 3*60*1000, absDist: 300, relDist: 0.10, absDur: 120, relDur: 0.10 },
  hike:  { timeMs: 3*60*1000, absDist: 500, relDist: 0.08, absDur: 180, relDur: 0.08 },
  cycle: { timeMs: 3*60*1000, absDist: 500, relDist: 0.05, absDur: 120, relDur: 0.08 },
  swim:  { timeMs: 6*60*1000, absDist: 50,  relDist: 0.05, absDur: 120, relDur: 0.08 },
  gym:   { timeMs: 5*60*1000, absDist: 0,   relDist: 0,    absDur: 300, relDur: 0.15 },
  other: { timeMs: 3*60*1000, absDist: 500, relDist: 0.10, absDur: 120, relDur: 0.10 },
};
```

时间窗、绝对距离容差、相对距离容差、绝对时长容差、相对时长容差五项同时生效。距离或时长任一缺失时，只依赖另一维度；两者都缺失（如力量训练），仅凭类型 + 时间窗判定。

---

### 坑 19：别用随机数伪装运动科学指标

**现象**：早期"当日详情 → 对比"页有一张"体能状况指数"曲线和一张"垂直步幅比"曲线。前者用 `hr > 0.85 ? -0.6 : hr > 0.75 ? -0.2 : ...` 的累积和模仿 Garmin Body Battery，后者直接是 `7.0 + sin(i/20) * 0.4 + Math.random() * 0.15`。用户截图分享后被人发现是假数据。

**原因**：Body Battery 是基于 HRV、睡眠、压力、活动强度的多因子模型，用单变量心率阈值累积根本无法模拟；垂直步幅比是真实 Running Dynamics 字段，不能凭空造时序曲线。

**解决**：

- **删除**这两张伪造曲线。
- **新增**心率漂移 (HR Drift) —— 真实有生理学意义的派生指标。
- **新增**心率-速度比 —— 逐点计算 `HR / Speed`，反应有氧效率漂移。
- **垂直步幅比、平均步长、垂直摆动、平均触地时间**改为**活动级真实平均值**，从 Garmin 官方 CSV 读取（Garmin 手表本身就计算这些字段），作为单一数字展示而非伪造时序曲线。

**教训**：伪科学比没有数据更糟。要么用真实数据，要么坦诚地不展示。

---

### 坑 20：全站 Emoji 图标难以统一风格

**现象**：导航、按钮、标签页混用 Emoji（🏠🏃📊📁⚙️✨），在不同操作系统上渲染差异极大（macOS 是彩色拟物，Windows 是扁平单色，Android 是 Noto 彩色），整体视觉凌乱，且 Emoji 无法跟随主题色变色。

**解决**：全站 Emoji 替换为**内联线性 SVG 图标**：

1. 建立 `ICONS` 注册表（`name → SVG innerHTML`），约 45 个 24×24 viewBox 的 Lucide 风格图标。
2. 提供 `ic(name, size)` 函数生成 `<svg class="ic-svg" ...>`，`stroke:currentColor` 自动继承颜色。
3. 静态 HTML 用 `<span data-ic="xxx" data-size="yy"></span>` 占位，`init()` 一开始调用 `materializeIcons()` 批量替换。
4. 动态 HTML（如列表渲染）直接拼 `ic(name, size)` 字符串。
5. CSS 定义 `.ic-svg { stroke:currentColor; fill:none; stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round; }`。
6. 填充点用内联 `style="fill:currentColor;stroke:none"` 覆盖全局 CSS。

**效果**：全站视觉重量一致、颜色随主题/状态自动变化、无外部依赖、无闪烁。

---

### 坑 21：文字符号图标（`☰ ↑ ↓ → +`）风格不统一

**现象**：导航折叠、方向提示、新增按钮等处直接用字符 `☰ ↑ ↓ → +` 充当图标。这些字符在不同字体下字重、基线、尺寸都不同，与线性 SVG 图标并排时明显不协调，且无法随主题描边走色。

**解决**：把 `☰ ↑ ↓ → +` 全部替换为线性 SVG 图标，并在 `ICONS` 注册表补齐 `menu / arrowUp / arrowDown / arrowLeft / arrowRight / plus`；同时新增 `all`（全部）等导航类图标，统一由 `ic()` 生成。

**教训**：字符在语义上接近图标，但在视觉上永远不是图标。

---

### 坑 22：「总次数」与「总用时」的详情页内容重复

**现象**：总览里「总用时」和「总次数」两张卡片点进去后，是同一套指标与图表，只是数字维度不同，用户会觉得"点哪个都一样"。

**解决**：把详情页渲染拆成 `mode: 'time' | 'count'` 两种模式：`time` 保留时长 / 距离 / 配速向图表，`count` 换成 5 张纯次数向图表（月度频次柱、星期 × 小时时段热力、12 月玫瑰、类型累计条形、累计增长折线），并核对与其它页零重复。

**教训**：两个入口背后应是两种视角，而不是同一份数据的两次展示。

---

### 坑 23：进步可视化不能凭空造「进步」

**现象**：想加"能力进步"图表时，很容易直接画一条"总体向上"的曲线来暗示进步。

**解决**：坚持用真实派生指标与统计方法——耐力趋势用散点 + OLS 回归、阶段能力用六维雷达对比早期 / 近期、稳定性用季度 KDE 脊线、心肺效率用月均 EF（距离 / 心率）面积线，并为每卡写方法学引言与判读说明，让"进步"有数据支撑而非视觉暗示。

**教训**：可视化的诚实性，取决于你把哪条线画出来、又为什么画它。

---

## ❓ 常见问题 FAQ

**Q：必须用中国区账号吗？**
A：当前后端强制 `is_cn=True`，适配 [garmin.cn](https://garmin.cn)。如果你用国际版，可以改为 `is_cn=False`。

**Q：不用 Garmin，能导入什么格式？**
A：支持 FIT（Garmin 二进制）、GPX（通用轨迹）、TCX（Garmin Training Center）、ZIP（自动解压）、XLSX（Keep / 悦跑圈）、CSV（Garmin 官方导出）。纯前端页面无需后端即可导入。

**Q：Garmin Activities.csv 与单次分圈 CSV 有什么区别？**
A：`Activities.csv` 是整个账号的活动汇总表，一次可导入几十上百条活动。`activity_*.csv`（如 `activity_639552615.csv`）是单次活动的分圈数据，含"摘要信息"行，用于精细分析。两种都能拖入导入页，代码通过表头自动识别。

**Q：同步的数据存在哪里？**
A：前端 **IndexedDB**（数据库 `proathlete_db`）。后端不存储。清除浏览器数据会丢失，建议定期导出 CSV。

**Q：后端会保存我的 Garmin 密码吗？**
A：不会。前端配置面板也不保存密码，每次同步前需手动输入，同步完成后立即从内存清空。

**Q：支持哪些 Garmin 设备？**
A：只要活动能同步到 Garmin Connect，就能拉取 FIT 文件，与设备型号无关。

**Q：为什么同步这么慢？**
A：每个活动需要单独下载 FIT，且代码加了 0.35 秒延时避免限流。活动多时耐心等待。

**Q：可以同时开多个前端吗？**
A：可以，但 IndexedDB 是按浏览器（域名）隔离的，数据不共享。

**Q：如何备份数据？**
A：在「活动记录」页点击「导出 CSV」，会生成含全部字段的 UTF-8 BOM CSV，可直接用 Excel 打开。图标与背景图暂不支持导出，可单独备份 IndexedDB。

**Q：为什么心率区间分布全是 Z1？**
A：请先到「设置 → 生理阈值参数」检查最大心率是否配置正确（默认 189），修改后会触发全量重算。

**Q：分段 PB 是怎么算的？**
A：对每段轨迹（含插值）做 O(n) 滑动窗口，找出覆盖目标距离（如 5km）的耗时最短窗口。允许起点不在轨迹首点，只要连续覆盖目标距离即可。

**Q：心率漂移 (HR Drift) 怎么理解？**
A：它衡量同样配速下心率随时间上升的程度。`(后半段 HR/Speed − 前半段 HR/Speed) / 前半段 HR/Speed × 100%`。经验判读：`< 5%` 优秀（有氧基础好），`5–10%` 良好，`> 10%` 提示疲劳或需加强有氧耐力。数值为负代表后段效率反而提升（常见于渐进加速的配速跑）。

**Q：为什么有些指标显示"—"？**
A：Garmin Running Dynamics 字段（垂直步幅比、步长、垂直摆动、触地时间）只有配备相关传感器的 Garmin 设备才能采集，从 FIT 文件导入的活动不包含这些字段，只有从 Garmin 官方 CSV 导入时才会读取。心率漂移需要轨迹含心率与速度数据。

---

## 🧪 验证后端是否正常

浏览器访问：

```text
http://localhost:5000/api/garmin/health
```

正常返回：

```json
{
  "status": "ok",
  "version": "2.0.0-cn",
  "region": "cn",
  "garminconnect": true,
  "garminconnect_version": "0.3.4",
  "curl_cffi": true,
  "server_time": "..."
}
```

如果 `garminconnect` 为 `false`，请安装依赖。
如果 `curl_cffi` 为 `false`，中国区登录可能失败。

---

## 📦 requirements.txt（参考）

```txt
flask>=2.0
flask-cors>=3.0
garminconnect>=0.3.4
curl_cffi>=0.5
ua-generator>=0.1
```

---

## 🧭 版本演进

| 版本 | 主要变化 |
| --- | --- |
| v1.x | 初版：单文件看板、基础 PB、周期详情、FIT/GPX/TCX/XLSX 导入、Garmin 中国区同步 |
| v2.0 | 液态玻璃 UI、9 款主题、IndexedDB 迁移、分段 PB（双指针 + 插值） |
| v2.1 | **P0 修复**：FIT developer fields 跳过、热力图图例跟随主题、当日详情多活动切换、查重按类型分层、ID 生成稳健化、CSV 导出 CRLF |
| v2.2 | **P1 修复**：删除伪科学曲线、引入心率漂移 (HR Drift)、心率-速度比、垂直步幅比改为活动级真实值 |
| v2.3 | **Garmin 官方 CSV 支持**：`Activities.csv` + `activity_*.csv` 分圈文件，宽容数值解析 |
| v2.4 | **全站线性 SVG 图标**：零 Emoji，45+ 图标，`ic(name, size)` + `materializeIcons()` 系统 |
| v2.5 | **图标系统深化 + 总次数详情页**：文字符号图标（`☰ ↑ ↓ → +`）全部换为线性 SVG，新增 `all / menu / plus / arrowRight / arrowDown`；「总次数」详情页与「总用时」按 `mode: time / count` 拆分去重，替换为 5 张次数向图表 |
| v2.6 | **进步可视化**：数据分析页新增 4 张进步图表（耐力趋势散点 + OLS 回归、阶段能力雷达、稳定性 KDE 脊线、心肺效率 EF 面积线），附方法学引言与逐卡讲解 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR。如果你遇到新的坑，也欢迎补充到 README 的踩坑记录中。

---

## 📄 许可

MIT License。仅供个人学习与自用，请遵守 Garmin 服务条款。


## 本次 README 更新要点

### 本轮（v0.0.0.2 - v0.0.1.0）

| 区块 | 主要变化 |
|---|---|
| **功能特性 · 界面** | 「全站线性 SVG 图标」扩充为**图标系统**条目：`ICONS` 注册表 / `ic()` / `data-ic` + `materializeIcons()` 物化 / `.ic-svg` 机制；文字符号图标（`☰ ↑ ↓ → +`）清零，新增 `all / menu / plus / arrowRight / arrowDown` |
| **功能特性 · 数据总览** | 新增「总次数详情页」小节：与总用时按 `mode: time / count` 去重，5 张次数向图表（月度频次柱、星期 × 小时时段热力、12 月玫瑰、类型累计条形、累计增长折线） |
| **功能特性 · 运动科学** | 新增「进步可视化（数据分析页）」小节：4 张进步图表 + 方法学引言与逐卡讲解 |
| **版本演进** | 新增 v2.5（图标深化 + 总次数详情页）、v2.6（进步可视化） |
| **踩坑记录** | 新增 3 条：坑 21 文字符号图标风格不统一、坑 22 总次数与总用时详情页重复、坑 23 进步可视化不能凭空造"进步" |

### 历史（v0.0.0.2 及以前）

| 区块 | 主要变化 |
|---|---|
| **徽章** | 新增 `icons-inline SVG-purple` |
| **项目简介** | 强调"全站线性 SVG 图标" |
| **功能特性 · 界面** | 新增「全站线性 SVG 图标」条目，说明 24×24 / 1.7px / `currentColor` 机制 |
| **功能特性 · 运动科学** | 新增独立小节：心率漂移、心率-速度比、Garmin Running Dynamics 活动级字段 |
| **功能特性 · 多格式导入** | 新增 `.csv`（Garmin 官方导出，含两种格式说明） |
| **快速开始** | 新增「6. 非 Garmin 用户」小节 |
| **踩坑记录** | 新增 4 条：<br>• 坑 17：Garmin 官方 CSV 解析的单位陷阱<br>• 坑 18：活动去重容差不能一刀切<br>• 坑 19：别用随机数伪装运动科学指标<br>• 坑 20：全站 Emoji 图标难以统一风格<br>（原坑 13 分段 PB、坑 14 IndexedDB、坑 15 XLSX、坑 16 FIT 保留，坑 16 补充 developer fields 修复细节） |
| **FAQ** | 新增 4 条：CSV 格式区别、心率漂移判读、Running Dynamics 字段来源、"为什么有些指标显示 —" |
| **版本演进** | 新增表格，追溯 v1.x → v2.4 的关键变化 |
