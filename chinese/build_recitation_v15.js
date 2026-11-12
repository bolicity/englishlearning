const fs = require("fs");
const vm = require("vm");

// 读取 V14 内容
const v14Path = "chinese/chinese-recitation-V14.html";
const v15Path = "chinese/chinese-recitation-V15.html";

const v14Content = fs.readFileSync(v14Path, "utf-8");

// 提取数据
const m_articles = v14Content.match(/const articles = (\[[\s\S]*?\]);\s*const PINYIN_PHRASES/);
const m_phrases = v14Content.match(/const PINYIN_PHRASES = ({[\s\S]*?});/);
const m_chars = v14Content.match(/const PINYIN_CHARS = ({[\s\S]*?});/);
const m_palace = v14Content.match(/const palaceData = ({[\s\S]*?});\s*let currentPalaceSpotIndex/);

if (!m_articles || !m_phrases || !m_chars || !m_palace) {
  console.error("Failed to parse V14 data structures!");
  process.exit(1);
}

const sandbox = {};
vm.runInNewContext(
  `
  articles = ${m_articles[1]};
  phrases = ${m_phrases[1]};
  chars = ${m_chars[1]};
  palace = ${m_palace[1]};
`,
  sandbox
);

const { articles, phrases, chars, palace } = sandbox;

// 构建《出师表》完整数据
const chushiArticle = {
  id: 4,
  title: "出师表",
  author: "〔三国·蜀汉〕诸葛亮",
  translations: [
    "先帝开创大业未完成一半就中途去世了。现在天下分裂为三国，益州人力疲敝、国力困乏，这实在是危急存亡的关键时刻啊。然而在朝中侍奉护卫的官员毫不懈怠，在战场上忠勇报国的将士舍身忘死，大概是追念先帝对他们的特殊恩遇，想要报答在陛下您的身上吧。陛下实在应该广泛听取臣民意见，来发扬光大先帝遗留的美德，振奋激发志士们的豪气；不应该盲目轻视自己，说话不合道理，从而堵塞忠诚进谏的言路。皇宫中和丞相府中的官员都是一个整体，提拔、惩罚、赞扬、批评，不应该有所不同。如果有做坏事触犯法律以及尽忠做好事的人，应该交给主管官员裁定他们应受的刑罚或赏赐，来显示陛下公正严明的治理，不应该偏袒徇私，使宫内宫外有不同的法制。",
    "侍中郭攸之、费祎，侍郎董允等人，这都是善良诚实、志向忠诚纯正的人，因此先帝选拔出来留给陛下。我认为宫廷中的事情，无论大小，都拿来向他们询问，然后再去执行，必定能够补救疏漏欠缺，收获很大益处。向宠将军，性格品行端庄公正，通晓军事，往日试用时，先帝称赞他有才能，因此大家商议推举他担任中部督。我认为军营中的事情，都拿来向他询问，必定能使军队团结和睦，品行优劣的人各有合适的安排。亲近贤臣，疏远小人，这是西汉兴盛的原因；亲近小人，疏远贤臣，这是东汉衰败的原因。先帝在世时，每次跟我谈论起这些事，没有一次不对桓帝、灵帝的乱政发出叹息和痛心遗憾的。侍中、尚书、长史、参军，这都是坚贞忠良、愿为节义献身的臣子，希望陛下亲近他们、信任他们，那么汉室的复兴，就可以指日以待了。",
    "我本来是平民百姓，在南阳亲自耕种，只想在乱世中苟且保全性命，不求在诸侯中扬名显达。先帝不介意我身份卑微鄙陋，委屈自己降低身份，三次到草庐之中探望我，拿当时的天下大事来向我询问，我因此感动奋发，于是答应为先帝奔走效劳。后来遇到兵败危局，在兵败溃退的时候接受任命，在危急患难的关头奉承使命，从那时以来已有二十一年了。",
    "先帝深知我处事谨慎，所以临终时把国家大事托付给我。自从接受托付以来，我早起晚睡忧愁叹息，唯恐托付的事情没有成效，从而损伤了先帝知人之明，所以五月份渡过泸水，深入荒无人烟的地带。现在南方叛乱已经平定，武器装备已经充足，应当激励率领全军将士，向北平定中原，希望能竭尽平庸的才能，铲除奸邪凶顽，复兴汉室江山，重回旧都洛阳。这是我用来报答先帝并尽忠于陛下的职责本分啊。至于权衡利弊得失，毫无保留地进献忠直言策，那就是郭攸之、费祎、董允他们的职责了。希望陛下把讨伐奸贼、复兴汉室的重任交给我，如果见不到成效，就惩处我的罪过，来告慰先帝的在天之灵。如果没有发扬圣德的言论，就责罚郭攸之、费祎、董允等人的懈怠，来公布他们的过失；陛下自己也应该深思谋划，询问治国良策，审查采纳正确合理的言论，深切追念先帝的临终遗诏。我承受陛下的深恩，心中感激不尽。今天我就要远离陛下了，面对奏表禁不住泪流满面，真不知道自己说了些什么。"
  ],
  storyboard: [
    {
      badge: "分镜 1 / 4",
      title: "镜头1：危急形势·广开言路与严明法度",
      img: "images/recitation-comics/chushibiao-c1.webp",
      passage: "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。",
      clue: "🔑 线索：创业未半 ➔ 天下三分/益州疲弊 ➔ 危急存亡之秋 ➔ 侍卫不懈/忠志忘身 ➔ 开张圣听 ➔ 陟罚臧否不宜异同 ➔ 平明之理",
      translation: "先帝开创大业未半就中途离世，如今天下三分、益州民力困乏，这实在是危急存亡的关键时刻。然而侍卫之臣不懈于内，忠志之士忘身于外，欲报之于陛下。诚宜开张圣听，恢弘志士之气；宫中府中俱为一体，陟罚臧否不宜异同，以昭陛下平明之理。"
    },
    {
      badge: "分镜 2 / 4",
      title: "镜头2：荐拔文武·亲贤远佞两汉兴衰",
      img: "images/recitation-comics/chushibiao-c2.webp",
      passage: "侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。",
      clue: "🔑 线索：郭攸之/费祎/董允（裨补阙漏） ➔ 向宠（行阵和睦） ➔ 亲贤臣远小人（先汉兴隆） ➔ 亲小人远贤臣（后汉倾颓） ➔ 叹息痛恨于桓灵 ➔ 计日而待",
      translation: "诸葛亮在表中恳切荐拔文臣郭攸之、费祎、董允，武将向宠；并总结千古治乱格言：亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。愿陛下亲之信之，汉室之隆可计日而待。"
    },
    {
      badge: "分镜 3 / 4",
      title: "镜头3：布衣躬耕·三顾草庐临危受命",
      img: "images/recitation-comics/chushibiao-c3.webp",
      passage: "臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。",
      clue: "🔑 线索：臣本布衣 ➔ 躬耕南阳 ➔ 苟全性命/不求闻达 ➔ 先帝不以臣卑鄙 ➔ 三顾臣于草庐之中 ➔ 许先帝以驱驰 ➔ 受任于败军之际/奉命于危难之间 ➔ 二十有一年",
      translation: "臣本平民百姓，躬耕南阳苟全性命。先帝不因我身份卑微自降身份，三次探访草庐垂询大事，我由是感激答应驱驰效力。后临倾覆，受任于败军之际，奉命于危难之间，转眼已有二十一年。"
    },
    {
      badge: "分镜 4 / 4",
      title: "镜头4：北伐誓师·严明职分临表涕零",
      img: "images/recitation-comics/chushibiao-c4.webp",
      passage: "先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。",
      clue: "🔑 线索：临崩寄大事 ➔ 夙夜忧叹 ➔ 深入不毛 ➔ 兵甲已足 ➔ 奖率三军/北定中原 ➔ 庶竭驽钝/兴复汉室 ➔ 托臣以讨贼兴复之效 ➔ 咨诹善道/察纳雅言 ➔ 临表涕零不知所言",
      translation: "受命以来日夜忧叹，五月渡泸深入不毛。如今南方已定兵甲已足，当奖率三军北定中原，竭尽平庸才能攘除奸凶、兴复汉室、还于旧都！陛下亦宜自谋，咨诹善道，察纳雅言。今当远离，临表涕零，不知所言。"
    }
  ],
  paragraphs: [
    "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。",
    "侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。",
    "臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。",
    "先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。"
  ],
  clozeKeyWords: [
    "崩殂", "益州疲弊", "危急存亡之秋", "殊遇", "开张圣听", "恢弘志士之气", "妄自菲薄", 
    "引喻失义", "塞忠谏之路", "俱为一体", "陟罚臧否", "作奸犯科", "平明之理", "内外异法", 
    "郭攸之", "费祎", "董允", "简拔", "裨补阙漏", "有所广益", "向宠", "性行淑均", 
    "晓畅军事", "行阵和睦", "优劣得所", "亲贤臣", "远小人", "叹息痛恨", "桓、灵", 
    "计日而待", "臣本布衣", "躬耕于南阳", "苟全性命", "不求闻达", "卑鄙", "猥自枉屈", 
    "三顾臣于草庐之中", "驱驰", "受任于败军之际", "奉命于危难之间", "二十有一年", 
    "夙夜忧叹", "深入不毛", "兵甲已足", "奖率三军", "北定中原", "庶竭驽钝", "攘除奸凶", 
    "兴复汉室", "还于旧都", "斟酌损益", "以彰其咎", "咨诹善道", "察纳雅言", "深追先帝遗诏", 
    "临表涕零", "不知所言"
  ]
};

const chushiPalace = [
  {
    spot: "📍 宫殿位置 1：蜀汉前殿丹墀大门",
    peg: "🗝️ 空间锚点：门前悬挂的三国鼎立图与先帝创业金钟",
    story: "🧠 图像联想：踏入蜀汉宫殿前门，看到门侧悬挂着三国鼎立舆图，益州疲弊的暗淡光芒让人警醒，诸葛丞相指着舆图向少主切谏‘开张圣听’，侍卫与忠臣整肃侍立。",
    text: "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。"
  },
  {
    spot: "📍 宫殿位置 2：尚书政务大殿正堂",
    peg: "🗝️ 空间锚点：堂前摆放的‘公正刑赏’青铜天平与律法竹简",
    story: "🧠 图像联想：来到政务大厅中央，正中放着一尊巨大青铜天平，两端分别刻着‘宫中’与‘府中’，严明法度、不偏不私，天平两端稳如泰山！",
    text: "宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。"
  },
  {
    spot: "📍 宫殿位置 3：内廷贤良殿书斋",
    peg: "🗝️ 空间锚点：郭攸之/费祎/向宠的功臣图谱与‘亲贤远佞’紫檀屏风",
    story: "🧠 图像联想：走进书斋，四壁绘着忠贞文武的画像，紫檀屏风上赫然写着两汉兴衰训诫，先帝抚胸叹息痛恨桓灵的背影历历在目。",
    text: "侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。"
  },
  {
    spot: "📍 宫殿位置 4：西侧南阳草庐怀旧阁",
    peg: "🗝️ 空间锚点：草庐模型、诸葛羽扇与当年的草鞋农具",
    story: "🧠 图像联想：阁内摆设如当年南阳草庐，刘备风雪三顾茅庐的画面重现，羽扇旁放着长坂坡突围的残破战旗，诉说着‘受任于败军之际’的峥嵘岁月。",
    text: "臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。"
  },
  {
    spot: "📍 宫殿位置 5：誓师点将校场与作战沙盘",
    peg: "🗝️ 空间锚点：泸水战甲、北定中原大旗与三军点将台",
    story: "🧠 图像联想：校场旌旗蔽日，沙盘上插着北伐中原的汉军战旗，案上放着沾满泸水泥泞的战甲，诸葛亮拔剑誓师，矢志兴复汉室、还于旧都！",
    text: "先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。"
  },
  {
    spot: "📍 宫殿位置 6：出师御道与白玉祭台",
    peg: "🗝️ 空间锚点：墨迹未干的《出师表》奏章与沾着泪痕的佩剑",
    story: "🧠 图像联想：登上出师御道，阶前白玉台上展开墨迹未干的《出师表》，老丞相躬身拜别，眼含热泪化作千古忠贞，全军向北浩荡启程！",
    text: "愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言。"
  }
];

// 重组 articles
const newArticles = [];
for (let i = 0; i < 4; i++) {
  newArticles.push(articles[i]);
}
newArticles.push(chushiArticle);
for (let i = 4; i < articles.length; i++) {
  const art = { ...articles[i], id: articles[i].id + 1 };
  newArticles.push(art);
}

// 重组 palaceData
const newPalaceData = {};
for (let i = 0; i < 4; i++) {
  newPalaceData[String(i)] = palace[String(i)];
}
newPalaceData["4"] = chushiPalace;
for (let i = 4; i < articles.length; i++) {
  newPalaceData[String(i + 1)] = palace[String(i)];
}

// 补充字词拼音
const extraPhrases = {
  "出师表": ["chū", "shī", "biǎo"],
  "崩殂": ["bēng", "cú"],
  "益州疲弊": ["yì", "zhōu", "pí", "bì"],
  "疲弊": ["pí", "bì"],
  "殊遇": ["shū", "yù"],
  "恢弘": ["huī", "hóng"],
  "妄自菲薄": ["wàng", "zì", "fěi", "bó"],
  "菲薄": ["fěi", "bó"],
  "引喻失义": ["yǐn", "yù", "shī", "yì"],
  "忠谏": ["zhōng", "jiàn"],
  "陟罚臧否": ["zhì", "fá", "zāng", "pǐ"],
  "臧否": ["zāng", "pǐ"],
  "作奸犯科": ["zuò", "jiān", "fàn", "kē"],
  "平明之理": ["píng", "míng", "zhī", "lǐ"],
  "郭攸之": ["guō", "yōu", "zhī"],
  "费祎": ["fèi", "yī"],
  "董允": ["dǒng", "yǔn"],
  "志虑忠纯": ["zhì", "lǜ", "zhōng", "chún"],
  "以遗陛下": ["yǐ", "wèi", "bì", "xià"],
  "裨补阙漏": ["bì", "bǔ", "quē", "lòu"],
  "有所广益": ["yǒu", "suǒ", "guǎng", "yì"],
  "向宠": ["xiàng", "chǒng"],
  "性行淑均": ["xìng", "xíng", "shū", "jūn"],
  "晓畅军事": ["xiǎo", "chàng", "jūn", "shì"],
  "晓畅": ["xiǎo", "chàng"],
  "行阵和睦": ["háng", "zhèn", "hé", "mù"],
  "行阵": ["háng", "zhèn"],
  "优劣得所": ["yōu", "liè", "dé", "suǒ"],
  "亲贤臣": ["qīn", "xián", "chén"],
  "远小人": ["yuǎn", "xiǎo", "rén"],
  "倾颓": ["qīng", "tuí"],
  "叹息痛恨": ["tàn", "xī", "tòng", "hèn"],
  "桓、灵": ["huán", "líng"],
  "死节之臣": ["sǐ", "jié", "zhī", "chén"],
  "计日而待": ["jì", "rì", "ér", "dài"],
  "臣本布衣": ["chén", "běn", "bù", "yī"],
  "躬耕于南阳": ["gōng", "gēng", "yú", "nán", "yáng"],
  "躬耕": ["gōng", "gēng"],
  "苟全性命": ["gǒu", "quán", "xìng", "mìng"],
  "不求闻达": ["bù", "qiú", "wén", "dá"],
  "猥自枉屈": ["wěi", "zì", "wǎng", "qū"],
  "三顾臣": ["sān", "gù", "chén"],
  "草庐": ["cǎo", "lú"],
  "驱驰": ["qū", "chí"],
  "受任于败军之际": ["shòu", "rèn", "yú", "bài", "jūn", "zhī", "jì"],
  "奉命于危难之间": ["fèng", "mìng", "yú", "wēi", "nàn", "zhī", "jiān"],
  "二十有一年": ["èr", "shí", "yǒu", "yī", "nián"],
  "夙夜忧叹": ["sù", "yè", "yōu", "tàn"],
  "五月渡泸": ["wǔ", "yuè", "dù", "lú"],
  "深入不毛": ["shēn", "rù", "bù", "máo"],
  "奖率三军": ["jiǎng", "shuài", "sān", "jūn"],
  "北定中原": ["běi", "dìng", "zhōng", "yuán"],
  "庶竭驽钝": ["shù", "jié", "nú", "dùn"],
  "驽钝": ["nú", "dùn"],
  "攘除奸凶": ["rǎng", "chú", "jiān", "xiōng"],
  "兴复汉室": ["xīng", "fù", "hàn", "shì"],
  "还于旧都": ["huán", "yú", "jiù", "dū"],
  "斟酌损益": ["zhēn", "zhuó", "sǔn", "yì"],
  "以彰其咎": ["yǐ", "zhāng", "qí", "jiù"],
  "咨诹善道": ["zī", "zōu", "shàn", "dào"],
  "咨诹": ["zī", "zōu"],
  "察纳雅言": ["chá", "nà", "yǎ", "yán"],
  "深追先帝遗诏": ["shēn", "zhuī", "xiān", "dì", "yí", "zhào"],
  "不胜受恩感激": ["bù", "shèng", "shòu", "ēn", "gǎn", "jī"],
  "临表涕零": ["lín", "biǎo", "tì", "líng"],
  "不知所言": ["bù", "zhī", "suǒ", "yán"]
};

Object.assign(phrases, extraPhrases);

// 读取从 Python 预生成的出师表字符单字拼音
const chushiChars = JSON.parse(fs.readFileSync("chinese/chushibiao_chars.json", "utf-8"));
Object.assign(chars, chushiChars);

// 替换 HTML 内容
let v15Content = v14Content;

// 1. 替换页面标题与 Badge
v15Content = v15Content.replace(
  "<title>九上古诗文动态注音分镜背诵卡 V14.0</title>",
  "<title>九上古诗文虚拟记忆宫殿背诵卡 V15.0（含出师表）</title>"
);
v15Content = v15Content.replace(
  '<h1>九上古诗文虚拟记忆宫殿背诵卡 <span class="logo-badge" style="background: linear-gradient(135deg, #2563EB, #7C3AED); color: #fff;">V14.0 原生文字高精注音版</span></h1>',
  '<h1>九上古诗文虚拟记忆宫殿背诵卡 <span class="logo-badge" style="background: linear-gradient(135deg, #2563EB, #7C3AED); color: #fff;">V15.0 经典扩充·新增《出师表》</span></h1>'
);
v15Content = v15Content.replace(
  '<div class="sidebar-title">背诵篇目 (12篇)</div>',
  '<div class="sidebar-title">背诵篇目 (13篇)</div>'
);

// 2. 侧边栏更新：在文言文组加入出师表 (loadArticle(4))
const oldNavGroup = `        <ul class="article-list">
          <li class="article-item active" onclick="loadArticle(0)">
            <span>岳阳楼记</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(1)">
            <span>醉翁亭记</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(2)">
            <span>湖心亭看雪</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(3)">
            <span>沁园春·雪</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
        </ul>`;

const newNavGroup = `        <ul class="article-list">
          <li class="article-item active" onclick="loadArticle(0)">
            <span>岳阳楼记</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(1)">
            <span>醉翁亭记</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(2)">
            <span>湖心亭看雪</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(3)">
            <span>沁园春·雪</span>
            <span class="article-tag">⚡ 图文同框</span>
          </li>
          <li class="article-item" onclick="loadArticle(4)">
            <span>出师表</span>
            <span class="article-tag" style="background: #EFF6FF; color: #2563EB; font-weight: 700;">⭐ 新增必背</span>
          </li>
        </ul>`;

v15Content = v15Content.replace(oldNavGroup, newNavGroup);

// 3. 诗词组的 loadArticle(X) 索引递增 (4->5, 5->6, ..., 11->12)
const oldPoetryGroup = `        <ul class="article-list">
          <li class="article-item" onclick="loadArticle(4)"><span>行路难（其一）</span><span class="article-tag">李白</span></li>
          <li class="article-item" onclick="loadArticle(5)"><span>酬乐天扬州初逢席上见赠</span><span class="article-tag">刘禹锡</span></li>
          <li class="article-item" onclick="loadArticle(6)"><span>水调歌头</span><span class="article-tag">苏轼</span></li>
          <li class="article-item" onclick="loadArticle(7)"><span>十五从军征</span><span class="article-tag">汉乐府</span></li>
          <li class="article-item" onclick="loadArticle(8)"><span>白雪歌送武判官归京</span><span class="article-tag">岑参</span></li>
          <li class="article-item" onclick="loadArticle(9)"><span>南乡子·登京口北固亭</span><span class="article-tag">辛弃疾</span></li>
          <li class="article-item" onclick="loadArticle(10)"><span>过零丁洋</span><span class="article-tag">文天祥</span></li>
          <li class="article-item" onclick="loadArticle(11)"><span>山坡羊·潼关怀古</span><span class="article-tag">张养浩</span></li>
        </ul>`;

const newPoetryGroup = `        <ul class="article-list">
          <li class="article-item" onclick="loadArticle(5)"><span>行路难（其一）</span><span class="article-tag">李白</span></li>
          <li class="article-item" onclick="loadArticle(6)"><span>酬乐天扬州初逢席上见赠</span><span class="article-tag">刘禹锡</span></li>
          <li class="article-item" onclick="loadArticle(7)"><span>水调歌头</span><span class="article-tag">苏轼</span></li>
          <li class="article-item" onclick="loadArticle(8)"><span>十五从军征</span><span class="article-tag">汉乐府</span></li>
          <li class="article-item" onclick="loadArticle(9)"><span>白雪歌送武判官归京</span><span class="article-tag">岑参</span></li>
          <li class="article-item" onclick="loadArticle(10)"><span>南乡子·登京口北固亭</span><span class="article-tag">辛弃疾</span></li>
          <li class="article-item" onclick="loadArticle(11)"><span>过零丁洋</span><span class="article-tag">文天祥</span></li>
          <li class="article-item" onclick="loadArticle(12)"><span>山坡羊·潼关怀古</span><span class="article-tag">张养浩</span></li>
        </ul>`;

v15Content = v15Content.replace(oldPoetryGroup, newPoetryGroup);

// 4. 替换 articles
v15Content = v15Content.replace(
  /const articles = \[[\s\S]*?\];\s*const PINYIN_PHRASES/,
  `const articles = ${JSON.stringify(newArticles, null, 2)};\n\n    const PINYIN_PHRASES`
);

// 5. 替换 PINYIN_PHRASES 与 PINYIN_CHARS
v15Content = v15Content.replace(
  /const PINYIN_PHRASES = {[\s\S]*?};/,
  `const PINYIN_PHRASES = ${JSON.stringify(phrases)};`
);

v15Content = v15Content.replace(
  /const PINYIN_CHARS = {[\s\S]*?};/,
  `const PINYIN_CHARS = ${JSON.stringify(chars)};`
);

// 6. 替换 palaceData
v15Content = v15Content.replace(
  /const palaceData = {[\s\S]*?};\s*let currentPalaceSpotIndex/,
  `const palaceData = ${JSON.stringify(newPalaceData)};\n    let currentPalaceSpotIndex`
);

fs.writeFileSync(v15Path, v15Content, "utf-8");
console.log("Successfully generated", v15Path);
console.log("Total articles in V15:", newArticles.length);
console.log("Titles in V15:", newArticles.map(a => `${a.id}: ${a.title}`));

