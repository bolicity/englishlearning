#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""鲁滨逊重画：33 格 → 9 张 2×2 母图（每母图右下格去水印）。
键直接写页面引用的最终文件名。"""
import json

STYLE = "中国传统水墨连环画风格，工笔线描加淡彩，米白色宣纸底色"
LB = "主角鲁滨逊是白种人英国男子，深棕卷发，高鼻深目，落难时穿破旧的亚麻衬衫马甲长裤长靴；热带加勒比荒岛场景（棕榈、海滩、山岩）"
ALONE = "画面中只有鲁滨逊一个人，岛上绝无他人"

GROUPS = [
    # r05 整行重画（原多人）
    {'mu': 'mu-lub-re1', 'quads': ['et-lubinxun-r05', 'et-lubinxun-r05-b2', 'et-lubinxun-r05-b3', 'et-lubinxun-r05-b4'],
     'scenes': [f"鲁滨逊独自在海边山坡搭起帐篷、立起木桩搭建住所；{ALONE}",
                f"鲁滨逊独自削尖木桩，沿帐篷外围一圈圈打进围栏桩；{ALONE}",
                f"鲁滨逊独自在山岩边挥镐凿洞，把家当搬进山洞作居所；{ALONE}",
                f"鲁滨逊独自用简陋工具刨木做桌椅，旁边火堆上烤着猎来的野味；{ALONE}"],
     'bg': "1659年荒岛，" },
    # r08 整行重画（原东亚女性化）
    {'mu': 'mu-lub-re2', 'quads': ['et-lubinxun-r08', 'et-lubinxun-r08-b2', 'et-lubinxun-r08-b3', 'et-lubinxun-r08-b4'],
     'scenes': [f"鲁滨逊独自用木栅栏把山坡圈成羊圈，圈住驯化的野羊群；{ALONE}",
                f"鲁滨逊独自把一只受伤瘸腿的小山羊抱回家，小心搀扶；{ALONE}",
                f"鲁滨逊独自蹲在棚下给小山羊的伤腿包扎、喂食，伤腿渐渐长好；{ALONE}",
                f"鲁滨逊独自站在木栅栏围起的牧场边，看繁殖起来的成群山羊；{ALONE}"],
     'bg': "1659年荒岛，" },
    # r14 整行重画（b1空白+东亚水手）
    {'mu': 'mu-lub-re3', 'quads': ['et-lubinxun-r14', 'et-lubinxun-r14-b2', 'et-lubinxun-r14-b3', 'et-lubinxun-r14-b4'],
     'scenes': ["一艘英国大商船停泊在岛边海湾，鲁滨逊与野人星期五、获救的英国船长一起登上大船准备启航",
                "英国商船甲板上一群英国水手因叛乱争吵扭打，场面混乱",
                "鲁滨逊与星期五协助忠诚的船长制服叛乱水手，叛徒被捆缚押跪甲板",
                "大船扬帆远航，鲁滨逊独立船头眺望大海，结束了二十八年的荒岛生活"],
     'bg': "1686年加勒比海，" },
    # r02-b3/b4 + r03-b2/b3
    {'mu': 'mu-lub-re4', 'quads': ['et-lubinxun-r02-b3', 'et-lubinxun-r02-b4', 'et-lubinxun-r03-b2', 'et-lubinxun-r03-b3'],
     'scenes': ["非洲海岸，年轻的英国水手鲁滨逊与当地黑人用手指点货物，在沙滩上以物易物",
                "商栈账房里，鲁滨逊在桌上清点金砂和象牙，满箱货物，心满意足",
                "北非海盗船突然逼近商船，摩尔人海盗挥刀跳帮登船，水手们四散奔逃",
                "鲁滨逊沦为摩尔人家的奴隶，戴着脚镣在庭院里做苦工，神情屈辱"],
     'bg': "1650年代非洲贸易航路，" },
    # r03-b4 + r04-b2/b3/b4
    {'mu': 'mu-lub-re5', 'quads': ['et-lubinxun-r03-b4', 'et-lubinxun-r04-b2', 'et-lubinxun-r04-b3', 'et-lubinxun-r04-b4'],
     'scenes': ["鲁滨逊与一个男孩乘一叶小舢板趁夜逃亡，两人在海上奋力划桨",
                "贩奴途中风暴骤起，大帆船撞上礁石断裂，英国水手们在惊涛骇浪中挣扎",
                "巨浪掀起，落水的同伴水手被浪吞没，鲁滨逊抱着木板在浪里浮沉",
                "鲁滨逊独自被海浪冲上荒岛沙滩，瘫坐岸边，身后只有搁浅的破船残骸，四野无人"],
     'bg': "1650年代大西洋航路，" },
    # r09-b2/b4 + r10-b2/b3
    {'mu': 'mu-lub-re6', 'quads': ['et-lubinxun-r09-b2', 'et-lubinxun-r09-b4', 'et-lubinxun-r10-b2', 'et-lubinxun-r10-b3'],
     'scenes': [f"鲁滨逊独自把大麦稻穗上的谷粒抖进陶罐，收集种子准备播种；{ALONE}",
                f"雨季里鲁滨逊独自冒雨在田垄间补播种子，嫩绿的麦苗已整齐抽芽；{ALONE}",
                f"鲁滨逊独自在河边挖黏土，双手捏制陶坯，一排泥坯晾在木板上；{ALONE}",
                f"鲁滨逊独自往土窑里堆柴烧火，火光映脸，专心烧制陶器；{ALONE}"],
     'bg': "1659年荒岛，" },
    # r10-b4 + r11-b2/b3/b4
    {'mu': 'mu-lub-re7', 'quads': ['et-lubinxun-r10-b4', 'et-lubinxun-r11-b2', 'et-lubinxun-r11-b3', 'et-lubinxun-r11-b4'],
     'scenes': [f"鲁滨逊独自从窑中捧出刚烧成的瓦锅瓦罐，对着天光端详，喜出望外；{ALONE}",
                f"鲁滨逊独自用石臼捣麦，用围巾和羽毛做成简陋的筛子筛面粉；{ALONE}",
                f"鲁滨逊独自砌起方砖炉子生火，把面团送进炉膛烘烤；{ALONE}",
                f"鲁滨逊独自捧着刚烤好的大麦面包，热气腾腾，满脸欢喜；{ALONE}"],
     'bg': "1659年荒岛，" },
    # r11 完成后 r12-b2/b3/b4 + r06-b2
    {'mu': 'mu-lub-re8', 'quads': ['et-lubinxun-r12-b2', 'et-lubinxun-r12-b3', 'et-lubinxun-r12-b4', 'et-lubinxun-r06-b2'],
     'scenes': ["鲁滨逊与野人星期五两人一起加固城堡木栅栏、检查火枪弹药，警惕四周",
                "鲁滨逊与星期五持枪冲向海滩上野人的人肉宴席，开火救人，野人四散奔逃",
                "鲁滨逊打手势教获救的野人说话，指着太阳教他说Friday，野人跪地感恩",
                f"鲁滨逊独自在木柱上刻下上岸日期的记号，做历法计时；{ALONE}"],
     'bg': "1680年代荒岛，" },
]

m = {'groups': [], 'singles': [
    {'img': 'et-lubinxun-r07-b4',
     'scene': f"鲁滨逊独自在窝棚的草铺上安然睡醒坐起，神清气爽，久病初愈恢复体力；{ALONE}",
     'bg': "1659年荒岛窝棚内，"}]}

for i, g in enumerate(GROUPS, 1):
    tok = f"鲁重画{i:02d}"
    parts = "；".join(f"{['左上格','右上格','左下格','右下格'][j]}：{s}" for j, s in enumerate(g['scenes']))
    prompt = (f"{tok}：{STYLE}。2×2四格布局，四格之间用细墨线分隔，每格一个完整场景，四格各自独立成画。"
              f"{g['bg']}{LB}。{parts}。画面中不出现任何文字或水印。")
    m['groups'].append({'mu': g['mu'], 'token': tok, 'prompt': prompt, 'quads': g['quads']})

s = m['singles'][0]
s['token'] = '鲁重画09'
s['prompt'] = (f"鲁重画09：{STYLE}。单幅完整画面。1659年荒岛窝棚内，{LB}。{s['scene']}。"
               f"画面中不出现任何文字或水印。")

json.dump(m, open('/tmp/lubin_redraw_manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = sum(len(g['quads']) for g in m['groups']) + len(m['singles'])
print(f"母图 {len(m['groups'])} 张 + 单图 {len(m['singles'])} = {n} 格")
