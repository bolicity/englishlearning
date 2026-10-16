# -*- coding: utf-8 -*-
"""
Builder for daofa/daofa-special-bank.html
上海初三道法 · 一模冲刺10次课专项题库与答题模板工作台
涵盖海报大纲：
- 10次课冲刺大纲全景与主线贯通
- 专项一：辨析 / 评析题（“四步定乾坤”满分模板）
- 专项二：材料分析题（“四角对应法”金公式，聚焦党的领导、中国式现代化、全过程人民民主）
- 专项三：实践探究开放题（宣传标语对偶式、活动方案三阶推进、建议对策主体表、倡议书规范）
- 综合套卷与全真模拟复盘
"""

import os
import json

HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>上海初三道法 · 一模冲刺专项题库与答题模板工作台 | 同步新课改新题型</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-page: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --border-color: #E2E8F0;
      --border-hover: #CBD5E1;

      --text-main: #0F172A;
      --text-sub: #334155;
      --text-muted: #64748B;

      --red-main: #DC2626;
      --red-dark: #991B1B;
      --red-light: #FEF2F2;
      --red-border: #FECDD3;

      --blue-main: #2563EB;
      --blue-light: #EFF6FF;
      --blue-border: #BFDBFE;

      --emerald-main: #059669;
      --emerald-light: #ECFDF5;
      --emerald-border: #A7F3D0;

      --amber-main: #D97706;
      --amber-light: #FFFBEB;
      --amber-border: #FDE68A;

      --purple-main: #7C3AED;
      --purple-light: #FAF5FF;
      --purple-border: #DDD6FE;

      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.07);
      --shadow-lg: 0 10px 20px -3px rgba(15, 23, 42, 0.08);

      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-page);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }

    /* 顶部导航 */
    header {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky; top: 0; z-index: 50;
      box-shadow: var(--shadow-sm);
    }
    .nav-inner {
      max-width: 1400px; margin: 0 auto;
      padding: 0.75rem 1.25rem;
      display: flex; justify-content: space-between; align-items: center;
      gap: 1rem;
    }
    .brand-link {
      display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: inherit;
    }
    .brand-icon {
      width: 40px; height: 40px; border-radius: var(--radius-sm);
      background: linear-gradient(135deg, var(--red-main), #B91C1C);
      color: white; font-weight: 800; font-size: 1.1rem;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 2px 6px rgba(220, 38, 38, 0.25);
    }
    .brand-name {
      font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.15rem; color: var(--text-main);
      display: flex; align-items: center; gap: 0.5rem;
    }
    .version-badge {
      font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 999px;
      background: var(--red-light); color: var(--red-main); border: 1px solid var(--red-border);
      font-weight: 600;
    }
    .nav-actions {
      display: flex; align-items: center; gap: 0.75rem;
    }
    .nav-btn {
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.45rem 0.85rem; border-radius: var(--radius-sm);
      background: var(--bg-card); border: 1px solid var(--border-color);
      color: var(--text-sub); font-size: 0.85rem; font-weight: 600; text-decoration: none;
      transition: all 0.2s;
    }
    .nav-btn:hover {
      background: var(--bg-subtle); border-color: var(--border-hover); color: var(--text-main);
    }
    .nav-btn-primary {
      background: var(--red-main); color: white; border-color: var(--red-main);
    }
    .nav-btn-primary:hover {
      background: var(--red-dark); color: white;
    }

    /* 主布局 */
    .main-wrap {
      max-width: 1400px; margin: 0 auto; padding: 1.5rem 1.25rem 4rem;
    }

    /* 海报冲刺横幅 */
    .sprint-hero {
      background: linear-gradient(135deg, #FFF1F2 0%, #FFFFFF 50%, #EFF6FF 100%);
      border: 1px solid #FECDD3; border-radius: var(--radius-lg);
      padding: 2rem 2rem 1.75rem; margin-bottom: 2rem;
      box-shadow: var(--shadow-sm); position: relative; overflow: hidden;
    }
    .sprint-hero::before {
      content: "上海新中考冲刺";
      position: absolute; right: -25px; top: 18px;
      background: linear-gradient(90deg, #DC2626, #EF4444);
      color: white; font-size: 0.75rem; font-weight: 800;
      padding: 4px 35px; transform: rotate(45deg);
      box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    .hero-top-tag {
      display: inline-flex; align-items: center; gap: 0.4rem;
      background: #FFFFFF; border: 1px solid var(--red-border);
      color: var(--red-main); font-size: 0.8rem; font-weight: 700;
      padding: 0.25rem 0.65rem; border-radius: 999px; margin-bottom: 0.75rem;
    }
    .hero-title {
      font-size: 1.85rem; font-weight: 800; color: #1E293B; line-height: 1.3; margin-bottom: 0.6rem;
    }
    .hero-title span {
      background: linear-gradient(120deg, var(--red-main), #B91C1C);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-desc {
      color: var(--text-sub); font-size: 0.95rem; line-height: 1.6; max-width: 900px; margin-bottom: 1.2rem;
    }

    /* 冲刺大纲三特色卡片 */
    .pillars-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-top: 1.2rem;
    }
    .pillar-card {
      background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(6px);
      border: 1px solid var(--border-color); border-radius: var(--radius-md);
      padding: 1rem 1.15rem; display: flex; align-items: flex-start; gap: 0.75rem;
      box-shadow: var(--shadow-sm);
    }
    .pillar-icon {
      width: 38px; height: 38px; border-radius: 8px; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center; font-size: 1.15rem;
    }
    .pillar-title { font-weight: 700; font-size: 0.95rem; color: var(--text-main); margin-bottom: 0.2rem; }
    .pillar-detail { font-size: 0.82rem; color: var(--text-muted); line-height: 1.45; }

    /* 10次课冲刺大纲进度条与折叠面板 */
    .syllabus-box {
      background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg);
      padding: 1.25rem 1.5rem; margin-bottom: 2rem; box-shadow: var(--shadow-sm);
    }
    .syllabus-header {
      display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none;
    }
    .syllabus-title-wrap {
      display: flex; align-items: center; gap: 0.75rem;
    }
    .syllabus-title-wrap h3 {
      font-size: 1.1rem; font-weight: 800; color: var(--text-main);
    }
    .syllabus-timeline {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.85rem; margin-top: 1.25rem;
    }
    .timeline-item {
      background: var(--bg-subtle); border: 1px solid var(--border-color); border-radius: var(--radius-md);
      padding: 0.8rem 1rem; position: relative; transition: all 0.2s;
    }
    .timeline-item:hover {
      border-color: var(--blue-border); background: var(--blue-light);
    }
    .timeline-item.active-special {
      background: #FFFBEB; border-color: #FDE68A;
    }
    .timeline-num {
      display: inline-block; width: 22px; height: 22px; line-height: 22px; text-align: center;
      background: var(--blue-main); color: white; border-radius: 50%; font-size: 0.75rem; font-weight: 800; margin-right: 0.4rem;
    }
    .timeline-item.active-special .timeline-num {
      background: var(--amber-main);
    }
    .timeline-name {
      font-size: 0.85rem; font-weight: 700; color: var(--text-main); display: inline;
    }
    .timeline-tag {
      display: block; font-size: 0.75rem; color: var(--text-muted); margin-top: 0.3rem;
    }

    /* 选项卡切换区 (四大专项) */
    .tabs-nav {
      display: flex; gap: 0.5rem; border-bottom: 2px solid var(--border-color); margin-bottom: 1.5rem;
      overflow-x: auto; padding-bottom: 2px;
    }
    .tab-btn {
      padding: 0.75rem 1.25rem; font-size: 0.92rem; font-weight: 700; border: none; background: none;
      cursor: pointer; color: var(--text-muted); position: relative; border-radius: 8px 8px 0 0;
      white-space: nowrap; transition: all 0.2s;
    }
    .tab-btn:hover { color: var(--text-main); background: var(--bg-subtle); }
    .tab-btn.active {
      color: var(--red-main); background: #FFFFFF; border: 1px solid var(--border-color); border-bottom: 2px solid #FFFFFF;
      margin-bottom: -2px; box-shadow: 0 -2px 6px rgba(0,0,0,0.03);
    }
    .tab-badge {
      font-size: 0.7rem; padding: 0.1rem 0.45rem; border-radius: 999px; margin-left: 0.35rem;
      background: var(--red-light); color: var(--red-main); font-weight: 700;
    }

    /* 模板指南展示卡 */
    .template-card {
      background: #FFFFFF; border: 1px solid var(--border-color); border-radius: var(--radius-lg);
      padding: 1.5rem; margin-bottom: 1.75rem; box-shadow: var(--shadow-sm);
    }
    .template-header {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;
    }
    .template-title {
      font-size: 1.2rem; font-weight: 800; color: var(--text-main); display: flex; align-items: center; gap: 0.5rem;
    }
    .template-formula-box {
      background: #FFFBEB; border: 1.5px dashed #F59E0B; border-radius: var(--radius-md);
      padding: 1rem 1.25rem; margin-bottom: 1.25rem; font-size: 0.95rem; color: #92400E; font-weight: 600; line-height: 1.6;
    }
    .steps-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1rem;
    }
    .step-box {
      background: var(--bg-subtle); border: 1px solid var(--border-color); border-radius: var(--radius-md);
      padding: 1rem;
    }
    .step-num {
      display: inline-block; font-size: 0.75rem; font-weight: 800; padding: 2px 8px; border-radius: 4px;
      background: var(--blue-main); color: white; margin-bottom: 0.5rem;
    }
    .step-name { font-size: 0.95rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem; }
    .step-desc { font-size: 0.83rem; color: var(--text-sub); line-height: 1.5; }
    .golden-phrases {
      background: var(--emerald-light); border: 1px solid var(--emerald-border); border-radius: var(--radius-md);
      padding: 0.85rem 1.15rem; font-size: 0.85rem; color: #065F46; line-height: 1.6;
    }

    /* 题库控制栏 */
    .filter-bar {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;
      flex-wrap: wrap; gap: 0.75rem; background: var(--bg-card); padding: 0.85rem 1.25rem;
      border: 1px solid var(--border-color); border-radius: var(--radius-md);
    }
    .search-input {
      padding: 0.45rem 0.85rem; border: 1px solid var(--border-color); border-radius: var(--radius-sm);
      font-size: 0.85rem; outline: none; width: 260px; transition: border-color 0.2s;
    }
    .search-input:focus { border-color: var(--blue-main); }
    .filter-pills { display: flex; gap: 0.4rem; flex-wrap: wrap; }
    .filter-pill {
      padding: 0.35rem 0.75rem; font-size: 0.8rem; font-weight: 600; border-radius: 999px;
      border: 1px solid var(--border-color); background: var(--bg-card); cursor: pointer; color: var(--text-sub);
    }
    .filter-pill.active {
      background: var(--red-main); color: white; border-color: var(--red-main);
    }

    /* 试题卡片 */
    .question-card {
      background: #FFFFFF; border: 1px solid var(--border-color); border-radius: var(--radius-lg);
      padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--shadow-sm); transition: border-color 0.2s, box-shadow 0.2s;
    }
    .question-card:hover {
      border-color: var(--border-hover); box-shadow: var(--shadow-md);
    }
    .q-meta {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem;
    }
    .q-tags { display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; }
    .q-tag {
      font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;
    }
    .tag-red { background: var(--red-light); color: var(--red-main); border: 1px solid var(--red-border); }
    .tag-blue { background: var(--blue-light); color: var(--blue-main); border: 1px solid var(--blue-border); }
    .tag-emerald { background: var(--emerald-light); color: var(--emerald-main); border: 1px solid var(--emerald-border); }
    .tag-amber { background: var(--amber-light); color: var(--amber-main); border: 1px solid var(--amber-border); }
    .q-score { font-size: 0.8rem; font-weight: 700; color: var(--text-muted); }

    .q-material {
      background: var(--bg-subtle); border-left: 4px solid var(--blue-main);
      padding: 1rem 1.25rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 0.92rem; color: var(--text-sub); line-height: 1.65; margin-bottom: 1rem;
    }
    .q-material b { color: var(--text-main); }
    .q-stem {
      font-size: 1.02rem; font-weight: 700; color: var(--text-main); margin-bottom: 1rem; line-height: 1.5;
    }

    /* 破题思路链 */
    .q-chain-box {
      background: #F8FAFC; border: 1px solid var(--border-color); border-radius: var(--radius-md);
      padding: 0.85rem 1rem; margin-bottom: 1rem; font-size: 0.85rem;
    }
    .chain-title { font-weight: 700; color: var(--purple-main); margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.35rem; }
    .chain-flow { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; font-size: 0.83rem; color: var(--text-sub); }
    .chain-step {
      background: #FFFFFF; border: 1px solid var(--purple-border); padding: 0.2rem 0.6rem; border-radius: 4px; font-weight: 600;
    }
    .chain-arrow { color: var(--purple-main); font-weight: 800; }

    /* 草稿本/自测作答区 */
    .draft-box {
      margin-bottom: 1rem;
    }
    .draft-textarea {
      width: 100%; min-height: 70px; padding: 0.65rem 0.85rem; border: 1px solid var(--border-color);
      border-radius: var(--radius-sm); font-size: 0.88rem; outline: none; font-family: inherit; resize: vertical;
      background: #FDFEFE; color: var(--text-main); transition: border-color 0.2s;
    }
    .draft-textarea:focus { border-color: var(--blue-main); background: #FFFFFF; }
    .draft-footer { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem; }

    /* 采分答案展开折叠 */
    .ans-toggle-btn {
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.5rem 1rem; border-radius: var(--radius-sm);
      background: var(--blue-light); border: 1px solid var(--blue-border);
      color: var(--blue-main); font-size: 0.85rem; font-weight: 700; cursor: pointer;
      transition: all 0.2s;
    }
    .ans-toggle-btn:hover { background: #DBEAFE; }
    .ans-panel {
      display: none; margin-top: 1rem; padding: 1.25rem;
      background: #FFFFFF; border: 1px solid var(--emerald-border); border-radius: var(--radius-md);
      box-shadow: 0 2px 8px rgba(5, 150, 105, 0.06);
    }
    .ans-panel.open { display: block; animation: fadeIn 0.25s ease-in-out; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .grading-points {
      background: var(--emerald-light); border-left: 3px solid var(--emerald-main);
      padding: 0.75rem 1rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 0.85rem; color: #065F46; margin-bottom: 0.85rem; line-height: 1.6;
    }
    .full-answer-text {
      font-size: 0.92rem; color: var(--text-main); line-height: 1.7;
    }
    .full-answer-text p { margin-bottom: 0.5rem; }
    .trap-warning {
      background: #FEF2F2; border: 1px solid #FECDD3; border-radius: var(--radius-sm);
      padding: 0.6rem 0.85rem; margin-top: 0.85rem; font-size: 0.82rem; color: #991B1B;
    }

    /* 复制通知 */
    .toast {
      position: fixed; bottom: 2rem; right: 2rem; z-index: 100;
      background: #0F172A; color: white; padding: 0.75rem 1.25rem;
      border-radius: var(--radius-md); font-size: 0.88rem; font-weight: 600;
      box-shadow: var(--shadow-lg); display: none; align-items: center; gap: 0.5rem;
    }

    footer {
      border-top: 1px solid var(--border-color); padding: 2.5rem 1.25rem;
      text-align: center; color: var(--text-muted); font-size: 0.85rem; background: #FFFFFF;
    }
  </style>
</head>
<body>

  <!-- 顶部导航栏 -->
  <header>
    <div class="nav-inner">
      <a href="../index.html" class="brand-link">
        <div class="brand-icon">道</div>
        <div>
          <div class="brand-name">
            上海初三道法 · 一模冲刺专项
            <span class="version-badge">2026新课改同款</span>
          </div>
        </div>
      </a>
      <div class="nav-actions">
        <a href="daofa-V7.html" class="nav-btn">📖 返回道法知识精要工作台</a>
        <a href="../history/history-special-bank.html" class="nav-btn">🏛️ 历史小论文专项</a>
        <a href="../index.html" class="nav-btn nav-btn-primary">🏠 学习中心</a>
      </div>
    </div>
  </header>

  <div class="main-wrap">

    <!-- 冲刺横幅 (对应海报理念) -->
    <section class="sprint-hero">
      <div class="hero-top-tag">🎯 聚焦上海新中考 · 同步新课改新题型</div>
      <h1 class="hero-title">初三道德与法治 <span>一模冲刺10次课</span> 题型专项与答题模板</h1>
      <p class="hero-desc">
        根据上海市初三一模与中考新课标考向，精准攻克开卷考试中“分值大、思维深、不易踩点”的核心失分题型。
        打通六至九年级知识主线，吃透“坚持党的领导”与“中国式现代化”新考点，告别死记硬背与盲目抄书！
      </p>

      <div class="pillars-grid">
        <div class="pillar-card">
          <div class="pillar-icon" style="background:#EFF6FF; color:#2563EB;">📘</div>
          <div>
            <div class="pillar-title">知识体系主线贯通</div>
            <div class="pillar-detail">六至七年级核心 + 八上社会公德 + 八下宪法法治 + 九上强国梦与中国式现代化专题。</div>
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-icon" style="background:#FEF2F2; color:#DC2626;">💡</div>
          <div>
            <div class="pillar-title">吃透新题型高分公式</div>
            <div class="pillar-detail">深度突破：辨析评析题（四步定乾坤）、材料分析题（四角对应法）、实践探究开放题（主体多元表）。</div>
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-icon" style="background:#ECFDF5; color:#059669;">🎯</div>
          <div>
            <div class="pillar-title">一二模同类全真实战</div>
            <div class="pillar-detail">精选浦东、徐汇、黄浦、闵行等区一二模真题变形卷，逐题解析采分点与失分避坑指南。</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 10次课冲刺大纲全景图 -->
    <section class="syllabus-box">
      <div class="syllabus-header" onclick="toggleSyllabus()">
        <div class="syllabus-title-wrap">
          <span style="font-size: 1.3rem;">📅</span>
          <h3>10次课·冲刺大纲导航（点击展开/收起进度表）</h3>
        </div>
        <span id="syllabus-arrow" style="font-weight: 700; color: var(--blue-main); font-size: 0.9rem;">收起 ▲</span>
      </div>
      <div class="syllabus-timeline" id="syllabus-body">
        <div class="timeline-item">
          <div><span class="timeline-num">1</span><span class="timeline-name">六、七年级核心知识梳理</span></div>
          <span class="timeline-tag">成长的节拍·友谊的天空·师生情谊·做情绪的主人</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">2</span><span class="timeline-name">八年级上册知识点梳理</span></div>
          <span class="timeline-tag">丰富的社会生活·网络生活·社会规则·责任与国家利益</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">3</span><span class="timeline-name">六～八上整合 + 八下法律基础</span></div>
          <span class="timeline-tag">宪法是根本法·公民基本权利与义务·国家权力机关运行</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">4</span><span class="timeline-name">九上单元1·坚持党的全面领导</span></div>
          <span class="timeline-tag">四个历史时期·初心使命·伟大建党精神·党的执政地位</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">5</span><span class="timeline-name">九上单元2、3·中国式现代化专题</span></div>
          <span class="timeline-tag">高质量发展·新质生产力·全过程人民民主·法治中国</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">6</span><span class="timeline-name">九上单元4·共圆中国梦+复盘</span></div>
          <span class="timeline-tag">民族团结·祖国统一·文化自信·社会主义核心价值观</span>
        </div>
        <div class="timeline-item active-special">
          <div><span class="timeline-num">7</span><span class="timeline-name">题型专项①·辨析 / 评析题</span></div>
          <span class="timeline-tag">🌟 判断定性 + 析合理 + 析片面 + 升华规范</span>
        </div>
        <div class="timeline-item active-special">
          <div><span class="timeline-num">8</span><span class="timeline-name">题型专项②·材料分析题</span></div>
          <span class="timeline-tag">🌟 材料提取 + 对接课本金句 + 多维深度论述</span>
        </div>
        <div class="timeline-item active-special">
          <div><span class="timeline-num">9</span><span class="timeline-name">题型专项③·实践探究开放题</span></div>
          <span class="timeline-tag">🌟 宣传标语 + 活动方案 + 倡议书 + 建言献策表</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">10</span><span class="timeline-name">综合套卷限时训练+错题复盘</span></div>
          <span class="timeline-tag">全真模拟限时实战·开卷快速检索策略·踩分卷面规范</span>
        </div>
      </div>
    </section>

    <!-- 专项导航选项卡 -->
    <div class="tabs-nav">
      <button class="tab-btn active" onclick="switchTab('tab-all', this)">全部专项精选题库 <span class="tab-badge">12题</span></button>
      <button class="tab-btn" onclick="switchTab('tab-bianxi', this)">题型专项①·辨析 / 评析题 <span class="tab-badge">4题</span></button>
      <button class="tab-btn" onclick="switchTab('tab-cailiao', this)">题型专项②·材料分析题 <span class="tab-badge">4题</span></button>
      <button class="tab-btn" onclick="switchTab('tab-kaifang', this)">题型专项③·实践探究开放题 <span class="tab-badge">4题</span></button>
      <button class="tab-btn" onclick="switchTab('tab-party', this)">新教材·党的领导与中国式现代化专题 <span class="tab-badge">重点</span></button>
    </div>

    <!-- 答题模板展示区 (根据激活的tab动态切换或总览) -->
    <div id="template-section">
      <!-- 专项一模板 -->
      <div class="template-card" id="tmpl-bianxi">
        <div class="template-header">
          <div class="template-title">
            <span>⚖️</span> 题型专项①：辨析 / 评析题 “四步定乾坤” 满分模板
          </div>
          <button class="nav-btn" onclick="copyTemplate('bianxi')">📋 复制此模板格式</button>
        </div>
        <div class="template-formula-box">
          【黄金口诀】：一表态定性（辩证不绝对）➔ 二析合理性（课本金句）➔ 三析片面处（漏洞与危害）➔ 四提升做法（行动与升华）
        </div>
        <div class="steps-grid">
          <div class="step-box">
            <span class="step-num">Step 1：明确判断</span>
            <div class="step-name">定性表态</div>
            <div class="step-desc">该观点/行为是<b>片面的</b>（或：将XX与XX割裂开来是错误的 / 是不科学的）。切忌直接只写“对”或“错”。</div>
          </div>
          <div class="step-box">
            <span class="step-num">Step 2：阐释合理</span>
            <div class="step-name">析合理之处</div>
            <div class="step-desc">“该观点看到了……这具有一定合理性。因为【对应教材金句/理论依据】……”</div>
          </div>
          <div class="step-box">
            <span class="step-num">Step 3：攻其破绽</span>
            <div class="step-name">析片面与危害</div>
            <div class="step-desc">“但是，该观点忽视了/否定了……因为【补充教材理论】。如果照此做法，会导致……”</div>
          </div>
          <div class="step-box">
            <span class="step-num">Step 4：总结升华</span>
            <div class="step-name">正确做法与升华</div>
            <div class="step-desc">“因此，我们应当坚持……与……相统一，在日常生活中做到【青少年具体行动】。”</div>
          </div>
        </div>
        <div class="golden-phrases">
          💡 <b>阅卷避坑红线</b>：① 遇到“只要……就……”、“只有……才能……”等绝对化表述，99%为片面观点；② 开卷考试严禁抄无关整段课本，每一个分句都必须与题目材料的情境词形成对应。
        </div>
      </div>

      <!-- 专项二模板 -->
      <div class="template-card" id="tmpl-cailiao">
        <div class="template-header">
          <div class="template-title">
            <span>📊</span> 题型专项②：材料分析题 “四角对应法” 黄金公式
          </div>
          <button class="nav-btn" onclick="copyTemplate('cailiao')">📋 复制此模板格式</button>
        </div>
        <div class="template-formula-box">
          【核心逻辑】：材料提取（析材料） ➔ 原理对接（引金句） ➔ 多维展开（讲意义） ➔ 回扣主题（下结论）
        </div>
        <div class="steps-grid">
          <div class="step-box">
            <span class="step-num">角 1：材料提取</span>
            <div class="step-name">精准概括</div>
            <div class="step-desc">“材料中提到【某项成就/某种做法】，反映了我国/上海在……方面的探索与成效。”</div>
          </div>
          <div class="step-box">
            <span class="step-num">角 2：原理对接</span>
            <div class="step-name">扣教材核心概念</div>
            <div class="step-desc">“这体现了/践行了【党的全面领导 / 高质量发展 / 全过程人民民主 / 坚持以人民为中心的发展思想】。”</div>
          </div>
          <div class="step-box">
            <span class="step-num">角 3：多维展开</span>
            <div class="step-name">阐释重要性与意义</div>
            <div class="step-desc">从“有利于保障人民权益”、“有利于推动科技自立自强”、“有利于实现共同富裕与中国式现代化”等维度铺展。</div>
          </div>
          <div class="step-box">
            <span class="step-num">角 4：扣题回应当事</span>
            <div class="step-name">扣题收尾</div>
            <div class="step-desc">呼应题目设问：“因此，这深刻说明了为什么…… / 充分展现了……的生动实践。”</div>
          </div>
        </div>
      </div>

      <!-- 专项三模板 -->
      <div class="template-card" id="tmpl-kaifang">
        <div class="template-header">
          <div class="template-title">
            <span>🌱</span> 题型专项③：实践探究开放题 “多元规范” 题型库
          </div>
          <button class="nav-btn" onclick="copyTemplate('kaifang')">📋 复制此模板格式</button>
        </div>
        <div class="steps-grid">
          <div class="step-box" style="border-top: 3px solid var(--red-main);">
            <div class="step-name">1. 宣传标语类（对偶式）</div>
            <div class="step-desc">
              <b>结构</b>：上句行动倡导 + 下句美好愿景。<br>
              <i>范例 1 (法治)</i>：树立法治信仰，共建和谐社会。<br>
              <i>范例 2 (创新)</i>：点燃创新火花，驱动科技强国。<br>
              <i>范例 3 (生态)</i>：践行低碳生活，守护美丽家园。
            </div>
          </div>
          <div class="step-box" style="border-top: 3px solid var(--blue-main);">
            <div class="step-name">2. 建议对策类（主体多元法）</div>
            <div class="step-desc">
              <b>国家/政府</b>：完善法律法规，强化执法监管；<br>
              <b>社会/企业/学校</b>：营造法治舆论氛围，承担社会责任，落实育人职责；<br>
              <b>青少年个人</b>：增强意识，自觉践行，从身边小事做起。
            </div>
          </div>
          <div class="step-box" style="border-top: 3px solid var(--emerald-main);">
            <div class="step-name">3. 活动方案设计类（三阶段）</div>
            <div class="step-desc">
              <b>① 准备阶段</b>：确定活动主题，制定方案，收集资料，分组分工；<br>
              <b>② 实施阶段</b>：开展实地调查、专家讲座、主题辩论或宣讲；<br>
              <b>③ 总结阶段</b>：撰写调查报告，召开交流分享会，建言有关部门。
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 题库控制过滤条 -->
    <div class="filter-bar">
      <div class="filter-pills">
        <button class="filter-pill active" onclick="filterByTag('all', this)">全部题目</button>
        <button class="filter-pill" onclick="filterByTag('bianxi', this)">⚖️ 辨析/评析题</button>
        <button class="filter-pill" onclick="filterByTag('cailiao', this)">📊 材料分析题</button>
        <button class="filter-pill" onclick="filterByTag('kaifang', this)">🌱 实践探究开放题</button>
        <button class="filter-pill" onclick="filterByTag('party', this)">🏛️ 党的领导与中国式现代化</button>
      </div>
      <div>
        <input type="text" id="q-search" class="search-input" placeholder="🔍 搜索试题关键词、考点..." oninput="searchQuestions()">
      </div>
    </div>

    <!-- 试题列表区 -->
    <div id="questions-container">

      <!-- Q1: 辨析题 · 科技创新与青少年 -->
      <div class="question-card" data-tag="bianxi">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag tag-red">专项① 辨析题</span>
            <span class="q-tag tag-blue">九上 创新驱动与科教兴国</span>
            <span class="q-tag tag-amber">2025浦东一模同类题</span>
          </div>
          <div class="q-score">满分：6分 | 难度：★★★☆☆</div>
        </div>
        <div class="q-material">
          <b>【情境材料】</b>
          某校九年级同学在参观完“上海国际创客大会”后开展热烈讨论。同学小李说：“科技创新是国家和科学家的事情，必须由国家统筹搞攻关。作为初中生，我们的唯一任务就是把课本考点背熟考个好分数，创新离我们太遥远，我们想搞也搞不了。”
        </div>
        <div class="q-stem">
          【设问】：请运用所学《道德与法治》九年级上册知识，对小李同学的观点进行评析。
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 审题与思维破题链：</div>
          <div class="chain-flow">
            <div class="chain-step">定性：观点片面</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">析对：国家主导攻关正确（创新是第一动力）</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">析错：创新不仅属于科学家，生活处处皆可创新</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">做法：青少年树立创新意识+敢于质疑实践</div>
          </div>
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 在此输入您的答题草稿思路（写完可点击下方按钮核对采分点）..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
            <span>💡 提示：按“表态-析合-析偏-升华”四步展开</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-1', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-1">
          <div class="grading-points">
            <b>【采分要点与赋分标准】</b>（满分6分）：<br>
            ① <b>判断定性（1分）</b>：指出小李的观点是片面的（或将国家攻关与个人创新对立是错误的）。<br>
            ② <b>合理性分析（2分）</b>：指出其看到科技创新是国家大事是正确的。创新是引领发展的第一动力，是全面建设社会主义现代化国家的基础性、战略性支撑，国家必须实施创新驱动发展战略、加强核心技术攻关。<br>
            ③ <b>片面性分析（2分）</b>：指出其认为“创新离中学生太远、想搞也搞不了”是错误的。创新不局限于科技领域，生活处处有创新；创新不只是科学家的专利，人人皆可创新；中学生努力学习课本知识并不排斥培养创新思维与实践能力。<br>
            ④ <b>正确做法与升华（1分）</b>：青少年应树立创新报国志向，敢于质疑，勤于思考，在日常实践中培养探究能力，争做创新型人才。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p><b>小李的观点是片面的。</b></p>
            <p>（1）小李认识到“科技创新是国家大事、需要国家统筹攻关”具有合理性。因为创新是引领发展的第一动力，科技自立自强是国家强盛之基、安全之要。我国深入实施科教兴国、人才强国和创新驱动发展战略，确实需要国家集中力量打好关键核心技术攻坚战。</p>
            <p>（2）但是，小李认为“搞创新是大人的事，与初中生无关且初中生搞不了”是错误的。因为生活处处有创新，创新不仅属于科学家，我们每个人都可以是创新者。刻苦学习文化知识是创新的基石，但绝不能把学习局限于死记硬背。</p>
            <p>（3）因此，我们初中生既要努力打牢科学文化知识基础，又要培养好奇心与批判性思维，积极参加科技小发明、小制作等社会实践，努力成长为担当民族复兴大任的创新型人才。</p>
          </div>
          <div class="trap-warning">
            ⚠️ <b>扣分警示</b>：如果只回答“小李观点错误”，且没有分层肯定合理点、直接抄写课本一大段“创新驱动发展战略”，将被降档扣除2-3分。
          </div>
        </div>
      </div>

      <!-- Q2: 辨析题 · 坚持党的领导与依法治国关系 -->
      <div class="question-card" data-tag="bianxi party">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag tag-red">专项① 辨析题</span>
            <span class="q-tag tag-emerald">新课标 党的领导与法治中国</span>
            <span class="q-tag tag-blue">九上 核心大题</span>
          </div>
          <div class="q-score">满分：6分 | 难度：★★★★☆</div>
        </div>
        <div class="q-material">
          <b>【情境材料】</b>
          在道法复习交流课上，小吴同学提出：“既然我国要坚持全面依法治国，宪法法律具有至高无上的权威，任何组织和个人都必须在宪法和法律范围内活动，那么‘坚持中国共产党的全面领导’就与‘全面依法治国’存在冲突，两者不能并列。”
        </div>
        <div class="q-stem">
          【设问】：请运用九年级上册“坚持党的全面领导”和“建设法治中国”的相关知识，对小吴同学的观点进行辨析。
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 审题与思维破题链：</div>
          <div class="chain-flow">
            <div class="chain-step">定性：观点错误（割裂两者的辩证统一）</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">论证1：党的领导是法治的根本保证</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">论证2：宪法法律由党领导人民制定执行</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">总结：三者有机统一（党的领导、人民当家作主、依法治国）</div>
          </div>
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 在此输入您的答题草稿思路..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
            <span>💡 提示：抓住“党的领导是全面依法治国的根本保证”这一核心命题</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-2', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-2">
          <div class="grading-points">
            <b>【采分要点与赋分标准】</b>（满分6分）：<br>
            ① <b>判断定性（1分）</b>：小吴的观点是错误的，割裂了党的领导与全面依法治国的内在统一关系。<br>
            ② <b>析法律权威的合理认知（1分）</b>：小吴认识到“宪法法律具有最高权威，任何组织和个人都必须在宪法法律范围内活动”是正确的，这是全面依法治国的必然要求。<br>
            ③ <b>核心理论反驳与阐述（3分）</b>：<br>
            - 党的领导是全面依法治国的根本保证。中国特色社会主义法治道路最本质的特征就是坚持中国共产党的领导；<br>
            - 党领导人民制定宪法法律，党领导人民实施宪法法律，党自身必须在宪法和法律范围内活动。这就是党的领导立法、保证执法、支持司法、带头守法；<br>
            - 坚持党的领导、人民当家作主、依法治国是有机统一的整体，绝不冲突。<br>
            ④ <b>结论升华（1分）</b>：推进法治中国建设必须坚定不移走中国特色社会主义法治道路，把党的领导贯彻到依法治国全过程。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p><b>小吴的观点是错误的。</b></p>
            <p>（1）小吴认识到“宪法和法律具有权威、任何组织都必须在宪法法律范围内活动”是正确的，全面依法治国必须维护宪法法律权威。</p>
            <p>（2）但他认为“党的领导与全面依法治国存在冲突”是完全错误的。因为：①党的领导是中国特色社会主义最本质的特征，是中国特色社会主义制度的最大优势，也是全面依法治国的根本保证；②党领导人民制定宪法和法律，党也带头遵守宪法和法律。党领导立法、保证执法、支持司法、带头守法，把党的主张通过法定程序上升为国家意志；③我国宪法以根本法的形式确立了中国共产党的领导地位，维护宪法权威与坚持党的领导高度一致。</p>
            <p>（3）因此，全面依法治国必须坚持党的领导、人民当家作主、依法治国有机统一，决不能把党的领导和依法治国对立起来。</p>
          </div>
        </div>
      </div>

      <!-- Q3: 材料分析题 · 中国式现代化与共同富裕 (上海践行人民城市) -->
      <div class="question-card" data-tag="cailiao party">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag tag-blue">专项② 材料分析题</span>
            <span class="q-tag tag-emerald">九上 中国式现代化专题</span>
            <span class="q-tag tag-red">上海“人民城市”本土化</span>
          </div>
          <div class="q-score">满分：8分 | 难度：★★★★☆</div>
        </div>
        <div class="q-material">
          <b>【情境材料】</b>
          材料一：新时代以来，上海全面践行“人民城市人民建，人民城市为人民”重要理念。五年间，上海累计完成中心城区成片二级旧里以下房屋改造超300万平方米，历史性解决困扰几代人的居住难题；打造“15分钟社区生活圈”，家门口有了便民食堂、托育点、口袋公园与长者运动健康之家；推行“一网通办”，让市民“足不出户、刷脸办成”。<br><br>
          材料二：党的二十大报告指出，中国式现代化是人口规模巨大的现代化，是全体人民共同富裕的现代化，是物质文明和精神文明相协调的现代化，是人与自然和谐共生的现代化，是走和平发展道路的现代化。
        </div>
        <div class="q-stem">
          【设问】：结合材料一、材料二，运用九年级上册相关知识，分析说明上海在推进人民城市建设中是如何生动诠释“中国式现代化”内涵的？
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 审题与思维破题链（四角对应）：</div>
          <div class="chain-flow">
            <div class="chain-step">旧区改造+15分钟生活圈 ➔ 共同富裕+以人民为中心</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">口袋公园+健康之家 ➔ 人与自然和谐+物质精神相协调</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">一网通办+数字赋能 ➔ 治理体系现代化+高品质生活</div>
          </div>
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 在此输入您的答题思路：分点提取材料 + 对接中国式现代化的具体特征..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
            <span>💡 提示：紧扣“全体人民共同富裕”、“以人民为中心”及五大特征</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-3', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-3">
          <div class="grading-points">
            <b>【采分要点与赋分标准】</b>（满分8分）：<br>
            ① <b>共同富裕与民生福祉角度（3分）</b>：材料中上海解决旧里改造、建设“15分钟社区生活圈”解决群众急难愁盼，体现了中国式现代化是<b>全体人民共同富裕的现代化</b>；体现了党和政府坚持<b>以人民为中心的发展思想</b>，让现代化建设成果更多更公平惠及全体市民，增进民生福祉。<br>
            ② <b>物质与精神文明协调、人与自然和谐角度（3分）</b>：建设便民食堂、托育点与口袋公园，既满足了市民物质生活便利，又丰富了居民文化精神需求与绿色生态空间，体现了中国式现代化是<b>物质文明和精神文明相协调、人与自然和谐共生</b>的现代化。<br>
            ③ <b>社会治理与高品质生活角度（2分）</b>：推行“一网通办”提高政务服务效能，体现了依靠数字化转型提升超大城市治理现代化水平，不断满足人民日益增长的美好生活需要，走出一条中国特色超大城市治理现代化的新路。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p>上海的人民城市建设生动体现了中国式现代化的丰富内涵：</p>
            <p><b>① 诠释了“全体人民共同富裕的现代化”</b>：上海大力推进成片旧改与15分钟社区圈，聚焦解决老百姓的住房、就餐、托幼养老等急难愁盼，践行了坚持以人民为中心的发展思想，守住了共享发展的底线，不断提升市民的获得感与幸福感。</p>
            <p><b>② 诠释了“物质文明与精神文明相协调、人与自然和谐共生的现代化”</b>：通过打造推窗见绿的口袋公园、运动健康之家与便民文化设施，上海既夯实了市民美好生活的物质保障，又优化了生态环境与健康生活方式，促进了人的全面发展。</p>
            <p><b>③ 诠释了国家治理体系和治理能力现代化的内在要求</b>：上海通过“一网通办”打造智慧政府、法治政府和服务型政府，让数据多跑路、市民少跑腿，以精细化、数字化治理保障人民群众的根本利益。</p>
          </div>
        </div>
      </div>

      <!-- Q4: 材料分析题 · 全过程人民民主的生动基层实践 -->
      <div class="question-card" data-tag="cailiao party">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag tag-blue">专项② 材料分析题</span>
            <span class="q-tag tag-purple">九上 政治建设与民主价值</span>
            <span class="q-tag tag-emerald">全国人大虹桥基层立法联系点</span>
          </div>
          <div class="q-score">满分：8分 | 难度：★★★★☆</div>
        </div>
        <div class="q-material">
          <b>【情境材料】</b>
          位于上海长宁区的虹桥街道是全国人大常委会法工委设立的首批基层立法联系点之一。在这里，下沉社区的立法意见征询会常常就在居民楼下的“古北市民议事厅”或咖啡馆举行。上至两院院士、专家学者，下至快递小哥、外国留学生、退休阿姨，都可以在这里为国家法律草案“挑刺”、提修改意见。成立以来，该联系点已听取上万人次意见，多条带着“烟火气”的草根建议被直接采纳写入国家正式法律法规中。
        </div>
        <div class="q-stem">
          【设问】：请运用“追求民主价值”与“全过程人民民主”的相关知识，分析为什么虹桥基层立法联系点的实践能够让“中国式民主”焕发勃勃生机？
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 审题与思维破题链：</div>
          <div class="chain-flow">
            <div class="chain-step">民主本质 ➔ 人民当家作主</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">特征 ➔ 最广泛、最真实、最管用</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">形式 ➔ 协商民主与选举民主相结合</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">机制 ➔ 基层民意直通国家立法机关</div>
          </div>
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 在此输入您的答题草稿..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-4', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-4">
          <div class="grading-points">
            <b>【采分要点与赋分标准】</b>（满分8分）：<br>
            ① <b>社会主义民主本质（2分）</b>：我国社会主义民主是维护人民根本利益的最广泛、最真实、最管用的民主。基层立法联系点让普通百姓直接参与国家立法，生动彰显了<b>人民当家作主</b>是社会主义民主政治的本质特征。<br>
            ② <b>协商民主的独特优势（2分）</b>：基层立法联系点搭建了基层议事平台，有事好商量，众人的事情众人商量，充分发挥了我国<b>协商民主</b>的独特优势，拓宽了公民参与民主生活的途径。<br>
            ③ <b>全过程人民民主的链条完整（2分）</b>：全过程人民民主不仅有完整的制度程序，而且有完整的参与实践。将民意民智直接吸纳转化为国家法律，实现了民主选举、民主协商、民主决策、民主管理、民主监督的环环相扣。<br>
            ④ <b>凝聚共识与制度自信（2分）</b>：推动了科学立法、民主立法，使法律更加体现人民意愿，增强了人民对中国特色社会主义政治制度的认同与法治信仰。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p>虹桥基层立法联系点的成功实践体现了全过程人民民主的强大生命力：</p>
            <p><b>① 彰显了人民当家作主的本质属性</b>：我国是人民民主专政的社会主义国家，基层立法联系点打破了立法与老百姓的距离感，让普通群众成为国家立法的主人翁，体现了民主权利的最真实与最管用。</p>
            <p><b>② 展现了中国协商民主的独特优势</b>：通过社区议事厅等接地气的形式，贯彻了“有事好商量，众人的事情由众人商量”的协商民主精神，广泛凝聚了社会各界最大共识。</p>
            <p><b>③ 践行了全过程人民民主的完整闭环</b>：群众的真实意见建议直达国家最高立法机关并被写进法律，实现了民意表达与立法决策的无缝衔接，提升了立法的科学性与民主性，增强了全社会的法治素养与制度自信。</p>
          </div>
        </div>
      </div>

      <!-- Q5: 实践探究开放题 · 宣传标语与活动方案 (红色基因传承) -->
      <div class="question-card" data-tag="kaifang party">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag tag-emerald">专项③ 实践探究题</span>
            <span class="q-tag tag-red">伟大建党精神与红色血脉</span>
            <span class="q-tag tag-blue">活动策划与标语撰写</span>
          </div>
          <div class="q-score">满分：6分 | 难度：★★☆☆☆</div>
        </div>
        <div class="q-material">
          <b>【背景材料】</b>
          上海是中国共产党的诞生地、初心始发地和伟大建党精神的孕育地。为迎接一模复习并深化爱国主义教育，某初级中学团委决定在九年级开展“寻访红色足迹，担当强国重任”系列主题实践探究活动。
        </div>
        <div class="q-stem">
          【任务一】：请你为本次主题活动拟写一条宣传标语。（要求：主题鲜明，对仗工整，20字以内，2分）<br>
          【任务二】：请为学校团委设计两个具体的活动形式，并简要写出开展“红色寻访”活动的三个推进步骤。（4分）
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 在此拟写您的宣传标语与活动步骤..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
            <span>💡 提示：标语字数20字以内对偶；步骤按准备-实施-总结三阶段</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-5', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-5">
          <div class="grading-points">
            <b>【采分要点与赋分标准】</b>：<br>
            - <b>任务一 标语（2分）</b>：符合对偶句式、朗朗上口、主题契合建党精神或强国担当、无错别字即可得2分。<br>
            - <b>任务二 活动形式（1分）</b>：列出两个可行且契合主题的形式（如参观会址、微党课演讲、情景朗诵等）。<br>
            - <b>任务二 推进步骤（3分）</b>：按照准备阶段（1分）、实施阶段（1分）、总结阶段（1分）逻辑清晰列出。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p><b>【任务一 宣传标语示范】</b>：<br>
            <i>示范 1</i>：<b>赓续红色血脉，勇担时代重任。</b>（12字）<br>
            <i>示范 2</i>：<b>追寻初心始发地，争做强国弄潮儿。</b>（14字）</p>

            <p style="margin-top:0.6rem;"><b>【任务二 活动方案设计】</b>：<br>
            <b>1. 活动形式（任选两种）</b>：<br>
            ① 实地寻访：组织前往中共一大会址纪念馆、中共二大会址进行沉浸式实地瞻仰；<br>
            ② 成果汇演：开展“红领巾讲党史故事”微视频拍摄比赛或主题演讲比赛。<br>
            <b>2. 推进步骤</b>：<br>
            ① <b>准备阶段</b>：成立活动筹备小组，查阅党史文献资料，确定寻访场馆路线与安全预案，设计学习打卡任务单；<br>
            ② <b>实施阶段</b>：赴红色场馆进行现场参观打卡，认真聆听讲解，收集老一辈革命家感人文物史料，开展现场微访谈；<br>
            ③ <b>总结阶段</b>：各小组合成寻访调研报告或摄影展，举办“红色记忆伴我成长”交流分享会，深化思想认识。
            </p>
          </div>
        </div>
      </div>

      <!-- Q6: 实践探究开放题 · 建议建言类 (绿色低碳与美丽上海) -->
      <div class="question-card" data-tag="kaifang">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag tag-emerald">专项③ 实践探究题</span>
            <span class="q-tag tag-blue">九上 绿色发展与生态文明</span>
            <span class="q-tag tag-amber">建言献策/建议题</span>
          </div>
          <div class="q-score">满分：6分 | 难度：★★★☆☆</div>
        </div>
        <div class="q-material">
          <b>【调研背景】</b>
          某校开展“减塑减碳，共建美丽生态上海”社会微调研。同学们发现：虽然“垃圾分类”已成市民习惯，但在部分快递站点与外卖商圈，依然存在“过度包装、一次性塑料制品泛滥、外卖餐盒回收难度大”等资源浪费与环境压力问题。
        </div>
        <div class="q-stem">
          【设问】：请你运用“坚持人与自然和谐共生”的相关知识，采用“主体分析法”，分别向<b>政府监管部门、相关企业商户、广大市民及青少年</b>提出各一条具体可行的合理化建议。（6分）
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 请按【政府】、【企业】、【市民/青少年】三个主体列出建议..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-6', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-6">
          <div class="grading-points">
            <b>【采分要点与赋分标准】</b>（6分，每个主体各2分）：<br>
            建议必须具备针对性和可操作性，不可出现“假大空”套话。<br>
            ① <b>政府/监管部门（2分）</b>：完善绿色包装相关行业标准，强化对快递外卖过度包装的执法监督，并出台绿色低碳税收补贴激励政策。<br>
            ② <b>企业/平台商户（2分）</b>：践行绿色发展理念，积极推广使用可降解环保包装袋、循环餐盒，在点餐下单页面默认“无需餐具”选项。<br>
            ③ <b>市民及青少年（2分）</b>：树立生态文明理念，自觉践行光盘行动与垃圾分类；在外卖购物时主动勾选无需一次性餐具，自带环保购物袋，做绿色低碳生活的践行者与宣传者。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p><b>① 对政府监管部门</b>：加强绿色包装地方立法与行业标准细化，运用数字化监管平台对快递外卖过度包装开展常态化抽查通报，并对主动采用可降解包装材料的绿色企业给予政策补贴或税收优惠。</p>
            <p><b>② 对相关企业商户</b>：主动承担环境保护社会责任，在平台算法中强化“绿色积分”激励机制，鼓励消费者减少使用一次性用品；加大对生物降解材质的研发投入，推广可循环使用周转箱。</p>
            <p><b>③ 对广大市民及青少年</b>：增强节约资源、保护环境的法治与道德意识，在外卖下单时主动勾选“无需一次性餐具”；外出购物常备布袋，从身边的绿色出行、垃圾分类等微行动做起，积极向家人和邻里宣传低碳生活方式。</p>
          </div>
        </div>
      </div>

      <!-- Q7: 【真实讲评大题】2024上海初三道法综合卷一·脱贫攻坚成果巩固与推测理由 -->
      <div class="question-card" data-tag="cailiao party">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag" style="background:#FEF2F2; color:#DC2626; border:1px solid #FECDD3; font-weight:800;">🔥 2024上海初三综合卷一原卷</span>
            <span class="q-tag tag-blue">专项② 材料分析推测题</span>
            <span class="q-tag tag-emerald">以人民为中心 · 乡村振兴促进法</span>
          </div>
          <div class="q-score">满分：6分 | 真实中考一模评分</div>
        </div>
        <div class="q-material">
          <b>【真实原卷材料与数据图表】</b><br>
          图 1（经济成就）：2018-2023年全国国内生产总值持续跃升，国家财政实力与科技创新驱动力显著增强；<br>
          图 2（民生成就）：脱贫攻坚取得全面胜利后，全国农村居民人均可支配收入增速持续快于城镇居民，城乡差距逐步缩小；国家颁布实施《中华人民共和国乡村振兴促进法》；各地通过“电商直播带货、农产品深加工”等新业态拓展增收渠道。
        </div>
        <div class="q-stem">
          【设问】：由此，同学们推测未来我国一定能够巩固和拓展脱贫攻坚成果。请结合上述材料，综合运用所学内容，说明同学们提出推测的理由。（6分）
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 官方讲评标准破题链（材 ➔ 知）：</div>
          <div class="chain-flow">
            <div class="chain-step">过去：经济实力大幅跃升 ➔ 坚实物质基础</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">政治：党的全面领导 ➔ 坚持以人民为中心</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">战略：乡村振兴战略 ➔ 缩小差距共同富裕</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">法治：乡村振兴促进法 ➔ 科学立法法治保障</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">技术：网络赋能 ➔ 生产方式变革增进民生</div>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-7', this)">👁️ 查看官方讲评采分思路与满分答案</button>
        <div class="ans-panel" id="ans-7">
          <div class="grading-points">
            <b>【官方讲评思路与采分要点】</b>（6分）：<br>
            ① <b>物质基础角度（1.5分）</b>：过去我国经济实力大幅跃升、发展质量显著提升，为未来巩固和拓展脱贫成果提供了坚实的经济基础和物质保障；<br>
            ② <b>党的领导与宗旨角度（1.5分）</b>：中国共产党坚持以人民为中心的发展思想，站稳人民立场，深入实施乡村振兴战略，促进区域与城乡协调发展，扎实推进共同富裕；<br>
            ③ <b>法治保障角度（1.5分）</b>：国家坚持科学立法，制定并实施《乡村振兴促进法》，为全面推进乡村振兴、巩固脱贫成果提供了坚强有力的法治保障；<br>
            ④ <b>科技与社会支撑角度（1.5分）</b>：互联网与现代科技推动生产生活方式变革，农村电商与直播助农拓宽了农民增收渠道，切实改善民生福祉。
          </div>
          <div class="full-answer-text">
            <p><b>【满分标准范文】</b>：</p>
            <p>同学们提出这一推测具有充分的现实与理论依据：</p>
            <p><b>① 坚实的物质保障</b>：我国经济实力大幅跃升，综合国力持续增强，为未来持续推进农业农村现代化、巩固脱贫成果提供了坚实的物质条件和财政支持。</p>
            <p><b>② 党的坚强领导与人民立场</b>：中国共产党坚持立党为公、执政为民，始终坚持以人民为中心的发展思想。深入实施乡村振兴战略，致力于缩小城乡发展差距，让全体人民共享改革发展成果。</p>
            <p><b>③ 完备的法治护航</b>：国家颁布施行《乡村振兴促进法》，坚持全面依法治国，为脱贫攻坚成果同乡村振兴有效衔接提供了坚强有力的法治保障。</p>
            <p><b>④ 数字化与科技赋能</b>：网络与数字化转型深度融入乡村产业，直播带货等新业态激发了农村内生发展动力，促进了农业提质增效与农民增收。</p>
          </div>
        </div>
      </div>

      <!-- Q8: 【真实讲评辨析题】2024上海初三道法综合卷一·建党精神与学习实践辨析 -->
      <div class="question-card" data-tag="bianxi party">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag" style="background:#FEF2F2; color:#DC2626; border:1px solid #FECDD3; font-weight:800;">🔥 2024上海初三综合卷一原卷</span>
            <span class="q-tag tag-red">专项① 辨析评析题</span>
            <span class="q-tag tag-emerald">伟大建党精神 · 学习观</span>
          </div>
          <div class="q-score">满分：6分 | 真实中考一模评分</div>
        </div>
        <div class="q-material">
          <b>【真实原卷材料】</b><br>
          学校组织“寻访红色足迹、传承建党精神”综合实践研学活动。个别同学认为：“学习只是在学校里听课刷题，初中生只要把课内文化课分数搞上去就行了，花时间去参加红色研学、宣讲建党精神纯属形式主义，对我们中考升学没有任何实质作用。”
        </div>
        <div class="q-stem">
          【设问】：请运用六至九年级相关知识，对该同学的观点进行评析。（6分）
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 官方讲评标准破题链：</div>
          <div class="chain-flow">
            <div class="chain-step">明任务判思路：判断不对</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">理由1（学习六上）：学习不局限于课本，社会实践是重要途径</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">理由2（建党精神九上）：精神之源+精神谱系，提供强大动力</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">回应与价值驱动：积极参加研学，弘扬伟大建党精神</div>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-8', this)">👁️ 查看官方讲评采分思路与满分答案</button>
        <div class="ans-panel" id="ans-8">
          <div class="grading-points">
            <b>【官方讲评思路与采分细则】</b>（6分）：<br>
            ① <b>判断定性（1分）</b>：该同学的观点是不对的（片面的）。<br>
            ② <b>理由一（学习观维度，2分）</b>：中学阶段的学习不局限于学校课本知识的传授，不仅表现为接受和掌握，而且表现为探究、发现、体验和感悟。参加社会实践与红色研学是重要的学习途径，有利于开阔眼界、磨砺意志、提升综合素养。<br>
            ③ <b>理由二（建党精神维度，2分）</b>：伟大建党精神是中国共产党的精神之源，构建了中国共产党人的精神谱系。弘扬伟大建党精神能够为青少年的健康成长和民族复兴大任提供强大的精神动力，绝非形式主义。<br>
            ④ <b>回应与升华（1分）</b>：我们初中生既要努力学好课内科学文化知识，又要积极参与红色实践活动，传承红色基因，努力成长为担当民族复兴大任的时代新人。
          </div>
        </div>
      </div>

      <!-- Q9: 【真实讲评微情境】2024上海初三道法综合卷一·竞争友谊与情绪管理 -->
      <div class="question-card" data-tag="kaifang">
        <div class="q-meta">
          <div class="q-tags">
            <span class="q-tag" style="background:#FEF2F2; color:#DC2626; border:1px solid #FECDD3; font-weight:800;">🔥 2024上海初三综合卷一原卷</span>
            <span class="q-tag tag-emerald">专项③ 实践探究与生活情境</span>
            <span class="q-tag tag-blue">做情绪的主人 · 呵护友谊</span>
          </div>
          <div class="q-score">满分：6分 | 真实中考一模评分</div>
        </div>
        <div class="q-material">
          <b>【真实生活情境】</b><br>
          九年级月考成绩揭晓后，好友小陈因几门科目成绩下滑而情绪低落，甚至因为同桌小李在本次考试中名列前茅而心生嫉妒、冷眼相待，两人陷入冷战。小陈在日记中写道：“竞争太残酷了，既然有了竞争，朋友之间就不可能再有真正的友谊，我控制不住自己的沮丧与烦躁。”
        </div>
        <div class="q-stem">
          【设问】：请运用七年级《情绪的管理》与八年级《友谊的天空》相关知识，给小陈提出合理化建议，帮助他走出心理困境。（6分）
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 官方讲评标准破题链：</div>
          <div class="chain-flow">
            <div class="chain-step">友谊认知：竞争并不必然伤害友谊，要学会欣赏对手与自我反思</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">情绪调控：运用改变认知评价、注意转移、合理宣泄做情绪的主人</div>
            <span class="chain-arrow">➔</span>
            <div class="chain-step">行动建议：敞开心扉主动沟通，请教学习方法，互助互学共同进步</div>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-9', this)">👁️ 查看官方讲评采分思路与满分答案</button>
        <div class="ans-panel" id="ans-9">
          <div class="grading-points">
            <b>【官方讲评思路与采分细则】</b>（6分）：<br>
            ① <b>竞争与友谊认知（2分）</b>：竞争并不必然伤害友谊，关键是我们对待竞争的态度。在竞争中能坦然接受并欣赏朋友的成就，做到自我反思；在合作中竞争，在竞争中合作。<br>
            ② <b>情绪调节方法（2分）</b>：学会合理调节情绪，运用改变认知评价、转移注意、合理宣泄或放松训练等方法，敞开心扉，在合适场合关照他人，做情绪的主人。<br>
            ③ <b>具体行动建议（2分）</b>：主动找同桌沟通交流化解误会，反思自身学习中的薄弱环节，虚心请教学习方法，在互帮互助中共同进步，成为更好的自己。
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- 提示弹窗 -->
  <div class="toast" id="toast-msg">✅ 答题模板已成功复制到剪贴板！可以直接粘贴复习！</div>

  <footer>
    <p>© 2026 Owen Learning Center · 上海初中道法教学研发中心</p>
    <p style="margin-top: 0.4rem; font-size: 0.8rem;">严格对标上海新课标与初三一模/二模考点大纲 · 结构化采分点 · 拒绝死记硬背</p>
  </footer>

  <script>
    // 切换大纲展开折叠
    function toggleSyllabus() {
      const body = document.getElementById('syllabus-body');
      const arrow = document.getElementById('syllabus-arrow');
      if (body.style.display === 'none') {
        body.style.display = 'grid';
        arrow.textContent = '收起 ▲';
      } else {
        body.style.display = 'none';
        arrow.textContent = '展开大纲 ▼';
      }
    }

    // 展开折叠答案
    function toggleAnswer(ansId, btn) {
      const panel = document.getElementById(ansId);
      if (panel.classList.contains('open')) {
        panel.classList.remove('open');
        btn.textContent = '👁️ 查看本题官方答案与采分细则';
      } else {
        panel.classList.add('open');
        btn.textContent = '🙈 收起本题答案与采分细则';
      }
    }

    // 标签过滤
    function filterByTag(tag, btn) {
      document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const cards = document.querySelectorAll('.question-card');
      cards.forEach(card => {
        if (tag === 'all') {
          card.style.display = 'block';
        } else {
          const tags = card.getAttribute('data-tag') || '';
          if (tags.includes(tag)) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        }
      });
    }

    // 选项卡切换
    function switchTab(tabKey, btn) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // 联动过滤
      if (tabKey === 'tab-all') {
        filterByTag('all', document.querySelectorAll('.filter-pill')[0]);
      } else if (tabKey === 'tab-bianxi') {
        filterByTag('bianxi', document.querySelectorAll('.filter-pill')[1]);
      } else if (tabKey === 'tab-cailiao') {
        filterByTag('cailiao', document.querySelectorAll('.filter-pill')[2]);
      } else if (tabKey === 'tab-kaifang') {
        filterByTag('kaifang', document.querySelectorAll('.filter-pill')[3]);
      } else if (tabKey === 'tab-party') {
        filterByTag('party', document.querySelectorAll('.filter-pill')[4]);
      }
    }

    // 实时搜索
    function searchQuestions() {
      const query = document.getElementById('q-search').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.question-card');
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    // 字数统计
    function updateWordCount(textarea) {
      const len = textarea.value.trim().length;
      const counter = textarea.parentElement.querySelector('.wc-num');
      if (counter) counter.textContent = len;
    }

    // 复制模板
    function copyTemplate(type) {
      let text = '';
      if (type === 'bianxi') {
        text = `【上海初三道法·辨析评析题 四步定乾坤满分模板】\\n1. 判断定性：该观点是片面的/不科学的/把XX与XX割裂开来是错误的。\\n2. 阐释合理：该观点看到……具有合理性。因为【对应教材金句/理论】……\\n3. 攻其破绽：但是，该观点忽视了/否定了……因为【补充教材原理】……如果……会导致……\\n4. 总结升华：因此，我们应该坚持……与……相统一，青少年要在实践中做到……`;
      } else if (type === 'cailiao') {
        text = `【上海初三道法·材料分析题 四角对应法黄金公式】\\n1. 析材料：材料中提到……反映了我国/上海在……方面的成效；\\n2. 引金句：这体现了/贯彻了【党的领导/高质量发展/以人民为中心/全过程人民民主】；\\n3. 讲意义：这有利于保障……有利于推动……有利于推进中国式现代化；\\n4. 扣结论：因此，这充分彰显了……的生动实践。`;
      } else if (type === 'kaifang') {
        text = `【上海初三道法·实践探究开放题 黄金公式】\\n- 标语对偶句：主题核心 + 行动倡导（如：树立法治信仰，共建和谐社会）\\n- 建议主体法：\\n  ① 政府：完善法规，严格执法监督，出台激励政策；\\n  ② 企业/学校：营造良好氛围，履行社会责任；\\n  ③ 青少年：提高思想认识，自觉践行，从身边小事做起。\\n- 方案三步骤：准备阶段（方案/调研） ➔ 实施阶段（宣讲/座谈） ➔ 总结阶段（报告/表彰）`;
      }

      navigator.clipboard.writeText(text).then(() => {
        const toast = document.getElementById('toast-msg');
        toast.style.display = 'flex';
        setTimeout(() => { toast.style.display = 'none'; }, 2500);
      });
    }
  </script>
</body>
</html>
"""

def main():
    out_dir = "/Users/emily/Documents/Projects/owenlearining/daofa"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "daofa-special-bank.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Generated successfully: {out_file} ({len(HTML_CONTENT)} bytes)")

if __name__ == "__main__":
    main()
