const fs = require('fs');
const assert = require('assert');
const vm = require('vm');

console.log("=== 开始全面功能测试验收 ===");

// 1. 测试 chinese-recitation-V15.html
console.log("\n[1/3] 测试 chinese/chinese-recitation-V15.html...");
const v15Text = fs.readFileSync('chinese/chinese-recitation-V15.html', 'utf-8');
assert(v15Text.includes("九上古诗文虚拟记忆宫殿背诵卡 V15.0"), "V15 标题缺失");
assert(v15Text.includes("背诵篇目 (13篇)"), "13篇侧边栏计数缺失");

const m_art = v15Text.match(/const articles = (\[[\s\S]*?\]);\s*const PINYIN_PHRASES/);
const m_pal = v15Text.match(/const palaceData = ({[\s\S]*?});\s*let currentPalaceSpotIndex/);
const m_phr = v15Text.match(/const PINYIN_PHRASES = ({[\s\S]*?});/);

assert(m_art && m_pal && m_phr, "JS 数据结构未完整匹配");

const sbox1 = {};
vm.runInNewContext(`articles = ${m_art[1]}; palace = ${m_pal[1]}; phrases = ${m_phr[1]};`, sbox1);

assert.strictEqual(sbox1.articles.length, 13, "文章总数应为 13");
const chushi = sbox1.articles[4];
assert.strictEqual(chushi.title, "出师表", "第 5 篇 (id: 4) 应为出师表");
assert.strictEqual(chushi.storyboard.length, 4, "出师表应有 4 个精美分镜");
assert(chushi.storyboard[0].img.includes("chushibiao-c1.webp"), "第1分镜图片路径正确");
assert(chushi.clozeKeyWords.includes("陟罚臧否"), "应包含中考核心重点词陟罚臧否");

assert(sbox1.palace["4"] && sbox1.palace["4"].length === 6, "出师表记忆宫殿应有 6 个空间锚点");
assert.strictEqual(sbox1.phrases["陟罚臧否"][3], "pǐ", "臧否的否必须注音为 pǐ");
assert.strictEqual(sbox1.phrases["以遗陛下"][1], "wèi", "以遗陛下的遗必须注音为 wèi");
console.log("✅ chinese-recitation-V15.html 验收通过！");

// 2. 测试 math-V4.html
console.log("\n[2/3] 测试 math/math-V4.html...");
const mathText = fs.readFileSync('math/math-V4.html', 'utf-8');
assert(mathText.includes("V4 逐题配速明细版"), "V4 标题标签缺失");
assert(mathText.includes("第 1 题") && mathText.includes("第 24 题"), "1-24 题逐题明细缺失");
assert(mathText.includes("12 分钟") && mathText.includes("16 分钟") && mathText.includes("5 分钟"), "图片中考板块时间数据缺失");
assert(mathText.includes("18 分钟") && mathText.includes("13 分钟") && mathText.includes("15 分钟"), "解答题板块时间缺失");
assert(mathText.includes("swQuestionSelect"), "考场模拟计时器缺失");
console.log("✅ math/math-V4.html 验收通过！");

// 3. 测试 recitation-comics-V2.html
console.log("\n[3/3] 测试 chinese/recitation-comics-V2.html...");
const comicsText = fs.readFileSync('chinese/recitation-comics-V2.html', 'utf-8');
assert(comicsText.includes("V2.0 考纲原文版"), "Comics V2 标题缺失");
assert(comicsText.includes("fulltextSection"), "考纲原文容器缺失");
assert(comicsText.includes("hardPillList"), "生僻字药丸容器缺失");

const m_cdata = comicsText.match(/const DATA = (\[[\s\S]*?\]);\s*\n/);
assert(m_cdata, "Comics DATA 结构未匹配");

const sbox2 = {};
vm.runInNewContext(`data = ${m_cdata[1]};`, sbox2);
let totalComics = 0;
let itemsWithFullParas = 0;
let itemsWithHard = 0;

sbox2.data.forEach(vol => {
  vol.items.forEach(it => {
    totalComics++;
    if (it.paras && it.paras.length > 0) itemsWithFullParas++;
    if (it.hard && it.hard.length > 0) itemsWithHard++;
  });
});

assert.strictEqual(totalComics, 86, "四格连环画应包含全部 86 篇");
assert.strictEqual(itemsWithFullParas, 86, "全部 86 篇均必须包含 PDF 考纲标准完整原文");
console.log(`- 86 篇完整原文覆盖率: ${itemsWithFullParas}/86 (100%)`);
console.log(`- 易错生僻字考点覆盖率: ${itemsWithHard}/86`);

// 检查宿建德江 (sujiandejiang)
const sujiandejiang = sbox2.data[0].items[0];
assert.strictEqual(sujiandejiang.title, "宿建德江", "首篇为宿建德江");
assert(sujiandejiang.paras[0].includes("移舟泊烟渚"), "宿建德江全文正确");
assert(sujiandejiang.hard.includes("渚（zhǔ，水中小块陆地）"), "宿建德江生僻字考点完全一致");

console.log("✅ recitation-comics-V2.html 验收通过！");

console.log("\n🎉 全部功能自动化验收 100% 通过！");
