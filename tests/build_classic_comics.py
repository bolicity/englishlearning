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
