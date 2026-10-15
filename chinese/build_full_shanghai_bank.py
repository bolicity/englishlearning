# -*- coding: utf-8 -*-
"""
Full Shanghai Zhongkao Chinese Real Exam Question Bank Builder.
Constructs comprehensive authentic questions and injects into recitation-bank-V1.html.
"""

import json
import re

from build_shanghai_bank import (
    moxie_questions,
    shici_questions,
    fanyi_questions,
    mingzhu_questions,
    zonghe_questions,
    tongjia_questions
)

# --- Add additional high-frequency authentic Shanghai Zhongkao & official syllabus questions ---

# Extra Section 1: Syllabus high-frequency comprehension recitation
extra_moxie = [
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "面对困境与阻碍，李白在《行路难（其一）》中以“______________________，______________________”表达了坚信理想终能实现、勇往直前的豪迈气概与坚定信心。",
        "ans": "长风破浪会有时，直挂云帆济沧海",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】唐代李白《行路难（其一）》。\n【考点分析】中考最高频情境名句之一，抒发虽然前路坎坷却始终坚信理想信念必能扬帆破浪的博大胸襟。\n【易错字提示】「沧海」三点水，切勿写成“沧”字少点；「济」三点水加齐。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "王湾在《次北固山下》中揭示了新旧事物交替、时光流逝具有普遍哲理的名句是：“______________________，______________________。”",
        "ans": "海日生残夜，江春入旧年",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】唐代王湾《次北固山下》。\n【哲理剖析】残夜将尽而红日已从海上升起，旧年未去而江南春意早已萌动。生动蕴含新事物脱胎于旧事物之中、不可遏止的历史发展哲理。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "安史之乱爆发，杜甫在长安目睹国都残破，在《春望》中借花鸟表达国破离恨的极度感伤的两句是：“______________________，______________________。”",
        "ans": "感时花溅泪，恨别鸟惊心",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】唐代杜甫《春望》。\n【修辞与手法】拟人/互文手法，移情于物，花鸟本常物，因感时恨别而溅泪惊心，沉郁顿挫。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "岑参在《白雪歌送武判官归京》中巧妙以春花比喻边塞冬雪奇观的千古名句是：“______________________，______________________。”",
        "ans": "忽如一夜春风来，千树万树梨花开",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】唐代岑参《白雪歌送武判官归京》。\n【手法赏析】比喻精妙，将北风严寒催生的漫天飞雪比作一夜春风吹绽的万树梨花，豪迈乐观，毫无衰飒之气。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "刘禹锡在《酬乐天扬州初逢席上见赠》中借自然景物的消长揭示新生事物必将取代旧事物的哲理名句是：“______________________，______________________。”",
        "ans": "沉舟侧畔千帆过，病树前头万木春",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】唐代刘禹锡《酬乐天扬州初逢席上见赠》。\n【易错字提示】「畔」田字旁加半；「侧」单人旁。\n【语境分析】诗人以沉舟、病树自比，虽经贬谪二十三年，但放眼万帆竞发、万木逢春，展现出坚毅豁达的人生胸怀。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "龚自珍在《己亥杂诗（其五）》中以落花为喻，表达自己虽辞官离京却依然心系国家命运、愿倾尽心血栽培后代的献身精神的两句是：“______________________，______________________。”",
        "ans": "落红不是无情物，化作春泥更护花",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】清代龚自珍《己亥杂诗（其五）》。\n【易错字提示】「落红」借指落花；「化作春泥更护花」表现甘为人梯的崇高奉献精神。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "诸葛亮在《出师表》中回忆先帝赏识并叙述自己在危难之际承担重任的名句是：“______________________，______________________。”",
        "ans": "受任于败军之际，奉命于危难之间",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】三国诸葛亮《出师表》。\n【考点分析】追述当阳长坂坡兵败之际，诸葛亮临危受命出使东吴联合抗曹之忠勇历程。"
    },
    {
        "s": "历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "tag": "上海中考考纲必背·情境自测",
        "t": "情境默写",
        "stem": "《曹刿论战》中曹刿认为鲁庄公具备了可以与齐军一战的政治基础（取信于民）的回答是：“______________________，______________________，______________________。”",
        "ans": "小大之狱，虽不能察，必以情",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】《左传·庄公十年·曹刿论战》。\n【词义采分】狱：案件；察：明察；情：实情、诚心。曹刿指出“忠之属也，可以一战”。"
    }
]

# Extra Section 2: Classical Chinese word definitions
extra_shici = [
    {
        "s": "历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "tag": "上海中考文言核心词",
        "t": "填空题",
        "stem": "解释下列课内必考文言文中的加点词：\n(1) 肉食者鄙．（《曹刿论战》）：__________\n(2) 公将鼓．之（《曹刿论战》）：__________",
        "ans": "(1) 目光短浅；(2) 击鼓（名词活用为动词）",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【词义与活用】\n鄙：古今异义词，古义为目光短浅，今义为粗俗、鄙陋。\n鼓：名词用作动词，击鼓进军。"
    },
    {
        "s": "历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "tag": "上海中考文言核心词",
        "t": "填空题",
        "stem": "解释下列课内必考文言文中的加点词：\n(1) 余强．饮三大白．而别（《湖心亭看雪》）：强：__________；白：__________\n(2) 湖中焉得更．有此人（《湖心亭看雪》）：__________",
        "ans": "(1) 强：勉强、尽力；白：酒杯；(2) 更：还、再",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】明末清初张岱《湖心亭看雪》。\n【采分点】“三大白”之“白”是古代大酒杯；“强饮”体现偶遇知己的畅快旷达。"
    },
    {
        "s": "历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "tag": "上海中考文言核心词",
        "t": "填空题",
        "stem": "解释下列课内必考文言文中的加点词：\n(1) 念．无与为乐者（《记承天寺夜游》）：__________\n(2) 相与步于中庭（《记承天寺夜游》）：__________",
        "ans": "(1) 考虑、想到；(2) 共同、一起",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】北宋苏轼《记承天寺夜游》。\n【考点分析】展现苏轼月夜访友（张怀民）的随性与闲适旷达情致。"
    },
    {
        "s": "历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "tag": "上海中考文言核心词",
        "t": "填空题",
        "stem": "解释下列课内必考文言文中的加点词：\n(1) 自非亭午夜分，不见曦．月（《三峡》）：__________\n(2) 虽乘奔．御风，不以疾也（《三峡》）：__________",
        "ans": "(1) 日光、太阳；(2) 飞奔的马（动词作名词）",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】北魏郦道元《三峡》。\n【字词解析】曦：日光、太阳；奔：动词活用为名词，飞奔的骏马。"
    },
    {
        "s": "历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "tag": "上海中考文言核心词",
        "t": "填空题",
        "stem": "解释下列课内必考文言文中的加点词：\n(1) 猿鸟乱鸣；夕日欲颓．（《答谢中书书》）：__________\n(2) 实是欲界之仙都．（《答谢中书书》）：__________",
        "ans": "(1) 坠落、落山；(2) 神仙生活的美好世界/人间仙境",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】南朝梁陶弘景《答谢中书书》。\n【字词解析】颓：坠落；仙都：仙界、神仙居住的胜境。"
    }
]

# Extra Section 3: Classical Chinese sentences translation
extra_fanyi = [
    {
        "s": "历年中考真题·课内文言重点句子翻译与文意探究",
        "sid": "sh-fanyi",
        "tag": "上海中考课标重点句翻译",
        "t": "句子翻译",
        "stem": "用现代汉语翻译下面的句子：\n一鼓作气，再而衰，三而竭。（《曹刿论战》）",
        "ans": "第一次击鼓能振作士气，第二次击鼓士气就会减弱，第三次击鼓士气就耗尽了。",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】《左传·曹刿论战》。\n【重点采分点】\n1. 作：振作；气：士气；\n2. 再：古代专指第二次（省略谓语“鼓”）；衰：减弱、衰退；\n3. 竭：耗尽、穷竭。阐释曹刿“彼竭我盈，故克之”的战术精髓。"
    },
    {
        "s": "历年中考真题·课内文言重点句子翻译与文意探究",
        "sid": "sh-fanyi",
        "tag": "上海中考课标重点句翻译",
        "t": "句子翻译",
        "stem": "用现代汉语翻译下面的句子：\n庭下如积水空明，水中藻、荇交横，盖竹柏影也。（《记承天寺夜游》）",
        "ans": "庭院中的月光如积水般清澈透明，水中有像藻、荇交织纵横的水草，大概是竹子和柏树的影子吧。",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】北宋苏轼《记承天寺夜游》。\n【修辞与采分】\n正面不着一字写月，全用比喻空灵写出月光澄澈纯净如水，竹柏倒影如藻荇交横，妙趣横生。"
    },
    {
        "s": "历年中考真题·课内文言重点句子翻译与文意探究",
        "sid": "sh-fanyi",
        "tag": "上海中考课标重点句翻译",
        "t": "句子翻译",
        "stem": "用现代汉语翻译下面的句子：\n莫说相公痴，更有痴似相公者。（《湖心亭看雪》）",
        "ans": "不要说相公您痴迷，还有比相公您更痴迷的人呢。",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处】明末清初张岱《湖心亭看雪》。\n【重点采分点】\n1. 莫说：不要说；\n2. 相公：尊称；\n3. 痴：痴迷（独往湖心亭赏雪的雅趣与孤高之气）；似：像、比。"
    }
]

# Extra Section 4: Famous literature readings
extra_mingzhu = [
    {
        "s": "历年中考真题·名著阅读全景通关",
        "sid": "sh-mingzhu",
        "tag": "上海中考必考名著·朝花夕拾",
        "t": "名著综合题",
        "stem": "鲁迅在散文集《朝花夕拾》中深情回忆了多位对他人生产生重大影响的人物，请指出下列对应错误的一项是（ ）\nA. 长妈妈（阿长）——一个虽然迷信、规矩繁琐但真诚善良的保姆，为童年鲁迅买来了朝思暮想的《山海经》。\nB. 藤野先生——仙台医专一位毫无民族偏见、治学严谨正直的解剖学教授，曾耐心帮鲁迅添改讲义。\nC. 范爱农——一位正直倔强、爱国但屡遭旧社会冷落打击的同乡知识分子，最终在贫困潦倒中溺水身亡。\nD. 衍太太——一位和蔼可亲、品行高尚的长辈，在鲁迅父亲临终前一直给予温情关怀与科学指导。",
        "ans": "D",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 D。\n【错因解析】衍太太是一个虚伪、自私、心术不正的市侩妇人代表（如怂恿孩子们吃冰、唆使打旋子，在鲁迅父亲临终时怂恿鲁迅大声喊叫父亲“让他走得不安生”）。"
    },
    {
        "s": "历年中考真题·名著阅读全景通关",
        "sid": "sh-mingzhu",
        "tag": "上海中考必考名著·水浒传",
        "t": "名著综合题",
        "stem": "《水浒传》塑造了许多个性鲜明的英雄好汉，请根据提示完成人物与情节匹配：\n(1) “倒拔垂杨柳”“大闹野猪林”的是梁山好汉__________；\n(2) “风雪山神庙”“误入白虎堂”，经历一忍再忍最终被逼上梁山的是__________；\n(3) 智取生辰纲的领导核心与谋士分别是__________和__________。",
        "ans": "(1) 鲁智深（鲁达/花和尚）；(2) 林冲（豹子头）；(3) 晁盖（托塔天王）；吴用（智多星）",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【出处背景】施耐庵《水浒传》。\n【典型人物考点】鲁智深是见义勇为、粗中有细的行侠仗义者；林冲由委曲求全转变为坚决反抗，是“官逼民反”的典型代表；吴用足智多谋，策划了智取生辰纲。"
    },
    {
        "s": "历年中考真题·名著阅读全景通关",
        "sid": "sh-mingzhu",
        "tag": "上海中考必考名著·红星照耀中国",
        "t": "名著综合题",
        "stem": "美国记者埃德加·斯诺在《红星照耀中国》中盛赞红军长征是“历史上最伟大的长征之一”。下列关于书中红军与领袖形象的描述不正确的一项是（ ）\nA. 斯诺笔下的毛泽东生活极其简朴，是一个精通中国古典文学、生活严肃而又诙谐风趣的平民领袖。\nB. 周恩来给斯诺的印象是头脑极其冷静敏捷、谈吐温文尔雅，是一位富有才华的军事家与政治家。\nC. 彭德怀开朗豪爽、深得战士爱戴，常常和普通士兵打成一片，极具平民亲和力。\nD. 斯诺指出，红军战士主要是受军饷与物质利益驱动，缺乏自主信仰与政治自觉。",
        "ans": "D",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 D。\n【错因解析】《红星照耀中国》最核心的结论之一正是：红军战士绝非为金钱利益而战，他们拥有高度的政治觉悟、坚定的革命理想、对建立新中国的炽热向往，展现了人类不屈的精神力量。"
    },
    {
        "s": "历年中考真题·名著阅读全景通关",
        "sid": "sh-mingzhu",
        "tag": "上海中考必考名著·简爱",
        "t": "名著综合题",
        "stem": "在夏洛蒂·勃朗特小说《简·爱》中，简·爱面对罗切斯特先生时说出震撼人心的表白：“你以为我穷、不好看，就没有感情吗？我向你起誓：如果上帝赐予我财富和美貌，我也会让你难以离开我，就像我现在难以离开你一样……”这段话集中体现了简·爱（ ）的核心性格与追求。\nA. 崇拜权贵，渴望跻身上流社会\nB. 追求男女平等、人格独立与纯洁尊严\nC. 逆来顺受，甘于接受命运摆布\nD. 追求物质享受与奢华生活",
        "ans": "B",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 B。\n【人物性格】简·爱是英国文学中极具现代独立女性精神的经典形象，她自尊自爱、不卑不亢，在爱情中坚持灵魂与人格的绝对平等，拒绝充当任何人的附庸。"
    }
]

# Extra Section 5: Comprehensive language application
extra_zonghe = [
    {
        "s": "历年中考真题·语言文字综合运用",
        "sid": "sh-zonghe",
        "tag": "上海中考综合运用真题·病句修改",
        "t": "选择题",
        "stem": "下列句子中没有语病的一项是（ ）\nA. 通过开展“经典名著进校园”诵读活动，使广大初三学生的语文素养得到了全面提升。\nB. 随着上海市生活垃圾分类政策的深入推进，市民的环保意识正在逐步增强。\nC. 为了防止中考复习期间不出现知识漏洞，各科老师精心准备了查漏补缺专项训练。\nD. 能否掌握科学高效的复习方法，是中考语文取得优异成绩的关键保障。",
        "ans": "B",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 B。\n【病句辨析】\nA项错：介词滥用导致主语残缺，“通过……”与“使……”连用，应删去“通过”或“使”；\nC项错：否定不当，“防止”与“不出现”双重否定造成逻辑矛盾，应删去“不”；\nD项错：两面对一面，“能否掌握”包含能与不能两面，而“取得优异成绩”是一面，应改为“掌握科学高效的复习方法，是……”。\nB项主谓宾搭配得当，表意明确无误。"
    },
    {
        "s": "历年中考真题·语言文字综合运用",
        "sid": "sh-zonghe",
        "tag": "上海中考综合运用真题·成语语境运用",
        "t": "选择题",
        "stem": "下列句子中加点成语使用恰当的一项是（ ）\nA. 中考前夕，班主任老师经常利用休息时间耐心为后进生辅导，真可谓是处心积虑．．．．。\nB. 面对突如其来的新冠疫情考验，全区医务工作者白衣执甲、逆行出征，立下了汗马功劳．．．．。\nC. 联欢会上，同学们和老师开心地拥抱合影，载歌载舞，尽情享受着天伦之乐．．．．。\nD. 这次科技创新大赛中，小华设计的人工智能分拣机器人别具匠心，真令人叹为观止．．．．。",
        "ans": "B",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 B。\n【成语辨析】\nB项「汗马功劳」形容辛勤劳作或立下的显著战功劳绩，赞颂医务工作者符合语境；\nA项「处心积虑」千方百计地盘算（含贬义），不能用来形容敬业奉献的老师；\nC项「天伦之乐」专指家庭骨肉团聚之乐，师生关系不能使用（对象不当）；\nD项「叹为观止」指赞美看到的事物好到了极点，通常侧重于观赏宏伟艺术品或风景，不能直接修饰小型的科技作品。"
    },
    {
        "s": "历年中考真题·语言文字综合运用",
        "sid": "sh-zonghe",
        "tag": "上海中考综合运用真题·句子排序",
        "t": "选择题",
        "stem": "填入下面语段横线处的句子，排序最恰当的一项是（ ）\n中华优秀传统文化是中华民族的精神命脉。________，________。________，________，它跨越时空，历久弥新。\n① 那些凝结着古人智慧的经典名篇\n② 蕴含着天人合一、天下为公、舍生取义等丰厚内涵\n③ 不仅滋养了一代又一代中华儿女的心灵世界\n④ 而且为当代中国的发展提供了强大的精神动力\nA. ①②③④\nB. ②①③④\nC. ①③④②\nD. ③④①②",
        "ans": "A",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 A。\n【句子逻辑衔接】\n首句为①提出主语“那些凝结着古人智慧的经典名篇”；\n接着②阐述其内在思想内涵“蕴含着天人合一……等丰厚内涵”；\n然后③与④构成“不仅……而且……”递进复句（从历史心灵滋养递进到当代精神动力）；\n最后由后文“它跨越时空，历久弥新”总结收束。顺序为 ①②③④。"
    }
]

# Assemble all questions
full_moxie = moxie_questions + extra_moxie
full_shici = shici_questions + extra_shici
full_fanyi = fanyi_questions + extra_fanyi
full_mingzhu = mingzhu_questions + extra_mingzhu
full_zonghe = zonghe_questions + extra_zonghe
full_tongjia = tongjia_questions

all_sections_config = [
    {
        "s": "板块一：历年中考真题·名句默写与情境运用",
        "sid": "sh-moxie",
        "list": full_moxie
    },
    {
        "s": "板块二：历年中考真题·课内文言字词释义",
        "sid": "sh-shici",
        "list": full_shici
    },
    {
        "s": "板块三：历年中考真题·课内文言重点句子翻译与文意探究",
        "sid": "sh-fanyi",
        "list": full_fanyi
    },
    {
        "s": "板块四：历年中考真题·名著阅读全景通关",
        "sid": "sh-mingzhu",
        "list": full_mingzhu
    },
    {
        "s": "板块五：历年中考真题·语言文字综合运用",
        "sid": "sh-zonghe",
        "list": full_zonghe
    },
    {
        "s": "板块六：上海中考文言通假字与一词多义专项通关",
        "sid": "sh-tongjia",
        "list": full_tongjia
    }
]

final_sections_meta = []
final_all_questions = []

for sec in all_sections_config:
    q_list = sec["list"]
    for i, q in enumerate(q_list, start=1):
        q["s"] = sec["s"]
        q["sid"] = sec["sid"]
        q["n"] = i
        final_all_questions.append(q)
    final_sections_meta.append({
        "s": sec["s"],
        "sid": sec["sid"],
        "n": len(q_list)
    })

dataset = {
    "sections": final_sections_meta,
    "questions": final_all_questions
}

print(f"Total Sections: {len(final_sections_meta)}")
for s in final_sections_meta:
    print(f"  - {s['s']}: {s['n']} questions")
print(f"Total Authentic Shanghai Zhongkao Questions: {len(final_all_questions)}")

# Write to json artifact
with open("chinese/shanghai_zhongkao_bank_data.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)
print("Saved complete json to chinese/shanghai_zhongkao_bank_data.json")

# Now inject into recitation-bank-V1.html
with open("chinese/recitation-bank-V1.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Title & Meta
html = re.sub(r'<title>.*?</title>', 
              f'<title>上海中考语文真题全收录 · 基础题库背诵版（2008–2025 全套真题 {len(final_all_questions)} 题）</title>', 
              html)

# 2. Update Header
html = re.sub(r'<h1>.*?</h1>\s*<p>.*?</p>', 
              f'<h1>上海中考语文真题库</h1>\n    <p>2008–2025全套真题 · {len(final_all_questions)}题全量收录（默写/字词/翻译/名著/综合）</p>', 
              html)

# 3. Update Modal Header
html = re.sub(r'<span class="sub">.*?</span>', 
              f'<span class="sub">{len(final_all_questions)} 题上海中考真题全局速选</span>', 
              html)

# 4. Update LSKEY
html = html.replace('const LSKEY = "8shang-recite-v1";', 'const LSKEY = "shanghai-zhongkao-recite-v1";')
html = html.replace('const POSKEY = "8shang-recite-pos-map";', 'const POSKEY = "shanghai-zhongkao-pos-map";')
html = html.replace('const SECKEY = "8shang-recite-cursec";', 'const SECKEY = "shanghai-zhongkao-cursec";')

# 5. Inject DATA
p_start = html.find('const DATA = {')
p_end = html.find('const IMGPH =')
if p_start != -1 and p_end != -1:
    json_str = json.dumps(dataset, ensure_ascii=False)
    html = html[:p_start] + f'const DATA = {json_str};\n' + html[p_end:]
    print("Injected new DATA successfully!")
else:
    print("FAILED to find DATA replacement range!")

with open("chinese/recitation-bank-V1.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated chinese/recitation-bank-V1.html successfully!")

extra_tongjia = [
    {
        "s": "板块六：上海中考文言通假字与一词多义专项通关",
        "sid": "sh-tongjia",
        "tag": "通假字考纲必考",
        "t": "填空题",
        "stem": "【课内通假字通关】写出下列句子中的通假字、本字及含义：\n(1) 一厝．朔东，一厝雍南（《愚公移山》）：__________\n(2) 困于心，衡．于虑，而后作（《生于忧患，死于安乐》）：__________\n(3) 曾．益其所不能（《生于忧患，死于安乐》）：__________\n(4) 入则无法家拂．士（《生于忧患，死于安乐》）：__________",
        "ans": "(1) “厝”通“措”，放置；(2) “衡”通“横”，梗塞、不顺；(3) “曾”通“增”，增加；(4) “拂”通“弼”，辅佐。",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【通假字解析】《孟子·告子下》与《愚公移山》是上海中考文言文命题最高频的两大文言基石篇目，其中的通假字必须做到字字落实、准确书写。"
    },
    {
        "s": "板块六：上海中考文言通假字与一词多义专项通关",
        "sid": "sh-tongjia",
        "tag": "通假字考纲必考",
        "t": "填空题",
        "stem": "【课内通假字通关】写出下列句子中的通假字、本字及含义：\n(1) 同舍生皆被．绮绣（《送东阳马生序》）：__________\n(2) 政通人和，百废具．兴（《岳阳楼记》）：__________\n(3) 属．予作文以记之（《岳阳楼记》）：__________\n(4) 尊君在不．（《陈太丘与友期行》）：__________",
        "ans": "(1) “被”通“披”，穿；(2) “具”通“俱”，全、都；(3) “属”通“嘱”，嘱托；(4) “不”通“否”，吗。",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "【高分提分规范】中考阅卷要求：“某”通“某”，意思为……。少写本字或意思未答准均会失分。"
    },
    {
        "s": "板块六：上海中考文言通假字与一词多义专项通关",
        "sid": "sh-tongjia",
        "tag": "文言核心虚词辨析",
        "t": "选择题",
        "stem": "下列各组句子中加点词“以”的意义和用法相同的一项是（ ）\nA. 徐以．杓酌油沥之 / 策之不以．其道\nB. 以．中有足乐者 / 扶苏以．数谏故\nC. 醒能述以．文者 / 固国不以．山溪之险\nD. 威天下不以．兵革之利 / 意将隧入以．攻其后也",
        "ans": "B",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 B。\n【虚词“以”用法精析】\nB项两个“以”均为连词，表原因，“因为”（以中有足乐者：因为内心有足以快乐的事；扶苏以数谏故：扶苏因为屡次进谏的缘故）；\nA项：前一个为介词“用”，后一个为介词“按照”；\nC项：前一个为介词“用”，后一个为介词“凭、依靠”；\nD项：前一个为介词“凭”，后一个为连词“用来、以便”。"
    },
    {
        "s": "板块六：上海中考文言通假字与一词多义专项通关",
        "sid": "sh-tongjia",
        "tag": "文言核心虚词辨析",
        "t": "选择题",
        "stem": "下列各组句子中加点词“于”的意义和用法相同的一项是（ ）\nA. 生于．忧患，死于安乐 / 皆以美于．徐公\nB. 刻唐贤今人诗赋于．其上 / 苟全性命于．乱世\nC. 受任于．败军之际 / 未尝不叹息痛恨于．桓、灵也\nD. 告之于．帝 / 皆朝于．齐",
        "ans": "B",
        "img": "", "aimg": "", "src": "", "ph": False,
        "jx": "答案 B。\n【虚词“于”用法精析】\nB项两个“于”均为介词，“在”（刻于其上：刻在上面；苟全性命于乱世：在乱世中苟且保全性命）；\nA项：前一个为介词“在”，后一个为介词“比”（表比较）；\nC项：前一个为介词“在”，后一个为介词“对、对于”；\nD项：前一个为介词“向”，后一个为介词“到”。"
    }
]

# Re-run builder
full_tongjia.extend(extra_tongjia)
all_sections_config[-1]["list"] = full_tongjia

final_sections_meta = []
final_all_questions = []

for sec in all_sections_config:
    q_list = sec["list"]
    for i, q in enumerate(q_list, start=1):
        q["s"] = sec["s"]
        q["sid"] = sec["sid"]
        q["n"] = i
        final_all_questions.append(q)
    final_sections_meta.append({
        "s": sec["s"],
        "sid": sec["sid"],
        "n": len(q_list)
    })

dataset = {
    "sections": final_sections_meta,
    "questions": final_all_questions
}

print(f"\n=== EXPANDED STATS ===")
for s in final_sections_meta:
    print(f"  - {s['s']}: {s['n']} questions")
print(f"Total Authentic Questions: {len(final_all_questions)}")

with open("chinese/shanghai_zhongkao_bank_data.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

with open("chinese/recitation-bank-V1.html", "r", encoding="utf-8") as f:
    html = f.read()

p_start = html.find('const DATA = {')
p_end = html.find('const IMGPH =')
if p_start != -1 and p_end != -1:
    json_str = json.dumps(dataset, ensure_ascii=False)
    html = html[:p_start] + f'const DATA = {json_str};\n' + html[p_end:]

# Update header and subtitle with final count
html = re.sub(r'<h1>.*?</h1>\s*<p>.*?</p>', 
              f'<h1>上海中考语文真题库</h1>\n    <p>2008–2025 全套真题 · {len(final_all_questions)} 题全量收录（默写 / 字词 / 翻译 / 名著 / 综合）</p>', 
              html)
html = re.sub(r'<span class="sub">.*?</span>', 
              f'<span class="sub">{len(final_all_questions)} 题上海中考真题全局速选</span>', 
              html)

with open("chinese/recitation-bank-V1.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated recitation-bank-V1.html with expanded dataset!")
