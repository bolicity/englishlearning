#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儒林外史连环画流水线：
1. 把 /tmp/rulin_comic 的原始 PNG（1024x1024，底部 94px 为 AI 水印带）
   居中裁成 930x930 并转 JPG 落盘到 chinese/images/
2. 在 p1/p2/p3 每个人物表格行后插入 <tr class="comic-row"> 连环画条带；
   p2 的杜少卿（不在表格里）插在板块四 summary-box 之后；
   p4 在矩阵卡片后追加一张“11位新增人物”连环画卡片，并给矩阵里
   已在他页有连环画的 19 人加跳转链接。
改前自动备份到 /tmp/rulin_backup/。幂等可重复执行。
"""
import glob, html, os, re, shutil, subprocess, sys

BASE = "/Users/emily/Developer/Projects/owenlearining/chinese"
IMG = os.path.join(BASE, "images")
COMIC_DIR = "/tmp/rulin_comic"
BACKUP = "/tmp/rulin_backup"
PAGES = {
    "p1": "rulinwaishi-p1-V1.html",
    "p2": "rulinwaishi-p2-V1.html",
    "p3": "rulinwaishi-p3-V1.html",
    "p4": "rulinwaishi-p4-V1.html",
}

# ---------------- 条带清单 ----------------
# panels: 槽位n -> "E"=复用已有行首图 rulinwaishi-{src}-{slug}.jpg；数字=用 comic 源图的格号
S = []
def strip(page, src, slug, name, chapter, caps, panels, anchor=None):
    S.append(dict(page=page, src=src, slug=slug, name=name, chapter=chapter,
                  caps=caps, panels=panels, anchor=anchor))

# ---- p2（分支二·假名士，11 人）----
strip("p2","p2","maer","马二先生","第 13-15 回",
  ["杭州街头倾囊资助落魄的匡超人返乡","倾囊相助，替蘧公孙赎回要紧的枕箱","自出银两，料理假神仙洪憨仙的后事","一生以批选八股文章为业，逢人劝学举业"],
  {1:"E",2:1,3:3,4:4})
strip("p2","p2","lubianxiu","鲁编修","第 10、11 回",
  ["把独生女儿当男子教养，亲自督课","鲁小姐自幼在窗下苦研八股","怒斥娄氏公子沉迷诗词、耽误举业","科场得意，视八股为世间唯一正途"],
  {1:"E",2:2,3:3,4:4})
strip("p2","p2","wangyuhui","王玉辉","第 48 回",
  ["家贫志大，伏案立志著述三部书","力劝女儿绝食殉夫，称可名留青史","女儿逝后，仰天大笑走出门去","一路睹物思人，老泪纵横、凄凉惶恐"],
  {1:1,2:2,3:3,4:"E"})
strip("p2","p2","kuangchaoren","匡超人","第 16-20 回",
  ["早年病父床前端汤奉药、苦读至深夜","到省城变质，灯下伪造官府朱签","收取重金，替金跃冒名代考","潘三下狱，他翻脸划清界限"],
  {1:1,2:"E",3:3,4:4})
strip("p2","p2","niupulang","牛浦郎","第 21-24 回",
  ["甘露庵中偷读牛布衣遗诗，据为己有","擅改庵中牌匾，冒名顶替","把来访的卜家兄弟当下人使唤","依附知县权势，怒拒恶霸敲诈"],
  {1:"E",2:2,3:3,4:4})
strip("p2","p2","qugongsun","蘧公孙","第 8-14 回",
  ["慷慨赠银，资助避难的罪官王惠","在禁书扉页署上自己的名字博名","依仗权势，深究仆人与丫鬟双红","娄府宴客，高谈诗文、沽名钓誉"],
  {1:1,2:"E",3:3,4:4})
strip("p2","p2","dushenqing","杜慎卿","第 29-31 回",
  ["受文士奉承，表面谦逊暗自得意","口称最厌女人，转身托媒纳妾","一毛不拔，却指点鲍廷玺去坑杜少卿","莫愁湖湖亭梨园大会，豪掷重金赏伶"],
  {1:1,2:2,3:3,4:"E"})
strip("p2","p2","hutuhu","胡屠户","第 3 回",
  ["中举前辱骂女婿“现世宝、穷鬼”","中举后极尽巴结“天上文曲星”","打了疯范进一巴掌，怕菩萨怪罪","一路弯腰，替女婿扯衣裂数十回"],
  {1:1,2:"E",3:3,4:4})
strip("p2","p2","baowenqing","鲍文卿","第 24-26 回",
  ["面对书办重金请托，义正词严拒绝","茶馆训诫戏子恪守本分","考棚中宽容放过作弊的贫苦童生","与向知县相交甚笃，仍恪守平民礼数"],
  {1:1,2:"E",3:3,4:4})
strip("p2","p2","baotingxi","鲍廷玺","第 25-32 回",
  ["遵父遗训，婉拒富室联姻","自称杜慎卿门人，抬高身价","戏班散伙，走投无路","向杜少卿哭穷乞银，重整戏班"],
  {1:1,2:2,3:3,4:"E"})
strip("p2","p2","dushaoqing","杜少卿","第 31-34 回",
  ["朝廷征辟，装病坚辞不出仕","携妻大方同游清凉山","出资助鲍廷玺重整戏班","赞许沈琼枝抗婚逃婚的独立精神"],
  {1:1,2:"E",3:3,4:4}, anchor="更多真儒行迹见分支三展开")

# ---- p1（分支一·文学常识，6 人；马二复用 p2 条带）----
strip("p1","p1","wangmian","王冕","第 1 回",
  ["湖边放牛，自学画荷名动乡里","卖画得钱，全买好吃的孝敬老母","闭门苦读，不到二十岁博览群书","朝廷征聘，避走会稽山隐居终老"],
  {1:1,2:2,3:3,4:4})
strip("p1","p1","wanghui","王惠","第 7、8 回",
  ["到任南昌故意不接印，逼下属送规费","上任便查办私情、大肆搜刮民脂","宁王叛乱，开城投降做伪官","兵败连夜出逃，削发为僧"],
  {1:1,2:2,3:3,4:4})
strip("p1","p1","tangfeng","汤奉","第 4 回",
  ["五十斤牛肉堆上长枷，活活压毙老师傅","偷鸡贼头顶捆鸡，游街百般折辱","公堂严刑苛断，酷吏做派","出巡仪仗森严，百姓跪伏侧目"],
  {1:1,2:2,3:3,4:4})
strip("p1","p1","yangongsheng","严贡生","第 5、6 回",
  ["强占邻居走失的猪，反咬索要饲料钱","几片云片糕讹称名贵药材，赖掉船资","弟死假意吊唁","转头强行霸占胞弟家产"],
  {1:1,2:2,3:3,4:4})
strip("p1","p1","yanjiansheng","严监生","第 5、6 回",
  ["万贯家财却省吃俭用，拨算盘核账","妻病垂危之际，顺水推舟扶正赵氏","临终伸着两根指头，不肯瞑目","挑掉一茎灯草，方才咽气"],
  {1:1,2:2,3:3,4:4})
strip("p1","p2","maer","马二先生","第 13-15 回",
  ["杭州街头倾囊资助落魄的匡超人返乡","倾囊相助，替蘧公孙赎回要紧的枕箱","自出银两，料理假神仙洪憨仙的后事","一生以批选八股文章为业，逢人劝学举业"],
  {1:"E",2:1,3:3,4:4})  # 复用 p2 的马二条带与图片

# ---- p3（分支三·真儒明贤，8 人；杜少卿复用 p2 条带）----
strip("p3","p3","chihengshan","迟衡山","第 33、34 回",
  ["编撰《诗说》，敢与朱熹唱反调","与庄绍光商议泰伯祠礼乐","主持名垂青史的泰伯祠大祭","力反堪舆迷信，不信发福发贵"],
  {1:1,2:2,3:3,4:4})
strip("p3","p3","zhuangshaoguang","庄绍光","第 34、35 回",
  ["柴门紧闭著书立说，不妄交一人","婉言谢绝朝廷征辟","自掏银两安葬街头贫苦老夫妇","举家迁往玄武湖幽居避扰"],
  {1:1,2:2,3:3,4:4})
strip("p3","p3","yuyude","虞育德","第 36、37 回",
  ["救起轻生青年，赠银助其葬父","考核如实禀报年岁，得闲职而怡然","门生张罗寿宴厚礼，严词谢绝","暗中为作弊秀才掩饰，绝口不提"],
  {1:1,2:2,3:3,4:4})
strip("p3","p3","guoxiaozi","郭孝子 (郭力)","第 37、38 回",
  ["万里寻父，途中遇虎历险不改初心","识破假吊死鬼骗子，反授武艺","竹山庵寻父，被拒之门外","庵旁挑土打柴，苦力供养生父"],
  {1:1,2:2,3:3,4:4})
strip("p3","p3","xiaoyunxian","萧云仙","第 39、40 回",
  ["峨眉山打瞎恶霸赵大，救下老僧","投军平叛，智勇双全","修城防、兴水利、办义学","革职还乡，跪父痛哭悔歉"],
  {1:1,2:2,3:3,4:4})
strip("p3","p3","fengsilaodie","凤四老爹","第 50-52 回",
  ["公堂之上，挺身代友亲试官刑","船头飞身跃起，追回被盗盘缠","揪住骗子，追回上千两被骗巨银","晨起操练拳棒，武风凛然"],
  {1:1,2:2,3:3,4:4})
strip("p3","p3","shenqiongzhi","沈琼枝","第 40、41 回",
  ["识破盐商骗婚，决然抗婚逃婚","南京钞库街悬牌卖诗卖刺绣","痛斥恶少、怒打索钱官差","当窗刺绣作诗，名动金陵"],
  {1:1,2:2,3:3,4:4})
strip("p3","p2","dushaoqing","杜少卿","第 31-34 回",
  ["朝廷征辟，装病坚辞不出仕","携妻大方同游清凉山","出资助鲍廷玺重整戏班","赞许沈琼枝抗婚逃婚的独立精神"],
  {1:1,2:"E",3:3,4:4})  # 复用 p2 的杜少卿条带与图片

# ---- p4（分支四·矩阵页，11 位新人物单独成条带）----
strip("p4","p4","fanjin","范进","组二·科举迷者",
  ["五十四岁皓首穷经，破屋苦读","一见捷报，喜极发疯满街奔走","被岳丈一掌打醒，恢复清醒","中举后攀附张乡绅，渐染官气"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","zhoujin","周进","组二·科举迷者",
  ["六十余岁仍是老童生，坐馆受嘲弄","贡院触景生情，撞号板痛哭吐血","商人凑银替他捐了监生","一朝得中，端坐公案风光显达"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","luxiaojie","鲁小姐","组二·科举迷者",
  ["自幼受父训，精通八股文章","嫁入蘧府，见丈夫无心举业而失望","以才学督促夫君攻习举业","严格督责幼子天天功课"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","qujingluan","瞿景鸾","组二·科举迷者",
  ["奔走权贵之门，捧帖求见","宴席上点头哈腰、一味迎合","竭力依附严氏豪强兄弟","谋得差事，志得意满"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","zhangjingzhai","张静斋","组三·虚伪丑态",
  ["范进一中举，立刻送银赠房巴结","把酒言欢，指点攀附门路","倚仗官绅之势，强占民田民房","公堂构陷无辜良民"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","pansan","潘三","组三·虚伪丑态",
  ["包揽词讼，操纵官府案由","教唆匡超人伪造朱签、代考替试","拐卖妇女、敲诈勒索","东窗事发，锒铛入狱"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","yangzhizhong","杨执中","组三·虚伪丑态",
  ["隐居乡野，高谈空洞议论","被娄公子奉为高士，沾沾自喜","引荐无赖小人入伙","被小人连累，家中鸡犬不宁"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","zhaoshi","赵氏","组四·奇人异士",
  ["妾室出身，低头侍奉、心思细密","挑掉一茎灯草，扶正为正室","智斗严氏恶霸族亲","保全孤儿与家产"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","bucheng","卜诚","组四·奇人异士",
  ["匡超人潦倒街头，卖豆腐糊口","卜诚真心收留，给落脚之处","赠盘缠干粮，送他上路","故人发达冷眼相待，淡然处之"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","libenying","李本瑛","组四·奇人异士",
  ["赏识匡超人文才，收为门生","提携举荐，师徒相得","被人参奏弹劾，摘印去职","落难途中遭旧门生划清界限"],
  {1:1,2:2,3:3,4:4})
strip("p4","p4","zhangjunmin","张俊民","组四·奇人异士",
  ["官宦门前趋奉，递帖求见","在官宦与豪绅间两头撮合","借范进之势为亲眷谋差事","宴席上周旋名流，志得意满"],
  {1:1,2:2,3:3,4:4})

# p4 矩阵里已在他页有连环画的人物 -> 链接
# （王玉辉/杜慎卿/鲍廷玺/迟衡山不在 p4 矩阵中，故只有 19 人需要链接）
P4_LINKS = {
    "王冕":("p1","wangmian"),"王惠":("p1","wanghui"),"汤奉":("p1","tangfeng"),
    "严贡生":("p1","yangongsheng"),"严监生":("p1","yanjiansheng"),
    "马二先生":("p2","maer"),"鲁编修":("p2","lubianxiu"),
    "匡超人":("p2","kuangchaoren"),"牛浦郎":("p2","niupulang"),"蘧公孙":("p2","qugongsun"),
    "胡屠户":("p2","hutuhu"),"鲍文卿":("p2","baowenqing"),
    "杜少卿":("p3","dushaoqing"),"虞育德":("p3","yuyude"),
    "庄绍光":("p3","zhuangshaoguang"),"沈琼枝":("p3","shenqiongzhi"),
    "萧云仙":("p3","xiaoyunxian"),"凤四老爹":("p3","fengsilaodie"),
    "郭孝子 (郭力)":("p3","guoxiaozi"),
}

CSS = """
    /* 人物连环画条带 */
    .comic-strip { padding: 1rem; border: 1px solid var(--border-color, #E2E8F0); border-radius: 10px; background: #F8FAFC; }
    .comic-head { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
    .comic-chapter { font-size: 0.75rem; color: var(--text-muted, #64748B); font-weight: 700; }
    .comic-panels { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }
    .comic-panels figure { margin: 0; min-width: 0; }
    .comic-panels img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; border: 1px solid var(--border-color, #E2E8F0); box-shadow: 0 1px 4px rgba(15,23,42,0.07); cursor: zoom-in; display: block; transition: transform 0.18s ease; }
    .comic-panels img:hover { transform: scale(1.03); }
    .comic-panels figcaption { font-size: 0.72rem; color: var(--text-secondary, #475569); line-height: 1.5; margin-top: 0.4rem; }
    .comic-link { font-size: 0.72rem; font-weight: 700; color: #1D4ED8; text-decoration: none; border: 1px solid #DBEAFE; background: #EFF6FF; border-radius: 4px; padding: 0.1rem 0.35rem; white-space: nowrap; margin-left: 0.3rem; }
    .comic-link:hover { background: #1D4ED8; color: #fff; }
    @media (max-width: 720px) { .comic-panels { grid-template-columns: repeat(2, 1fr); } }
"""

def find_comic(slug, n):
    hits = sorted(glob.glob(os.path.join(COMIC_DIR, f"连环画_{slug}_{n}_*.png")))
    return hits[0] if hits else None

def to_jpg(src_png, dest_jpg):
    # 底部 94px 为 AI 水印带；水平居中裁成 930x930 正方形
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                    "--cropOffset", "0", "47", "-c", "930", "930",
                    src_png, "--out", dest_jpg], check=True, capture_output=True)

def panel_file(st):
    """返回 (每格文件名列表, 待生成任务列表)。"""
    tasks, files = [], []
    for n in range(1, 5):
        v = st["panels"][n]
        if v == "E":
            files.append(f"rulinwaishi-{st['src']}-{st['slug']}.jpg")
        else:
            fname = f"rulinwaishi-{st['src']}-{st['slug']}-c{n}.jpg"
            tasks.append((find_comic(st["slug"], v), os.path.join(IMG, fname), st, v))
            files.append(fname)
    return files, tasks

def strip_html(st, files):
    caps = st["caps"]
    figs = []
    for i in range(4):
        f = files[i]
        cap = caps[i] if caps else ""
        circ = "①②③④"[i]
        alt = html.escape(f"{st['name']}连环画第{i+1}格")
        figs.append(
            f'          <figure><img src="images/{f}" alt="{alt}" loading="lazy" '
            f"onclick=\"openLightbox('images/{f}')\">"
            f"<figcaption>{circ} {html.escape(cap)}</figcaption></figure>"
        )
    ch = html.escape(st["chapter"])
    inner = "\n".join(figs)
    return (
        f'<div class="comic-strip" id="comic-{st["slug"]}">\n'
        f'          <div class="comic-head"><span class="role-badge">{html.escape(st["name"])}</span>'
        f'<span class="comic-chapter">{ch} · 故事连环画（点击可放大）</span></div>\n'
        f'          <div class="comic-panels">\n{inner}\n          </div>\n        </div>'
    )

def backup(page):
    os.makedirs(BACKUP, exist_ok=True)
    shutil.copy2(os.path.join(BASE, PAGES[page]), os.path.join(BACKUP, PAGES[page]))

DIV_RE = re.compile(r"<div\b|</div>")

def find_strip_block(src, slug):
    """按 <div> 配对找到 comic-strip 块的 [起, 止)。"""
    key = f'<div class="comic-strip" id="comic-{slug}">'
    s = src.find(key)
    if s == -1:
        return None
    depth, i = 0, s
    while True:
        m = DIV_RE.search(src, i)
        if not m:
            return None
        if m.group(0) == "</div>":
            depth -= 1
            if depth == 0:
                return (s, m.end())
        else:
            depth += 1
        i = m.end()

def colspan_of_table(src, badge_idx):
    """badge 所在表格的列数 = 该表格 thead 里 <th 的个数。"""
    t = src.rfind("<table", 0, badge_idx)
    if t == -1:
        return 3
    head_end = src.find("</thead>", t, badge_idx)
    if head_end == -1:
        return 3
    return max(1, src[t:head_end].count("<th"))

def insert_row_strip(src, st):
    """在包含 role-badge 的 </tr> 之后插入 comic-row。"""
    badge = src.find(f'class="role-badge">{html.escape(st["name"])}<')
    assert badge != -1, f"找不到人物 {st['name']}"
    tr_end = src.find("</tr>", badge)
    assert tr_end != -1
    pos = tr_end + len("</tr>")
    span = colspan_of_table(src, badge)
    frag = (f'\n\n                <tr class="comic-row"><td colspan="{span}" '
            f'style="padding-top:0.35rem;">\n                '
            + strip_html(st, panel_file(st)[0]) + '\n                </td></tr>')
    return src[:pos] + frag + src[pos:]

def insert_after_anchor(src, anchor, st):
    """找 anchor，再找其后 10 空格 </div>（summary-box 收口），在其后插入。"""
    a = src.find(anchor)
    assert a != -1, f"找不到锚点 {anchor}"
    m = src.find("\n          </div>", a)
    assert m != -1, "找不到 summary-box 收口"
    pos = m + len("\n          </div>")
    frag = ('\n\n          ' + strip_html(st, panel_file(st)[0]))
    return src[:pos] + frag + src[pos:]

def process_p4(src, strips):
    changed = []
    new_strips = [st for st in strips if f'id="comic-{st["slug"]}"' not in src]
    if new_strips:
        t = src.find('id="matrixTable"')
        assert t != -1
        tb = src.find("</table>", t)
        assert tb != -1
        m = src.find("\n        </div>", tb)
        assert m != -1, "找不到矩阵 card-block 收口"
        pos = m + len("\n        </div>")
        inner = "".join(
            "\n\n          " + strip_html(st, panel_file(st)[0]) for st in new_strips
        )
        block = ('\n\n        <div class="card-block">\n'
                 '          <h2 class="block-title"><span class="icon">画</span> '
                 '11位新增人物 · 故事连环画（其余 19 位点击矩阵中的“连环画→”跳转）</h2>'
                 + inner + '\n        </div>')
        src = src[:pos] + block + src[pos:]
        changed.append(f"{len(new_strips)} strips")
    links = 0
    for name, (pg, slug) in P4_LINKS.items():
        old = f'<td><span class="role-badge">{name}</span></td>'
        if old in src and f'href="rulinwaishi-{pg}-V1.html#comic-{slug}"' not in src:
            href = f'rulinwaishi-{pg}-V1.html#comic-{slug}'
            new = (f'<td><span class="role-badge">{name}</span>'
                   f'<a class="comic-link" href="{href}">连环画→</a></td>')
            src = src.replace(old, new, 1)
            links += 1
    if links:
        changed.append(f"{links} links")
    return src, changed

def main():
    only = sys.argv[1:] or ["p1", "p2", "p3", "p4"]
    made, skipped_src = 0, []
    # 1) 图片处理
    seen_dest = set()
    for st in S:
        if st["page"] not in only:
            continue
        _, tasks = panel_file(st)
        for s, dest, stx, v in tasks:
            if dest in seen_dest:
                continue
            seen_dest.add(dest)
            if s is None:
                skipped_src.append(f"{stx['slug']} 格{v} -> {os.path.basename(dest)}")
                continue
            if not os.path.exists(dest):
                to_jpg(s, dest)
                made += 1
    print(f"新处理图片 {made} 张")
    for x in skipped_src:
        print(f"!! 缺源图: {x}")

    # 2) 页面嵌入
    for page in only:
        path = os.path.join(BASE, PAGES[page])
        backup(page)
        src = open(path, encoding="utf-8").read()
        changed = []

        if ".comic-strip" not in src:
            assert src.count("  </style>") == 1, f"{page} style 收口异常"
            src = src.replace("  </style>", CSS + "  </style>", 1)
            changed.append("css")

        strips = [st for st in S if st["page"] == page]
        if page in ("p1", "p2", "p3"):
            for st in strips:
                new = strip_html(st, panel_file(st)[0])
                blk = find_strip_block(src, st["slug"])
                if blk:
                    if src[blk[0]:blk[1]] != new:  # 幂等 + 说明文字有更新就替换
                        src = src[:blk[0]] + new + src[blk[1]:]
                        changed.append(f'{st["slug"]}(更新)')
                    continue
                if st["anchor"]:
                    src = insert_after_anchor(src, st["anchor"], st)
                else:
                    src = insert_row_strip(src, st)
                changed.append(st["slug"])
        else:
            src, ch = process_p4(src, strips)
            changed += ch

        open(path, "w", encoding="utf-8").write(src)
        print(f"{page}: {', '.join(changed) if changed else '无变更（已就绪）'}")

if __name__ == "__main__":
    main()
