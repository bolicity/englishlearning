# -*- coding: utf-8 -*-
import os
import sys

# Import the CASES_DATA from upgrade_interdisciplinary
from upgrade_interdisciplinary import CASES_DATA

cases_html = []
for c in CASES_DATA:
    img_html = ""
    if c.get("images"):
        img_items = []
        for img in c["images"]:
            img_items.append(f"""
          <div class="exam-img-item">
            <img src="{img['src']}" alt="{img['caption']}" onclick="openLightbox(this.src)" title="点击放大查看">
            <div class="exam-img-caption">{img['caption']}</div>
          </div>""")
        img_html = f"""
        <div class="exam-img-grid">
          {"".join(img_items)}
        </div>"""

    badges_html = "".join([f'<span class="c-badge c-badge-{btype}">{text}</span>' for text, btype in c["badges"]])

    questions_html = []
    for i, q in enumerate(c["questions"]):
        q_id = f"{c['id']}-q{i+1}"
        questions_html.append(f"""
        <div class="question-item">
          <div class="q-header">
            <span><b>{q['num']}</b></span>
            <span class="q-score-badge">{q['score']}</span>
          </div>
          <div class="q-stem">{q['stem']}</div>
          <button class="q-answer-toggle" onclick="toggleAnswer('{q_id}', this)">💡 查看本题采分答案</button>
          <div class="q-answer-box" id="{q_id}">
            <div><b>【官方标准答案】</b>：<span class="ans-highlight">{q['answer']}</span></div>
            <div class="grading-point">{q['point']}</div>
          </div>
        </div>""")

    nodes_html = []
    for idx, node in enumerate(c["chain"]):
        nodes_html.append(f'<div class="node-box">{node}</div>')
        if idx < len(c["chain"]) - 1:
            nodes_html.append('<span class="arrow-sign">➔</span>')

    case_block = f"""
    <!-- {c['id']}: {c['title']} -->
    <div class="case-card" data-cat="{c['cat']}" id="{c['id']}">
      <div class="case-card-header">
        <div class="case-title-row">
          <span class="case-index">{c['index']}</span>
          <span class="case-title">{c['title']}</span>
        </div>
        <div class="case-badges">
          {badges_html}
        </div>
      </div>
      <div class="case-body">

        <!-- 真实原卷考题情境材料与配图 -->
        <div class="exam-material-card">
          <div class="exam-material-title">
            <span>📌 真实原卷情境材料与考查图表</span>
          </div>
          <div class="exam-material-text">
            {c['bg_text']}
          </div>
          {img_html}
        </div>

        <!-- 真实原题设问清单 -->
        <div class="exam-questions-section">
          <div class="questions-title-row">
            <h4>📋 原卷设问清单（中考 15 分全真题目）</h4>
            <button class="batch-toggle-btn" onclick="toggleAllAnswersInCase('{c['id']}', this)">👁️ 展开/收起全部答案</button>
          </div>
          <div class="questions-list">
            {"".join(questions_html)}
          </div>
        </div>

        <!-- 逻辑链与踩分范本 -->
        <div class="cause-chain-wrap">
          <div class="cause-chain-title">🔗 官方满分因果逻辑链推演</div>
          <div class="chain-nodes">
            {"".join(nodes_html)}
          </div>
          <div class="standard-answer-text">
            <b>满分采分范本</b>：{c['std_answer']}
          </div>
        </div>

        <!-- 易错失分雷区 -->
        <div class="trap-box">
          ⚠️ <b>易错失分雷区与避坑指南</b>：{c['trap']}
        </div>

      </div>
    </div>"""
    cases_html.append(case_block)

all_cases_rendered = "\n".join(cases_html)

full_page_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>上海中考跨学科案例分析 12 篇全真题专项拆解与答卷套路工作台 V3</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --border-color: #E2E8F0;
      
      --text-primary: #0F172A;
      --text-secondary: #475569;
      --text-muted: #64748B;
      
      --purple-main: #7C3AED;
      --purple-light: #9333EA;
      --purple-bg: #FAF5FF;
      --purple-border: #E9D5FF;
      
      --blue-main: #2563EB;
      --blue-bg: #EFF6FF;
      --blue-border: #BFDBFE;
      
      --green-main: #059669;
      --green-bg: #ECFDF5;
      
      --amber-main: #D97706;
      --amber-bg: #FFFBEB;
      
      --red-main: #DC2626;
      --red-bg: #FEF2F2;

      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.07);
      --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.08);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-main);
      color: var(--text-primary);
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
    }}

    /* Header Sticky */
    header {{
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 50;
    }}
    .header-inner {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 0.85rem 1.4rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .header-brand {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      text-decoration: none;
      color: inherit;
    }}
    .brand-badge {{
      width: 36px;
      height: 36px;
      border-radius: 9px;
      background: var(--purple-main);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.05rem;
    }}
    .header-title-box h1 {{
      font-size: 1.1rem;
      font-weight: 800;
      line-height: 1.25;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .v-tag {{
      background: var(--purple-bg);
      color: var(--purple-main);
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 20px;
      border: 1px solid var(--purple-border);
    }}
    .header-title-box span {{
      font-size: 0.78rem;
      color: var(--text-muted);
    }}
    .header-nav {{
      display: flex;
      align-items: center;
      gap: 0.8rem;
      font-size: 0.86rem;
      font-weight: 600;
    }}
    .header-nav a {{
      color: var(--text-secondary);
      text-decoration: none;
      padding: 0.35rem 0.65rem;
      border-radius: var(--radius-sm);
      transition: all 0.15s ease;
    }}
    .header-nav a:hover {{
      color: var(--purple-main);
      background: var(--purple-bg);
    }}
    .back-dash-btn {{
      background: var(--purple-main) !important;
      color: #fff !important;
      padding: 0.4rem 0.9rem !important;
      border-radius: var(--radius-sm);
    }}
    .back-dash-btn:hover {{
      background: var(--purple-light) !important;
    }}

    /* Main Container */
    .container {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 1.8rem 1.4rem 6rem;
    }}

    /* Hero Section */
    .hero {{
      background: linear-gradient(135deg, #4C1D95 0%, #6D28D9 50%, #7C3AED 100%);
      color: white;
      border-radius: var(--radius-lg);
      padding: 2.2rem 2.2rem;
      margin-bottom: 2rem;
      box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.3);
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      top: -40%;
      right: -10%;
      width: 420px;
      height: 420px;
      background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
      border-radius: 50%;
    }}
    .hero-meta {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.8rem;
    }}
    .hero-tag {{
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(8px);
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .hero h2 {{
      font-size: 1.85rem;
      font-weight: 800;
      margin-bottom: 0.8rem;
      line-height: 1.3;
    }}
    .hero p {{
      font-size: 0.95rem;
      line-height: 1.7;
      color: #E9D5FF;
      max-width: 900px;
      margin-bottom: 1.4rem;
    }}
    .formula-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1rem;
    }}
    .formula-card {{
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: var(--radius-md);
      padding: 1rem 1.15rem;
    }}
    .formula-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: #FDE047;
      margin-bottom: 0.35rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .formula-body {{
      font-size: 0.85rem;
      line-height: 1.55;
      color: #FAF5FF;
    }}

    /* Section Headers */
    .section-header {{
      margin-bottom: 1.2rem;
      margin-top: 2.2rem;
    }}
    .section-title {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .section-title::before {{
      content: "";
      width: 4px;
      height: 1.15rem;
      background: var(--purple-main);
      border-radius: 2px;
    }}
    .section-desc {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 0.3rem;
      margin-left: 0.85rem;
    }}

    /* Card Box */
    .card-box {{
      background: var(--bg-card);
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 1.4rem 1.5rem;
      margin-bottom: 1.4rem;
    }}

    /* Step boxes */
    .step-box-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem;
      margin-top: 1.2rem;
    }}
    .step-item {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 1rem;
    }}
    .step-num {{
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--purple-main);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 0.25rem;
    }}
    .step-item h4 {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 0.4rem;
    }}
    .step-item p {{
      font-size: 0.84rem;
      color: var(--text-secondary);
      line-height: 1.6;
    }}

    /* Filter Bar */
    .filter-bar {{
      display: flex;
      gap: 0.6rem;
      margin-bottom: 1.4rem;
      flex-wrap: wrap;
    }}
    .filter-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 0.45rem 1rem;
      border-radius: 20px;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .filter-btn:hover, .filter-btn.active {{
      background: var(--purple-main);
      color: #fff;
      border-color: var(--purple-main);
      box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
    }}

    /* Case Card */
    .case-card {{
      background: var(--bg-card);
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      margin-bottom: 1.8rem;
      overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .case-card:hover {{
      box-shadow: var(--shadow-md);
    }}
    .case-card-header {{
      padding: 1.1rem 1.4rem;
      background: linear-gradient(90deg, #F8FAFC 0%, #FFFFFF 100%);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .case-title-row {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      flex-wrap: wrap;
    }}
    .case-index {{
      font-size: 0.75rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 6px;
      background: #E2E8F0;
      color: #334155;
    }}
    .case-title {{
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--text-primary);
    }}
    .case-badges {{
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }}
    .c-badge {{
      font-size: 0.72rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 12px;
    }}
    .c-badge-geo {{ background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }}
    .c-badge-bio {{ background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }}

    .case-body {{
      padding: 1.4rem;
    }}

    /* Exam material card */
    .exam-material-card {{
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      border-radius: var(--radius-md);
      padding: 1.2rem;
      margin-bottom: 1.2rem;
    }}
    .exam-material-title {{
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--purple-main);
      margin-bottom: 0.6rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .exam-material-text {{
      font-size: 0.92rem;
      line-height: 1.7;
      color: var(--text-primary);
      margin-bottom: 0.8rem;
    }}
    .exam-img-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1rem;
      margin-top: 0.8rem;
    }}
    .exam-img-item {{
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: var(--radius-sm);
      padding: 0.8rem;
      text-align: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .exam-img-item img {{
      max-width: 100%;
      height: auto;
      max-height: 250px;
      object-fit: contain;
      cursor: zoom-in;
      transition: transform 0.2s;
    }}
    .exam-img-item img:hover {{
      transform: scale(1.02);
    }}
    .exam-img-caption {{
      font-size: 0.8rem;
      color: var(--text-secondary);
      font-weight: 600;
      margin-top: 0.5rem;
      line-height: 1.4;
    }}

    /* Questions Section */
    .exam-questions-section {{
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: var(--radius-md);
      padding: 1.2rem;
      margin-bottom: 1.2rem;
    }}
    .questions-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.8rem;
      padding-bottom: 0.6rem;
      border-bottom: 2px solid var(--purple-border);
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    .questions-title-row h4 {{
      font-size: 1rem;
      font-weight: 800;
      color: #1e293b;
    }}
    .batch-toggle-btn {{
      background: #f3e8ff;
      border: 1px solid var(--purple-border);
      color: var(--purple-main);
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .batch-toggle-btn:hover {{
      background: var(--purple-main);
      color: #fff;
    }}
    .question-item {{
      border-bottom: 1px dashed var(--border-color);
      padding: 0.85rem 0;
    }}
    .question-item:last-child {{
      border-bottom: none;
    }}
    .q-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 700;
      font-size: 0.9rem;
      color: var(--text-primary);
      margin-bottom: 0.35rem;
    }}
    .q-score-badge {{
      font-size: 0.72rem;
      font-weight: 700;
      background: #f1f5f9;
      color: #475569;
      padding: 2px 8px;
      border-radius: 10px;
    }}
    .q-stem {{
      font-size: 0.9rem;
      line-height: 1.65;
      color: #334155;
      margin-bottom: 0.5rem;
    }}
    .q-answer-toggle {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--purple-main);
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .q-answer-toggle:hover {{
      background: #f3e8ff;
      border-color: var(--purple-border);
    }}
    .q-answer-box {{
      display: none;
      background: #faf5ff;
      border: 1px solid var(--purple-border);
      border-radius: 6px;
      padding: 0.75rem 1rem;
      margin-top: 0.5rem;
      font-size: 0.88rem;
      line-height: 1.65;
    }}
    .q-answer-box.active {{
      display: block;
    }}
    .ans-highlight {{
      color: #7c3aed;
      font-weight: 700;
    }}
    .grading-point {{
      color: #059669;
      font-size: 0.8rem;
      margin-top: 0.4rem;
      background: #ecfdf5;
      padding: 3px 8px;
      border-radius: 4px;
      display: block;
    }}

    /* Cause Chain */
    .cause-chain-wrap {{
      background: linear-gradient(90deg, #FAF5FF 0%, #FFFFFF 100%);
      border: 1.5px solid var(--purple-border);
      border-radius: var(--radius-sm);
      padding: 1.1rem;
      margin-bottom: 1.1rem;
    }}
    .cause-chain-title {{
      font-size: 0.88rem;
      font-weight: 800;
      color: var(--purple-main);
      margin-bottom: 0.75rem;
    }}
    .chain-nodes {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 0.85rem;
    }}
    .node-box {{
      background: #FFFFFF;
      border: 1px solid var(--purple-border);
      color: var(--purple-main);
      font-size: 0.82rem;
      font-weight: 700;
      padding: 0.45rem 0.75rem;
      border-radius: 6px;
      box-shadow: 0 1px 2px rgba(124, 58, 237, 0.08);
    }}
    .arrow-sign {{
      color: var(--purple-light);
      font-weight: 800;
      font-size: 0.9rem;
    }}
    .standard-answer-text {{
      font-size: 0.88rem;
      line-height: 1.65;
      color: var(--text-primary);
      background: #FFFFFF;
      padding: 0.75rem 0.9rem;
      border-radius: 6px;
      border-left: 3px solid var(--purple-main);
    }}

    .trap-box {{
      background: var(--red-bg);
      border: 1px solid #FECACA;
      border-radius: var(--radius-sm);
      padding: 0.85rem 1.1rem;
      font-size: 0.85rem;
      color: #991B1B;
      line-height: 1.6;
    }}

    /* Lightbox Modal */
    .lightbox-modal {{
      display: none;
      position: fixed;
      z-index: 1000;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(5px);
      align-items: center;
      justify-content: center;
      cursor: zoom-out;
    }}
    .lightbox-modal.active {{
      display: flex;
    }}
    .lightbox-modal img {{
      max-width: 92%;
      max-height: 90%;
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      background: #fff;
    }}

    footer {{
      margin-top: 4rem;
      padding-top: 1.8rem;
      border-top: 1px solid var(--border-color);
      font-size: 0.82rem;
      color: var(--text-muted);
      text-align: center;
    }}

    @media (max-width: 768px) {{
      .container {{ padding: 1.2rem 1rem 4rem; }}
      .hero {{ padding: 1.6rem 1.25rem; }}
      .hero h2 {{ font-size: 1.45rem; }}
      .chain-nodes {{ flex-direction: column; align-items: stretch; }}
      .arrow-sign {{ text-align: center; transform: rotate(90deg); }}
      .exam-img-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="header-brand">
      <div class="brand-badge">跨</div>
      <div class="header-title-box">
        <h1>跨学科案例分析专项拆解工作台 <span class="v-tag">V3 真题全真试卷版</span></h1>
        <span>上海中考 15 分必考 · 12 篇真题全卷原题设问 · 原卷图表配图 · 采分点闭环</span>
      </div>
    </div>
    <div class="header-nav">
      <a href="#sec-formula">📐 核心解题套路</a>
      <a href="#sec-read-charts">📊 读图三步法</a>
      <a href="#sec-cases">📚 12篇全真题拆解</a>
      <a href="../index.html" class="back-dash-btn">← 返回全景看板</a>
    </div>
  </div>
</header>

<div class="container">

  <!-- Hero Section -->
  <div class="hero">
    <div class="hero-meta">
      <span class="hero-tag">上海中考 27 届跨学科冲满分专刊 · 全卷真题版</span>
      <span style="font-size: 0.82rem; color: #D8B4FE;">满分 15 分 · 综合卷 25~30 题 · 读图与设问全景还原</span>
    </div>
    <h2>原题呈现 + 原图解析 + 因果链三段论</h2>
    <p>
      在初三九上第一次月考中，跨学科只得了 <b>4 分（丢了 11 分）</b>，根本原因是对“图表读数”和“跨学科设问套路”陌生。
      跨学科的本质是<b>用地理非生物环境因素（气候、地形、水文、土壤）去解释生命科学现象（植物器官适应性、动物行为、生态平衡）</b>。
      本工作台现已补齐<b>全部 12 篇案例的原题材料、原卷高清配图、1~6 题全真设问、逐题分值及官方评分标准</b>，真正做到考场实战模拟！
    </p>

    <div class="formula-grid">
      <div class="formula-card">
        <div class="formula-title">
          <span>📊 读图读数原则</span>
        </div>
        <div class="formula-body">
          看轴找变量、看峰找极值、看折找拐点。<b>绝不能只抄数字</b>，必须用“随着……增加，呈现……趋势”的规范语表述趋势！
        </div>
      </div>
      <div class="formula-card">
        <div class="formula-title">
          <span>🔗 因果链推理公式</span>
        </div>
        <div class="formula-body">
          <b>【环境条件】</b>（非生物因素）+ <b>【生理适应】</b>（器官结构/生理机能）-&gt; <b>【因果关联词】</b> -&gt; <b>【生产/生态结论】</b>。
        </div>
      </div>
      <div class="formula-card">
        <div class="formula-title">
          <span>🚫 绝不丢空白分</span>
        </div>
        <div class="formula-body">
          遇到最后 3~4 分开放大题，即使不确定，也把<b>材料中对应的地理环境词和生物词抄进三段论句式</b>，保底抓 2~3 分！
        </div>
      </div>
    </div>
  </div>

  <!-- Section 1: Methodology Formula -->
  <section id="sec-formula">
    <div class="section-header">
      <h3 class="section-title">跨学科核心解题公式：三层因果链答题模型</h3>
      <p class="section-desc">阅卷老师评分标准的底层逻辑：必须同时出现“地理环境”、“生命特征”与“逻辑连接词”</p>
    </div>

    <div class="card-box">
      <div style="background: linear-gradient(90deg, #F5F3FF 0%, #FFFFFF 100%); padding: 1.2rem 1.4rem; border-radius: var(--radius-md); border: 1.5px solid var(--purple-border);">
        <h4 style="font-size: 1.05rem; font-weight: 800; color: var(--purple-main); margin-bottom: 0.6rem;">
          【官方采分万能模板】因果链闭环句式
        </h4>
        <div style="font-size: 0.92rem; line-height: 1.7; color: var(--text-primary);">
          “因为该地区<b>【地理环境特征：如半干旱气候/昼夜温差大/沙壤土通气/地下水位高】</b>，
          这促使该生物<b>【生物形态或生理适应：如根系深扎/光合产物消耗少/防止有氧呼吸受阻】</b>，
          因此有利于<b>【生态/生长结果：如吸收深层水/糖分积累/防止烂根】</b>，
          从而实现了<b>【生产生活/可持续发展价值】</b>。”
        </div>
      </div>

      <div class="step-box-grid">
        <div class="step-item">
          <div class="step-num">Step 1：锁住地理源头</div>
          <h4>提取非生物环境要素</h4>
          <p>
            • <b>气候</b>：气温年较差/日较差、年降水量、降水集中月份、伏旱、光照时数；<br>
            • <b>地形与地质</b>：冲积平原、山谷盆地、喀斯特溶洞、坡度坡向；<br>
            • <b>水文与土壤</b>：地下水位高低、沙壤土/黏土、盐分、透水透气性。
          </p>
        </div>
        <div class="step-item">
          <div class="step-num">Step 2：对应生物生理</div>
          <h4>调动生命科学核心机理</h4>
          <p>
            • <b>植物</b>：根系（主根深扎/侧根浅展）、叶片（退化成刺/蜡质层蒸腾弱）、气孔开闭；<br>
            • <b>代谢</b>：光合作用（制造淀粉/糖类）、呼吸作用（温度低消耗少）、细胞缺氧烂根；<br>
            • <b>动物</b>：逆流游动、肌纤维致密、变温/恒温调节。
          </p>
        </div>
        <div class="step-item">
          <div class="step-num">Step 3：打通因果连环</div>
          <h4>使用严密逻辑副词与动词</h4>
          <p>
            • 拒绝“因为……所以它很好”等大白话；<br>
            • 必须使用专业连接词：<b>“促使……”、“阻碍了……”、“从而有利于……”、“诱发了……酶活性”、“抑制了……消耗”</b>。
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 2: Chart Reading 3 Steps -->
  <section id="sec-read-charts">
    <div class="section-header">
      <h3 class="section-title">突破图表题：柱状图与折线图读数三步法</h3>
      <p class="section-desc">中考跨学科 26、27 题必考图表题，不丢分的核心是掌握“变量-趋势-极值”标准答法</p>
    </div>

    <div class="step-box-grid" style="margin-top:0;">
      <!-- 柱状图技巧 -->
      <div class="card-box" style="margin-bottom: 0;">
        <h4 style="font-size: 1rem; font-weight: 800; color: var(--blue-main); margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.4rem;">
          📊 柱状图（比较型与离散数据）读法
        </h4>
        <ul style="font-size: 0.86rem; color: var(--text-secondary); line-height: 1.7; padding-left: 1.2rem;">
          <li><b>读柱顶数值与极值对比</b>：直接找出最大柱与最小柱（如 7-8 月降水量最高，1-2 月降水量最低）。</li>
          <li><b>读组间差异（对照组 vs 实验组）</b>：看不同处理下柱子高低差异（如起垄组比平畦组根系腐烂率低 40%）。</li>
          <li><b>定性结论转化</b>：数字差距 -> 转化成生物学结论（如“降水集中期根部渍水严重”、“遮光率越高叶绿素含量越少”）。</li>
        </ul>
      </div>

      <!-- 折线图技巧 -->
      <div class="card-box" style="margin-bottom: 0;">
        <h4 style="font-size: 1rem; font-weight: 800; color: var(--purple-main); margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.4rem;">
          📈 折线图（连续变化与速率趋势）读法
        </h4>
        <ul style="font-size: 0.86rem; color: var(--text-secondary); line-height: 1.7; padding-left: 1.2rem;">
          <li><b>先看横纵坐标物理意义</b>：横轴是自变量（如深度、时间、温度），纵轴是因变量（如含水量、呼吸速率）。</li>
          <li><b>抓拐点与平台期</b>：折线在何处急剧上升、在何处平缓饱和（如土层 100cm 以下含水量达到稳定平台期）。</li>
          <li><b>三段论趋势描述</b>：“在 0~X 范围内随 X 增加而快速上升；超过 X 后趋于平稳/下降”。</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Section 3: 12 Cases Breakdown -->
  <section id="sec-cases">
    <div class="section-header">
      <h3 class="section-title">近 3 年上海统考与各区一模 / 西延安实考 12 篇全真题拆解库</h3>
      <p class="section-desc">包含完整考题情境、原卷附图与数据表、1~6 题全真设问、逐题采分点与易错雷区（点击图片可放大查看）</p>
    </div>

    <div class="filter-bar">
      <button class="filter-btn active" onclick="filterCases('all', this)">全部 12 篇案例</button>
      <button class="filter-btn" onclick="filterCases('zhongkao', this)">⭐ 中考统考真题 (3篇)</button>
      <button class="filter-btn" onclick="filterCases('plant', this)">🌾 农林特色植物类 (5篇)</button>
      <button class="filter-btn" onclick="filterCases('ecology', this)">🌱 生态治理与水土环境 (5篇)</button>
    </div>

    <!-- Case Cards Container -->
    <div id="casesContainer">
      {all_cases_rendered}
    </div>
  </section>

  <!-- Lightbox Modal for Image Zoom -->
  <div class="lightbox-modal" id="imgLightbox" onclick="closeLightbox()">
    <img src="" id="lightboxImg" alt="大图预览">
  </div>

  <footer>
    <p>© 2026 Owen 中考跨学科案例分析通关系统 · 上海中考 27 届专项教研 · 西延安实考真卷全解析</p>
  </footer>

</div>

<script>
  // Filter cases
  function filterCases(cat, btn) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const cards = document.querySelectorAll('.case-card');
    cards.forEach(card => {{
      const cardCat = card.getAttribute('data-cat') || '';
      if (cat === 'all' || cardCat.includes(cat)) {{
        card.style.display = 'block';
      }} else {{
        card.style.display = 'none';
      }}
    }});
  }}

  // Toggle single answer
  function toggleAnswer(qId, btn) {{
    const box = document.getElementById(qId);
    if (!box) return;
    if (box.classList.contains('active')) {{
      box.classList.remove('active');
      btn.innerText = '💡 查看本题采分答案';
    }} else {{
      box.classList.add('active');
      btn.innerText = '收起答案';
    }}
  }}

  // Batch toggle all answers in a case
  function toggleAllAnswersInCase(caseId, btn) {{
    const caseEl = document.getElementById(caseId);
    if (!caseEl) return;
    const answerBoxes = caseEl.querySelectorAll('.q-answer-box');
    const buttons = caseEl.querySelectorAll('.q-answer-toggle');
    const isAnyHidden = Array.from(answerBoxes).some(b => !b.classList.contains('active'));

    answerBoxes.forEach(b => {{
      if (isAnyHidden) {{
        b.classList.add('active');
      }} else {{
        b.classList.remove('active');
      }}
    }});

    buttons.forEach(b => {{
      b.innerText = isAnyHidden ? '收起答案' : '💡 查看本题采分答案';
    }});

    btn.innerText = isAnyHidden ? '🙈 收起全部答案' : '👁️ 展开全部答案';
  }}

  // Lightbox
  function openLightbox(src) {{
    const modal = document.getElementById('imgLightbox');
    const img = document.getElementById('lightboxImg');
    img.src = src;
    modal.classList.add('active');
  }}
  function closeLightbox() {{
    const modal = document.getElementById('imgLightbox');
    modal.classList.remove('active');
  }}
</script>

</body>
</html>
"""

output_path = "/Users/emily/Documents/Projects/owenlearining/interdisciplinary/interdisciplinary-V3.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_page_html)

print("Successfully written upgraded interdisciplinary-V3.html!")
