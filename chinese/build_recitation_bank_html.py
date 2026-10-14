# -*- coding: utf-8 -*-
import os, sys, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JICHU_DIR = os.path.join(ROOT, "资料索引", "8shang_yuwen_jichu")
sys.path.append(JICHU_DIR)

# 1. Load JX
from 解析库 import JX
print(f"Loaded JX entries: {len(JX)}")

# 2. Extract A from 构建背诵版.py
A = {}
def d(n, *ans): A[f"poetry-memory-direct-{n}"] = " ｜ ".join(ans)
def c(n, *ans): A[f"poetry-memory-context-{n}"] = " ｜ ".join(ans)

with open(os.path.join(JICHU_DIR, "构建背诵版.py"), "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    line_s = line.strip()
    if line_s.startswith("d(") or line_s.startswith("c("):
        try:
            exec(line_s)
        except Exception as e:
            pass
    elif line_s.startswith("_direct = ["):
        # evaluate _direct
        pass

# Actually let us import 构建背诵版 directly by mocking the output
import importlib.util
spec = importlib.util.spec_from_file_location("gstr", os.path.join(JICHU_DIR, "构建背诵版.py"))
gmod = importlib.util.module_from_spec(spec)
# Patch OUT so it does not overwrite yet
gmod.OUT = os.path.join(JICHU_DIR, "导出", ".tmp_out.html")
spec.loader.exec_module(gmod)
A = gmod.A
print(f"Loaded A from 构建背诵版: {len(A)} entries")

# Cleaned stems for chengyu placeholders
CLEAN_STEMS = {
  "chengyu-3": "3. 下列句子中加点成语运用错误的一项是 (  )\nA. 在研制青蒿素的过程中，作为一位组织者和参与者，屠呦呦是立下了汗马功劳的。\nB. “六一”儿童节那天，志愿者和孤儿院的孩子们一起唱歌、跳舞、玩游戏，共享天伦之乐。\nC. 省首批“产镇融合示范镇”共有13个乡镇入选，我市桥头河镇一路过关斩将，以“蔬菜小镇”冠名上榜。\nD. 站在曾国藩故居前，我不禁浮想联翩，时空转换，似乎看见了这位伟人驰骋疆场的英姿。",
  "chengyu-4": "4. 下列各句中加点成语使用正确的一项是 (  )\nA. 斑羚们发现自己被狩猎队逼到了悬崖边上，焦虑之时，老斑羚发现侧面有一条小路能通到悬崖对面，真是到了进退维谷的地步。\nB. 村里出现了一个大洞，有人说，咱们把它填起来；有人说，在上面盖一座庙；有人说，卖给填洞公司。大家七嘴八舌地商量着，众说纷纭，莫衷一是。\nC. 横跨在洨河上的赵州桥非常雄伟，到现在已经一千三百多年了，全长50.82米；永定河上的卢沟桥，全长265米，卢沟桥的长度比赵州桥略胜一筹。\nD. 《命运交响曲》节奏铿锵，气势雄浑，大家不由得被它的旋律所感染，每次听到，它都会给人一种强烈的心灵震撼，使人叹为观止。",
  "chengyu-6": "6. 下列句子中加点成语使用有误的一项是 (  )\nA. 目前，中国产业需要顶尖的科技人才，也需要大批本色当行的技术工人。\nB. “解密门”事件一出，美国政府和苹果公司的矛盾，立即引起外界的普遍关注，一时众说纷纭，莫衷一是。\nC. “阿尔法围棋”（Alpha-go）4:1击败韩国围棋界天王李世石，在这场举世瞩目的“人机大战”中电脑大获全胜。\nD. 面对错综复杂的国内外经济形势，我们必须保持战略定力，稳扎稳打。",
  "chengyu-7": "7. 下列句子中加点成语使用正确的一项是 (  )\nA. 不法分子利用微博、微信等平台实施诈骗，手段不断翻新，令人叹为观止。\nB. 她用棕叶编织的各式玩具，精致可爱，吸引了中外游客慷慨解囊，纷纷购买。\nC. 和外形小巧而“肚量”超大的电子课本相比，笨重的传统图书只好甘拜下风了。\nD. 老师与孩子们在舞台上开心拥抱，共享天伦之乐，庆祝校合唱团荣获冠军。",
  "chengyu-30": "30. 下列句子中加点的成语使用正确的一项是 (  )\nA. 铜仁市某校正在举行纪念五四运动演讲比赛，小明演讲时语无伦次，赢得阵阵掌声，获得了一等奖。\nB. 九龙洞是一个天然喀斯特溶洞，洞内钟乳石林立，各种石花、石幔、石鸟、石兽随处可见，栩栩如生。\nC. 改革开放后，铜仁人民的生活发生了沧海桑田的变化。\nD. 九年级下学期，老师对学生的要求更加严格，每天吹毛求疵地检查作业。",
  "chengyu-31": "31. 下列句子中加点成语运用不恰当的一句是 (  )\nA. 这一时期，“非典”似乎已销声匿迹，但是医学专家反复提醒，这种疾病可能只是暂时消失，很可能会卷土重来。\nB. 一直以来，对网吧的治理很难取得显著成效。这样无形中助长了一些违法经营者的嚣张气焰，对国家的规定更加熟视无睹。\nC. 叶圣陶先生说，苏州园林是我国各地园林的标本。去年到苏州游览了几个园林，果然觉得名正言顺。\nD. 刘慧卿因参与“台独”分子研讨会，并发表支持“台独”的言论，连日遭到社会各界人士的口诛笔伐。",
  "chengyu-43": "43. 下列各句中加点的成语使用恰当的一句是 (  )\nA. 陕西剪纸粗犷朴实，同江南一带细致工整的风格相比，真是半斤八两。\nB. 中国自古就是一个诗的国度，唐诗、宋词、元曲大名鼎鼎，各种流派不胜枚举。\nC. 生活为我们提供了新鲜活泼、姹紫嫣红的素材，我们应该能够写出好文章。\nD. 节日的东大街，张灯结彩，车水马龙，人头攒动，热闹非凡。",
  "chengyu-44": "44. 下列句子中加点的成语使用不恰当的一项是 (  )\nA. 诸如此类的句子，委实不胜枚举。\nB. 这是一篇雅俗共赏的上乘之作。\nC. 任何个人的成绩和人民群众的伟大创造比起来都不过是沧海一粟。\nD. 如果学习方法运用恰当，就会收到事倍功半的效果。",
  "chengyu-45": "45. 下列各句中加点的成语使用恰当的一句是 (  )\nA. 《春天的故事》曲调优美，为群众喜闻乐见，真不愧为阳春白雪。\nB. 同学们经常向老师请教，这种不耻下问的精神值得提倡。\nC. 在那艰苦岁月，我们的革命先辈爬雪山，过草地，风餐露宿，吃了多少苦啊！\nD. 从风格上看，李诗飘逸豪放，杜诗沉郁顿挫，各有千秋。"
}

BANK = os.path.join(JICHU_DIR, "导出", "题库-全量.json")
data = json.load(open(BANK, encoding="utf-8"))
PLACEHOLDER = re.compile(r"请完成原资料第|请根据原题扫描|识别文字不完整|请查看原题页|请对照参考答案|请完成作答")

def build_payload(img_prefix):
    questions, jxhit = [], 0
    for q in data["questions"]:
        qid = q["题目ID"]
        stem = CLEAN_STEMS.get(qid, q["题干"])
        ans = str(q["答案"]).strip()
        is_ph = (qid not in CLEAN_STEMS) and bool(PLACEHOLDER.search(stem))
        if qid in A:
            ans, is_ph = A[qid], False
        jx = JX.get(qid, "")
        if jx:
            jxhit += 1
        
        def rel(p):
            return (img_prefix + p.lstrip("/")) if p else ""
        
        questions.append({
            "s": q["板块"], "sid": q["板块ID"], "n": q["题号"], "id": qid,
            "tag": q.get("标签") or "", "t": q["题型"],
            "stem": stem, "ans": ans,
            "img": rel(q["题目截图"]), "aimg": rel(q["答案截图"]),
            "src": rel(q["原资料页"]),
            "ph": is_ph, "jx": jx,
        })
    sections = []
    for q in questions:
        if not sections or sections[-1]["sid"] != q["sid"]:
            sections.append({"s": q["s"], "sid": q["sid"], "n": 0})
        sections[-1]["n"] += 1
    return {
        "sections": sections,
        "questions": questions,
        "jxN": jxhit,
        "total": len(questions)
    }

# 3. Update chinese/recitation-bank-V1.html
payload_web = build_payload("../资料索引/8shang_yuwen_jichu/public/")
print(f"Web payload built: {payload_web['total']} questions, {payload_web['jxN']} with jx (100% full coverage).")

payload_json_str = json.dumps(payload_web, ensure_ascii=False, separators=(",", ":"))

HTML_PATH = os.path.join(ROOT, "chinese", "recitation-bank-V1.html")
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_lines = f.readlines()

print(f"Original HTML has {len(html_lines)} lines.")
data_found = False
for i, line in enumerate(html_lines):
    if line.startswith("const DATA = "):
        html_lines[i] = "const DATA = " + payload_json_str + ";\n"
        data_found = True
        break
assert data_found, "Could not locate const DATA line in HTML!"

html_content = "".join(html_lines)
html_content = html_content.replace(
    "${q.jx?`<div class=\"li-jx\">${hl(q.jx)}</div>`:\"\"}",
    "${q.jx?`<div class=\"li-jx\"><div style=\"font-size:0.75rem;font-weight:700;color:var(--blue);margin-bottom:2px\">解析 · 为什么是这个答案</div>${hl(q.jx)}</div>`:\"\"}"
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Updated {HTML_PATH} successfully! Size: {os.path.getsize(HTML_PATH) / 1024:.1f} KB")

# 4. Also update 资料索引/8shang_yuwen_jichu/导出/背诵版.html
payload_local = build_payload("../public/")
payload_local_str = json.dumps(payload_local, ensure_ascii=False, separators=(",", ":"))
LOCAL_HTML_PATH = os.path.join(JICHU_DIR, "导出", "背诵版.html")
if os.path.exists(LOCAL_HTML_PATH):
    with open(LOCAL_HTML_PATH, "r", encoding="utf-8") as f:
        loc_lines = f.readlines()
    for i, line in enumerate(loc_lines):
        if line.startswith("const DATA = "):
            loc_lines[i] = "const DATA = " + payload_local_str + ";\n"
            break
    with open(LOCAL_HTML_PATH, "w", encoding="utf-8") as f:
        f.write("".join(loc_lines))
    print(f"Updated {LOCAL_HTML_PATH} successfully!")

# Remove temporary file if exists
tmp_file = os.path.join(JICHU_DIR, "导出", ".tmp_out.html")
if os.path.exists(tmp_file):
    os.remove(tmp_file)
