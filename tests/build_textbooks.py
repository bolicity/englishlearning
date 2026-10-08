#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从国家中小学智慧教育平台的公开页图（1303x1842，比官方转码 PDF 的 744x1056 清晰一倍）
自建 8 册语文教材 PDF。官方 PDF 直链对下册 401 鉴权，页图全量公开，故统一走页图重建。

流程：探测页数 → 并行下载页图 → sips 重压缩(q65) → 纯 Python 组装 DCTDecode PDF。
可重复运行：已完成的册次跳过，缺页补下。
"""
import json, os, re, subprocess, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/Users/emily/Developer/Projects/owenlearining/学科材料/01_语文/教材"
RAW = "/tmp/keben"
DETAIL = "https://s-file-{h}.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{rid}.json"
HOSTS = ["r1-ndr", "r2-ndr", "r3-ndr"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
Q = 65                       # sips 重压缩质量
BOOKS = [
    ("六年级上册", "2ca4002f-cb3d-4a21-bcfe-ebb94032a400"),
    ("六年级下册", "a953eeec-db0c-4c8b-860f-aa94f4727b6b"),
    ("七年级上册", "df82f043-281e-48ef-931a-34b951ae8c26"),
    ("七年级下册", "d08cae24-887e-45bd-8ccb-b56af508a293"),
    ("八年级上册", "c8b697f9-6a7a-4057-85ef-7651f68aa91e"),
    ("八年级下册", "03491549-8712-48a3-8fc8-5a616e6f492e"),
    ("九年级上册", "d6941a82-0aa3-4c6c-a198-b95ea84a6852"),
    ("九年级下册", "ab06a72c-93e6-4135-b549-900db6783fa9"),
]


def enc(u):
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc,
                                    "/".join(urllib.parse.quote(x) for x in p.path.split("/")), "", ""))


def fetch(url, rng=None, timeout=60):
    h = {"User-Agent": UA, "Referer": "https://basic.smartedu.cn/"}
    if rng:
        h["Range"] = rng
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout)


def image_base(rid):
    """从 details 的 ti_items 里拿页图 folder 的 base 路径。"""
    for h in (2, 1, 3):
        try:
            with fetch(DETAIL.format(h=h, rid=rid)) as r:
                d = json.loads(r.read().decode())
            break
        except Exception:                                       # noqa: BLE001
            continue
    else:
        raise RuntimeError("details 拉取失败")
    for t in d.get("ti_items", []):
        if t.get("ti_format") == "folder" and "/transcode/image" in t.get("ti_storage", ""):
            u = t["ti_storages"][0]
            return re.sub(r"^https://[^/]+", "", u).replace("-private.ykt", ".ykt")
    raise RuntimeError("无页图资源")


def page_ok(base, n):
    for h in HOSTS:
        try:
            with fetch(f"https://{h}.ykt.cbern.com.cn{base}/{n}.jpg", rng="bytes=0-64", timeout=20) as r:
                if r.status in (200, 206):
                    return h
        except Exception:                                       # noqa: BLE001
            pass
    return None


def probe_count(base):
    """二分探测最大页码（页图 1..N 连续存在）。"""
    lo, hi = 1, 400
    while not page_ok(base, hi):
        hi //= 2
        if hi < 40:
            raise RuntimeError("探测页数失败")
    lo = hi
    while True:
        n = min(hi * 2, 400)
        if page_ok(base, n):
            hi = n
            if n == 400:
                return 400
        else:
            break
    a, b = hi, hi * 2
    while a + 1 < b:
        m = (a + b) // 2
        if page_ok(base, m):
            a = m
        else:
            b = m
    return a


def dl_page(args):
    base, n, dest = args
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        return n, "cached"
    for h in HOSTS:
        for attempt in range(2):
            try:
                with fetch(f"https://{h}.ykt.cbern.com.cn{base}/{n}.jpg", timeout=90) as r:
                    d = r.read()
                if d[:2] == b"\xff\xd8":
                    with open(dest, "wb") as f:
                        f.write(d)
                    return n, "ok"
            except Exception:                                   # noqa: BLE001
                time.sleep(1)
    return n, "FAIL"


def jpg_size(data):
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        m = data[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3):
            h = (data[i + 5] << 8) | data[i + 6]
            w = (data[i + 7] << 8) | data[i + 8]
            return w, h
        i += 2 + ((data[i + 2] << 8) | data[i + 3])
    return 0, 0


def recompress(src, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        return
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(Q),
                    src, "--out", dst], check=True, capture_output=True)


def build_pdf(pages, out):
    """pages: 按页码排序的 jpg 路径列表。A4 纵向整页铺放。"""
    PW, PH = 595.276, 841.89
    objs = {}                                   # obj_id -> bytes
    n = len(pages)
    kids = []
    for i, p in enumerate(pages, 1):
        data = open(p, "rb").read()
        w, h = jpg_size(data)
        pid, iid, cid = 3 + (i - 1) * 3, 4 + (i - 1) * 3, 5 + (i - 1) * 3
        kids.append(f"{pid} 0 R")
        objs[pid] = (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PW} {PH}] "
                     f"/Resources << /XObject << /Im{i} {iid} 0 R >> >> /Contents {cid} 0 R >>").encode()
        objs[iid] = (f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} "
                     f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(data)} >>\nstream\n").encode() + data + b"\nendstream"
        content = f"q {PW} 0 0 {PH} 0 0 cm /Im{i} Do Q".encode()
        objs[cid] = b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream"
    buf = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    order = [1, 2] + [x for i in range(n) for x in (3 + i * 3, 4 + i * 3, 5 + i * 3)]
    objs[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objs[2] = ("<< /Type /Pages /Kids [" + " ".join(kids) + f"] /Count {n} >>").encode()
    for oid in order:
        offsets[oid] = len(buf)
        buf += f"{oid} 0 obj\n".encode() + objs[oid] + b"\nendobj\n"
    xref = len(buf)
    size = max(order) + 1
    buf += f"xref\n0 {size}\n0000000000 65535 f \n".encode()
    for oid in range(1, size):
        buf += (f"{offsets.get(oid, 0):010d} 00000 n \n").encode()
    buf += (f"trailer\n<< /Size {size} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n").encode()
    with open(out, "wb") as f:
        f.write(bytes(buf))


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    os.makedirs(OUT_DIR, exist_ok=True)
    summary = []
    for grade, rid in BOOKS:
        if only and not any(k in grade for k in only):
            continue
        name = f"义务教育教科书（五·四学制）语文 {grade}.pdf"
        out = os.path.join(OUT_DIR, name)
        rawdir = os.path.join(RAW, grade)
        os.makedirs(rawdir, exist_ok=True)
        print(f"=== {grade}", flush=True)
        if os.path.exists(out) and os.path.getsize(out) > 5_000_000:
            print("    PDF 已存在，跳过", flush=True)
            summary.append((grade, "skip"))
            continue
        base = image_base(rid)
        t0 = time.time()
        count = probe_count(base)
        print(f"    页数探测: {count} 页（{time.time()-t0:.0f}s）", flush=True)
        tasks = [(base, n, os.path.join(rawdir, f"{n:04d}.jpg")) for n in range(1, count + 1)]
        fails = []
        done = 0
        with ThreadPoolExecutor(6) as ex:
            futs = [ex.submit(dl_page, t) for t in tasks]
            for fut in as_completed(futs):
                n, st = fut.result()
                done += 1
                if st == "FAIL":
                    fails.append(n)
                if done % 40 == 0:
                    print(f"    下载 {done}/{count}（缺 {len(fails)}）", flush=True)
        if fails:
            print(f"    !! 下载失败页: {sorted(fails)}", flush=True)
            summary.append((grade, f"FAIL pages {fails[:5]}"))
            continue
        cdir = os.path.join(rawdir, "c")
        os.makedirs(cdir, exist_ok=True)
        with ThreadPoolExecutor(4) as ex:
            list(ex.map(lambda t: recompress(t[0], t[1]),
                        [(os.path.join(rawdir, f"{n:04d}.jpg"), os.path.join(cdir, f"{n:04d}.jpg"))
                         for n in range(1, count + 1)]))
        pages = [os.path.join(cdir, f"{n:04d}.jpg") for n in range(1, count + 1)]
        build_pdf(pages, out)
        sz = os.path.getsize(out) / 1048576
        print(f"    完成: {sz:.1f} MB / {count} 页", flush=True)
        summary.append((grade, f"{sz:.1f}MB {count}p"))
    print("\n=== 汇总 ===")
    for g, s in summary:
        print(f"{g}  {s}")


if __name__ == "__main__":
    main()
