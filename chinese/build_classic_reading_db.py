import json
import re
import os

with open('/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-ocr-raw-V1.json', 'r', encoding='utf-8') as f:
    raw_pages = json.load(f)

# 1. 过滤垃圾广告字符
def clean_lines(lines):
    cleaned = []
    for line in lines:
        l = line.strip()
        if not l:
            continue
        if '更多课程资料添加小百' in l or 'kshxjh888' in l:
            continue
        if re.search(r'^第\s*\d+\s*页[，,\s]*共\s*39\s*页', l):
            continue
        cleaned.append(l)
    return cleaned

cleaned_pages = {}
for p in raw_pages:
    num = p['page']
    cleaned_pages[num] = clean_lines(p['lines'])

# 书籍对应页码定义
books_meta = [
    {
        "id": "tongnian",
        "index": "一",
        "title": "《童年》",
        "subtitle": "培养良好的阅读习惯",
        "grade": "七下",
        "category": "外国名著 · 自传体",
        "pages": [1, 2, 3],
        "author": "高尔基",
        "author_desc": "苏联伟大的无产阶级作家，社会主义、现实主义文学的奠基人，无产阶级革命文学导师，苏联文学的创始人，列宁称他为“无产阶级艺术最杰出的代表”。代表作有以自身经历为原型创作的自传体小说三部曲《童年》《在人间》《我的大学》。",
        "badge": "重点考点"
    },
    {
        "id": "lubinxun",
        "index": "二",
        "title": "《鲁滨逊漂流记》",
        "subtitle": "张开想象的翅膀",
        "grade": "七下",
        "category": "外国名著 · 冒险小说",
        "pages": [3, 4, 5],
        "author": "丹尼尔·笛福",
        "author_desc": "18世纪英国启蒙时期的现实主义小说家，被誉为“英国小说之父”“英国散文之父”。代表作《鲁滨逊漂流记》开创了英国现实主义小说的先河。",
        "badge": "常考名著"
    },
    {
        "id": "zhaohuaxishi",
        "index": "三",
        "title": "《朝花夕拾》",
        "subtitle": "消除与经典的隔膜",
        "grade": "七上",
        "category": "现代名著 · 回忆性散文",
        "pages": [5, 6, 7, 8],
        "author": "鲁迅",
        "author_desc": "原名周树人，字豫才，浙江绍兴人。伟大的文学家、思想家、革命家，中国现代文学的奠基人。代表作有小说集《呐喊》《彷徨》《故事新编》，散文集《朝花夕拾》，散文诗集《野草》，杂文集《坟》《热风》等。",
        "badge": "中考必考"
    },
    {
        "id": "xiyouji",
        "index": "四",
        "title": "《西游记》",
        "subtitle": "精读和跳读",
        "grade": "七上",
        "category": "古典小说 · 古典神魔",
        "pages": [8, 9, 10, 11, 12],
        "author": "吴承恩",
        "author_desc": "字汝忠，号射阳山人，淮安府山阳县（今江苏省淮安市淮安区）人，明代杰出小说家。",
        "badge": "中考高频"
    },
    {
        "id": "luotuoxiangzi",
        "index": "五",
        "title": "《骆驼祥子》",
        "subtitle": "圈点与批注",
        "grade": "七下",
        "category": "现代名著 · 现实主义",
        "pages": [12, 13],
        "author": "老舍",
        "author_desc": "原名舒庆春，字舍予，北京人，满族。中国现代著名小说家、剧作家，被誉为“人民艺术家”。代表作有长篇小说《骆驼祥子》《四世同堂》，话剧《茶馆》《龙须沟》等。",
        "badge": "中考高频"
    },
    {
        "id": "haidiliangwanli",
        "index": "六",
        "title": "《海底两万里》",
        "subtitle": "快速阅读",
        "grade": "七下",
        "category": "外国名著 · 科幻小说",
        "pages": [12, 13, 14],
        "author": "儒勒·凡尔纳",
        "author_desc": "19世纪法国著名科幻小说家、剧作家，被誉为“科幻小说之父”。凡尔纳“凡尔纳三部曲”包括《格兰特船长的儿女》《海底两万里》《神秘岛》。",
        "badge": "常考名著"
    },
    {
        "id": "hongxingzhaoyao",
        "index": "七",
        "title": "《红星照耀中国》",
        "subtitle": "纪实作品的阅读",
        "grade": "八上",
        "category": "纪实文学 · 红色经典",
        "pages": [14, 15],
        "author": "埃德加·斯诺",
        "author_desc": "美国著名记者、作家。1936年夏访问陕甘宁边区，成为第一个采访红区的西方记者。代表作有《红星照耀中国》《远东前线》《活的中国》等。",
        "badge": "中考必考"
    },
    {
        "id": "kunchongji",
        "index": "八",
        "title": "《昆虫记》",
        "subtitle": "科普作品的阅读",
        "grade": "八上",
        "category": "科普作品 · 自然科学",
        "pages": [15, 16],
        "author": "让-亨利·卡西米尔·法布尔",
        "author_desc": "法国著名昆虫学家、文学家。被世人称为“昆虫界的荷马”“昆虫界的维吉尔”，雨果称其为“昆虫世界的荷马”。",
        "badge": "中考必考"
    },
    {
        "id": "jingdianchangtan",
        "index": "九",
        "title": "《经典常谈》",
        "subtitle": "选择性阅读",
        "grade": "八下",
        "category": "文化经典 · 学术通俗",
        "pages": [16, 17, 18, 19],
        "author": "朱自清",
        "author_desc": "字佩弦，号秋实，现代著名散文家、诗人、学者、民主战士。代表作有诗文集《踪迹》，散文集《背影》《欧游杂记》，学术著作《经典常谈》等。",
        "badge": "中考高频"
    },
    {
        "id": "gangtieshi",
        "index": "十",
        "title": "《钢铁是怎样炼成的》",
        "subtitle": "摘抄和做笔记",
        "grade": "八下",
        "category": "外国名著 · 革命励志",
        "pages": [19, 20],
        "author": "尼古拉·奥斯特洛夫斯基",
        "author_desc": "苏联著名无产阶级作家。以顽强毅力战胜瘫痪失明，创作出这部闪耀崇高理想主义光芒的自传体巨著。",
        "badge": "常考名著"
    },
    {
        "id": "aiqingshixuan",
        "index": "十一",
        "title": "《艾青诗选》",
        "subtitle": "如何读诗",
        "grade": "九上",
        "category": "现代诗歌 · 经典诗选",
        "pages": [20, 21],
        "author": "艾青",
        "author_desc": "原名蒋正涵，号海澄，笔名莪加、克阿等。中国现当代文学史上的著名诗人。主要意象：土地与光明。",
        "badge": "中考高频"
    },
    {
        "id": "shuihuzhuan",
        "index": "十二",
        "title": "《水浒传》",
        "subtitle": "古典小说的阅读",
        "grade": "九上",
        "category": "古典小说 · 章回演义",
        "pages": [22, 23, 24, 25],
        "author": "施耐庵",
        "author_desc": "元末明初著名小说家。《水浒传》是中国历史上第一部用白话文写成的章回体长篇英雄传奇小说。",
        "badge": "中考核心"
    },
    {
        "id": "rulinwaishi",
        "index": "十三",
        "title": "《儒林外史》",
        "subtitle": "讽刺作品的阅读",
        "grade": "九上",
        "category": "古典小说 · 讽刺名著",
        "pages": [25, 26, 27, 28],
        "author": "吴敬梓",
        "author_desc": "字敏轩，一字文木，号粒民，安徽全椒人，清代著名小说家。《儒林外史》开创了中国讽刺小说的先河。",
        "badge": "中考核心"
    },
    {
        "id": "jianai",
        "index": "十四",
        "title": "《简·爱》",
        "subtitle": "外国小说的阅读",
        "grade": "九下",
        "category": "外国名著 · 女性成长",
        "pages": [28],
        "author": "夏洛蒂·勃朗特",
        "author_desc": "19世纪英国著名女作家，与妹妹艾米莉·勃朗特、安妮·勃朗特并称为“勃朗特三姐妹”。代表作《简·爱》。",
        "badge": "常考名著"
    },
    {
        "id": "hongyan",
        "index": "八上新增",
        "title": "《红岩》",
        "subtitle": "红色经典的阅读（新教材新增）",
        "grade": "八上新增",
        "category": "红色经典 · 革命长篇",
        "pages": [29, 30, 31, 32, 33, 34],
        "author": "罗广斌、杨益言",
        "author_desc": "现代著名作家，均曾被国民党反动派逮捕并囚禁于重庆中美合作所渣滓洞集中营，是狱中斗争的幸存者与见证人。",
        "badge": "统编新考点"
    },
    {
        "id": "tangshisanbaishou",
        "index": "九上新增",
        "title": "《唐诗三百首》",
        "subtitle": "古典诗歌的阅读（新教材新增）",
        "grade": "九上新增",
        "category": "古典诗歌 · 诗歌总集",
        "pages": [35, 36, 37, 38, 39],
        "author": "孙洙（蘅塘退士 选编）",
        "author_desc": "清代江苏无锡人，字临飞，号蘅塘退士。于乾隆二十九年（1764）编成《唐诗三百首》，选入77位唐代诗人310余首诗作。",
        "badge": "统编新考点"
    }
]

# 将各页内容整合进每部名著
books_data = []
for b in books_meta:
    book_pages = []
    full_text_list = []
    for p_num in b["pages"]:
        lines = cleaned_pages.get(p_num, [])
        book_pages.append({
            "page_num": p_num,
            "image": f"images/classic-reading/page-{p_num:02d}.jpg",
            "lines": lines
        })
        full_text_list.extend(lines)
    
    b_data = dict(b)
    b_data["pages_data"] = book_pages
    b_data["full_text"] = "\n".join(full_text_list)
    books_data.append(b_data)

output_path = '/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-data-V1.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        "version": "V1",
        "title": "初中语文中考名著阅读核心考点整理（39页全真提取）",
        "totalPages": 39,
        "totalBooks": len(books_data),
        "books": books_data
    }, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {output_path} with {len(books_data)} books and 39 pages!")
