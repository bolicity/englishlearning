# GitHub 上海中考复习资源清单

> 检索日期：2026-10-06 · 检索方式：GitHub 仓库搜索（21 组关键词）+ 网页交叉验证
> 结论：**GitHub 无"高星上海中考"专属库**。高星库均为泛 K12 教材聚合；真正对口的上海库集中在 0–30 星区间。

---

## A. 综合教材/试卷库（星数最高，先看）★★★★

| 仓库 | ★ | 体积 | 最后更新 | 说明 |
|---|---|---|---|---|
| https://github.com/TapXWorld/ChinaTextbook | 82,573 | 42.5 GB | 2025-10-18 | 小初高+大学 PDF 教材全集，含沪教版。子目录 `学数学最重要的刷习题在这里/初中练习题_带答案` 含《2018上海市中考数学试题及解析》等分省中考卷 |
| https://github.com/weiyayun925104/Mathematics_Physics_Chemistry_Books | 339 | — | 2026-05-19 | 小学→高中数理化自学教材、甲种本、中学数学实验教材 |
| https://github.com/BigShuang/elementary-math | 89 | — | — | 初高中数学学习笔记（纯笔记，非题库） |
| https://github.com/mmlong818/k12-knowledge-points | 38 | — | — | K12 知识点数据集：25,332 知识点 + 20,714 条关系，适合做知识图谱 |
| https://github.com/Hefei-little-fat-man/edu | 3 | — | — | 小初高全科：电子课本 + 教学 PPT + 随堂练习 + 试卷 |

## B. 上海专项（星少，但最对口）★★★

| 仓库 | ★ | 体积 | 最后更新 | 说明 |
|---|---|---|---|---|
| https://github.com/Onion12138/math | 30 | 27 MB | 2021-08-02 | **上海初中数学讲义 LaTeX 版**（已停更，内容对口） |
| https://github.com/ShawnZhong/Shanghai-Textbook | 27 | — | 2022-03-26 | 上海沪教版高中教材（2015 爬取自 shkegai.net） |
| https://github.com/Xnye/Smse | 7 | 101 MB | 2023-07-25 | **上海市中考数学 · 一二模卷** |
| https://github.com/Code1ce/2024-shzk-Math | 3 | — | — | 2024 上海中考数学真题（TeX 排版） |
| https://github.com/SteveTDX/shanghai_textbooks | 2 | — | 2026-04-16 | 上海小学初中高中教材下载 |
| https://github.com/mylukin/shici | 0 | 102 MB | 2025-03-30 | **上海中考 150 文言文实词**（含分段音频 mp3） |
| https://github.com/weiliangma/englishworld | 1 | — | — | 上海中考英语语法练习平台 |
| https://github.com/kevin178plus/shanghai-zhongkao-fenshuxian | 1 | — | — | 上海中考分数线 |
| https://github.com/DeverAI/zizhao-learning | 0 | 5 MB | 2026-09-26 | 上海中考自招每日素材系统（AGPL-3.0） |

## C. 中考通用工具/题库（可作项目素材）★★

| 仓库 | ★ | 体积 | 最后更新 | 说明 |
|---|---|---|---|---|
| https://github.com/rongchenxu100/shuxueshuo | 13 | 171 MB | 2026-10-05 | ⚠️ **名不副实**：275 题中 228 题是高中数学，中考部分为天津压轴题 40 道，**上海仅 2 题**。已下载验证后删除，无实际价值 |
| https://github.com/mikigo/english-chinese-words | 57 | — | — | Web 版单词库：小学→考研全阶段，含中考 |
| https://github.com/Xww-coder/pep-math-taxonomy | 44 | — | — | 初中数学教材知识图谱（人教版） |
| https://github.com/ichangting/taotao-skills | 12 | — | 2026-07-28 | 初中语文 AI 教学技能合集（备课/中考备考/文言文），MIT |
| https://github.com/fangfengcao/Personal-Leraning-Core-Resources | 4 | — | — | 初中物理/化学/语文/英语 知识点 + 习题 |
| https://github.com/Tim-JoJo/zhongkao-reading-toolchain | 2 | — | — | 中考英语阅读 AI 工具链（改写出题/题库匹配） |
| https://github.com/protoss0928/zhongkao-physics-zhuang | 2 | — | — | 中考物理核心考点复习小程序（22 章 83 题 + 艾宾浩斯） |

## D. 已失效 / 谨慎

- **`mswnlz/edu-knowlege` → 404**：曾被全网博客与新浪推荐（"含学而思·万维·猿辅导 100TB 资料"），**仓库已删除**，仅剩 0 星 fork。不要再引用。
- `Smartuil/China-Exam-Papers`（★1）：试卷站框架，本身不含大量试卷。
- `1wri/Exams`、`34426/Examination`（★0）：标称"2013–2026 全国中考真题"，实际资源多在网盘链接，可用性不保证。

---

## 使用提醒

1. **优先 B 组**。上海中考出题口径（沪教版、150 文言实词、一模二模 16 区卷）在通用大库里基本检索不到。
2. **A 组胜在体量**，`ChinaTextbook` 42 GB 建议用 sparse-checkout 只拉需要的子目录，别整库 clone。
3. 这类仓库**多为扫描版 PDF 转存**，版权状态模糊；"高星"多来自"资源聚合"而非内容质量。
4. 判断仓库是否可用，看 `pushed_at` 而非 star——很多高星库已两三年未更新。
