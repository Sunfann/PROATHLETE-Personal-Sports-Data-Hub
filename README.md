# PROATHLETE · 个人多生态运动数据中枢

> 一个纯前端 + 本地代理后端的个人运动数据看板。支持 Garmin 中国区一键同步，多主题液态玻璃 UI，FIT / GPX / TCX / XLSX 多格式导入，以及完整的运动科学分析。

[https://img.shields.io/badge/status-active-brightgreen](https://img.shields.io/badge/status-active-brightgreen)
[https://img.shields.io/badge/license-MIT-blue](https://img.shields.io/badge/license-MIT-blue)
[https://img.shields.io/badge/python-3.9%252B-blue](https://img.shields.io/badge/python-3.9%252B-blue)

---

## 📖 项目简介

PROATHLETE 是一个自托管的运动数据中枢，包含：

- **前端**：单文件 `index.html`，纯静态，无需构建。液态玻璃设计，9 款精美主题，支持拖拽导入、数据可视化、ACWR 分析、心率区间等。
- **后端**：`garmin_server.py`，一个本地 Flask 服务，作为 Garmin Connect 的代理，解决纯前端无法直连 Garmin 的问题。特别适配 **Garmin 中国区（[garmin.cn](https://garmin.cn)）** 账号。

整个项目无需数据库，数据保存在浏览器 `localStorage`，后端仅负责同步中转，不存储任何账号信息。

---

## ✨ 功能特性

### 前端

- 🎨 **9 款主题**：Dracula、Nord、Mocha、Latte、Rosé Pine、Tokyo Night、Gruvbox、One Dark、深空。全部适配液态玻璃，切换平滑。
- 💎 **液态玻璃 UI**：可调节透明度、模糊强度、饱和度，类似 Apple 的毛玻璃质感。
- 📊 **总览卡片**：总用时、总次数、跑步/骑行/步行/徒步分类统计，当日数据高亮。
- 📈 **周期详情**：点击卡片进入周/月/年/全部周期对比，含图表、心率区间、星期分布、最近活动。
- 🗺️ **轨迹与图表**：单次活动详情弹窗，显示 GPS 轨迹、海拔、配速、心率、步频、功率。
- 📁 **多格式导入**：支持 `.fit`、`.gpx`、`.tcx`、`.zip`、`.xlsx`（Keep/悦跑圈等导出表），自动去重。
- 🔄 **Garmin 同步**：配置账号后一键拉取新活动，进度条实时显示，自动解析 FIT。
- 📤 **CSV 导出**：一键导出全部活动数据。
- ✨ **演示数据**：内置生成器，点击即可体验完整分析功能。

### 后端

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
```

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- 现代浏览器（Chrome / Edge / Safari / Firefox）
- Garmin 中国区账号（[garmin.cn](https://garmin.cn)）

### 2. 安装后端依赖

```bash
pip install flask flask-cors
pip install --upgrade "garminconnect>=0.3.4" curl_cffi ua-generator
```

> ⚠️ **版本非常重要**：`garminconnect` 必须 ≥ 0.3.4，否则中国区登录会失败。`curl_cffi` 和 `ua-generator` 用于绕过 Cloudflare，中国区必需。

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
   - **密码**：你的 [garmin.cn](https://garmin.cn) 密码
   - **后端地址**：`http://localhost:5000`
   - **首次拉取天数**：建议 30
3. 点击「保存配置」，然后「测试连接」。
4. 连接正常后，点击「同步新活动」，等待进度条完成。

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

## ❓ 常见问题 FAQ

**Q：必须用中国区账号吗？**
A：当前后端强制 `is_cn=True`，适配 [garmin.cn](https://garmin.cn)。如果你用国际版，可以改为 `is_cn=False`。

**Q：同步的数据存在哪里？**
A：前端 `localStorage`，后端不存储。清除浏览器数据会丢失，建议定期导出 CSV。

**Q：支持哪些 Garmin 设备？**
A：只要活动能同步到 Garmin Connect，就能拉取 FIT 文件，与设备型号无关。

**Q：为什么同步这么慢？**
A：每个活动需要单独下载 FIT，且代码加了 0.35 秒延时避免限流。活动多时耐心等待。

**Q：可以同时开多个前端吗？**
A：可以，但 `localStorage` 是按浏览器隔离的，数据不共享。

**Q：后端会保存我的 Garmin 密码吗？**
A：不会。密码仅用于当次登录，保存在前端 `localStorage` 的配置中，后端内存中用完即弃。

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

## 🤝 贡献

欢迎提交 Issue 和 PR。如果你遇到新的坑，也欢迎补充到 README 的踩坑记录中。

---

## 📄 许可

MIT License。仅供个人学习与自用，请遵守 Garmin 服务条款。