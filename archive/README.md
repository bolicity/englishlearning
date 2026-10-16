# 历史版本与废弃文件归档清单 (Archive Inventory)

本文档记录了项目中所有已归档的历史版本、中间构建脚本与冗余文件。
**所有归档文件均已与现行系统解耦，若后续磁盘需要释放空间，可直接删除本目录中的相关文件而不会影响线上系统运行。**

---

## 目录索引与对照表

### 1. 学习看板追踪模块 (`archive/tracker-legacy/`)
* **已归档文件**：
  * `unified-tracker-V1.html` 至 `unified-tracker-V8.html`（8 个早期迭代版本）
  * `unified-tracker-V9.html`、`unified-tracker-V10.html`（先前已归档）
* **现行运行版本**：`tracker/unified-tracker-V11.html`（完整云端同步与本地 IndexedDB 存储）

---

### 2. 道德与法治模块 (`archive/daofa/`)
* **已归档文件**：
  * `daofa-V1.html`（先前已归档）
  * `daofa-V2.html` 至 `daofa-V6.html`（5 个旧版页面）
  * `build_daofa_v7.py`（V7 页面历史构建脚本）
* **现行运行版本**：
  * 学科门户：`daofa/index.html` / `daofa/daofa.html`
  * 核心全景题库：`daofa/daofa-special-bank.html`
  * 考点与资料库：`daofa/daofa-V7.html`

---

### 3. 英语学习模块 (`archive/english/`)
* **已归档文件**：
  * `english-hub-V38.html`（V38 历史全景主页，现行为 V39/english-hub）
  * `doc-viewer-V4.html`、`doc-viewer.html`（旧版文档阅读器）
  * `unit-study-hub-V2.html`、`unit-study-hub-V8-STABLE.html`、`unit-study-hub-V9-BASELINE.html`、`unit-study-hub-BASELINE.html`（与 V1 完全一致的冗余备份文件）
  * 根目录 `archive/` 下的历史版本：`english-hub-V18.html` ~ `english-hub-V37.html`
* **现行运行版本**：
  * 英语中心：`english/english-hub.html`（即 `english-hub-V39.html`）
  * 阅读与点读器：`english/doc-viewer-V5.html`、`english/unit-study-hub-V1.html`
  * 单词星球：`english/word-planet.html`

---

### 4. 语文学习模块 (`archive/chinese/`)
* **已归档文件**：
  * **旧版门户与背诵冗余副本**：
    * `chinese-V2.html`、`chinese-V3-hub.html`（早期门户）
    * `chinese-V3.html`、`chinese-recitation.html`（与现行 `chinese-recitation-V14.html` 内容一致的副本）
  * **名著阅读早期版本与中间数据**：
    * `classic-reading-V1.html`、`classic-reading-V2.html`、`classic-reading-V3.html`
    * `classic-reading-data-V1.json`、`classic-reading-structured-V2.json`、`classic-reading-v2-full.json`、`classic-reading-v3-tables.json`
    * 旧版名著构建脚本：`build_classic_reading_html.py`、`build_classic_reading_v2_html.py`、`generate_html_v1.py`、`generate_v2_final.py`、`build_v2_clean_tables.py`、`build_v3_complete.py`、`enhance_v3_tables.py`、`generate_classic_reading_v3_html.py`、`generate_structured_v2_data.py`、`enhance_db.py`
  * **儒林外史早期草稿**：
    * `rulinwaishi-V1.html`、`rulinwaishi-V3.html`
* **现行运行版本**：
  * 语文门户：`chinese/chinese.html`
  * 默写背诵：`chinese/chinese-recitation-V14.html`、`chinese/recitation-drill-V1.html`、`chinese/recitation-comics-V1.html`、`chinese/recitation-bank-V1.html`
  * 名著阅读：`chinese/classic-reading-V4.html`、`chinese/classic-reading-ocr-raw-V1.json`、`chinese/classic-reading-v4-full.json`
  * 儒林外史矩阵：`chinese/rulinwaishi-nav-V1.html`、`chinese/rulinwaishi-p1-V1.html` ~ `p4-V1.html`、`chinese/rulinwaishi-cards-V1.html`、`chinese/rulinwaishi-V2.html`

---

### 5. 化学模块 (`archive/chemistry/`)
* **已归档文件**：
  * `chemistry-V3.html`（与 V4 一致的旧版文件）
  * `doc-viewer-V1.html`、`doc-viewer-V2.html`、`doc-viewer.html`
* **现行运行版本**：
  * 化学主页：`chemistry/chemistry-V4.html` / `chemistry/chemistry.html`
  * 知识清单：`chemistry/chemistry-knowledge.html`
  * 试卷阅读器：`chemistry/doc-viewer-V3.html`

---

### 6. 物理模块 (`archive/physics/`)
* **已归档文件**：
  * `physics-hub-V3.html`（与 V4 一致的旧版文件）
  * `doc-viewer-V1.html`、`doc-viewer-V2.html`、`doc-viewer.html`
* **现行运行版本**：
  * 物理主页：`physics/physics-hub-V4.html` / `physics/physics-hub.html`
  * 试卷阅读器：`physics/doc-viewer-V3.html`
  * 年级专题：`physics/physics-grade8-review.html`、`physics-grade9-summer.html`、`physics-grade9.html`

---

### 7. 跨学科案例模块 (`archive/interdisciplinary/`)
* **已归档文件**：
  * `interdisciplinary-V1.html`、`interdisciplinary-V2.html`
  * `build_full_v3.py`
* **现行运行版本**：`interdisciplinary/interdisciplinary-V3.html`、`upgrade_interdisciplinary.py`

---

### 8. 红色研学/出国模块 (`archive/red-study/`)
* **已归档文件**：`red-study-abroad-V2.html`
* **现行运行版本**：`red-study/red-study-abroad-V3.html`

---

### 9. 中本贯通模块 (`archive/zhongben-guide/`)
* **已归档文件**：`zhongben-guide-V5.html`（先前已归档 V1~V4）
* **现行运行版本**：`zhongben/zhongben-guide-V6.html`

---

### 10. 历史页面与样式旧版 (`archive/history_versions/`)
* **已归档文件**：
  * `index-V1.css`（原根目录下旧版全屏卡片样式文件，现行使用的是紧凑全景看板 `index-V3.css`）
  * `index-V2.html` 至 `index-V15.html`（原各阶段主看板历史版本）
* **现行运行版本**：根目录 `index.html` + `index-V3.css`
