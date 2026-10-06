#!/usr/bin/env python3
"""新版 classic-reading-V4（静态表格版）挂载连环画。

- 人物表（row4）：每行 <tr> 后插 4 格 comic-row，复用已有 76 人图 + 8 位新画；
- 叙事表 / 雅号表（gallery）：表后插整条画廊，每行 1 格；
- 灯箱复用页面已有 openModal()。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST = ROOT / 'chinese' / 'classic-reading-V4.html'
IMG = 'images/classic-comics'

def c4(base, caps, imgs=None):
    return {'imgs': imgs or [f'{IMG}/{base}-c{i}.jpg' for i in range(1, 5)], 'caps': caps}

def ru(base, caps):
    return c4(base, caps, imgs=[f'images/{base}-c{i}.jpg' for i in range(1, 5)])

# ------------------------------------------------- 人物表（每行 4 格）
ROW4 = {
    '主要人物典型情节与人物形象对照表': [   # 童年
        c4('tongnian-alisha', ['①随母投奔外祖父家', '②看清人性善恶', '③学校受刁难结友', '④母亲病逝走向人间']),
        c4('tongnian-waizu', ['①火中抢出硫酸盐桶', '②挺身拦住受惊的马', '③灯下讲优美的民间故事', '④忍受打骂虔诚祈祷']),
        c4('waizufu', ['①执皮鞭抽打孩子', '②吝啬成性刻薄寡恩', '③破产分家赶走亲人', '④病榻前讲纤夫往事']),
        c4('haoshiqing', ['①贫困房客潜心实验', '②被小市民视为异端', '③教阿廖沙观察生活', '④被外祖父强行赶走']),
        c4('lianggejiujiu', ['①为争家产互相殴斗', '②逼母亲放弃嫁妆', '③戏弄盲眼工匠', '④酿成小茨冈惨死']),
        c4('xiaocigang', ['①弃儿被外祖母收养', '②伸臂替阿廖沙挡鞭', '③深得外祖父赏识', '④背负十字架惨死']),
    ],
    '六大核心人物外貌、典型情节与形象辨识表': [  # 朝花夕拾
        c4('shoujingwu', ['①方正质朴博学长者', '②待学生严格有风范', '③读书入迷摇头晃脑', '④备戒尺却极少罚人']),
        c4('yantaitai', ['①怂恿孩子冬天吃冰', '②唆使偷母亲首饰', '③暗中散布流言', '④临终催促呼喊父亲']),
        c4('tengye', ['①黑瘦八字须不修边幅', '②红笔逐字添改讲义', '③关心解剖实习', '④赠照片背面题惜别']),
        c4('achang', ['①睡觉摆大字切切察察', '②满口繁琐年节规矩', '③踩死隐鼠低头隐瞒', '④捧来心爱的山海经']),
        c4('shaoyimingyi', ['①圆胖名医出门应诊', '②长胖名医故弄玄虚', '③药引奇特蟋蟀成对', '④庸医误人父亲病故']),
        c4('fanainong', ['①横滨初识生误会', '②回国受排挤困顿', '③光复后任学监遭压', '④借酒浇愁溺水亡']),
    ],
    '师徒四人及白龙马全景辨识表': [
        c4('wukong', ['①大闹天宫战天兵', '②三打白骨精遭逐', '③车迟国斗法除三妖', '④三借芭蕉扇灭火']),
        c4('tangseng', ['①受重托单骑西行', '②四圣试禅心不改', '③误信白骨精逐悟空', '④女儿国坚守佛心']),
        c4('bajie', ['①高老庄做农活招赘', '②偷吃人参果', '③进谗言害悟空被逐', '④流沙河红孩儿出死力']),
        c4('shaseng', ['①流沙河受点化归依', '②一路牵马挑担', '③宝象国苦谏迎悟空', '④赴南海求证真假']),
        c4('bailongma', ['①纵火犯天条待罪', '②化白马代步西行', '③变身刺杀黄袍怪', '④催促八戒迎师兄']),
    ],
    '《骆驼祥子》主要人物辨识表': [
        c4('xiangzi', ['①健壮车夫拼命拉车', '②买上新车笑得灿烂', '③遭抢后苦撑善待雇主', '④叼烟颓然走向堕落']),
        c4('huniu', ['①车厂拨算盘掌账', '②假称有孕设计逼婚', '③闹翻置办二手洋车', '④难产卧床痛苦死去']),
        c4('liusiye', ['①地痞起家开车厂', '②放高利贷剥削车夫', '③与虎妞决裂卖厂', '④晚年孤老遭嘲弄']),
        c4('xiaofuzi', ['①贫苦温顺的弱女', '②被父亲卖与军官', '③为养幼弟被迫卖身', '④不堪重压上吊自尽']),
        c4('caoxiansheng', ['①社会改良知识分子', '②待祥子如家人', '③绝境中答应收留', '④遭告密离北平避难']),
    ],
    '四大核心人物形象表': [
        c4('nimo', ['①驾驭诺第留斯号', '②斗鲨救采珠人赠珍珠', '③海底财宝支援义军', '④驾艇撞沉殖民战舰']),
        c4('alongnasi', ['①追海怪落水被俘', '②舷窗观察海洋生物', '③埋头记录科考笔记', '④策划乘小艇出逃']),
        c4('kangsai', ['①教授的忠诚仆人', '②随主跳入冰海', '③精通生物分类', '④冷静归纳科属种']),
        c4('nidelan', ['①加拿大捕鲸高手', '②一标枪救船长', '③思念陆地自由', '④大漩涡中生还']),
    ],
    '领袖与红军英雄群像辨识表': [
        c4('maozedong', ['①窑洞油灯秉烛长谈', '②穿打补丁的旧军服', '③与战士同吃小米饭', '④谈笑风生手势从容']),
        c4('zhouenlai', ['①百家坪会见斯诺', '②流利英语交谈', '③开列全套访问日程', '④举止优雅军纪严明']),
        c4('pengdehuai', ['①与战士赤脚打篮球', '②战壕前指挥若定', '③仅有两套统一制服', '④降落伞改成背心穿']),
        c4('helong', ['①两把菜刀闹革命', '②带兵有方体魄过人', '③深受部下百姓爱戴', '④少数民族地区威望高']),
        c4('zude', ['①讲武堂出身的名将', '②与士兵同挑粮共苦', '③爱打篮球天性活跃', '④窑洞向斯诺自述身世']),
        c4('hongxiaogui', ['①平均二十岁的战士', '②艰苦中保持乐观', '③严守纪律拒收小费', '④长征途中视死如归']),
    ],
    '典型昆虫形态习性与人性化评价全景表': [
        c4('tanglang', ['①张开纱翅威吓敌人', '②举镰前臂伏击猎物', '③迅猛捕食蝗虫', '④草叶间雌雄相会']),
        c4('chan', ['①地下蛹伏黑暗四年', '②金蝉脱壳攀上枝头', '③尖喙刺皮吸食树汁', '④蚂蚁成群围抢撕咬']),
        c4('xishuai', ['①向阳斜坡挖洞穴', '②洞前设精致前庭', '③绝不寄人篱下', '④入夜振翅鸣唱']),
        c4('yinghuochong', ['①尾部柔和荧光', '②袭击蜗牛', '③喷射麻醉毒液', '④分解吸食猎物']),
        c4('huangfeng', ['①腰细色艳腹藏毒针', '②纸浆筑巢巧匠', '③捕猎麻醉毛虫', '④群居护巢井然有序']),
        c4('shengqianglang', ['①体黑如炭额生齿铲', '②奋力推滚粪球', '③地下储粮育幼虫', '④勤劳的自然清道夫']),
        c4('hongmayi', ['①红褐体色巨颚獠牙', '②远征抢劫黑蚁蛹', '③只认来路原途返', '④凭记忆指路归巢']),
    ],
    '《钢铁是怎样炼成的》主要人物辨识表': [
        c4('baoer', ['①少年智救朱赫来', '②战场冲锋死里逃生', '③严冬筑路带病苦干', '④病榻口述写成小说']),
        c4('zhulai', ['①水兵装束地下工作', '②教保尔练习拳击', '③被押途中获救', '④政委关怀保尔成长']),
        c4('dongniya', ['①林务官的女儿', '②借书指导保尔', '③留恋小资享乐', '④阶级鸿沟决裂']),
        c4('lida', ['①团省委常委', '②战友与精神伴侣', '③误闻死讯另嫁', '④重逢互勉敬重']),
        c4('daya', ['①遭虐待的房东女儿', '②保尔助其独立', '③结为革命伴侣', '④入党并助创作']),
    ],
    '梁山五大核心好汉典型回目及性格对照全景表': [
        c4('luzhishen', ['①三拳打死镇关西', '②五台山醉打金刚', '③倒拔垂杨柳', '④野猪林抡杖救林冲']),
        c4('linchong', ['①误入白虎堂遭陷', '②刺配沧州受折磨', '③风雪山神庙复仇', '④雪夜投奔上梁山']),
        c4('songjiang', ['①飞马私放晁盖', '②怒杀阎婆惜', '③浔阳楼题反诗', '④力主招安终饮鸩']),
        c4('wusong', ['①景阳冈赤手打虎', '②斗杀西门庆', '③醉打蒋门神', '④血溅鸳鸯楼']),
        c4('likui', ['①江州劫法场', '②沂岭怒杀四虎', '③痛打假李逵', '④赠银放行李鬼']),
        c4('wuyong', ['①智取生辰纲献计', '②巧计赚卢俊义上山', '③军师运筹帷幄', '④宋江墓前自缢尽忠']),
    ],
    '四大类型典型人物与情节讽刺全景表': [
        ru('rulinwaishi-p4-zhoujin', ['①六旬仍是老童生', '②塾中受尽冷遇', '③撞号板痛哭吐血', '④捐监后中举升官']),
        ru('rulinwaishi-p4-fanjin', ['①五十四岁才中秀才', '②瞒着岳父乡试中举', '③看榜狂喜痰迷发疯', '④一记耳光方才清醒']),
        ru('rulinwaishi-p1-yanjiansheng', ['①病榻垂危竖两指', '②亲人纷纷猜不透', '③挑掉一根灯草', '④点头咽气吝啬至终']),
        c4('yangongsheng', ['①云片糕讹诈船家', '②赖掉船钱扬长去', '③弟尸未寒谋夺家产', '④恶霸劣绅嘴脸尽显']),
        c4('kuangchaoren', ['①流落杭州孝养病父', '②灯下勤奋读书', '③结识马二先生', '④充枪手堕落下场']),
        ru('rulinwaishi-p1-wangmian', ['①母子相依勤学画荷', '②淡泊名利拒做官', '③危机中指点时务', '④隐居会稽山终老']),
        c4('dushaoqing', ['①蔑视八股科举', '②装病拒朝廷征召', '③挥金资助穷友', '④携妻游山饮酒']),
    ],
    '英雄群像谱与典型情节全景表': [
        c4('jiangjie', ['①忍痛奔赴华蓥山', '②被捕押入渣滓洞', '③竹签钉指宁死不屈', '④狱中密绣五星红旗']),
        c4('xuyunfeng', ['①识破特务阴谋', '②掩护同志不幸被捕', '③痛斥特务头子', '④十指抠出越狱通道']),
        c4('chenggang', ['①秘密承印挺进报', '②被捕身受酷刑', '③粉碎测谎逼供', '④放声嘲笑敌人无能']),
        c4('qixiaoxuan', ['①装疯麻痹特务', '②组织狱中越狱', '③带头绝食斗争', '④出身豪门矢志不移']),
        c4('huaziliang', ['①装疯潜伏十五年', '②每日疯癫扫院卖菜', '③暗中传递情报', '④关键时刻引队越狱']),
        c4('xiaoluobotou', ['①襁褓随父母入狱', '②头大身小狱中长大', '③跟黄将军学文化', '④放风传递秘密纸条']),
        c4('shuangqiang', ['①华蓥山传奇英雄', '②双手各使驳壳枪', '③百发百中出神入化', '④川东岭间打击敌人']),
    ],
}

# ------------------------------------------------- 叙事表 / 雅号表（每行 1 格画廊）
# key -> (img_prefix, caption_col, strip_title)
GALLERY = {
    '四次出海历险': ('et-lubinxun', 0, '鲁滨逊历险 14 事件连环画（按行序）'),
    '十篇回忆散文全景分析表': ('et-zhaohua', 1, '《朝花夕拾》十篇散文连环画（按行序）'),
    '三起三落': ('et-sanqisanlu', 0, '祥子「三起三落」连环画（按行序）'),
    '环球航线与六大险境表': ('et-haidi', 1, '「鹦鹉螺号」六大险境连环画（按行序）'),
    '长征路线关键节点表': ('et-changzheng', 1, '红军长征六阶段连环画（按行序）'),
    '十三篇核心章节全景考点表': ('et-jingdian', 0, '《经典常谈》十三篇连环画（按行序）'),
    '六大成长阶段与四次死里逃生表': ('et-gangtie', 0, '保尔成长六阶段连环画（按行序）'),
    '十首经典诗作鉴赏全景表': ('et-aiqing', 0, '《艾青诗选》十首诗作连环画（按行序）'),
    '人生四大阶段环境蜕变与精神成长表': ('et-jianai', 0, '简·爱成长四阶段连环画（按行序）'),
    '六大革命斗争场景与环境表': ('et-hongyancj', 0, '《红岩》六大斗争场景连环画（按行序）'),
    '诗歌体裁演变全景表': ('et-tangshiti', 0, '唐诗体裁演变连环画（按行序）'),
    '雅号与称号全景表': ('et-yahao', -1, '唐代诗人雅号连环画（按行序）'),
}

# 雅号表逐格图（前 4 位复用旧人物图第 1 格）
YAHAO_IMGS = [
    f'{IMG}/libai-c1.jpg', f'{IMG}/dufu-c1.jpg', f'{IMG}/wangwei-c1.jpg', f'{IMG}/baijuyi-c1.jpg',
    f'{IMG}/et-yahao-liuyuxi.jpg', f'{IMG}/et-yahao-lihe.jpg', f'{IMG}/et-yahao-mengjiao.jpg',
    f'{IMG}/et-yahao-jiadao.jpg', f'{IMG}/et-yahao-chenziang.jpg', f'{IMG}/et-yahao-wangbo.jpg',
    f'{IMG}/et-yahao-xiaolidu.jpg',
]

CSS = """
  /* ===== 表格连环画 (V4) ===== */
  .comic-row > td { background: transparent; border-bottom: 1px solid var(--border-color); }
  .comic-strip { background: linear-gradient(180deg, #fbfaf7 0%, #f7f5f0 100%); border: 1px solid var(--border-color); border-radius: 12px; padding: 0.75rem 0.9rem 0.9rem; margin: 0.55rem 0 0.9rem; }
  .comic-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.55rem; }
  .comic-title-badge { display: inline-flex; align-items: center; gap: 0.3rem; background: var(--primary, #2563eb); color: white; font-size: 0.72rem; font-weight: 700; padding: 0.16rem 0.55rem; border-radius: 999px; }
  .comic-chapter { font-size: 0.74rem; font-weight: 600; color: var(--text-muted); }
  .comic-panels { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; }
  .comic-panels figure { margin: 0; }
  .comic-panels img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; border: 1px solid var(--border-color); cursor: zoom-in; background: #fff; transition: transform 0.15s ease, box-shadow 0.15s ease; }
  .comic-panels img:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(15, 23, 42, 0.14); }
  .comic-panels figcaption { margin-top: 0.3rem; font-size: 0.72rem; line-height: 1.5; color: var(--text-main); font-weight: 600; text-align: center; }
  @media (max-width: 760px) { .comic-panels { grid-template-columns: repeat(2, 1fr); } }
"""

def strip_html(title, cells):
    figs = '\n'.join(
        f'            <figure><img src="{img}" alt="{title}第{i+1}格" loading="lazy" '
        f'onclick="openModal(this.src, this.alt)"><figcaption>{cap}</figcaption></figure>'
        for i, (img, cap) in enumerate(cells))
    return (f'      <div class="comic-strip">\n'
            f'        <div class="comic-head">\n'
            f'          <span class="comic-title-badge">🎞 连环画</span>\n'
            f'          <span class="comic-chapter">{title}（点击可放大）</span>\n'
            f'        </div>\n'
            f'        <div class="comic-panels">\n{figs}\n        </div>\n'
            f'      </div>')

def comic_row_html(name, data, colspan):
    figs = '\n'.join(
        f'              <figure><img src="{img}" alt="{name}连环画第{i+1}格" loading="lazy" '
        f'onclick="openModal(this.src, this.alt)"><figcaption>{cap}</figcaption></figure>'
        for i, (img, cap) in enumerate(zip(data['imgs'], data['caps'])))
    return (f'                <tr class="comic-row"><td colspan="{colspan}" style="padding-top:0.2rem;">\n'
            f'                  <div class="comic-strip">\n'
            f'                    <div class="comic-head">\n'
            f'                      <span class="comic-title-badge">🎞 四格连环画</span>\n'
            f'                      <span class="comic-chapter">{name} · 典型情节画传（点击可放大）</span>\n'
            f'                    </div>\n'
            f'                    <div class="comic-panels">\n{figs}\n                    </div>\n'
            f'                  </div>\n'
            f'                </td></tr>')

def main():
    src = DST.read_text(encoding='utf-8')
    assert 'class="comic-row"' not in src, '已挂载过，请勿重复执行'

    # 定位全部表：h3 位置 -> 表体范围
    tables = []  # (h3text, t_start, t_end, trs[(r_start,r_end,cells)])
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', src, re.S):
        h3 = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        tm = re.search(r'<table class="data-table">(.*?)</table>', src[m.end():], re.S)
        if not tm:
            continue
        t_start = m.end() + tm.start()
        t_end = m.end() + tm.end()
        body = tm.group(1)
        trs = []
        for tr in re.finditer(r'<tr[^>]*>(.*?)</tr>', body, re.S):
            cells = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>', tr.group(1), re.S)]
            if cells:
                trs.append((m.end() + tm.start() + tr.start(), m.end() + tm.start() + tr.end(), cells))
        tables.append((h3, t_start, t_end, trs))

    inserts = []  # (pos, text)
    used = set()
    for h3, t_start, t_end, trs in tables:
        # row4 人物表
        for key, rows in ROW4.items():
            if key in h3 and key not in used:
                assert len(trs) == len(rows), f'{key}: 行数 {len(trs)} != 配置 {len(rows)}'
                for (rs, re_, cells), data in zip(reversed(trs), reversed(rows)):
                    name = re.sub(r'\s+', '', cells[0])[:14]
                    inserts.append((re_, '\n' + comic_row_html(name, data, len(cells))))
                used.add(key)
                break
        else:
            # gallery 表
            for key, (prefix, capcol, title) in GALLERY.items():
                if key in h3 and key not in used:
                    cells_out = []
                    for i, (rs, re_, cells) in enumerate(trs):
                        if capcol == -1:  # 雅号
                            img = YAHAO_IMGS[i]
                            cap = f'{cells[0]}·{cells[1]}'
                        else:
                            img = f'{IMG}/{prefix}-r{i+1:02d}.jpg'
                            cap = cells[capcol] if capcol < len(cells) else cells[0]
                        cells_out.append((img, cap[:46]))
                    # 插在 table-responsive-box 结束的 </div> 之后
                    dm = re.compile(r'</table>\s*</div>').search(src, t_start)
                    assert dm, key
                    pos = dm.end()
                    inserts.append((pos, '\n' + strip_html(title, cells_out)))
                    used.add(key)
                    break

    print(f'命中配置 {len(used)}/{len(ROW4)+len(GALLERY)} 张表')
    assert len(used) == len(ROW4) + len(GALLERY), '有表未命中'

    for pos, text in sorted(inserts, reverse=True):
        src = src[:pos] + text + src[pos:]
    src = src.replace('</style>', CSS + '</style>', 1)
    DST.write_text(src, encoding='utf-8')
    n4 = sum(len(v) for v in ROW4.values())
    n1 = sum(len(trs) for h3, _, _, trs in tables for k in GALLERY if k in h3)
    print(f'OK -> {DST.name} ({len(src)/1024:.0f} KB)：人物 4 格 {n4} 条 + 单格画廊 {n1} 格')

if __name__ == '__main__':
    sys.exit(main())
