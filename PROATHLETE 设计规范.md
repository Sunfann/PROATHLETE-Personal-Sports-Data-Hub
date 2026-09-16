# PROATHLETE 设计规范

> 本文档定义了 PROATHLETE 项目的统一视觉语言。所有新页面、新组件必须严格遵守本规范，以保证全站风格一致。
> 所有值均为 CSS 变量，已内置于 `:root`，直接引用即可，不要硬编码。

---

## 目录

1. 配色系统
2. 字体系统
3. 间距系统
4. 圆角系统
5. 组件样式
6. 动效系统
7. 玻璃质感
8. 响应式断点
9. 编码规范速查

---

## 1. 配色系统

### 1.1 背景色

| 变量 | 色值 | 用途 |
| --- | --- | --- |
| `--bg` | `#04060a` | 页面最底层背景（深空主题默认值） |
| `--bg-scrim` | `rgba(4,6,10,.62)` | 背景图上的遮罩层 |

各主题的 `--bg` 不同（例如 Latte 为 `#eff1f5`），但语义一致：**页面最底层、不透明的底色**。

### 1.2 文字色（4 级层次）

| 变量 | 色值 | 用途 |
| --- | --- | --- |
| `--t1` | `#fff` | **一级文字**：标题、KPI 数字、主要信息 |
| `--t2` | `rgba(255,255,255,.72)` | **二级文字**：副标题、卡片标签、正文内容 |
| `--t3` | `rgba(255,255,255,.46)` | **三级文字**：说明文字、单位、辅助元信息 |
| `--t4` | `rgba(255,255,255,.28)` | **四级文字**：占位符、禁用态、极弱提示 |

> ⚠️ 使用原则：**同一区域最多出现 3 级文字色**，避免层次混乱。

### 1.3 主色与辅助色

| 变量 | 色值 | 语义 |
| --- | --- | --- |
| `--blue` | `#0A84FF` | **主色**：导航选中、按钮、链接、强调 |
| `--green` | `#30D158` | 成功、步行、正向趋势 |
| `--orange` | `#FF9F0A` | 跑步、警告、配速 |
| `--red` | `#FF453A` | 错误、危险、心率、下降趋势 |
| `--purple` | `#BF5AF2` | 力量、时长、辅助强调 |
| `--teal` | `#64D2FF` | 游泳、速度 |
| `--pink` | `#FF375F` | 心率区间高亮 |
| `--indigo` | `#5E5CE6` | 备用强调色 |
| `--yellow` | `#FFD60A` | 徒步 |
| `--gold` | `#FFD700` | **PB/成就专用**（唯一允许的金色语义） |
| `--mint` | `#63E6E2` | 备用清新色 |

**运动类型映射（固定不变）**：

| 运动 | 图标 | 色值 |
| --- | --- | --- |
| 跑步 | 🏃 | `--orange` `#FF9F0A` |
| 骑行 | 🚴 | `--blue` `#0A84FF` |
| 游泳 | 🏊 | `--teal` `#64D2FF` |
| 力量 | 🏋️ | `--purple` `#BF5AF2` |
| 步行 | 🚶 | `--green` `#30D158` |
| 徒步 | 🥾 | `--yellow` `#FFD60A` |
| 其他 | 📌 | `#8E8E93`（中性灰） |

### 1.4 表面色（Surface）

用于卡片内部区分层次，采用**半透明白**叠加在玻璃上：

| 变量 | 色值 | 用途 |
| --- | --- | --- |
| `--surface-a` | `rgba(255,255,255,.028)` | 最轻：卡片内嵌块、图标背景 |
| `--surface-b` | `rgba(255,255,255,.05)` | 轻：hover 态行、次级容器 |
| `--surface-c` | `rgba(255,255,255,.085)` | 中：按钮 ghost 态、标签背景 |
| `--surface-d` | `rgba(255,255,255,.14)` | 重：激活指示器、进度条底 |

### 1.5 分隔线

| 变量 | 色值 | 用途 |
| --- | --- | --- |
| `--hairline` | `rgba(255,255,255,.065)` | 常规分隔线（1px） |
| `--hairline-strong` | `rgba(255,255,255,.14)` | 强调分隔线、输入框边框 |

### 1.6 语义化颜色用法（透明叠加）

强调色一律用 `color-mix` 生成半透明背景，**禁止硬编码 RGBA**：

```css
/* ✅ 正确 */
background: color-mix(in srgb, var(--blue) 18%, transparent);   /* 浅色背景 */
border:     1px solid color-mix(in srgb, var(--blue) 30%, transparent);

/* ❌ 错误 */
background: rgba(10,132,255,.18);
```

标准叠加档位：

| 强度 | 百分比 | 场景 |
| --- | --- | --- |
| 极浅 | 8% | 卡片填充底色 |
| 浅 | 14–18% | 标签背景、徽章背景 |
| 中 | 22–30% | 边框、hover 强调 |
| 深 | 40%+ | 阴影光晕、聚焦环 |

---

## 2. 字体系统

### 2.1 字体族

```css
--font: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text',
        'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif;

--mono: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;
```

- **正文/UI**：`var(--font)`，优先苹果系统字体，中文回退 PingFang SC。
- **数字/代码**：`var(--mono)`，配合 `font-variant-numeric: tabular-nums;` 让数字等宽对齐。

### 2.2 全局字重字距

```css
body {
  line-height: 1.5;
  letter-spacing: -0.01em;   /* 全局轻微收紧 */
  -webkit-font-smoothing: antialiased;
}
```

### 2.3 字号规范（严格遵循）

| 层级 | 类名 | 字号 | 字重 | 行高 | 字距 | 用途 |
| --- | --- | --- | --- | --- | --- | --- |
| **H1 页面标题** | `.header-title`（大） | 24px | 700 | 1.3 | -0.3px | 各视图页头主标题 |
| **H2 区块标题** | `.header-title` | 19px | 700 | 1.3 | -0.3px | 页头标题、详情页标题 |
| **H3 卡片标题** | `.group-title` | 16–17px | 700 | 1.4 | -0.2px | 分组标题、弹窗小标题 |
| **H4 卡片标签** | `.card-label` | 13px | 600 | 1.5 | 0 | 卡片标题文字 |
| **正文** | — | 14px | 400–600 | 1.5 | 0 | 活动名称、行内容 |
| **辅助正文** | `.sub` | 12px | 400 | 1.6 | 0 | 卡片说明、副标题 |
| **元信息** | `.r-meta` | 11px | 500 | 1.5 | 0 | 时间、单位、次要信息 |
| **微小标签** | `.nav-title` | 10px | 700 | 1.4 | 1.1px | 大写英文导航分组 |

### 2.4 数字字体规范

| 场景 | 类名 | 字号 | 字重 | 字距 | 备注 |
| --- | --- | --- | --- | --- | --- |
| **超大数字（KPI）** | `.kpi` | 40px | 800 | -1.6px | 总览页核心数字 |
| **大数字** | `.kpi-sm` | 26px | 800 | -1px | 次级卡片数字 |
| **中数字** | `.stat-v` | 17px | 700 | -0.3px | 统计项数值 |
| **小数字** | `.dc-metric .v` | 19px | 800 | -0.6px | 详情页指标 |
| **微型数字** | `.dc-act-stat .v` | 13px | 700 | 0 | 活动列表数值 |

**数字统一规则**：

```css
font-variant-numeric: tabular-nums;   /* 数字等宽，对齐更稳 */
```

### 2.5 单位字号

数值后面的单位（km、bpm、kcal 等）**永远比数字小 2–3 级**：

```css
.kpi .unit {
  font-size: 15px;              /* 对比 kpi 的 40px */
  font-weight: 600;
  color: var(--t2);             /* 永远用二级色 */
  margin-left: 3px;
}
```

### 2.6 字重使用原则

| 字重 | 用途 |
| --- | --- |
| 400 | 纯正文（极少用） |
| 500 | 辅助信息、元数据 |
| **600** | **默认 UI 字重**（正文、标签、导航项） |
| **650–700** | 标题、按钮、强调 |
| **800** | 仅用于数字（KPI、统计值） |

> ⚠️ 全局**不使用 900**，最大字重限制在 800。

---

## 3. 间距系统

采用 **4px 基准的 8 档间距**，所有内外边距必须从此表选取，**禁止使用 5px、7px、13px 等非规范值**。

| 变量 | 值 | 语义 | 典型用途 |
| --- | --- | --- | --- |
| `--s1` | 4px | XXXS | 图标与文字、紧凑间隙 |
| `--s2` | 8px | XXS | 按钮内图标与文字、标签内间隙 |
| `--s3` | 12px | XS | 卡片内小间隙、列表行内间距 |
| `--s4` | 16px | S | 卡片内边距、行与行间距 |
| `--s5` | 20px | M | **卡片内边距（默认）**、栅格间距 |
| `--s6` | 24px | L | **主内容区边距（默认）**、页头内边距 |
| `--s8` | 32px | XL | 大区块分隔、空状态内边距 |

### 3.1 布局典型间距

```css
/* 页面主内容区 */
.main { padding: var(--s6); }                    /* 24px */

/* 卡片 */
.card { padding: var(--s5); gap: var(--s3); }    /* 20px 内边距，12px 内部间距 */

/* 栅格 */
.grid { gap: var(--s5); }                        /* 20px */

/* 列表行 */
.row { padding: 11px var(--s3); gap: var(--s4); }/* 上下 11px，左右 12px，列间 16px */

/* 按钮 */
.btn { padding: 10px 18px; gap: 7px; }
.btn-sm { padding: 7px 13px; }

/* 分组 */
.group { margin-bottom: var(--s8); }             /* 32px */
```

### 3.2 内边距层级原则

> **容器越大，内边距越大。**

- 页面级容器：`--s6`（24px）
- 卡片级容器：`--s5`（20px）
- 内嵌块（metric-tile、row）：`--s3 ~ --s4`（12–16px）
- 标签、按钮：`--s2`（8px）

---

## 4. 圆角系统

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `--r-xs` | 8px | 极小控件、热力图格 |
| `--r-sm` | 12px | 小卡片、列表图标块 |
| `--r-md` | 16px | 导航项、设置行、内嵌块、标准按钮 |
| `--r-lg` | 20px | 中等卡片 |
| `--r-xl` | 24px | **主卡片（默认）** |
| `--r-2xl` | 30px | 弹窗、拖拽区、详情大卡片 |

### 4.1 组件圆角对照

| 组件 | 圆角 |
| --- | --- |
| 主卡片 | `--r-xl` (24px) |
| 按钮（默认） | 14px |
| 按钮（小） | 11px |
| 圆形按钮 | 50% |
| 导航项 | `--r-md` (16px) |
| 标签 / 徽章 | 20px（胶囊） |
| 输入框 | 10px |
| 图标方块 | `--r-sm` (12px) |
| 进度条 | 高的一半 |

---

## 5. 组件样式

### 5.1 卡片（Card）

```css
.card {
  border-radius: var(--r-xl);           /* 24px */
  padding: var(--s5);                    /* 20px */
  display: flex;
  flex-direction: column;
  gap: var(--s3);                        /* 12px */
  min-height: 168px;
  position: relative;
  overflow: hidden;
}

/* 可点击卡片 */
.card.clickable:hover {
  transform: translateY(-2px);           /* 轻微上浮 */
  border-color: var(--hairline-strong);  /* 边框微微提亮 */
}
```

**卡片结构（必须遵守的层次）**：

```text
┌──────────────────────────────────┐
│ [icon] 标签文字        [操作入口] │  ← card-head，高 z-index
│                                  │
│  KPI 大数字                      │  ← 主信息，40px / 800 字重
│                                  │
│  辅助说明 / 统计行               │  ← sub / stat-row
└──────────────────────────────────┘
```

**卡片图标（可选）**：

- 使用 `--card-accent`（每张卡片的专属色）填充 `fig-mask`。
- 通过 `mask-image: url(图标)` 渲染，**默认透明度 0.10，hover 时 0.24**。
- 图标容器尺寸：卡片宽高的 66%，上限 280×280。

### 5.2 按钮（Button）

#### 按钮尺寸

| 类名 | 高度 | 内边距 | 字号 | 圆角 |
| --- | --- | --- | --- | --- |
| `.btn` | ≈40px | 10px 18px | 14px | 14px |
| `.btn-sm` | ≈32px | 7px 13px | 13px | 11px |
| `.btn-icon` | 40×40 | 0 | — | 50% |

#### 按钮变体

**主按钮（Primary）** — 用于页面主要操作，每屏不超过 2 个

```css
.btn-primary {
  background: linear-gradient(180deg,
              color-mix(in srgb, var(--blue) 88%, #fff 12%),
              var(--blue));
  color: #fff;
  box-shadow: 0 4px 16px color-mix(in srgb, var(--blue) 40%, transparent),
              inset 0 1px 0 rgba(255,255,255,.28);
}
```

**次按钮（Ghost）** — 默认按钮，用于次要操作

```css
.btn-ghost {
  background: var(--surface-c);
  color: var(--t1);
  border: 1px solid var(--hairline-strong);
  backdrop-filter: blur(12px);
}
```

**危险按钮（Danger）** — 仅用于删除、清空

```css
.btn-danger {
  background: color-mix(in srgb, var(--red) 16%, transparent);
  color: var(--red);
  border: 1px solid color-mix(in srgb, var(--red) 30%, transparent);
}
```

**按钮交互**：

```css
.btn:active { transform: scale(.96); }   /* 按下缩放到 96% */
.btn { transition: transform .18s var(--spring), ...; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
```

#### 按钮内布局

```css
.btn { display: inline-flex; align-items: center; gap: 7px; }
/* 图标与文字固定 7px 间距，图标字号通常 1.1em */
```

### 5.3 侧边导航（Sidebar）

**容器**：

```css
.sidebar {
  width: 68px;                            /* 折叠态 */
  padding: var(--s5) var(--s3);           /* 20px 12px */
  border-right: 1px solid var(--hairline);
  display: flex; flex-direction: column;
  gap: var(--s5);                         /* 20px */
}
.app.sb-expanded { --sb-w: 248px; }       /* 悬停展开到 248px */
```

**导航项**：

```css
.nav-item {
  min-height: 44px;                       /* 触控友好 */
  padding: 10px 12px;
  border-radius: var(--r-md);             /* 16px */
  gap: var(--s3);                         /* 图标与文字 12px */
  font-size: 14px;
  font-weight: 600;
  color: var(--t2);
  transition: color .2s var(--ease);
}
.nav-item:hover { color: var(--t1); }
.nav-item.active { color: var(--t1); }
```

**激活指示条**（左侧 3px 竖条 + 光晕）：

```css
.nav-item.active::before {
  content: '';
  position: absolute;
  left: -10px; top: 50%; transform: translateY(-50%);
  width: 3px; height: 18px;
  background: var(--blue);
  border-radius: 0 3px 3px 0;
  box-shadow: 0 0 10px var(--blue);
}
```

**液态指示器**（hover 时跟随鼠标的滑动块）：

```css
.nav .liquid-indicator {
  background: var(--surface-d);
  border-radius: var(--r-md);
  box-shadow: inset 0 1px 0 var(--glass-inner);
  transition: transform .42s cubic-bezier(.34,1.42,.64,1),
              width .42s cubic-bezier(.34,1.42,.64,1),
              height .42s cubic-bezier(.34,1.42,.64,1),
              opacity .25s var(--ease);
}
```

### 5.4 标签（Tag / Badge）

```css
.tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 20px;                    /* 胶囊 */
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

/* 语义变体 */
.tag.green  { background: color-mix(in srgb, var(--green)  18%, transparent); color: var(--green); }
.tag.blue   { background: color-mix(in srgb, var(--blue)   18%, transparent); color: var(--blue); }
.tag.orange { background: color-mix(in srgb, var(--orange) 18%, transparent); color: var(--orange); }
.tag.red    { background: color-mix(in srgb, var(--red)    18%, transparent); color: var(--red); }
.tag.gold   { background: color-mix(in srgb, var(--gold)   18%, transparent); color: var(--gold); }
.tag.gray   { background: var(--surface-c); color: var(--t2); }
```

### 5.5 Tabs（分段控制器）

```css
.tabs {
  display: inline-flex;
  gap: 3px;                               /* tab 间 3px 缝隙 */
  padding: 3px;                           /* 内边距 3px */
  border-radius: 14px;                    /* 外层圆角 */
  background: var(--surface-b);
  border: 1px solid var(--hairline);
  position: relative;
  isolation: isolate;                     /* 让液态指示器正常层叠 */
}

.tabs .tab {
  padding: 7px 16px;
  border-radius: 11px;                    /* 内层圆角 = 外层 - 内边距 */
  font-size: 13px;
  font-weight: 600;
  color: var(--t2);
  cursor: pointer;
  background: transparent !important;     /* 高亮由液态指示器承载 */
  position: relative;
  z-index: 1;
}

.tabs .tab.active { color: var(--t1); }
```

> **圆角公式**：内层圆角 = 外层圆角 − 内边距 → `14 - 3 = 11px`

### 5.6 输入框（Input）

```css
.garmin-input {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid var(--hairline-strong);
  background: var(--surface-b);
  color: var(--t1);
  font-size: 13px;
  font-family: var(--font);
  outline: none;
}
.garmin-input:focus {
  border-color: var(--blue);
  background: var(--surface-c);
}
```

### 5.7 设置行（Setting Row）

```css
.setting {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--s5);                         /* 20px */
  padding: var(--s4) 0;                   /* 16px 上下 */
  border-bottom: 1px solid var(--hairline);
}
.setting:last-child { border-bottom: none; }   /* 最后一行去线 */

.setting-label { font-size: 14px; font-weight: 600; }
.setting-desc  { font-size: 11.5px; color: var(--t3); margin-top: 2px; }
.control       { min-width: 290px; flex-shrink: 0; }   /* 右侧控件固定宽度 */
```

### 5.8 列表行（List Row）

```css
.row {
  display: grid;
  align-items: center;
  gap: var(--s4);                         /* 16px */
  padding: 11px var(--s3);                /* 上下 11px，左右 12px */
  border-radius: var(--r-md);             /* 16px */
  cursor: pointer;
  transition: background .18s var(--ease);
}
.row:hover { background: var(--surface-b); }   /* 悬浮浅色底 */
```

### 5.9 图标容器

```css
.r-ico {
  width: 38px; height: 38px;
  border-radius: var(--r-sm);             /* 12px */
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  flex: 0 0 38px;
}
/* 背景用对应语义色的 20% 叠加 */
.r-ico.run   { background: color-mix(in srgb, var(--orange) 20%, transparent); }
```

### 5.10 空状态（Empty State）

```css
.empty {
  padding: var(--s8) var(--s5);           /* 32px 20px */
  text-align: center;
  color: var(--t3);
  display: flex; flex-direction: column;
  align-items: center;
  gap: var(--s3);                         /* 12px */
}
.empty .e-ico { font-size: 38px; opacity: .5; }   /* 大图标，50% 透明 */
.empty .e-t   { font-size: 15px; font-weight: 600; color: var(--t2); }
.empty .e-d   { font-size: 12.5px; max-width: 340px; line-height: 1.65; }
```

### 5.11 弹窗（Modal）

```css
.modal {
  background: var(--modal-scrim);         /* rgba(0,0,0,.62) */
  backdrop-filter: blur(8px);
  padding: var(--s6);                     /* 24px 安全边距 */
}
.modal-box {
  width: min(900px, 100%);
  max-height: 90vh;
  border-radius: var(--r-2xl);            /* 30px */
  padding: var(--s6);                     /* 24px */
  overflow-y: auto;
  gap: var(--s5);                         /* 20px */
}
```

### 5.12 Toast 提示

```css
.toast {
  padding: 13px 18px;
  border-radius: var(--r-md);             /* 16px */
  min-width: 250px;
  max-width: 380px;
  font-size: 13.5px;
  font-weight: 600;
  /* 从右侧滑入，spring 动画 */
}
@keyframes tIn { from { opacity: 0; transform: translateX(50px) scale(.94); } }
```

---

## 6. 动效系统

### 6.1 缓动曲线

```css
--ease:   cubic-bezier(.22, 1, .36, 1);      /* 常规：快进慢出，柔和自然 */
--spring: cubic-bezier(.34, 1.4, .64, 1);    /* 弹性：用于按钮、指示器 */
```

**使用场景**：

| 曲线 | 场景 |
| --- | --- |
| `--ease` | 颜色、背景、透明度渐变，边框变化 |
| `--spring` | 按钮按下、液态指示器、弹性反馈 |

### 6.2 标准过渡时长

| 时长 | 场景 |
| --- | --- |
| **.15s–.2s** | 颜色、hover 反馈 |
| **.25s** | 背景、边框、阴影 |
| **.4s** | 视图切换、弹窗淡入 |
| **.6s–.9s** | 卡片位移、光效扫过 |

```css
/* 颜色/背景类 */
transition: background-color .25s var(--ease), color .25s var(--ease);

/* 位移类 */
transition: transform .62s cubic-bezier(.22,1,.36,1), opacity .5s var(--ease);
```

### 6.3 视图进入动画

```css
@keyframes viewIn {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
.view.active { animation: viewIn .45s var(--ease); }
```

---

## 7. 玻璃质感

### 7.1 `.glass` 类（全局统一）

**所有**需要玻璃质感的容器都必须加 `.glass` 类，**不要重复定义**：

```css
.glass {
  background-color: var(--glass-base);
  background-image: linear-gradient(155deg,
                     var(--glass-tint) 0%,
                     rgba(255,255,255,0) 58%);
  backdrop-filter: blur(var(--glass-blur))
                   saturate(var(--glass-sat))
                   brightness(var(--glass-bright));
  border: 1px solid var(--glass-border);
  box-shadow: 0 8px 32px rgba(0,0,0,var(--glass-shadow-a)),
              0 1px 0 var(--glass-inner),
              inset 0 1px 0 var(--glass-inner);
}
```

### 7.2 运行时参数（用户可调）

| 变量 | 默认值 | 范围 | 含义 |
| --- | --- | --- | --- |
| `--glass-blur` | 40px | 0–80px | 模糊强度 |
| `--glass-sat` | 170% | 100–280% | 饱和度 |
| `--glass-bright` | 1.06 | 固定 | 亮度 |
| `--glass-shadow-a` | 0.45 | 动态 | 阴影透明度 |

### 7.3 光效扫过（Shine）

用于卡片 hover 时的扫光效果，**按需添加**：

```html
<div class="card glass shine"> ... </div>
```

```css
.glass.shine::after {
  content: '';
  position: absolute;
  top: 0; left: -60%;
  width: 45%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.07), transparent);
  transform: skewX(-22deg);
  transition: left .9s var(--ease);
}
.glass.shine:hover::after { left: 140%; }
```

### 7.4 玻璃层次规则

| 层次 | 用途 | 透明度 |
| --- | --- | --- |
| **不透明** | 弹窗背景、设置面板 | 100% |
| **半透明玻璃** | 主卡片、侧边栏、弹窗 | 用户可调（默认 92%） |
| **微弱玻璃** | 内嵌块、二级卡片 | 用户可调 |

---

## 8. 响应式断点

### 8.1 断点定义

| 断点 | 宽度 | 主要变化 |
| --- | --- | --- |
| **Desktop** | ≥ 1101px | 4 列栅格，展开侧边栏 |
| **Tablet** | 821–1100px | 卡片内边距缩小，3 列栅格 |
| **Mobile** | ≤ 820px | 2 列栅格，汉堡菜单，垂直堆叠 |

### 8.2 栅格响应

```css
/* 桌面：4 列 */
.grid { grid-template-columns: repeat(4, 1fr); gap: var(--s5); }

/* 平板：3 列（部分区块） */
@media (max-width: 1100px) { ... }

/* 移动：2 列，跨列折叠 */
@media (max-width: 820px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
  .col-2 { grid-column: span 2; }
  .col-4 { grid-column: span 2; }
  .main  { padding: var(--s4); }         /* 24px → 16px */
}
```

### 8.3 移动端关键调整

- `.main` 内边距：`--s6` → `--s4`（24px → 16px）
- `.setting` 从水平布局改为垂直堆叠
- `.control`（右侧控件）宽度 100%
- 侧边栏折叠为汉堡按钮（`.btn-icon#menuToggle`）
- 大数字自动降一级（`.kpi` 40px → 移动端可保持，但 `.kpi-sm` 26px → 18px）

---

## 9. 编码规范速查

### 9.1 命名约定

| 类型 | 前缀 | 示例 |
| --- | --- | --- |
| 布局容器 | 语义名 | `.main`、`.sidebar`、`.header` |
| 卡片/块 | `.card-*` | `.card-head`、`.card-label` |
| 按钮 | `.btn-*` | `.btn-primary`、`.btn-sm` |
| 标签 | `.tag-*` | `.tag-blue` |
| 状态 | 形容词 | `.active`、`.open`、`.has-image` |
| 变体 | 连字符 | `.pb-tile.empty`、`.seg-pb-card.empty` |

### 9.2 必须遵守的规则

- ✅ **颜色必须用 CSS 变量**，禁止硬编码十六进制或 RGB
- ✅ **间距必须用 `--s1 ~ --s8`**，禁止 5px、13px、17px 等
- ✅ **圆角必须用 `--r-xs ~ --r-2xl`**，禁止任意值
- ✅ **动效缓动必须用 `--ease` 或 `--spring`**
- ✅ **字体族必须用 `--font` 或 `--mono`**
- ✅ **卡片默认圆角 `--r-xl`（24px），内边距 `--s5`（20px）**
- ✅ **玻璃容器统一加 `.glass` 类，不重复定义**
- ✅ **数字后面跟单位，单位用二级文字色 + 更小字号**
- ✅ **语义色背景用 `color-mix` 生成半透明**
- ❌ 禁止 `z-index: 9999` 之外的魔数（除 toast、tooltip 层）
- ❌ 禁止使用 `!important`（除抵消内联样式的 `.tabs .tab`）

### 9.3 组件复用清单

可直接复用的现成组件类：

```text
.glass              玻璃容器
.glass.shine        带扫光的玻璃卡片
.card.glass         标准玻璃卡片
.btn .btn-primary   主按钮
.btn .btn-ghost     次按钮
.btn .btn-danger    危险按钮
.btn .btn-sm        小按钮
.btn .btn-icon      圆形图标按钮
.tag .tag-{color}   语义标签
.tabs + .tab        分段控制器（需 initLiquidTabs）
.row                列表行
.empty              空状态
.metric-tile        指标小块
.pb-tile            PB 徽章块
.seg-pb-card        分段 PB 卡片
```

### 9.4 新增页面检查清单

完成新页面后，逐项核对：

- □  所有颜色来自 CSS 变量（无硬编码）
- □  所有间距来自 `--s1 ~ --s8`
- □  所有圆角来自 `--r-xs ~ --r-2xl`
- □  卡片使用 `.glass` + `.card` 基础类
- □  标题字号为 24px（H1）或 19px（H2）
- □  正文默认 14px / 600 字重
- □  辅助文字使用 `--t3` 或 `--t4`
- □  数字使用 `tabular-nums` 等宽
- □  按钮包含 `:active { transform: scale(.96); }`
- □  交互元素有 hover 状态
- □  移动端（≤820px）布局已测试
- □  至少在一个深色主题 + Latte 浅色主题下视觉正常
- □  键盘可访问（Enter/Space 触发按钮）

---

## 📎 附录：CSS 变量完整清单

```css
:root {
  /* === 颜色 === */
  --blue: #0A84FF;  --green: #30D158;   --orange: #FF9F0A;
  --red: #FF453A;   --purple: #BF5AF2;  --teal: #64D2FF;
  --pink: #FF375F;  --indigo: #5E5CE6;  --yellow: #FFD60A;
  --mint: #63E6E2;  --gold: #FFD700;

  /* === 文字 === */
  --t1: #fff;
  --t2: rgba(255,255,255,.72);
  --t3: rgba(255,255,255,.46);
  --t4: rgba(255,255,255,.28);

  /* === 表面 === */
  --surface-a: rgba(255,255,255,.028);
  --surface-b: rgba(255,255,255,.05);
  --surface-c: rgba(255,255,255,.085);
  --surface-d: rgba(255,255,255,.14);

  /* === 分隔线 === */
  --hairline:        rgba(255,255,255,.065);
  --hairline-strong: rgba(255,255,255,.14);

  /* === 背景 === */
  --bg: #04060a;
  --bg-scrim: rgba(4,6,10,.62);
  --modal-scrim: rgba(0,0,0,.62);

  /* === 间距 === */
  --s1: 4px;  --s2: 8px;  --s3: 12px;  --s4: 16px;
  --s5: 20px; --s6: 24px; --s8: 32px;

  /* === 圆角 === */
  --r-xs: 8px;  --r-sm: 12px; --r-md: 16px;
  --r-lg: 20px; --r-xl: 24px; --r-2xl: 30px;

  /* === 字体 === */
  --font: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
          'PingFang SC', 'Microsoft YaHei', sans-serif;
  --mono: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;

  /* === 动效 === */
  --ease:   cubic-bezier(.22, 1, .36, 1);
  --spring: cubic-bezier(.34, 1.4, .64, 1);

  /* === 玻璃 === */
  --glass-blur: 40px;
  --glass-sat: 170%;
  --glass-bright: 1.06;
  --glass-border: rgba(255,255,255,.16);
  --glass-inner:  rgba(255,255,255,.10);
  --glass-shadow-a: .45;
}
```

---

**版本**：v1.0 · 对应 PROATHLETE 当前代码库
**维护原则**：本规范随代码演进，任何新增视觉约定必须同步更新此文档，并追加到相应章节。