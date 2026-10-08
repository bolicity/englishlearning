#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从国家中小学智慧教育平台（教育部 basic.smartedu.cn）拉取官方电子教材 PDF。
范围：义务教育教科书（五·四学制）·语文 六年级~九年级 上下册，共 8 册。

流程：教材索引 part_*.json → 条目 id → ndrv2 details 接口 → ti_items 中 format=pdf 的
ti_storages（去掉 -private 后缀即可公开访问）→ 下载 → 校验页数。
"""
import json, os, re, sys, time, urllib.parse, urllib.request

OUT_DIR = "/Users/emily/Developer/Projects/owenlearining/学科材料/01_语文/教材"
IDS = [
    ("六年级上册", "2ca4002f-cb3d-4a21-bcfe-ebb94032a400"),
    ("六年级下册", "a953eeec-db0c-4c8b-860f-aa94f4727b6b"),
    ("七年级上册", "df82f043-281e-48ef-931a-34b951ae8c26"),
    ("七年级下册", "d08cae24-887e-45bd-8ccb-b56af508a293"),
    ("八年级上册", "c8b697f9-6a7a-4057-85ef-7651f68aa91e"),
    ("八年级下册", "03491549-8712-48a3-8fc8-5a616e6f492e"),
    ("九年级上册", "d6941a82-0aa3-4c6c-a198-b95ea84a6852"),
    ("九年级下册", "ab06a72c-93e6-4135-b549-900db6783fa9"),
]
DETAIL = "https://s-file-{h}.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{rid}.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"


def enc_url(u):
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc,
                                    "/".join(urllib.parse.quote(x) for x in p.path.split("/")),
                                    p.query, ""))


def get(url, rng=None, timeout=90):
    h = {"User-Agent": UA, "Referer": "https://basic.smartedu.cn/"}
    if rng:
        h["Range"] = rng
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout)


def details(rid):
    last = None
    for h in (2, 1, 3):
        try:
            with get(DETAIL.format(h=h, rid=rid)) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:                                    # noqa: BLE001
            last = e
    raise RuntimeError(f"details 失败 {rid}: {last}")


def pdf_url(det):
    for t in det.get("ti_items", []):
        if t.get("ti_format") == "pdf":
            for u in t.get("ti_storages", []):
                return u.replace("-private.ykt", ".ykt"), t.get("ti_size", 0)
    raise RuntimeError("未找到 pdf 资源")


def page_count(path):
    with open(path, "rb") as f:
        blob = f.read(4_000_000)
        f.seek(max(0, os.path.getsize(path) - 2_000_000))
        blob += f.read()
    counts = [int(m) for m in re.findall(rb"/Type\s*/Pages[^>]*?/Count\s+(\d+)", blob)]
    if not counts:
        counts = [int(m) for m in re.findall(rb"/Count\s+(\d+)", blob)]
    return max(counts) if counts else 0


def download(url, dest, expect=0):
    tmp = dest + ".part"
    done = os.path.getsize(tmp) if os.path.exists(tmp) else 0
    if expect and done >= expect:
        os.replace(tmp, dest)
        return done
    rng = f"bytes={done}-" if done else None
    with get(enc_url(url), rng=rng, timeout=300) as r:
        total = None
        cr = r.headers.get("Content-Range")
        if cr and "/" in cr:
            total = int(cr.split("/")[-1])
        elif r.headers.get("Content-Length"):
            total = int(r.headers["Content-Length"]) + done
        mode = "ab" if done else "wb"
        t0 = time.time()
        with open(tmp, mode) as f:
            while True:
                chunk = r.read(262144)
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                if total and done % (4 << 20) < 262144:
                    pct = done * 100 // total
                    sp = done / max(1e-6, time.time() - t0) / 1048576
                    print(f"    {pct:3d}%  {done/1048576:6.1f}/{total/1048576:.1f} MB  {sp:.1f} MB/s", flush=True)
    size = os.path.getsize(tmp)
    if expect and size != expect:
        print(f"    ! 大小不符: {size} != {expect}", flush=True)
    os.replace(tmp, dest)
    return size


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    report = []
    for grade, rid in IDS:
        name = f"义务教育教科书（五·四学制）语文 {grade}.pdf"
        dest = os.path.join(OUT_DIR, name)
        print(f"=== {grade}  ({rid})", flush=True)
        if os.path.exists(dest) and page_count(dest) > 10:
            print("    已存在，跳过", flush=True)
            report.append((grade, os.path.getsize(dest), page_count(dest), "skip"))
            continue
        try:
            u, expect = pdf_url(details(rid))
            size = download(u, dest, expect)
            pc = page_count(dest)
            ok = open(dest, "rb").read(5) == b"%PDF-"
            print(f"    完成 {size/1048576:.1f} MB / {pc} 页 / PDF头={ok}", flush=True)
            report.append((grade, size, pc, "ok" if ok and pc else "BAD"))
        except Exception as e:                                     # noqa: BLE001
            print(f"    !! 失败: {e}", flush=True)
            report.append((grade, 0, 0, f"FAIL {e}"))
    print("\n=== 汇总 ===")
    for g, s, p, st in report:
        print(f"{g:6s} {s/1048576:7.1f} MB  {p:4d} 页  {st}")


if __name__ == "__main__":
    main()
