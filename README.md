# owenlearining

面向上海中考（27 届）自用的「初中全学科学习中心 + 升学规划」静态站点。
一页全景看板 + 各学科独立学习页，纯手写 HTML，从仓库根目录部署到 Vercel。

> **⚠️ 本仓库为 Public。**
> 站点内容、提交记录、`supabase-config.js` 均对外可见。**不要在此仓库存放或提交任何个人信息**
> （真实姓名、学校、证件号、健康状况、联系方式等）。新增页面前先确认这一点。

---

## 本地预览

```bash
python3 -m http.server 8899 --bind 127.0.0.1
# 浏览器打开 http://127.0.0.1:8899/index.html
```

**必须用 HTTP 起服，不要直接双击打开（`file://`）**：部分页面用相对路径加载
`supabase-config.js` 等资源，`file://` 下与线上行为不一致。
（例外：`tests/` 下的验证脚本刻意走 `file://`，见「测试」。）

---

## 首页卡片地图

`index.html` 是总入口，标题「极简科目全景看板 **V16**」，**四大板块 / 19 张卡片**。

### 一、核心学科与中考复习（10）

| 卡片 | 入口 |
|---|---|
| 初中语文 | `chinese/chinese.html` |
| 初中数学 | `math/math.html` |
| 初中英语 V38 | `english/english-hub.html` |
| 初中物理 V4 | `physics/physics-hub-V4.html` |
| 初中化学 V4 | `chemistry/chemistry-V4.html` |
| 初中道法 V6 | `daofa/daofa-V6.html` |
| 初中体育 V2 | `pe/pe-guide-V2.html` |
| 初中生物 | `biology/biology.html` |
| 初中历史 | `history/history.html` |
| 跨学科研究 V2 | `interdisciplinary/interdisciplinary-V2.html` |

语文卡片另有快捷入口：`chinese/chinese-repair-plan-V1.html`（8 个月补习计划）、
`chinese/recitation-drill-V1.html`（86 篇默写自测）。

### 二、升学规划与专项拓展（6）

| 卡片 | 入口 |
|---|---|
| 中本贯通 (3+4) V6 | `zhongben/zhongben-guide-V6.html` |
| 全轨升学指南 V14 | `zhongkao/zhongkao-guide-V14.html` |
| 上海国际高中全景 V1 | `guoji/shanghai-international-highschools-V1.html` |
| 上海中考真题库 V2 | `zhongkao/shanghai-zhongkao-papers-V2.html` |
| A-Level 教程教辅 V2 | `alevel/alevel-guide-V2.html` |
| 留学生避坑全景库 V3 | `red-study/red-study-abroad-V3.html` |

本板块下方有一组「真题直达」胶囊入口（`.zsl-wrap`），指向真题库页内的科目锚点 `#s-<科目>`。

### 三、家庭日程打卡与费用核算中心（2）

| 卡片 | 入口 |
|---|---|
| 学科补课费用结算中心 V11 | `tracker/unified-tracker-V11.html` |
| 每月打针与复诊打卡中心 V11 | `tracker/unified-tracker-V11.html` |

两张卡片指向同一页（该页内含两个标签视图）。

### 四、家庭财富与资产规划中心（1）

| 卡片 | 入口 |
|---|---|
| 家庭财富传承 V11 | `insurance/insurance-V11.html` |

---

## 目录结构

| 目录 | 内容 | HTML | 体量 |
|---|---|---:|---:|
| `index.html` / `index-V3.css` | 首页看板与其样式表 | 1 | — |
| `chinese/` | 语文：教材、默写、名著（儒林外史等） | 37 | 289M |
| `english/` | 英语：单词星球、菜单等 | 21 | 324M |
| `physics/` | 物理 | 10 | 245M |
| `chemistry/` | 化学 | 8 | 88M |
| `daofa/` | 道德与法治 | 5 | 49M |
| `history/` | 历史 | 3 | 6.3M |
| `biology/` | 生物 | 2 | 72M |
| `math/` | 数学 | 3 | 102M |
| `interdisciplinary/` | 跨学科案例分析 | 2 | 8.3M |
| `pe/` `health/` | 体育、健康 | 各 1 | 小 |
| `zhongkao/` `zhongben/` `guoji/` `alevel/` `red-study/` | 升学规划各专题 | 11 | 小 |
| `tracker/` | 费用结算 / 打卡（localStorage + Supabase） | 9 | 1.5M |
| `insurance/` | 家庭财富与资产 | 2 | 5.6M |
| `archive/` | 历史版本堆积（`history_versions/`、`tracker-legacy/`、english-hub-V18…V37 …） | 86 | 10M |
| `tests/` | Playwright 验证脚本 + 素材装配脚本 | — | — |
| `supabase/` | `schema.sql`（表与 RLS 策略） | — | — |
| `学科材料/` | 教材 / 练习册 / 复习素材归档（`01_语文` … `06_历史`） | 0 | 834M |
| `资料索引/` | 真题本地归档与资源清单 | 1 | 480M |

合计 **203 个 HTML、约 3.7G**。其中 `学科材料/`、`资料索引/` 的绝大部分是扫描件与音频素材，
按 `.gitignore` 决定是否入库（见「大文件策略」）。

`资料索引/8shang_yuwen_jichu/` 是一个**独立的 Next.js 子项目**（自带 `package.json`、drizzle、vite），
与主站无关，仅靠 `.gitignore` 白名单放行其 `导出/` 与 `public/`。

---

## 技术约定

这是本项目的**刻意选择**，不是遗漏，改动前请先确认是否有必要破坏它：

- **无框架、无构建、无 `package.json`**。纯手写 HTML + 内联 CSS/JS，单页普遍 2000–4200 行。
- **版本管理靠文件名**：`english-hub-V38.html` → `V39`，`zhongkao-guide-V14.html`，`unified-tracker-V11.html`。
  **升版 = 另存为新文件，不覆盖旧文件**；旧版本移入 `archive/`，不删除。
- **不做批量重构**。页面之间没有构建依赖，一次只改一页，改完立刻实跑验证。
- `index.html` 的标题里带版本（当前 **V16**），但文件名不带。这是现状，不是笔误。
- 唯一的第三方依赖是 `node_modules/` 里的 **playwright**，仅供 `tests/` 使用。

---

## 数据层

| 数据 | 存储 |
|---|---|
| 单词星球进度、音频 | **Supabase** `hllfcxpefnrmtxcaylxa.supabase.co`，表 `word_planet_app_state`（jsonb 单行），bucket `word-planet-audio` |
| Supabase 配置 | 仓库根 `supabase-config.js`（页面用 `../supabase-config.js` 引用，见下） |
| 费用结算 / 打卡 | 浏览器 **localStorage** |

**注意相对路径**：`supabase-config.js` 在仓库根，而页面在子目录下，引用必须写成
`../supabase-config.js`。曾因写成 `./supabase-config.js` 导致线上 404、SDK 未初始化（已修）。

---

## 部署

| 项 | 值 |
|---|---|
| 托管 | Vercel 项目 `englishlearining` |
| 域名 | **https://english.bolicity.com** |
| 远端 | `https://github.com/bolicity/englishlearning.git`（分支 `main`） |
| 基线标签 | `golden-baseline-v9`、`v8.0-stable`、`v8.1-mobile-audio` |

> **验证线上只用 `english.bolicity.com`。**
> `englishlearining.vercel.app` 在本机被 DNS 解析到黑洞地址 `198.18.1.223`，`curl` 恒返 `000`，
> 会误判为「挂了」。

`vercel.json` 只保留两条 rewrite（把任意路径下的「背诵版.html」指向
`/chinese/recitation-bank-V1.html`）。**新增 rewrite 前先确认目标文件确实存在**——
曾有一条 `/` → `/word-planet.html` 的规则指向不存在的路径，永远命中不到，已删除。

---

## 测试

`tests/*.js` 共 **27 个 Playwright 验证脚本**，全部走 `file://` 直接打开本地文件。

```bash
NODE_PATH=./node_modules node tests/verify-yuwen-repair-V1.js
```

**已知的可移植性问题**（换机器时需要改）：

- 3 个脚本硬编码了绝对路径 `/Users/emily/Developer/Projects/owenlearining/…`；
- `tests/verify-v11-cloud-sync.js` 指定使用系统 Chrome（`/Applications/Google Chrome.app`）。

**写新脚本时容易踩的坑：**

1. 页面图片带 `loading="lazy"`——断言前必须逐屏滚动，否则图永不加载；
2. 已提交的输入框会变 `readonly`——定位用 `.nth(i).locator('input')`，**不要用 `.first()`**；
3. **404 既不会触发 `pageerror`，也不会触发 `requestfailed`**（4xx 是正常响应）。
   查资源缺失必须单独监听响应状态：
   ```js
   page.on('response', r => { if (r.status() >= 400) bad.push(r.url()); });
   ```
   否则像 `supabase-config.js` 那种 404 会被静默漏掉。

`tests/*.py` 是**素材装配脚本**（儒林外史连环画切片与挂载、教材构建、PDF 抽取等），
不是测试，按需手动运行。

---

## 大文件策略

GitHub 单文件上限 50MB（警告）/ 100MB（拒绝）。仓库通过 `.gitignore` 排除：

- 超限的扫描版 PDF（数学 / 物理 / 英语练习册答案、语文教材目录）；
- `/资料索引/上海中考真题-夸克下载/`（约 499MB，**仅本地留存，不上线**）；
- Playwright 输出目录 `/test-results/`。

**新增素材前先看体积**：超过 10MB 的资源应放到仓库外或用外部存储，只把索引页入库。

---

## 已知问题 / 待办

| # | 问题 | 影响 |
|---|---|---|
| 1 | `node_modules/`（179 个文件）与 `test-results/`（40 个文件）**已被 git 跟踪**，而 `.gitignore` 里没有 `node_modules` 条目 | 仓库无谓膨胀；依赖变更会产生噪音 diff |
| 2 | `supabase-config.js` 已入库，且 `schema.sql` 中 RLS 策略对 `anon` 开放 `select` / `insert` / `update` | 仓库公开 → 任何人可读改 `word_planet_app_state` |
| 3 | 版本标识仍是「文件名带版本」制，`index.html` 标题 V16 但文件名无版本号 | 历史约定，暂不统一 |
| 4 | `archive/history_versions/` 内的旧快照引用了已归档的 `tracker/unified-tracker-V9/V10.html`，相对路径本就是坏的 | **历史快照一律不动** |

---

## 每次改动的固定流程

1. **改**：一次一页，不顺手重构别的；
2. **本地实跑**：起服 + Chromium 打开，`pageerror` 为空、**且响应状态码无 4xx/5xx**；
3. **提交**：`git add` + 有信息量的 commit message（中文，说清「改了什么、为什么」）；
4. **推送**：`git push origin main`；
5. **轮询线上**：`curl` 轮询 `https://english.bolicity.com`，确认改动已生效再收工。

> 第 5 步不能省。Vercel 构建需要时间，本地 commit 成功 ≠ 线上已生效。
