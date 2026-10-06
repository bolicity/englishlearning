#!/usr/bin/env python3
"""classic-reading-V3.html -> V4.html：人物对照表每行下挂 4 格连环画。

- COMICS_DB 以 `bookId:人物下标` 为键，渲染时查表插入 comic-row；
- 新增 CSS（comic-strip/comic-panels/灯箱）与全局灯箱；
- 图注走 maskText，背诵模式下人名自动挖空。
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CH = ROOT / 'chinese'
SRC = CH / 'classic-reading-V3.html'
DST = CH / 'classic-reading-V4.html'

# ---------------------------------------------------------------- 连环画数据
# imgs 缺省 = images/classic-comics/{base}-c{i}.jpg
def P(base, caps, imgs=None):
    if imgs is None:
        imgs = [f'images/classic-comics/{base}-c{i}.jpg' for i in range(1, 5)]
    return {'caps': caps, 'imgs': imgs}

COMICS = {
    # 一 童年
    'tongnian:0': P('tongnian-alisha', ['①丧父随母投奔外祖父家', '②小茨冈伸臂替他挡鞭', '③课余捡破烂贴补家用', '④母亲病逝走向人间']),
    'tongnian:1': P('tongnian-waizu', ['①火中抢出硫酸盐桶', '②挺身拦住受惊的马', '③灯下讲优美的民间故事', '④忍受打骂虔诚祈祷']),
    # 二 鲁滨逊漂流记
    'lubinxun:0': P('lubinxun-lubinxun', ['①执意登船扬帆远航', '②海难孤身漂上荒岛', '③建房种粮驯羊立足', '④举枪救下俘虏星期五']),
    'lubinxun:1': P('lubinxun-xingqiwu', ['①被野人追捕命悬一线', '②枪响获救跪谢恩人', '③学穿衣吃熟食说英语', '④并肩击退野人救父']),
    # 三 朝花夕拾
    'zhaohuaxishi:0': P('achang', ['①睡觉摆大字切切察察', '②满口繁琐年节规矩', '③踩死隐鼠低头隐瞒', '④捧来心爱的山海经']),
    'zhaohuaxishi:1': P('tengye', ['①黑瘦八字须不修边幅', '②红笔逐字添改讲义', '③关心解剖实习', '④赠照片背面题惜别']),
    # 四 西游记
    'xiyouji:0': P('wukong', ['①大闹天宫战天兵', '②三打白骨精遭逐', '③车迟国斗法除三妖', '④三借芭蕉扇灭火']),
    'xiyouji:2': P('bajie', ['①高老庄做农活招赘', '②偷吃人参果', '③进谗言害悟空被逐', '④流沙河红孩儿出死力']),
    # 五 骆驼祥子
    'luotuoxiangzi:0': P('xiangzi', ['①健壮车夫拼命拉车', '②买上新车笑得灿烂', '③遭抢后苦撑善待雇主', '④叼烟颓然走向堕落']),
    'luotuoxiangzi:1': P('huniu', ['①车厂拨算盘掌账', '②假称有孕设计逼婚', '③闹翻置办二手洋车', '④难产卧床痛苦死去']),
    # 六 海底两万里
    'haidiliangwanli:0': P('nimo', ['①驾驭诺第留斯号', '②斗鲨救采珠人赠珍珠', '③海底财宝支援义军', '④驾艇撞沉殖民战舰']),
    'haidiliangwanli:1': P('alongnasi', ['①追海怪落水被俘', '②舷窗观察海洋生物', '③埋头记录科考笔记', '④策划乘小艇出逃']),
    # 七 红星照耀中国
    'hongxingzhaoyao:0': P('maozedong', ['①窑洞油灯秉烛长谈', '②穿打补丁的旧军服', '③与战士同吃小米饭', '④谈笑风生手势从容']),
    'hongxingzhaoyao:2': P('pengdehuai', ['①与战士赤脚打篮球', '②战壕前指挥若定', '③仅有两套统一制服', '④降落伞改成背心穿']),
    # 八 昆虫记
    'kunchongji:0': P('tanglang', ['①张开纱翅威吓敌人', '②举镰前臂伏击猎物', '③迅猛捕食蝗虫', '④草叶间雌雄相会']),
    'kunchongji:1': P('chan', ['①地下蛹伏黑暗四年', '②金蝉脱壳攀上枝头', '③尖喙刺皮吸食树汁', '④蚂蚁成群围抢撕咬']),
    # 九 经典常谈
    'jingdianchangtan:0': P('shuowen', ['①许慎伏案著书', '②象形字例日月山水', '③会意形声字例讲解', '④五百四十部首编排']),
    'jingdianchangtan:2': P('shijing', ['①采诗官摇木铎采风', '②关关雎鸠在河之洲', '③风雅颂分赋比兴', '④孔子弦歌思无邪']),
    # 十 钢铁是怎样炼成的
    'gangtieshi:0': P('baoer', ['①少年智救朱赫来', '②战场冲锋死里逃生', '③严冬筑路带病苦干', '④病榻口述写成小说']),
    'gangtieshi:1': P('zhulai', ['①水兵装束地下工作', '②教保尔练习拳击', '③被押途中获救', '④政委关怀保尔成长']),
    # 十一 艾青诗选
    'aiqingshixuan:0': P('dayanhe', ['①雪落保姆荒草坟头', '②怀抱婴儿轻拍哄睡', '③搭灶洗衣操持家务', '④狱中含泪写下诗行']),
    'aiqingshixuan:1': P('woaizhedi', ['①抗战烽烟漫原野', '②嘶哑喉咙歌唱的鸟', '③暴风雨打击着土地', '④眼含泪水爱得深沉']),
    # 十二 水浒传
    'shuihuzhuan:0': P('luzhishen', ['①三拳打死镇关西', '②五台山醉打金刚', '③倒拔垂杨柳', '④野猪林抡杖救林冲']),
    'shuihuzhuan:1': P('linchong', ['①误入白虎堂遭陷', '②刺配沧州受折磨', '③风雪山神庙复仇', '④雪夜投奔上梁山']),
    # 十三 儒林外史（复用现有图）
    'rulinwaishi:1': P('fanjin', ['①五十四岁才中秀才', '②瞒着岳父乡试中举', '③看榜狂喜痰迷发疯', '④一记耳光方才清醒'],
                       imgs=[f'images/rulinwaishi-p4-fanjin-c{i}.jpg' for i in range(1, 5)]),
    'rulinwaishi:2': P('yanjiansheng', ['①病榻垂危竖两指', '②亲人纷纷猜不透', '③挑掉一根灯草', '④点头咽气吝啬至终'],
                       imgs=[f'images/rulinwaishi-p1-yanjiansheng-c{i}.jpg' for i in range(1, 5)]),
    # 十四 简·爱
    'jianai:0': P('jianai', ['①反抗表哥怒斥舅母', '②洛伍德寒窗苦读', '③庄园宣言灵魂平等', '④芬丁重逢患难与共']),
    'jianai:1': P('luochesite', ['①阴郁傲慢的庄园主', '②倾心求婚简爱', '③火场救人失明断手', '④芬丁庄园静候重逢']),
    # 十五 红岩
    'hongyan:0': P('jiangjie', ['①忍痛奔赴华蓥山', '②被捕押入渣滓洞', '③竹签钉指宁死不屈', '④狱中密绣五星红旗']),
    'hongyan:3': P('xiaoluobotou', ['①襁褓随父母入狱', '②头大身小狱中长大', '③跟黄将军学文化', '④放风传递秘密纸条']),
    # 十六 唐诗三百首
    'tangshisanbaishou:0': P('libai', ['①仗剑辞亲远游', '②斗酒诗百篇', '③梦游天姥邀明月', '④飞流直下三千尺']),
    'tangshisanbaishou:1': P('dufu', ['①乱世携家流离', '②国破山河在', '③茅屋为秋风所破', '④高台独立吟登高']),

    # ---------------------------- 第二批：补齐其余 44 位 ----------------------------
    'tongnian:2': P('waizufu', ['①执皮鞭抽打孩子', '②吝啬成性刻薄寡恩', '③破产分家赶走亲人', '④病榻前讲纤夫往事']),
    'tongnian:3': P('xiaocigang', ['①弃儿被外祖母收养', '②伸臂替阿廖沙挡鞭', '③深得外祖父赏识', '④背负十字架惨死']),
    'tongnian:4': P('haoshiqing', ['①贫困房客潜心实验', '②被小市民视为异端', '③教阿廖沙观察生活', '④被外祖父强行赶走']),
    'tongnian:5': P('lianggejiujiu', ['①为争家产互相殴斗', '②逼母亲放弃嫁妆', '③戏弄盲眼工匠', '④酿成小茨冈惨死']),
    'zhaohuaxishi:2': P('fanainong', ['①横滨初识生误会', '②回国受排挤困顿', '③光复后任学监遭压', '④借酒浇愁溺水亡']),
    'zhaohuaxishi:3': P('shoujingwu', ['①方正质朴博学长者', '②待学生严格有风范', '③读书入迷摇头晃脑', '④备戒尺却极少罚人']),
    'zhaohuaxishi:4': P('yantaitai', ['①怂恿孩子冬天吃冰', '②唆使偷母亲首饰', '③暗中散布流言', '④临终催促呼喊父亲']),
    'xiyouji:1': P('tangseng', ['①受重托单骑西行', '②四圣试禅心不改', '③误信白骨精逐悟空', '④女儿国坚守佛心']),
    'xiyouji:3': P('shaseng', ['①流沙河受点化归依', '②一路牵马挑担', '③宝象国苦谏迎悟空', '④赴南海求证真假']),
    'xiyouji:4': P('bailongma', ['①纵火犯天条待罪', '②化白马代步西行', '③变身刺杀黄袍怪', '④催促八戒迎师兄']),
    'luotuoxiangzi:2': P('liusiye', ['①地痞起家开车厂', '②放高利贷剥削车夫', '③与虎妞决裂卖厂', '④晚年孤老遭嘲弄']),
    'luotuoxiangzi:3': P('xiaofuzi', ['①贫苦温顺的弱女', '②被父亲卖与军官', '③为养幼弟被迫卖身', '④不堪重压上吊自尽']),
    'luotuoxiangzi:4': P('caoxiansheng', ['①社会改良知识分子', '②待祥子如家人', '③绝境中答应收留', '④遭告密离北平避难']),
    'haidiliangwanli:2': P('kangsai', ['①教授的忠诚仆人', '②随主跳入冰海', '③精通生物分类', '④冷静归纳科属种']),
    'haidiliangwanli:3': P('nidelan', ['①加拿大捕鲸高手', '②一标枪救船长', '③思念陆地自由', '④大漩涡中生还']),
    'hongxingzhaoyao:1': P('zhouenlai', ['①百家坪会见斯诺', '②流利英语交谈', '③开列全套访问日程', '④举止优雅军纪严明']),
    'hongxingzhaoyao:3': P('helong', ['①两把菜刀闹革命', '②带兵有方体魄过人', '③深受部下百姓爱戴', '④少数民族地区威望高']),
    'hongxingzhaoyao:4': P('hongxiaogui', ['①平均二十岁的战士', '②艰苦中保持乐观', '③严守纪律拒收小费', '④长征途中视死如归']),
    'kunchongji:2': P('xishuai', ['①向阳斜坡挖洞穴', '②洞前设精致前庭', '③绝不寄人篱下', '④入夜振翅鸣唱']),
    'kunchongji:3': P('yinghuochong', ['①尾部柔和荧光', '②袭击蜗牛', '③喷射麻醉毒液', '④分解吸食猎物']),
    'jingdianchangtan:1': P('shangshu', ['①最早的历史文件汇编', '②上古君臣诏令', '③文辞佶屈聱牙', '④今古文尚书之争']),
    'jingdianchangtan:3': P('chunqiuzhuan', ['①孔子笔削春秋', '②微言大义笔法', '③编年体史书之始', '④左传公羊谷梁三传']),
    'jingdianchangtan:4': P('sishu', ['①朱熹抽出大学中庸', '②合编论语孟子', '③著四书章句集注', '④元明清科举教材']),
    'jingdianchangtan:5': P('shijihanshu', ['①司马迁发愤著史记', '②五体例纪传通史', '③史家之绝唱', '④班固作断代汉书']),
    'gangtieshi:2': P('dongniya', ['①林务官的女儿', '②借书指导保尔', '③留恋小资享乐', '④阶级鸿沟决裂']),
    'gangtieshi:3': P('lida', ['①团省委常委', '②战友与精神伴侣', '③误闻死讯另嫁', '④重逢互勉敬重']),
    'gangtieshi:4': P('daya', ['①遭虐待的房东女儿', '②保尔助其独立', '③结为革命伴侣', '④入党并助创作']),
    'aiqingshixuan:2': P('xiangtaiyang', ['①出狱后歌颂太阳', '②高举火把前行', '③呼唤驱逐黑暗', '④太阳象征民族希望']),
    'aiqingshixuan:3': P('limingdetongzhi', ['①黎明开口呼唤', '②呼唤城乡人民', '③准备迎接白日', '④预告光明破晓']),
    'aiqingshixuan:4': P('yuhuashi', ['①岩层中的游鱼化石', '②离开运动便无生命', '③镜子真实直率', '④光的赞歌颂正义']),
    'shuihuzhuan:2': P('songjiang', ['①飞马私放晁盖', '②怒杀阎婆惜', '③浔阳楼题反诗', '④力主招安终饮鸩']),
    'shuihuzhuan:3': P('likui', ['①江州劫法场', '②沂岭怒杀四虎', '③痛打假李逵', '④赠银放行李鬼']),
    'shuihuzhuan:4': P('wusong', ['①景阳冈赤手打虎', '②斗杀西门庆', '③醉打蒋门神', '④血溅鸳鸯楼']),
    'rulinwaishi:0': P('zhoujin', ['①六旬仍是老童生', '②塾中受尽冷遇', '③撞号板痛哭吐血', '④捐监后中举升官'],
                       imgs=[f'images/rulinwaishi-p4-zhoujin-c{i}.jpg' for i in range(1, 5)]),
    'rulinwaishi:3': P('kuangchaoren', ['①流落杭州孝养病父', '②灯下勤奋读书', '③结识马二先生', '④充枪手堕落下场']),
    'rulinwaishi:4': P('dushaoqing', ['①蔑视八股科举', '②装病拒朝廷征召', '③挥金资助穷友', '④携妻游山饮酒']),
    'jianai:2': P('hailun', ['①简爱最亲密的朋友', '②受罚仍宽恕仁爱', '③宗教安详坚韧', '④在简爱怀中离世']),
    'hongyan:1': P('xuyunfeng', ['①识破特务阴谋', '②掩护同志不幸被捕', '③痛斥特务头子', '④十指抠出越狱通道']),
    'hongyan:2': P('chenggang', ['①秘密承印挺进报', '②被捕身受酷刑', '③粉碎测谎逼供', '④放声嘲笑敌人无能']),
    'hongyan:4': P('shuangqiang', ['①华蓥山传奇英雄', '②双手各使驳壳枪', '③百发百中出神入化', '④川东岭间打击敌人']),
    'hongyan:5': P('qixiaoxuan', ['①装疯麻痹特务', '②组织狱中越狱', '③带头绝食斗争', '④出身豪门矢志不移']),
    'tangshisanbaishou:2': P('wangwei', ['①山居秋暝清幽', '②诗中有画画中有诗', '③使至塞上大漠孤烟', '④孟浩然平淡自然']),
    'tangshisanbaishou:3': P('gaoshi', ['①燕歌行慷慨悲壮', '②白雪歌雄奇瑰丽', '③出塞边关豪情', '④七绝圣手王昌龄']),
    'tangshisanbaishou:4': P('baijuyi', ['①倡导新乐府运动', '②文章合为时而著', '③长恨歌凄美绵长', '④琵琶行同是天涯']),
}

# ---------------------------------------------------------------- CSS
CSS = """
  /* ===== 四格连环画 (V4) ===== */
  .comic-row > td { background: transparent; border-bottom: 1px solid var(--border-color); }
  .comic-strip { background: linear-gradient(180deg, #fbfaf7 0%, #f7f5f0 100%); border: 1px solid var(--border-color); border-radius: 12px; padding: 0.75rem 0.9rem 0.9rem; }
  .comic-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.55rem; }
  .comic-title-badge { display: inline-flex; align-items: center; gap: 0.3rem; background: var(--brand-red); color: white; font-size: 0.72rem; font-weight: 700; padding: 0.16rem 0.55rem; border-radius: 999px; }
  .comic-chapter { font-size: 0.74rem; font-weight: 600; color: var(--text-muted); }
  .comic-panels { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; }
  .comic-panels figure { margin: 0; }
  .comic-panels img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px; border: 1px solid var(--border-color); cursor: zoom-in; background: #fff; transition: transform 0.15s ease, box-shadow 0.15s ease; }
  .comic-panels img:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(15, 23, 42, 0.14); }
  .comic-panels figcaption { margin-top: 0.3rem; font-size: 0.72rem; line-height: 1.5; color: var(--text-main); font-weight: 600; text-align: center; }
  @media (max-width: 760px) { .comic-panels { grid-template-columns: repeat(2, 1fr); } }
  .comic-lightbox { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.86); display: none; align-items: center; justify-content: center; z-index: 1200; cursor: zoom-out; }
  .comic-lightbox.show { display: flex; }
  .comic-lightbox img { max-width: 92vw; max-height: 92vh; border-radius: 10px; box-shadow: 0 18px 60px rgba(0, 0, 0, 0.5); }
"""

# ---------------------------------------------------------------- JS 数据与渲染
COMICS_JS = """
    const COMICS_DB = %s;
    function openComicLightbox(src) {
      document.getElementById('comicLightboxImg').src = src;
      document.getElementById('comicLightbox').classList.add('show');
    }
""" % json.dumps(COMICS, ensure_ascii=False, indent=2)

OLD_MAP = """                  ${b.characters_table.map(c => `
                    <tr>
                      <td>
                        <span class="char-name-tag">${c.name}</span>
                      </td>
                      <td class="char-plot-cell">
                        ${maskText(c.plots)}
                      </td>
                      <td>
                        <div class="char-trait-cell">
                          ${maskText(c.traits)}
                        </div>
                      </td>
                    </tr>
                  `).join('')}"""

NEW_MAP = """                  ${b.characters_table.map((c, cidx) => {
                    const comic = COMICS_DB[b.id + ':' + cidx];
                    return `
                    <tr>
                      <td>
                        <span class="char-name-tag">${c.name}</span>
                        ${comic ? '<span class="comic-title-badge" style="margin-top:0.3rem;">🎞 连环画</span>' : ''}
                      </td>
                      <td class="char-plot-cell">
                        ${maskText(c.plots)}
                      </td>
                      <td>
                        <div class="char-trait-cell">
                          ${maskText(c.traits)}
                        </div>
                      </td>
                    </tr>
                    ${comic ? `
                    <tr class="comic-row"><td colspan="3" style="padding-top:0.2rem;">
                      <div class="comic-strip">
                        <div class="comic-head">
                          <span class="comic-title-badge">🎞 四格连环画</span>
                          <span class="comic-chapter">${escapeMarkup(c.name)} · 典型情节画传（点击可放大）</span>
                        </div>
                        <div class="comic-panels">
                          ${comic.imgs.map((img, i) => `
                            <figure><img src="${img}" alt="${escapeMarkup(c.name)}连环画第${i + 1}格" loading="lazy" onclick="openComicLightbox('${img}')"><figcaption>${maskText(comic.caps[i])}</figcaption></figure>
                          `).join('')}
                        </div>
                      </div>
                    </td></tr>` : ''}
                  `;
                  }).join('')}"""

LIGHTBOX_HTML = """
  <div class="comic-lightbox" id="comicLightbox" onclick="this.classList.remove('show')">
    <img id="comicLightboxImg" src="" alt="连环画放大">
  </div>
"""

def main():
    src = SRC.read_text(encoding='utf-8')

    assert OLD_MAP in src, '人物表格模板未命中（V3 已被改动？）'
    assert '</style>' in src and LIGHTBOX_HTML.strip() not in src

    src = src.replace(OLD_MAP, NEW_MAP, 1)

    # COMICS_DB + 灯箱函数：插到 renderTocNav 定义之前，运行时先于 DOMContentLoaded
    anchor = '    function renderTocNav() {'
    assert anchor in src
    src = src.replace(anchor, COMICS_JS + '\n' + anchor, 1)

    src = src.replace('</style>', CSS + '</style>', 1)
    src = src.replace('  <footer>', LIGHTBOX_HTML + '\n  <footer>', 1)

    src = src.replace('中考名著阅读 39页考点精编全书 (V3)', '中考名著阅读 39页考点精编全书 (V4 · 名家四格连环画版)')
    src = src.replace('(V3 全景精排版)', '(V4 全景精排版 · 连环画版)')

    DST.write_text(src, encoding='utf-8')
    print(f'OK -> {DST}  ({len(src)/1024:.0f} KB)')
    print(f'连环画条目: {len(COMICS)} 人')

if __name__ == '__main__':
    sys.exit(main())
