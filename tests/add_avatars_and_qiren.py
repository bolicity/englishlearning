#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1) p3：给「第55回市井四大奇人」四张卡片各加一幅单人画 + 图下小标题
2) p4：取消矩阵里 4 条分组插画行；给 30 位人物各加一个小头像
   （头像复用已生成的连环画首格，裁成 240x240 方图）
改前备份到 /tmp/rulin_backup/。幂等。
"""
import glob, html, os, re, shutil, subprocess

BASE = "/Users/emily/Developer/Projects/owenlearining/chinese"
IMG = os.path.join(BASE, "images")
COMIC = "/tmp/rulin_comic"
BACKUP = "/tmp/rulin_backup"

# ---------- p3 四大奇人 ----------
QIREN = [
    ("季遐年", "jixianian", "写字冠绝一时，傲骨铮铮"),
    ("王太",   "wangtai",   "布衣棋手，横扫京城国手"),
    ("盖宽",   "gaikuan",   "开茶馆营生，慷慨济贫"),
    ("荆元",   "jingyuan",  "裁缝操琴，大隐隐于市"),
]
QCSS = """
    .hero-mini-img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 8px;
      border: 1px solid var(--border-color); box-shadow: 0 1px 4px rgba(15,23,42,0.07);
      cursor: zoom-in; display: block; margin-bottom: 0.5rem; transition: transform 0.18s ease; }
    .hero-mini-img:hover { transform: scale(1.02); }
    .hero-mini-cap { font-size: 0.74rem; color: var(--text-muted); font-weight: 600; margin-bottom: 0.45rem; }
"""

# ---------- p4 头像 ----------
AVCSS = """
    .matrix-avatar { width: 52px; height: 52px; object-fit: cover; border-radius: 8px;
      border: 1px solid var(--border-color); box-shadow: 0 1px 3px rgba(15,23,42,0.08);
      cursor: zoom-in; display: block; margin-bottom: 0.35rem; }
"""

def crop_sq(src_png, dest_jpg, size=240, q=82):
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(q),
                    "--cropOffset", "0", "47", "-c", "930", "930", "-Z", str(size),
                    src_png, "--out", dest_jpg], check=True, capture_output=True)

def comic_panel(slug, n):
    hits = sorted(glob.glob(os.path.join(COMIC, f"连环画_{slug}_{n}_*.png")))
    return hits[0] if hits else None

def avatar_source(slug, fallback):
    for n in (1, 2, 3):
        p = comic_panel(slug, n)
        if p:
            return p
    return fallback

def backup(path):
    os.makedirs(BACKUP, exist_ok=True)
    shutil.copy2(path, os.path.join(BACKUP, os.path.basename(path)))

def do_p3():
    path = os.path.join(BASE, "rulinwaishi-p3-V1.html")
    src = open(path, encoding="utf-8").read()
    if "hero-mini-img" in src:
        print("p3 奇人配图: 已处理，跳过")
        return
    for name, slug, cap in QIREN:
        pat = re.compile(
            r'(<div class="hero-mini-card">\s*<div class="hero-mini-name"><span>'
            + re.escape(name) + r"</span>)")
        m = pat.search(src)
        assert m, f"p3 找不到 {name} 卡片"
        img = (f'\n              <img class="hero-mini-img" src="images/rulinwaishi-p3-{slug}.jpg" '
               f'alt="{name}故事插图" loading="lazy" '
               f"onclick=\"openLightbox('images/rulinwaishi-p3-{slug}.jpg')\">\n"
               f'              <div class="hero-mini-cap">🖼 {html.escape(cap)}</div>')
        src = src[:m.end(1)] + img + src[m.end(1):]
    assert src.count("  </style>") == 1
    src = src.replace("  </style>", QCSS + "  </style>", 1)
    backup(path)
    open(path, "w", encoding="utf-8").write(src)
    print("p3 奇人配图: 4 张已插入")

def matrix_names(src):
    t0 = src.find('id="matrixTable"'); t1 = src.find("</table>", t0)
    rows = re.findall(r'<tr data-group="\w+">(.*?)</tr>', src[t0:t1], re.S)
    out = []
    for row in rows:
        b = re.search(r'class="role-badge">([^<]+)</span>', row)
        if b:
            out.append(b.group(1))
    return out

def do_p4():
    path = os.path.join(BASE, "rulinwaishi-p4-V1.html")
    src = open(path, encoding="utf-8").read()
    changed = []
    # 1) 取消 4 条分组插画行
    grp = re.compile(r'\n\s*<tr><td colspan="3"[^>]*><img src="images/rulinwaishi-g\d-[^"]*"[^>]*/></td></tr>')
    n = len(grp.findall(src))
    if n:
        src = grp.sub("", src)
        changed.append(f"删除 {n} 条分组插画")
    # 2) 30 人头像
    if "matrix-avatar" not in src:
        import importlib.util
        spec = importlib.util.spec_from_file_location("b", os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "build_rulin_comics.py"))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        name2slug = {st["name"]: st["slug"] for st in m.S}
        name2slug["郭孝子 (郭力)"] = "guoxiaozi"
        name2slug["凤四老爹"] = "fengsilaodie"
        made = 0
        for name in matrix_names(src):
            slug = name2slug.get(name)
            assert slug, f"p4 矩阵人物 {name} 无 slug 映射"
            dest = os.path.join(IMG, f"rulinwaishi-av-{slug}.jpg")
            if not os.path.exists(dest):
                fb = os.path.join(IMG, f"rulinwaishi-p2-{slug}.jpg")  # 兜底：行首故事图
                s = avatar_source(slug, fb)
                assert s, f"{slug} 无头像源图"
                crop_sq(s, dest)
                made += 1
            badge = f'<td><span class="role-badge">{name}</span>'
            if f'rulinwaishi-av-{slug}.jpg' in src and f'class="matrix-avatar"' not in src.split(badge)[0][-400:]:
                pass
            av = (f'<td><img class="matrix-avatar" src="images/rulinwaishi-av-{slug}.jpg" '
                  f'alt="{html.escape(name)}头像" loading="lazy" '
                  f"onclick=\"openLightbox('images/rulinwaishi-av-{slug}.jpg')\">"
                  f'<span class="role-badge">{name}</span>')
            if badge in src:
                src = src.replace(badge, av, 1)
            else:
                print(f"!! p4 找不到 {name} 的 badge 单元格")
        changed.append(f"新增头像 {made} 张")
        assert src.count("  </style>") == 1
        src = src.replace("  </style>", AVCSS + "  </style>", 1)
    if not changed:
        print("p4: 无变更")
        return
    backup(path)
    open(path, "w", encoding="utf-8").write(src)
    print("p4:", ", ".join(changed))

if __name__ == "__main__":
    do_p3()
    do_p4()
