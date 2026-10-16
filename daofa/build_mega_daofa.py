# -*- coding: utf-8 -*-
"""
Mega Daofa Special Question Bank Builder
上海初三道德与法治 · 一模冲刺10次课专项真题库与满分答题工作台
包含22道源自上海中考原卷、各区一模（浦东、徐汇、黄浦、闵行、静安、虹口、宝山、松江等）
以及官方教学教研综合卷一、课后练习讲评资料1-6的全真真题与详尽采分细则。
"""

import os
import sys

def get_html_head():
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>上海初三道法 · 一模冲刺10次课专项真题库与满分答题工作台 | 22套中考与区一模全真试题</title>
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
      --blue-dark: #1D4ED8;
      --blue-light: #EFF6FF;
      --blue-border: #BFDBFE;

      --emerald-main: #059669;
      --emerald-light: #ECFDF5;
      --emerald-border: #A7F3F0;

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
      font-weight: 700;
    }
    .nav-actions {
      display: flex; align-items: center; gap: 0.75rem;
    }
    .nav-btn {
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.45rem 0.85rem; border-radius: var(--radius-sm);
      background: var(--bg-card); border: 1px solid var(--border-color);
      color: var(--text-sub); font-size: 0.85rem; font-weight: 600; text-decoration: none;
      transition: all 0.2s; cursor: pointer;
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

    /* 主容器 */
    .main-wrap {
      max-width: 1400px; margin: 0 auto; padding: 1.5rem 1.25rem 4rem;
    }

    /* 冲刺横幅 */
    .sprint-hero {
      background: linear-gradient(135deg, #FFF1F2 0%, #FFFFFF 50%, #EFF6FF 100%);
      border: 1px solid #FECDD3; border-radius: var(--radius-lg);
      padding: 2rem 2rem 1.75rem; margin-bottom: 2rem;
      box-shadow: var(--shadow-sm); position: relative; overflow: hidden;
    }
    .sprint-hero::before {
      content: "上海新中考真题全覆盖";
      position: absolute; right: -32px; top: 22px;
      background: linear-gradient(90deg, #DC2626, #EF4444);
      color: white; font-size: 0.72rem; font-weight: 800;
      padding: 4px 40px; transform: rotate(45deg);
      box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    .hero-top-tag {
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.25rem 0.65rem; border-radius: 999px;
      background: white; border: 1px solid var(--red-border);
      color: var(--red-main); font-size: 0.8rem; font-weight: 700;
      margin-bottom: 0.75rem;
    }
    .hero-title {
      font-size: 1.85rem; font-weight: 800; color: #1E293B; line-height: 1.3;
      margin-bottom: 0.75rem;
    }
    .hero-title span {
      background: linear-gradient(135deg, #DC2626, #B91C1C);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-desc {
      font-size: 0.95rem; color: var(--text-sub); max-width: 960px; line-height: 1.6;
      margin-bottom: 1.25rem;
    }

    /* 三大支柱卡片 */
    .pillars-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem; margin-top: 1rem;
    }
    .pillar-card {
      background: rgba(255, 255, 255, 0.85); border: 1px solid var(--border-color);
      border-radius: var(--radius-md); padding: 1rem 1.2rem;
      display: flex; gap: 0.85rem; align-items: flex-start;
      transition: all 0.2s;
    }
    .pillar-card:hover {
      background: white; border-color: var(--border-hover);
      transform: translateY(-2px); box-shadow: var(--shadow-sm);
    }
    .pillar-icon {
      width: 36px; height: 36px; border-radius: var(--radius-sm);
      display: flex; align-items: center; justify-content: center;
      font-size: 1.2rem; flex-shrink: 0;
    }
    .pillar-title {
      font-size: 0.95rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.2rem;
    }
    .pillar-detail {
      font-size: 0.82rem; color: var(--text-muted); line-height: 1.45;
    }

    /* 10次课冲刺大纲折叠盒 */
    .syllabus-box {
      background: var(--bg-card); border: 1px solid var(--border-color);
      border-radius: var(--radius-md); margin-bottom: 2rem; overflow: hidden;
      box-shadow: var(--shadow-sm);
    }
    .syllabus-header {
      padding: 1rem 1.25rem; background: var(--bg-subtle);
      display: flex; justify-content: space-between; align-items: center;
      cursor: pointer; user-select: none;
    }
    .syllabus-header:hover { background: #E2E8F0; }
    .syllabus-title-wrap {
      display: flex; align-items: center; gap: 0.75rem;
    }
    .syllabus-title {
      font-weight: 700; font-size: 1.05rem; color: var(--text-main);
    }
    .syllabus-badge {
      background: var(--red-light); color: var(--red-main); border: 1px solid var(--red-border);
      font-size: 0.75rem; padding: 0.15rem 0.5rem; border-radius: 999px; font-weight: 700;
    }
    .syllabus-timeline {
      padding: 1.25rem; display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 0.75rem; background: white;
    }
    .timeline-item {
      padding: 0.75rem 1rem; border-radius: var(--radius-sm);
      background: var(--bg-page); border: 1px solid var(--border-color);
      display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.85rem;
    }
    .timeline-item.active-special {
      background: #FEF2F2; border-color: #FECDD3;
    }
    .timeline-num {
      font-weight: 800; color: var(--red-main); margin-right: 0.35rem;
    }
    .timeline-name {
      font-weight: 700; color: var(--text-main);
    }
    .timeline-tag {
      font-size: 0.75rem; color: var(--text-muted);
    }

    /* 答题模板卡片组 */
    .templates-section {
      margin-bottom: 2rem;
    }
    .section-head {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 1rem;
    }
    .section-title {
      font-size: 1.3rem; font-weight: 800; color: var(--text-main);
      display: flex; align-items: center; gap: 0.5rem;
    }
    .section-subtitle {
      font-size: 0.85rem; color: var(--text-muted);
    }
    .tmpl-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 1.25rem;
    }
    .tmpl-card {
      background: var(--bg-card); border: 1px solid var(--border-color);
      border-radius: var(--radius-md); padding: 1.25rem;
      box-shadow: var(--shadow-sm); display: flex; flex-direction: column;
      position: relative;
    }
    .tmpl-header {
      display: flex; justify-content: space-between; align-items: flex-start;
      margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px dashed var(--border-color);
    }
    .tmpl-title {
      font-size: 1.05rem; font-weight: 700; color: var(--text-main);
    }
    .tmpl-tag {
      font-size: 0.72rem; padding: 0.2rem 0.5rem; border-radius: 999px;
      font-weight: 700;
    }
    .steps-grid {
      display: grid; gap: 0.75rem;
    }
    .step-box {
      background: var(--bg-page); border: 1px solid var(--border-color);
      border-radius: var(--radius-sm); padding: 0.75rem 0.9rem;
    }
    .step-name {
      font-weight: 700; font-size: 0.85rem; color: var(--text-main); margin-bottom: 0.25rem;
      display: flex; align-items: center; gap: 0.35rem;
    }
    .step-desc {
      font-size: 0.8rem; color: var(--text-sub); line-height: 1.5;
    }

    /* 题库控制与过滤条 */
    .filter-bar {
      background: white; border: 1px solid var(--border-color);
      border-radius: var(--radius-md); padding: 1rem 1.25rem;
      margin-bottom: 1.5rem; box-shadow: var(--shadow-sm);
      display: flex; flex-wrap: wrap; gap: 0.75rem; justify-content: space-between; align-items: center;
    }
    .filter-pills {
      display: flex; flex-wrap: wrap; gap: 0.5rem;
    }
    .filter-pill {
      padding: 0.45rem 0.9rem; border-radius: 999px;
      background: var(--bg-subtle); border: 1px solid var(--border-color);
      color: var(--text-sub); font-size: 0.85rem; font-weight: 600;
      cursor: pointer; transition: all 0.2s;
    }
    .filter-pill:hover {
      background: #E2E8F0; color: var(--text-main);
    }
    .filter-pill.active {
      background: var(--red-main); color: white; border-color: var(--red-main);
    }
    .search-input {
      padding: 0.45rem 1rem; border-radius: 999px;
      border: 1px solid var(--border-color); background: var(--bg-page);
      font-size: 0.85rem; width: 260px; outline: none; transition: all 0.2s;
    }
    .search-input:focus {
      border-color: var(--red-main); background: white; box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
    }

    /* 试题卡片 */
    .question-card {
      background: var(--bg-card); border: 1px solid var(--border-color);
      border-radius: var(--radius-md); padding: 1.5rem;
      margin-bottom: 1.5rem; box-shadow: var(--shadow-sm);
      transition: all 0.2s;
    }
    .question-card:hover {
      box-shadow: var(--shadow-md); border-color: var(--border-hover);
    }
    .q-meta {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;
    }
    .q-tags {
      display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;
    }
    .q-tag {
      font-size: 0.75rem; padding: 0.2rem 0.55rem; border-radius: 4px;
      font-weight: 700;
    }
    .tag-red { background: var(--red-light); color: var(--red-main); border: 1px solid var(--red-border); }
    .tag-blue { background: var(--blue-light); color: var(--blue-main); border: 1px solid var(--blue-border); }
    .tag-emerald { background: var(--emerald-light); color: var(--emerald-main); border: 1px solid var(--emerald-border); }
    .tag-amber { background: var(--amber-light); color: var(--amber-main); border: 1px solid var(--amber-border); }
    .tag-purple { background: var(--purple-light); color: var(--purple-main); border: 1px solid var(--purple-border); }

    .q-score {
      font-size: 0.85rem; font-weight: 700; color: var(--text-muted);
    }
    .q-material {
      background: var(--bg-page); border-left: 4px solid var(--blue-main);
      padding: 1rem 1.2rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      margin-bottom: 1rem; font-size: 0.92rem; color: #1E293B; line-height: 1.7;
    }
    .q-stem {
      font-size: 1rem; font-weight: 700; color: var(--text-main);
      margin-bottom: 1rem; line-height: 1.5;
    }

    /* 破题链 */
    .q-chain-box {
      background: #F8FAFC; border: 1px solid var(--border-color);
      border-radius: var(--radius-sm); padding: 0.85rem 1rem;
      margin-bottom: 1rem;
    }
    .chain-title {
      font-size: 0.82rem; font-weight: 800; color: var(--text-sub);
      margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;
    }
    .chain-flow {
      display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem;
    }
    .chain-step {
      background: white; border: 1px solid var(--border-color);
      padding: 0.25rem 0.65rem; border-radius: var(--radius-sm);
      font-size: 0.8rem; font-weight: 600; color: var(--text-main);
    }
    .chain-arrow {
      color: var(--red-main); font-weight: bold; font-size: 0.85rem;
    }

    /* 草稿做题区 */
    .draft-box {
      margin-bottom: 1rem;
    }
    .draft-textarea {
      width: 100%; min-height: 95px; padding: 0.85rem 1rem;
      border: 1px solid var(--border-color); border-radius: var(--radius-sm);
      font-family: inherit; font-size: 0.88rem; line-height: 1.6;
      resize: vertical; background: white; color: var(--text-main);
      outline: none; transition: border-color 0.2s;
    }
    .draft-textarea:focus {
      border-color: var(--blue-main); box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
    }
    .draft-footer {
      display: flex; justify-content: space-between; align-items: center;
      margin-top: 0.4rem; font-size: 0.78rem; color: var(--text-muted);
    }

    /* 答案手风琴 */
    .ans-toggle-btn {
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.55rem 1rem; border-radius: var(--radius-sm);
      background: var(--bg-subtle); border: 1px solid var(--border-color);
      color: var(--text-main); font-size: 0.85rem; font-weight: 700;
      cursor: pointer; transition: all 0.2s;
    }
    .ans-toggle-btn:hover {
      background: #E2E8F0;
    }
    .ans-panel {
      display: none; margin-top: 1rem; padding-top: 1rem;
      border-top: 1px dashed var(--border-color);
    }
    .ans-panel.open {
      display: block; animation: fadeIn 0.25s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .grading-points {
      background: #FFFBEB; border: 1px solid #FDE68A;
      border-radius: var(--radius-sm); padding: 0.9rem 1.1rem;
      margin-bottom: 0.85rem; font-size: 0.86rem; color: #92400E; line-height: 1.65;
    }
    .full-answer-text {
      background: #F0FDF4; border: 1px solid #BBF7D0;
      border-radius: var(--radius-sm); padding: 0.9rem 1.1rem;
      font-size: 0.9rem; color: #166534; line-height: 1.7;
      margin-bottom: 0.85rem;
    }
    .trap-warning {
      background: #FEF2F2; border: 1px solid #FECDD3;
      border-radius: var(--radius-sm); padding: 0.75rem 1rem;
      font-size: 0.82rem; color: #991B1B; line-height: 1.5;
    }

    /* 页脚与提示 */
    footer {
      text-align: center; padding: 3rem 1rem 2rem;
      color: var(--text-muted); font-size: 0.85rem;
      border-top: 1px solid var(--border-color); margin-top: 4rem;
    }
    .toast {
      position: fixed; bottom: 24px; right: 24px;
      background: #1E293B; color: white; padding: 0.75rem 1.25rem;
      border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
      font-size: 0.85rem; font-weight: 600; z-index: 100;
      display: none; align-items: center; gap: 0.5rem;
      animation: toastIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes toastIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 768px) {
      .hero-title { font-size: 1.45rem; }
      .search-input { width: 100%; }
      .filter-bar { flex-direction: column; align-items: stretch; }
      .tmpl-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <!-- 顶部导航 -->
  <header>
    <div class="nav-inner">
      <a href="../index.html" class="brand-link">
        <div class="brand-icon">道</div>
        <div>
          <div class="brand-name">
            上海初中道法教研中心
            <span class="version-badge">22套真题全覆盖</span>
          </div>
        </div>
      </a>
      <div class="nav-actions">
        <a href="daofa.html" class="nav-btn" style="color: #DC2626; background: #FEF2F2; border-color: #FECDD3; font-weight: 700;">⚖️ 道法复习中心</a>
        <a href="daofa-V7.html" class="nav-btn">🧠 知识精要自测</a>
        <a href="../history/index.html" class="nav-btn">🏛️ 历史复习中心</a>
        <a href="../index.html" class="nav-btn nav-btn-primary">🏠 返回主页</a>
      </div>
    </div>
  </header>

  <div class="main-wrap">

    <!-- 面包屑导航 -->
    <div style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; color: #64748B;">
      <a href="../index.html" style="color: #2563EB; text-decoration: none; font-weight: 600;">🏠 学习中心首页</a>
      <span>/</span>
      <a href="daofa.html" style="color: #059669; text-decoration: none; font-weight: 600;">⚖️ 初中道法中心</a>
      <span>/</span>
      <span style="color: #DC2626; font-weight: 700;">🔥 22套一模冲刺专项题库</span>
    </div>

    <!-- 冲刺横幅 -->
    <section class="sprint-hero">
      <div class="hero-top-tag">🎯 聚焦上海新中考 · 同步新课改新考法</div>
      <h1 class="hero-title">初三道德与法治 <span>一模冲刺10次课</span> 题型专项与全真题库</h1>
      <p class="hero-desc">
        结合上海教科研真题汇编、综合卷一讲评思路及各区（浦东、徐汇、黄浦、闵行、静安、虹口、宝山、松江等）一模二模真题，严格归纳“辨析四步法”、“材料四角公式”和“实践开放主体表”。22套高质量真题逐题配备标准破题链、采分点与答题工作区。
      </p>

      <div class="pillars-grid">
        <div class="pillar-card">
          <div class="pillar-icon" style="background:#EFF6FF; color:#2563EB;">📘</div>
          <div>
            <div class="pillar-title">官方讲评标准链 (材 ➔ 知)</div>
            <div class="pillar-detail">完全对标2024综合卷一与课后练习讲评1-6：明任务、判主体、构思路、定知识，直击采分关键。</div>
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-icon" style="background:#FEF2F2; color:#DC2626;">💡</div>
          <div>
            <div class="pillar-title">三大题型万能满分模板</div>
            <div class="pillar-detail">辨析题“四步定乾坤”、材料题“四角对应法”、探究题“主体对策三阶推进”，考场直接套用。</div>
          </div>
        </div>
        <div class="pillar-card">
          <div class="pillar-icon" style="background:#ECFDF5; color:#059669;">🎯</div>
          <div>
            <div class="pillar-title">22套市区全真真题</div>
            <div class="pillar-detail">涵盖脱贫攻坚、建党精神、人民城市、基层立法点、新质生产力、文物双治保护等新课标高频必考命题。</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 10次课冲刺大纲折叠盒 -->
    <section class="syllabus-box">
      <div class="syllabus-header" onclick="toggleSyllabus()">
        <div class="syllabus-title-wrap">
          <span style="font-size:1.2rem;">📋</span>
          <div class="syllabus-title">海报大纲：上海初三道法 一模冲刺10次课知识树全景</div>
          <span class="syllabus-badge">考前必通</span>
        </div>
        <div style="font-size:0.85rem; color:var(--text-muted);" id="syllabus-arrow">收起 ▲</div>
      </div>
      <div class="syllabus-timeline" id="syllabus-body">
        <div class="timeline-item">
          <div><span class="timeline-num">1</span><span class="timeline-name">六、七年级核心知识梳理</span></div>
          <span class="timeline-tag">成长的节拍·友谊的天空·师生情谊·做情绪的主人</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">2</span><span class="timeline-name">八年级上册知识点梳理</span></div>
          <span class="timeline-tag">丰富的社会生活·网络生活·社会规则·国家利益</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">3</span><span class="timeline-name">六～八上整合 + 八下法律基础</span></div>
          <span class="timeline-tag">宪法是根本法·公民基本权利义务·国家权力机关运行</span>
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
          <div><span class="timeline-num">7</span><span class="timeline-name">专项一：辨析/评析题（四步模板）</span></div>
          <span class="timeline-tag">判断定性·阐释合理·攻其破绽·升华做法</span>
        </div>
        <div class="timeline-item active-special">
          <div><span class="timeline-num">8</span><span class="timeline-name">专项二：材料分析题（四角公式）</span></div>
          <span class="timeline-tag">析材料·引金句·讲意义·扣结论</span>
        </div>
        <div class="timeline-item active-special">
          <div><span class="timeline-num">9</span><span class="timeline-name">专项三：实践探究开放题</span></div>
          <span class="timeline-tag">标语对偶式·方案三阶推进·建议对策主体表</span>
        </div>
        <div class="timeline-item">
          <div><span class="timeline-num">10</span><span class="timeline-name">综合套卷与全真模拟复盘</span></div>
          <span class="timeline-tag">综合实战演练·查漏补缺·采分点冲刺压轴</span>
        </div>
      </div>
    </section>

    <!-- 三大题型解题万能模板卡片 -->
    <section class="templates-section">
      <div class="section-head">
        <div>
          <h2 class="section-title"><span>📐</span> 三大考法万能答题模板（一键复制复习）</h2>
          <div class="section-subtitle">上海中考阅卷采分点思维模式化拆解 · 拒绝盲目罗列课本知识</div>
        </div>
      </div>

      <div class="tmpl-grid">
        <!-- 模板1: 辨析题 -->
        <div class="tmpl-card" id="tmpl-bianxi" style="border-top: 4px solid var(--red-main);">
          <div class="tmpl-header">
            <div>
              <div class="tmpl-title">专项一：辨析/评析题 “四步定乾坤”</div>
              <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">适用题型：对某人观点、争议言论进行辨析或评析</div>
            </div>
            <button class="nav-btn" onclick="copyTemplate('bianxi')">📋 复制模板</button>
          </div>
          <div class="steps-grid">
            <div class="step-box">
              <div class="step-name"><span style="color:var(--red-main)">① 判断表态</span>（1分）</div>
              <div class="step-desc">该观点是不科学的 / 片面的 / 将XX与XX对立是错误的。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--emerald-main)">② 析其合理</span>（2分）</div>
              <div class="step-desc">“XX同学看到……具有合理性。” 指出题干正确一面，调用教材原理（如科技是第一动力、法律具有强制性等）。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--amber-main)">③ 攻其破绽</span>（2分）</div>
              <div class="step-desc">“但是，认为……则是片面的/错误的。” 补充被忽视的另一面原理（如生活处处皆可创新、德治与法治不可分割等）。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--blue-main)">④ 升华做法</span>（1分）</div>
              <div class="step-desc">“因此，我们应该坚持……与……相统一，作为青少年应……” 落实到价值观与行动践行。</div>
            </div>
          </div>
        </div>

        <!-- 模板2: 材料分析题 -->
        <div class="tmpl-card" id="tmpl-cailiao" style="border-top: 4px solid var(--blue-main);">
          <div class="tmpl-header">
            <div>
              <div class="tmpl-title">专项二：材料分析题 “四角对应法”</div>
              <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">适用题型：说明材料反映的道理、阐述原因或推测理由</div>
            </div>
            <button class="nav-btn" onclick="copyTemplate('cailiao')">📋 复制模板</button>
          </div>
          <div class="steps-grid">
            <div class="step-box">
              <div class="step-name"><span style="color:var(--blue-main)">① 析材料</span>（找关键信息）</div>
              <div class="step-desc">提取时间、主体（党/政府/企业/市民）、举措（立法/投入/减税/保障）及具体数据对比。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--purple-main)">② 引金句</span>（材 ➔ 知对应）</div>
              <div class="step-desc">对应教材核心命题：党的坚强领导、以人民为中心、全过程人民民主、新质生产力、法治护航。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--emerald-main)">③ 讲意义</span>（多维阐发）</div>
              <div class="step-desc">有利于……（物质基础、社会公平、增进民生福祉、促进共同富裕、推进中国式现代化）。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--red-main)">④ 扣结论</span>（回应设问）</div>
              <div class="step-desc">“由此可见，我国/上海……为未来……提供了坚实保障 / 注入了强劲动力。”</div>
            </div>
          </div>
        </div>

        <!-- 模板3: 实践探究题 -->
        <div class="tmpl-card" id="tmpl-kaifang" style="border-top: 4px solid var(--emerald-main);">
          <div class="tmpl-header">
            <div>
              <div class="tmpl-title">专项三：实践探究开放题 “黄金三式”</div>
              <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">适用题型：拟宣传标语、提建议对策、设计活动方案</div>
            </div>
            <button class="nav-btn" onclick="copyTemplate('kaifang')">📋 复制模板</button>
          </div>
          <div class="steps-grid">
            <div class="step-box">
              <div class="step-name"><span style="color:var(--red-main)">1. 标语对偶式</span></div>
              <div class="step-desc">上句行动倡导 + 下句美好愿景（如：树立法治信仰，共建和谐社会；点燃创新火花，驱动科技强国）。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--blue-main)">2. 建议主体多元法</span></div>
              <div class="step-desc">国家/政府（科学立法/严格监管）+ 企业/社会（履行责任/营造氛围）+ 青少年个人（增强意识/自觉践行）。</div>
            </div>
            <div class="step-box">
              <div class="step-name"><span style="color:var(--emerald-main)">3. 活动方案三阶法</span></div>
              <div class="step-desc">准备阶段（制定方案/收集资料）➔ 实施阶段（专家讲座/实地调研/座谈恳谈）➔ 总结阶段（撰写报告/成果展示）。</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 题库控制过滤条 -->
    <div class="filter-bar">
      <div class="filter-pills">
        <button class="filter-pill active" onclick="filterByTag('all', this)">全部试题 (22)</button>
        <button class="filter-pill" onclick="filterByTag('official', this)">🔥 官方综合卷一 & 课后讲评 (6)</button>
        <button class="filter-pill" onclick="filterByTag('bianxi', this)">⚖️ 专项一·辨析/评析题 (6)</button>
        <button class="filter-pill" onclick="filterByTag('cailiao', this)">📊 专项二·材料分析题 (5)</button>
        <button class="filter-pill" onclick="filterByTag('kaifang', this)">🌱 专项三·实践探究开放题 (5)</button>
      </div>
      <div>
        <input type="text" id="q-search" class="search-input" placeholder="🔍 搜索试题、考点、区属..." oninput="searchQuestions()">
      </div>
    </div>

    <!-- 试题容器区 -->
    <div id="questions-container">
"""

def get_html_tail():
    return """
    </div>
  </div>

  <!-- 悬浮快捷返回主页与道法中心按钮 -->
  <div style="position: fixed; bottom: 24px; left: 24px; z-index: 45; display: flex; gap: 8px;">
    <a href="../index.html" title="返回中心主页" style="display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.55rem 0.95rem; border-radius: 999px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); border: 1.5px solid var(--border-color); color: var(--text-main); font-size: 0.85rem; font-weight: 700; text-decoration: none; box-shadow: var(--shadow-md); transition: all 0.2s;">
      <span>🏠</span>
      <span>返回主页</span>
    </a>
    <a href="daofa.html" title="返回道法中心" style="display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.55rem 0.95rem; border-radius: 999px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); border: 1.5px solid #FECDD3; color: #DC2626; font-size: 0.85rem; font-weight: 700; text-decoration: none; box-shadow: var(--shadow-md); transition: all 0.2s;">
      <span>⚖️</span>
      <span>道法中心</span>
    </a>
  </div>

  <!-- 提示弹窗 -->
  <div class="toast" id="toast-msg">✅ 答题模板已成功复制到剪贴板！可以直接粘贴复习！</div>

  <footer>
    <div style="margin-bottom: 0.85rem; display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap;">
      <a href="../index.html" style="display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.9rem; border-radius: 999px; background: white; border: 1px solid #CBD5E1; color: #1E293B; font-size: 0.82rem; font-weight: 700; text-decoration: none;">🏠 返回学习中心主页</a>
      <a href="daofa.html" style="display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.9rem; border-radius: 999px; background: #FEF2F2; border: 1px solid #FECDD3; color: #DC2626; font-size: 0.82rem; font-weight: 700; text-decoration: none;">⚖️ 返回道法复习中心</a>
      <a href="../history/index.html" style="display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.9rem; border-radius: 999px; background: #FFFBEB; border: 1px solid #FDE68A; color: #B45309; font-size: 0.82rem; font-weight: 700; text-decoration: none;">🏛️ 历史复习中心</a>
    </div>
    <p>© 2026 Owen Learning Center · 上海初中道法教学研发中心</p>
    <p style="margin-top: 0.4rem; font-size: 0.8rem;">严格对标上海新课改中考与区一模/二模真题 · 结构化采分点 · 拒绝死记硬背</p>
  </footer>

  <script>
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

    function updateWordCount(textarea) {
      const len = textarea.value.trim().length;
      const counter = textarea.parentElement.querySelector('.wc-num');
      if (counter) counter.textContent = len;
    }

    function copyTemplate(type) {
      let text = '';
      if (type === 'bianxi') {
        text = `【上海初三道法·辨析评析题 四步定乾坤满分模板】\\n1. 判断定性：该观点是不科学的/片面的/把XX与XX割裂开来是错误的。\\n2. 阐释合理：该观点看到……具有合理性。因为【对应教材金句/理论】……\\n3. 攻其破绽：但是，该观点忽视了/否定了……因为【补充教材原理】……如果……会导致……\\n4. 总结升华：因此，我们应该坚持……与……相统一，青少年要在实践中做到……`;
      } else if (type === 'cailiao') {
        text = `【上海初三道法·材料分析题 四角对应法黄金公式】\\n1. 析材料：材料中提到……反映了我国/上海在……方面的成效；\\n2. 引金句：这体现了/贯彻了【党的领导/高质量发展/以人民为中心/全过程人民民主】；\\n3. 讲意义：这有利于保障……有利于推动……有利于推进中国式现代化；\\n4. 扣结论：因此，这充分彰显了……的生动实践。`;
      } else if (type === 'kaifang') {
        text = `【上海初三道法·实践探究开放题 黄金公式】\\n- 标语对偶句：主题核心 + 行动倡导（如：树立法治信仰，共建和谐社会）\\n- 建议主体法：\\n  ① 国家/政府：完善法规，严格执法监督，出台激励政策；\\n  ② 社会/企业/学校：营造良好氛围，履行社会责任；\\n  ③ 青少年个人：提高思想认识，自觉践行，从身边小事做起。\\n- 方案三步骤：准备阶段（方案/调研） ➔ 实施阶段（宣讲/座谈） ➔ 总结阶段（报告/表彰）`;
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

def generate_questions():
    questions = []

    # ==================== MODULE A: 官方综合卷一 & 课后讲评核心真题 (6题) ====================

    # Q1: 综合卷一原卷·脱贫攻坚成果巩固与乡村振兴推测理由
    questions.append({
        "id": "q-1",
        "tag": "official cailiao",
        "meta_tags": [
            ("🔥 2024上海初三综合卷一原卷", "tag-red"),
            ("专项② 材料分析题", "tag-blue"),
            ("乡村振兴与民生福祉", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★★☆",
        "material": """<b>【真实原卷情境材料】</b><br>
图1显示新时代以来我国国内生产总值持续跃升，国家财政综合实力不断迈上新台阶；图2显示贫困地区脱贫人口人均纯收入年均增长超12%，农村基础设施持续改善；近年来，国家颁布实施《中华人民共和国乡村振兴促进法》，各地大力发展现代特色农业、农村电商与网络直播带货，助力农产品出山入海。""",
        "stem": "【设问】：由此，同学们推测未来我国一定能够巩固和拓展脱贫攻坚成果。请结合上述材料，综合运用所学内容，说明同学们提出推测的理由。（6分）",
        "chain": [
            "过去成效 ➔ 经济实力大幅提升提供坚实物质保障",
            "政治引领 ➔ 党坚持以人民为中心 + 深入推进乡村振兴",
            "法治护航 ➔ 科学制定《乡村振兴促进法》提供法律保障",
            "科技赋能 ➔ 数字化与电商新业态变革生产生活方式"
        ],
        "draft_tip": "按照官方讲评“材 ➔ 知”四维匹配法：物质基础 + 党的领导/民生 + 法治保障 + 科技赋能",
        "rubric": """<b>【官方讲评思路与采分细则】</b>（满分6分，答出任意4点得满分）：<br>
① <b>物质基础角度（1.5分）</b>：过去我国经济实力大幅跃升、发展质量显著提升，为未来巩固和拓展脱贫成果提供了坚实的经济基础和物质保障；<br>
② <b>党的领导与宗旨角度（1.5分）</b>：中国共产党坚持以人民为中心的发展思想，站稳人民立场，深入实施乡村振兴战略，促进区域与城乡协调发展，扎实推进共同富裕；<br>
③ <b>法治保障角度（1.5分）</b>：国家坚持科学立法，制定并实施《乡村振兴促进法》，为全面推进乡村振兴、巩固脱贫成果提供了坚强有力的法治保障；<br>
④ <b>科技与社会支撑角度（1.5分）</b>：互联网与现代科技推动生产生活方式变革，农村电商与直播助农拓宽了农民增收渠道，切实改善民生福祉。""",
        "model_ans": """<p>同学们提出这一推测具有充分的现实与理论依据：</p>
<p><b>① 坚实的物质保障</b>：我国经济持续健康发展，综合国力大幅跃升，为未来持续推进农业农村现代化、巩固脱贫成果提供了充足的物质条件与财力支持。</p>
<p><b>② 党的坚强领导与人民立场</b>：中国共产党坚持立党为公、执政为民，始终坚持以人民为中心的发展思想。深入实施乡村振兴战略，促进区域协调发展，让全体人民共享改革发展成果。</p>
<p><b>③ 完备的法治护航</b>：国家颁布施行《乡村振兴促进法》，坚持全面依法治国，为脱贫攻坚成果同乡村振兴有效衔接提供了坚实有力的法律保障。</p>
<p><b>④ 数字化与科技赋能</b>：网络与数字化转型深度赋能乡村特色产业，直播带货等新业态激发了农村内生发展动力，促进了农业提质增效与农民增收致富。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：切忌只空洞复述“我国一定能成功”，必须严格做到材料与考点一一对应（经济、党/民生、法治、科技四维缺一不可）。"
    })

    # Q2: 综合卷一原卷·伟大建党精神与学校课内学习辨析
    questions.append({
        "id": "q-2",
        "tag": "official bianxi",
        "meta_tags": [
            ("🔥 2024上海初三综合卷一原卷", "tag-red"),
            ("专项① 辨析评析题", "tag-amber"),
            ("伟大建党精神 · 学习观", "tag-purple")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【真实原卷情境材料】</b><br>
学校组织初三年级开展“寻访红色足迹·传承建党精神”综合社会研学活动。个别同学认为：“学习只是在学校里听课刷题，初中生只要把课内文化课分数搞上去就行了，花时间去参加红色研学、宣讲建党精神纯属形式主义，对我们中考升学没有任何实质作用。”""",
        "stem": "【设问】：请运用六至九年级相关知识，对该同学的观点进行评析。（6分）",
        "chain": [
            "定性判断 ➔ 观点错误（狭隘割裂学习与德育实践）",
            "理由1(六上学习观) ➔ 学习不局限于课内，实践感悟更重要",
            "理由2(九上建党精神) ➔ 精神之源+精神谱系，提供强大精神动力",
            "价值升华 ➔ 课内学业与红色研学相辅相成，知行合一"
        ],
        "draft_tip": "辨析四步：定性判断 ➔ 理由1（六上学习认知） ➔ 理由2（九上建党精神价值） ➔ 回应与行动",
        "rubric": """<b>【官方讲评思路与采分细则】</b>（满分6分）：<br>
① <b>判断定性（1分）</b>：该同学的观点是不对的（片面的）。<br>
② <b>理由一（学习观维度，2分）</b>：中学阶段的学习不局限于学校课本知识的传授，不仅表现为接受和掌握，而且表现为探究、发现、体验和感悟。参加社会实践与红色研学是重要的学习途径，有利于开阔眼界、磨砺意志、提升综合素养。<br>
③ <b>理由二（建党精神维度，2分）</b>：伟大建党精神是中国共产党的精神之源，构建了中国共产党人的精神谱系。弘扬伟大建党精神能够为青少年的健康成长和民族复兴大任提供强大的精神动力，绝非形式主义。<br>
④ <b>回应与升华（1分）</b>：我们初中生既要努力学好课内科学文化知识，又要积极参与红色实践活动，传承红色基因，努力成长为担当民族复兴大任的时代新人。""",
        "model_ans": """<p><b>该同学的观点是不正确的。</b></p>
<p>（1）<b>从学习的角度看</b>：初中阶段的学习不局限于学校课堂内的书本知识，不仅表现为接受和掌握，而且表现为探究、发现、体验和感悟。走出校门参与红色研学是拓展认知边界、提升社会实践能力和综合素养的重要途径。</p>
<p>（2）<b>从建党精神的角度看</b>：伟大建党精神是中国共产党的精神之源，构筑起中国共产党人的精神谱系。传承红色基因绝非形式主义，它能帮助中学生树立崇高理想信念、磨砺坚韧意志，为青少年的健康成长与学业进步提供源源不断的精神动力。</p>
<p>（3）<b>因此</b>，我们中学生既要脚踏实地学好课堂文化知识，又要积极走出校园，投身红色寻访与社会大课堂，做到知行合一，争做德智体美劳全面发展的时代新人。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：若未调用六上“学习不仅局限于课内”这一跨学段考点，将直接损失2分。"
    })

    # Q3: 综合卷一原卷·月考失利、竞争友谊与情绪管理
    questions.append({
        "id": "q-3",
        "tag": "official kaifang",
        "meta_tags": [
            ("🔥 2024上海初三综合卷一原卷", "tag-red"),
            ("专项③ 实践探究与生活情境", "tag-emerald"),
            ("情绪调节 · 呵护友谊", "tag-blue")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【真实生活情境】</b><br>
九年级月考成绩揭晓后，好友小陈因几门科目成绩下滑而情绪低落，甚至因为同桌小李在本次考试中名列前茅而心生嫉妒、冷眼相待，两人陷入冷战。小陈在日记中写道：“竞争太残酷了，既然有了竞争，朋友之间就不可能再有真正的友谊，我控制不住自己的沮丧与烦躁。”""",
        "stem": "【设问】：请运用七年级《情绪的管理》与八年级《友谊的天空》相关知识，给小陈提出合理化建议，帮助他走出心理困境。（6分）",
        "chain": [
            "友谊认知 ➔ 竞争并不必然伤害友谊，要坦然欣赏对手并反思",
            "情绪调控 ➔ 运用改变认知评价、转移注意等做情绪的主人",
            "行动举措 ➔ 主动沟通破冰，互帮互学实现共同进步"
        ],
        "draft_tip": "建议类设问双角度覆盖：友谊维度（对待竞争的态度） + 情绪维度（科学调节方法与具体行动）",
        "rubric": """<b>【官方讲评思路与采分细则】</b>（满分6分）：<br>
① <b>竞争与友谊认知（2分）</b>：竞争并不必然伤害友谊，关键是我们对待竞争的态度。在竞争中能坦然接受并欣赏朋友的成就，做到自我反思；在合作中竞争，在竞争中合作。<br>
② <b>情绪调节方法（2分）</b>：学会合理调节情绪，运用改变认知评价、转移注意、合理宣泄或放松训练等方法，敞开心扉，在合适场合关照他人，做情绪的主人。<br>
③ <b>具体行动建议（2分）</b>：主动找同桌沟通交流化解误会，反思自身学习中的薄弱环节，虚心请教学习方法，在互帮互助中共同进步，成为更好的自己。""",
        "model_ans": """<p>我给小陈提出以下三点建议：</p>
<p><b>① 正确认识竞争与友谊</b>：竞争并不必然伤害友谊，关键是我们对待竞争的态度。同桌的优秀正是自己学习的榜样，应学会真诚欣赏朋友的成就，在合作中竞争、在竞争中合作。</p>
<p><b>② 掌握调节情绪的科学方法</b>：学会做情绪的主人。可以运用“改变认知评价”调整心态，化嫉妒为动力；也可通过运动、听音乐等“转移注意”和“合理宣泄”，疏解负面情绪。</p>
<p><b>③ 主动沟通破冰与反思提升</b>：找合适时机主动与同桌敞开心扉交流，坦诚化解误会；同时认真反思自己月考失利的具体知识漏洞，虚心向同桌请教高效复习方法，互帮互助、携手并进。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：若只提生活鸡汤建议而未写出教材术语（如“改变认知评价”、“转移注意”、“在合作中竞争”），最高只能得3分。"
    })

    # Q4: 讲评资料4·2025上海民生改善原因图表分析
    questions.append({
        "id": "q-4",
        "tag": "official cailiao",
        "meta_tags": [
            ("🔥 九上课后练习讲评资料4", "tag-red"),
            ("专项② 材料分析题", "tag-blue"),
            ("坚持以人民为中心 · 人民城市", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★★☆",
        "material": """<b>【上海本地图表与事实材料】</b><br>
<b>材料一</b>：2025年上海全市生产总值（GDP）达到57608亿元，经济增速持续高于全国平均水平，经济结构持续优化升级。<br>
<b>材料二</b>：上海市委、市政府出台多项民心工程，居民人均可支配收入稳步增长；新增普惠性养老床位5000张，新建社区长者食堂100家；加装电梯突破3000台，老旧小区改造稳步推进。""",
        "stem": "【设问】：请结合上述材料，综合运用九年级上册知识，深入分析上海民生福祉持续改善的原因。（6分）",
        "chain": [
            "政治核心 ➔ 党坚持在发展中改善民生，全心全意为人民服务",
            "物质基础 ➔ 上海GDP持续跃升，为民生举措提供坚实财力支撑",
            "宗旨目的 ➔ 上海政府以人民为中心，将增进民生福祉作为发展根本目的"
        ],
        "draft_tip": "官方讲评三维角度：党（领导核心/为人民服务） + 经济（GDP增速提供物质基础） + 民生（以人民为中心/政府举措）",
        "rubric": """<b>【官方讲评思路与采分细则】</b>（满分6分，三角度各2分）：<br>
① <b>党的领导核心角度（2分）</b>：中国共产党坚持在发展中保障和改善民生。中国共产党是中国特色社会主义事业的坚强领导核心，始终坚持立党为公、执政为民，站稳人民立场，全心全意为人民服务；<br>
② <b>经济物质基础角度（2分）</b>：上海经济持续健康快速发展，综合实力和财政收入大幅提升，为各项民生改善举措的落实落地提供了雄厚的经济基础和物质保障；<br>
③ <b>政府与民生宗旨角度（2分）</b>：上海市政府坚持以人民为中心的发展思想，打造服务型政府，不断完善社会保障体系，将增进民生福祉作为发展的根本目的，切实解决人民群众急难愁盼问题。""",
        "model_ans": """<p>上海民生福祉持续改善的深层原因在于：</p>
<p><b>（1）中国共产党的坚强领导与根本宗旨</b>：中国共产党始终坚持以人民为中心，把为人民谋幸福作为初心使命。党始终坚持在发展中保障和改善民生，站稳人民立场，全心全意为人民服务。</p>
<p><b>（2）健康快速发展的经济提供了坚实物质基础</b>：上海2025年GDP突破5.7万亿元且保持高质量增长，综合经济实力的持续跃升为增加养老床位、社区食堂和旧区改造等民生工程提供了充裕的财政资金与物质支撑。</p>
<p><b>（3）上海政府坚持以人民为中心、建设服务型政府</b>：上海市委、市政府深入践行“人民城市人民建，人民城市为人民”重要理念，将增进民生福祉作为发展的根本目的，不断完善多层次社会保障体系，让现代化建设成果更多更公平惠及全体市民。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：很多同学漏答“经济基础”，直接谈民生政策，导致材料一GDP数据未被利用而失掉2分。"
    })

    # Q5: 讲评资料2·GDP跃升与研发经费（R&D）上升双图关系论证
    questions.append({
        "id": "q-5",
        "tag": "official cailiao",
        "meta_tags": [
            ("🔥 九上课后练习讲评资料2", "tag-red"),
            ("专项② 图表关系题", "tag-blue"),
            ("经济高质量发展 · 创新驱动", "tag-amber")
        ],
        "score_diff": "满分：6分 | 难度：★★★★☆",
        "material": """<b>【图表材料】</b><br>
<b>图1</b>：2022-2024年我国国内生产总值（GDP）稳步攀升，从120万亿元持续迈向高台阶。<br>
<b>图2</b>：2013-2021年我国研究与试验发展（R&D）经费支出持续走高，占GDP比重持续突破新高。""",
        "stem": "【设问】：（1）请根据图1、图2分别得出结论。（2分）<br>（2）请运用所学知识，阐明图1与图2所反映现象之间的内在辩证关系。（4分）",
        "chain": [
            "图1结论 ➔ 新时代以来我国经济持续健康发展，综合国力大幅提升",
            "图2结论 ➔ 我国深入实施创新驱动发展战略，创新活力持续激发",
            "图1 ➔ 图2 ➔ 经济持续健康发展为激发创新活力提供雄厚经济物质基础",
            "图2 ➔ 图1 ➔ 科技创新能力提升促进国家经济更快更好高质量发展"
        ],
        "draft_tip": "图表关系题标准范式：分别得结论 + 双向双箭头阐述内在相互作用",
        "rubric": """<b>【官方讲评思路与采分细则】</b>（满分6分）：<br>
① <b>图1结论（1分）</b>：新时代以来，我国经济持续健康发展，综合国力大幅跃升，发展质量持续提升；<br>
② <b>图2结论（1分）</b>：我国深入实施创新驱动发展战略，基础研究与原始创新不断加强，全社会创新活力不断激发；<br>
③ <b>关系论证 图1 ➔ 图2（2分）</b>：我国经济的持续健康发展和综合国力增强，为国家持续加大研发经费投入、激发创新活力提供了坚实的经济基础和物质保障；<br>
④ <b>关系论证 图2 ➔ 图1（2分）</b>：我国自主创新能力的持续提升和科技成果的转化应用，为转变经济发展方式、推动经济高质量发展注入了强劲新动能。""",
        "model_ans": """<p><b>（1）图表结论：</b><br>
<b>图1结论</b>：新时代以来，我国经济持续健康发展，综合实力大幅上升。<br>
<b>图2结论</b>：我国深入实施创新驱动发展战略，基础研究与原始创新不断加强，创新活力不断激发。</p>
<p><b>（2）内在辩证关系：</b><br>
① <b>图1 ➔ 图2（经济为创新筑基）</b>：我国经济的持续健康发展和财政实力的壮大，为科技研发提供了雄厚的物质基础和充足的资金保障。<br>
② <b>图2 ➔ 图1（创新促经济腾飞）</b>：科技是第一生产力，创新是引领发展的第一动力。自主创新能力的持续跃升加快培育新质生产力，有力推动我国经济实现质量更高、韧性更强的高质量发展。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：关系阐述切忌只写单向“经济好所以科技好”，必须做到双向闭环互促论证。"
    })

    # Q6: 讲评资料6·西夏陵申遗成功后文化遗产保护与文创传承对策表
    questions.append({
        "id": "q-6",
        "tag": "official kaifang",
        "meta_tags": [
            ("🔥 九上课后练习讲评资料6", "tag-red"),
            ("专项③ 实践探究与主体对策", "tag-emerald"),
            ("坚定文化自信 · 法治与德治双轨", "tag-purple")
        ],
        "score_diff": "满分：8分 | 难度：★★★★★",
        "material": """<b>【真实文化遗产保护背景】</b><br>
2024年，我国多项重要历史文化遗存申遗取得重大突破（如西夏陵等项目申报世界文化遗产）。但在文化遗产活化保护中，也面临部分游客不文明乱刻乱画、部分历史文物缺乏专业修缮与数字保护手段、部分年轻人对传统历史文化认知淡漠等现实挑战。""",
        "stem": "【设问】：请结合所学《道德与法治》知识，从“法治”与“德治”相结合的视角，分别从“国家”和“公民”两个主体维度，为更好守护文化遗产、让传统文化焕发生机提出具体建议。（8分）",
        "chain": [
            "国家法治 ➔ 科学立法出台遗产保护法规 + 公安司法严格执法加大违法处罚",
            "国家德治 ➔ 融媒体弘扬优秀传统文化 + 营造全社会保护文物的浓厚舆论氛围",
            "公民法治 ➔ 全民守法遵规 + 增强法律红线意识，主动监督举报违法行为",
            "公民德治 ➔ 坚定文化自信 + 参与志愿服务 + 开展文创制作赋能创新性发展"
        ],
        "draft_tip": "建议类 2×2 矩阵式答题：国家(法治+德治) + 公民(法治+德治)，主体明晰！",
        "rubric": """<b>【官方讲评思路与采分细则】</b>（满分8分，四维度各2分）：<br>
① <b>国家·法治角度（2分）</b>：国家立法机关完善文化遗产保护政策法规，做到科学立法；行政执法与公安部门加强巡查监管，严厉打击盗掘破坏文物行为，严格执法；<br>
② <b>国家·德治角度（2分）</b>：通过主流媒体与网络平台加大传统文化宣传普及力度，深化学校传统美德与历史教育，增强全民文化保护意识，筑牢道德底线；<br>
③ <b>公民·法治角度（2分）</b>：自觉学习文物保护相关法律法规，做到尊法学法守法用法；在参观游览中文明守规，发现破坏文物的违法行为积极制止并向有关部门举报；<br>
④ <b>公民·德治角度（2分）</b>：坚定文化自信，积极学习传承非遗技艺与民俗知识；踊跃参与文化保护志愿活动，利用网络平台传播正能量，设计国潮文创产品，推动中华优秀传统文化创造性转化、创新性发展。""",
        "model_ans": """<p>针对文化遗产的保护与活化传承，我提出以下建议：</p>
<p><b>【国家角度】：</b><br>
<b>① 法治保障</b>：国家立法机关要制定和完善文化遗产保护的法律法规，实现科学立法；公安与文物行政监管部门要严格执法，加大对破坏损毁文物的巡查与处罚力度，坚决筑牢法治底线。<br>
<b>② 德治引领</b>：国家要广泛利用新媒体与公益宣传，加强对文化遗产时代价值的挖掘与传播；将传统文化教育融入大中小学德育课堂，引导全社会形成尊崇历史、爱护文物的浓厚氛围。</p>
<p><b>【公民角度】：</b><br>
<b>① 遵法守法</b>：广大青少年和公民要树立法治观念，严格遵守文物保护法律规章与景区文明公约；增强法律监督意识，勇于劝阻并积极举报破坏文化遗产的违法行为。<br>
<b>② 道德践行与文化创新</b>：坚定文化自信，积极学习并亲身体验中华优秀传统文化；参与文物保护志愿宣讲行动；借助数字化创意制作短视频、文创手作，推动传统文化“创造性转化、创新性发展”。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：若未将“法治”与“德治”双轨区分，仅泛泛罗列“保护文物”，将被扣除一半分数。"
    })

    # ==================== MODULE B: 专项一 · 辨析/评析题“四步定乾坤”（6题） ====================

    # Q7: 2024徐汇一模真题·新质生产力与青少年科技创新辨析
    questions.append({
        "id": "q-7",
        "tag": "bianxi",
        "meta_tags": [
            ("2024徐汇一模真题", "tag-blue"),
            ("专项① 辨析评析题", "tag-red"),
            ("新质生产力 · 创新驱动", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
在探讨国家加快培育“新质生产力”的主题班会上，小张同学说：“新质生产力都是人工智能、量子科技、航空航天等高精尖领域，主要依靠科学家攻坚和领军企业研发。我们初中生现在唯一的任务就是抓紧刷题考高分，搞创新发明离我们太遥远，我们想搞也搞不了，与我们毫无关系。”""",
        "stem": "【设问】：请运用九年级上册第二单元《创新驱动发展》相关知识，对小张同学的观点进行评析。（6分）",
        "chain": [
            "判断表态 ➔ 小张的观点是片面的",
            "阐释合理 ➔ 看到发展新质生产力需要国家与高尖人才攻关是正确的",
            "攻其破绽 ➔ 忽视了生活处处有创新，人人皆可创新，课内学习与创新相辅相成",
            "升华做法 ➔ 青少年应打牢文化基础，敢于质疑探索，争做未来创新人才"
        ],
        "draft_tip": "四步答题：判断定性 ➔ 析其合理（科技是第一生产力） ➔ 析其片面（人人皆可创新） ➔ 升华做法",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
① <b>判断表态（1分）</b>：指出小张同学的观点是片面的（或割裂了国家攻关与青少年创新的联系）；<br>
② <b>合理性分析（2分）</b>：小张认识到新质生产力需要高精尖人才和领军企业攻关具有合理性。创新是引领发展的第一动力，科技自立自强是国家强盛之基，推进关键核心技术攻坚确实需要集中力量办大事，依赖拔尖科学家和领航企业；<br>
③ <b>片面性分析（2分）</b>：但是他认为“搞创新与初中生无关、中学生搞不了”是错误的。因为生活处处有创新，创新不只是少数科学家的专利，人人皆可创新；中学生努力学好文化知识与培养创新思维并不对立；<br>
④ <b>升华做法（1分）</b>：青少年既要刻苦打牢学科学文化基础，又要保持好奇心与批判性思维，积极参加科技小发明小制作，争做新时代的创新型人才。""",
        "model_ans": """<p><b>小张同学的观点是片面的。</b></p>
<p>（1）<b>小张看到科技攻关需要国家与科学家主导具有合理性</b>。因为创新是引领发展的第一动力，是推动高质量发展的核心要素。培育新质生产力、实现关键核心技术自主可控，确实需要国家统筹布局，发挥高精尖人才和领航企业的战略科技先锋作用。</p>
<p>（2）<b>但是，小张认为“创新与初中生无关且初中生搞不了”是错误的</b>。因为生活处处有创新，创新不仅属于实验室，更属于每一个善于发现的人；人人皆可创新，创新可以从日常小发明、小革新做起。初中生努力学习文化课是创新的基石，但绝不能把学习局限于死记硬背。</p>
<p>（3）<b>因此</b>，我们青少年既要刻苦钻研科学文化知识，又要敢于质疑批判，积极参与青少年科技创新大赛等实践活动，在日常探索中点燃创新火花，成长为强国建设所需的栋梁之材。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：如果全盘否定小张，判“该观点错误”，未肯定其看到“国家高精尖攻关”合理点，会被扣除1-2分。"
    })

    # Q8: 2024黄浦一模真题·坚持党的全面领导与全面依法治国关系辨析
    questions.append({
        "id": "q-8",
        "tag": "bianxi",
        "meta_tags": [
            ("2024黄浦一模真题", "tag-blue"),
            ("专项① 辨析评析题", "tag-red"),
            ("坚持党的领导 · 法治中国", "tag-purple")
        ],
        "score_diff": "满分：6分 | 难度：★★★★☆",
        "material": """<b>【情境材料】</b><br>
在“法治中国建设”的主题讨论中，小周同学提出：“既然我国要坚持全面依法治国，宪法法律具有至高无上的权威，任何组织和个人都必须在宪法和法律范围内活动，那么强调‘坚持中国共产党的全面领导’就与‘全面依法治国’相互矛盾，两者只能二选一。”""",
        "stem": "【设问】：请运用九年级上册“坚持党的全面领导”和“建设法治中国”的相关知识，对小周同学的观点进行辨析。（6分）",
        "chain": [
            "判断表态 ➔ 观点错误（割裂了党的领导与依法治国的辩证统一）",
            "阐释法治 ➔ 宪法法律至上，党自身严格在宪法法律范围内活动",
            "阐释党导 ➔ 党的领导是全面依法治国的根本保证，法由党领导人民制定",
            "三者统一 ➔ 必须坚持党的领导、人民当家作主、依法治国有机统一"
        ],
        "draft_tip": "抓住根本命题：党的领导是全面依法治国的根本保证，宪法是党的主张和人民意愿的统一",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
① <b>判断定性（1分）</b>：小周的观点是错误的（割裂了党的全面领导与全面依法治国的内在统一性）；<br>
② <b>论证一（党的领导与法治的关系，2分）</b>：党的领导是全面依法治国的根本保证。中国特色社会主义法治道路最本质的特征就是坚持中国共产党的领导；<br>
③ <b>论证二（党与宪法法律的关系，2分）</b>：宪法和法律是党的主张和人民意愿的高度统一。中国共产党领导人民制定宪法法律，领导人民实施宪法法律，党自身必须在宪法和法律范围内活动，两者不仅不矛盾，而且相辅相成；<br>
④ <b>总结升华（1分）</b>：建设社会主义法治国家，必须坚持党的领导、人民当家作主、依法治国有机统一，绝不能把党的领导与依法治国割裂或对立起来。""",
        "model_ans": """<p><b>小周同学的观点是错误的。</b></p>
<p>（1）<b>党的领导是全面依法治国的根本保证</b>。中国特色社会主义最本质的特征是中国共产党领导，中国特色社会主义制度的最大优势是中国共产党领导。只有坚持党的领导，全面依法治国才有坚强政治保障与正确政治方向。</p>
<p>（2）<b>宪法和法律是党的主张和人民意志的高度统一</b>。党领导人民制定宪法法律，又领导人民实施宪法法律；同时，党自身必须带头尊崇法治、在宪法和法律范围内活动。这充分证明坚持党的领导与坚持宪法法律至上是有机统一的，绝非相互对立。</p>
<p>（3）<b>因此</b>，推进全面依法治国，必须坚持党的领导、人民当家作主、依法治国有机统一。把两者割裂开来甚至对立起来的观点在理论上是错误的，在实践中是有害的。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：必须准确说出“党的领导是全面依法治国的根本保证”以及“三者有机统一”的课本标准金句。"
    })

    # Q9: 2024闵行一模真题·未成年人网络保护立法辨析题
    questions.append({
        "id": "q-9",
        "tag": "bianxi",
        "meta_tags": [
            ("2024闵行一模真题", "tag-blue"),
            ("专项① 辨析评析题", "tag-red"),
            ("网络法治 · 未成年人保护", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
国务院颁布施行《未成年人网络保护条例》后，班级开展专题交流。小林同学兴奋地说：“有了国家专门出台的这部法宝，未成年人沉迷网络游戏、遭遇网络欺凌和电信网络诈骗的问题就一定能够彻底彻底解决了，我们自己不需要操心了。”""",
        "stem": "【设问】：请运用八年级和九年级法治中国建设相关知识，对小林同学的看法进行辨析。（6分）",
        "chain": [
            "判断表态 ➔ 观点是片面的",
            "阐释合理 ➔ 肯定出台条例是科学立法的重大成果，提供坚实法律依据",
            "攻其破绽 ➔ 全面依法治国不仅靠立法，还需要严格执法、司法、社会多方保护与自律",
            "升华做法 ➔ 筑牢六大保护屏障，未成年人自身提高网络素养与法治观念"
        ],
        "draft_tip": "法治系统性思维：科学立法 + 严格执法 + 公正司法 + 全民守法 + 六大保护协同",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
① <b>判断定性（1分）</b>：小林的观点是片面的；<br>
② <b>肯定合理性（2分）</b>：小林看到专门立法的重大作用是正确的。法律是由国家制定并由国家强制力保证实施的行为规范，出台《未成年人网络保护条例》体现了科学立法，使未成年人网络权益保护有法可依，为净化网络空间提供了坚强的法治保障；<br>
③ <b>指出片面性（2分）</b>：认为“仅靠一部法律就能彻底解决、自己无需操心”是错误的。全面依法治国需要科学立法、严格执法、公正司法、全民守法齐头并进；保障网络健康还需要家庭、学校、社会、网络、政府、司法六大保护协同发力；<br>
④ <b>青少年做法（1分）</b>：未成年人自身要提高网络素养和法治观念，增强防范意识，自觉抵制不良诱惑，合理文明利用网络。""",
        "model_ans": """<p><b>小林同学的观点是片面的。</b></p>
<p>（1）<b>小林认识到专门立法的巨大价值具有合理性</b>。因为法律是治理现代社会的有力武器。出台《未成年人网络保护条例》推进了科学立法，使保护未成年人网络合法权益有法可依，筑牢了网络空间法治屏障。</p>
<p>（2）<b>但是，小林认为“只要有了法律就能彻底解决且个人无需操心”是错误的</b>。法律的生命在于实施。全面依法治国需要严格执法、公正司法与全民守法共同推进。解决网络沉迷等顽疾，必须依靠家庭、学校、社会、网络、政府和司法六大保护体系协同联动。</p>
<p>（3）<b>因此</b>，解决网络问题不仅需要法律护航，更需要青少年自身提高网络媒介素养，树立规则与法治意识，学会信息节食，做健康文明上网的小主人。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：遗漏“青少年自身提高素养与自律”角度往往会被扣除1分。"
    })

    # Q10: 2024浦东一模真题·共同富裕与平均主义辨析
    questions.append({
        "id": "q-10",
        "tag": "bianxi",
        "meta_tags": [
            ("2024浦东一模真题", "tag-blue"),
            ("专项① 辨析评析题", "tag-red"),
            ("共同富裕 · 中国式现代化", "tag-amber")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
在学习“中国式现代化是全体人民共同富裕的现代化”内容时，小赵同学认为：“既然党和国家强调实现共同富裕，那就是要消除社会上所有人的一切收入差距，让大家拿同样的工资、享同样的待遇，实现同步同时富裕。”""",
        "stem": "【设问】：请运用所学九年级《道德与法治》知识，对小赵同学的观点进行评析。（6分）",
        "chain": [
            "判断表态 ➔ 观点错误（混淆了共同富裕与平均主义的本质区别）",
            "阐释本旨 ➔ 共同富裕是中国特色社会主义的本质要求，要缩小差距而非平均主义",
            "攻其破绽 ➔ 共同富裕不是同步同时富裕，允许一部分人先富带动后富",
            "总结升华 ➔ 扎实推进共同富裕，坚持按劳分配为主体、兼顾效率与公平"
        ],
        "draft_tip": "辨析核心概念：共同富裕 ≠ 同步富裕 ≠ 平均主义，是渐进的过程",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
① <b>判断定性（1分）</b>：小赵同学的观点是错误的（混淆了共同富裕与同步富裕、平均主义）；<br>
② <b>阐释本质（2分）</b>：共同富裕是中国特色社会主义的本质要求，也是中国式现代化的重要特征。党和国家致力于保障和改善民生、缩小贫富差距、促进社会公平正义，但共同富裕绝不是搞吃大锅饭和平均主义；<br>
③ <b>阐明特征（2分）</b>：共同富裕不是同时富裕、同步富裕、同等富裕。我国坚持按劳分配为主体、多种分配方式并存，鼓励辛勤劳动、合法经营，允许并鼓励一部分人、一部分地区先富起来，先富带后富，最终逐步达到共同富裕；<br>
④ <b>升华结论（1分）</b>：共同富裕是一个长期的历史过程，需要全体人民通过辛勤奋斗逐步实现。""",
        "model_ans": """<p><b>小赵同学的观点是错误的。</b></p>
<p>（1）<b>共同富裕是中国特色社会主义的本质要求，也是中国式现代化的重要特征</b>。党和国家坚持以人民为中心的发展思想，着力解决发展不平衡不充分问题，努力缩小城乡区域差距，促进社会公平正义。</p>
<p>（2）<b>但是，共同富裕绝不等于平均主义，更不是同步富裕、同等富裕</b>。平均主义会扼杀社会劳动生产积极性。我国实行按劳分配为主体、多种分配方式并存的社会主义基本分配制度，鼓励勤劳致富、创新致富，允许一部分人、一部分地区先富起来，通过先富帮后富，逐步走向共同富裕。</p>
<p>（3）<b>因此</b>，共同富裕是一个分阶段逐步实现的渐进过程，必须把搞好经济“做大蛋糕”与推进公平“分好蛋糕”统一起来，依靠全体人民共同奋斗来实现。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：必须准确阐明“共同富裕不是同时富裕、同等富裕、平均主义”三个“不是”。"
    })

    # Q11: 2024静安一模真题·经济发展与生态环保对立辨析
    questions.append({
        "id": "q-11",
        "tag": "bianxi",
        "meta_tags": [
            ("2024静安一模真题", "tag-blue"),
            ("专项① 辨析评析题", "tag-red"),
            ("两山理念 · 绿色发展", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
在生态文明建设座谈中，某企业负责人表示：“经济发展与生态环境保护就像鱼和熊掌不可兼得。抓生态环保就必然会增加治理成本、压缩利润空间、拉低经济增速。要想守护绿水青山，就必须牺牲金山银山。”""",
        "stem": "【设问】：请运用九年级上册“建设美丽中国”相关知识，对该负责人的言论进行评析。（6分）",
        "chain": [
            "判断表态 ➔ 该负责人的言论是不正确的（割裂了保护与发展的辩证统一）",
            "阐释两山 ➔ 保护生态就是保护生产力，改善生态就是发展生产力",
            "攻其破绽 ➔ 绿水青山和金山银山绝非不可兼得，绿色转型赋能高质量发展",
            "升华做法 ➔ 坚持生态优先、绿色低碳的高质量发展道路"
        ],
        "draft_tip": "核心金句：绿水青山就是金山银山，保护生态环境就是保护生产力",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
① <b>判断定性（1分）</b>：该负责人的言论是不正确的（割裂了经济发展与环境保护的辩证统一关系）；<br>
② <b>论证两山理念（2分）</b>：绿水青山就是金山银山。保护生态环境就是保护生产力，改善生态环境就是发展生产力。生态环境保护与经济发展不是非此即彼的对立关系，而是相互促进、相得益彰的；<br>
③ <b>论证绿色发展优势（2分）</b>：绝不能以牺牲生态环境为代价换取一时的经济增长，但保护环境并不意味着放弃经济发展。坚持走绿色低碳循环发展之路，能够倒逼产业转型升级，培育新的经济增长点；<br>
④ <b>升华结论（1分）</b>：实现人与自然和谐共生的中国式现代化，必须坚定不移走生态优先、绿色发展的高质量发展之路。""",
        "model_ans": """<p><b>该企业负责人的言论是不正确的。</b></p>
<p>（1）<b>经济发展与生态环境保护绝非“鱼和熊掌不可兼得”的对立关系</b>。绿水青山就是金山银山，保护生态环境就是保护生产力，改善生态环境就是发展生产力。良好生态环境是最普惠的民生福祉。</p>
<p>（2）<b>牺牲环境换取短期利益是不可持续的，但保护环境也绝不需要放弃经济发展</b>。绿色转型不仅不会阻碍经济，反而能倒逼企业技术创新、淘汰落后产能，培育节能环保与绿色低碳新兴产业，实现经济效益与生态效益双赢。</p>
<p>（3）<b>因此</b>，我们必须摒弃把环保与发展割裂开来的旧观念，协同推进降碳、减污、扩绿、增长，坚定不移走生产发展、生活富裕、生态良好的文明发展道路。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：未答出“保护生态环境就是保护生产力”课本理论扣1分。"
    })

    # Q12: 2024虹口一模真题·传统文化传承守旧与创新辨析
    questions.append({
        "id": "q-12",
        "tag": "bianxi",
        "meta_tags": [
            ("2024虹口一模真题", "tag-blue"),
            ("专项① 辨析评析题", "tag-red"),
            ("文化自信 · 两创方针", "tag-purple")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
针对近年来故宫文创、国风动漫、戏曲新编等“国潮热”，有学者提出质疑：“传承优秀传统文化必须原汁原味、恪守古训，保持古代风貌分毫不动；现代商业文创和网络科技改编都是浮躁迎合，只会冲淡传统的底蕴，根本算不上真正的传承。”""",
        "stem": "【设问】：请运用九年级上册“延续文化血脉”相关知识，对该观点进行评析。（6分）",
        "chain": [
            "判断表态 ➔ 该观点是片面的",
            "阐释合理 ➔ 看到传承文化要守护优秀根脉和精神底蕴具有合理性",
            "攻其破绽 ➔ 忽视了文化传承需要创造性转化、创新性发展，科技赋予文化新活力",
            "升华做法 ➔ 坚定文化自信，推动优秀传统文化与现代生活相融合"
        ],
        "draft_tip": "文化两创方针：创造性转化 + 创新性发展，传承与创新辩证统一",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
① <b>判断定性（1分）</b>：该学者的观点是片面的；<br>
② <b>合理性分析（2分）</b>：该学者强调恪守古训、守护文化精神内核具有一定合理性。中华文化源远流长、博大精深，传承优秀传统文化必须尊重历史真实性，守护文化根脉与精神精髓；<br>
③ <b>片面性分析（2分）</b>：但是把创新和现代表达对立起来是错误的。文化具有与时俱进的品格。传承中华优秀传统文化必须坚持创造性转化、创新性发展，借助现代科技与大众文创形式，才能让传统文化走进现代生活、焕发时代生机；<br>
④ <b>升华结论（1分）</b>：我们要坚定文化自信，坚持古为今用、推陈出新，做到在继承中发展、在发展中继承。""",
        "model_ans": """<p><b>该学者的观点是片面的。</b></p>
<p>（1）<b>学者主张守护传统文化的原真性与精神底蕴有其合理性</b>。中华优秀传统文化是中华民族的精神命脉。传承文化必须尊重历史，坚守优秀文化的精神内核与根基，防止低俗化解构。</p>
<p>（2）<b>但是，把传统文化与现代科技文创创新对立起来是错误的</b>。中华文化历久弥新，关键在于不断创新。传承中华优秀传统文化必须坚持“创造性转化、创新性发展”方针。国潮文创和数字赋能让沉睡的文物和典籍鲜活起来，极大地增强了优秀传统文化的吸引力与感召力。</p>
<p>（3）<b>因此</b>，我们要坚定文化自信，坚持取其精华、推陈出新，在固本培元的基础上大胆融合现代生活审美，让中华优秀传统文化展现永久魅力和时代风采。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：遗漏“推动优秀传统文化创造性转化、创新性发展（两创方针）”将被严重扣分。"
    })

    # ==================== MODULE C: 专项二 · 材料分析题“四角对应法”（5题） ====================

    # Q13: 2024上海中考真题·上海长宁基层立法联系点与全过程人民民主
    questions.append({
        "id": "q-13",
        "tag": "cailiao",
        "meta_tags": [
            ("2024上海中考真题", "tag-red"),
            ("专项② 材料分析题", "tag-blue"),
            ("全过程人民民主 · 基层立法点", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★★☆",
        "material": """<b>【2024上海中考原卷材料】</b><br>
全国人大常委会法工委设立在上海长宁虹桥街道的基层立法联系点，是首批设在基层的国家立法联系点。自设立以来，联系点听取了反电信网络诈骗法、体育法、未成年人保护法等上百部法律草案的意见建议，召开座谈会数百场，收集社情民意万余条，其中数百条原汁原味的百姓建议被国家最高立法机关采纳并写入法律条款。小到弄堂垃圾分类、老旧小区无障碍坡道，大到国家法典草案，居民在家门口就能直接与立法专家面对面。""",
        "stem": "【设问】：请结合上述材料，运用“追求民主价值”的相关知识，说明上海长宁虹桥街道基层立法联系点是如何展现“全过程人民民主”的？（6分）",
        "chain": [
            "析材料 ➔ 社区居民立法建议直通全国人大最高立法机关",
            "引金句 ➔ 全过程人民民主是社会主义民主政治的本质属性（最广泛、最真实、最管用）",
            "讲意义 ➔ 架起民意直通车，落实科学立法民主立法，保障人民当家作主",
            "扣结论 ➔ 生动诠释全过程人民民主不仅有完整制度，更有生动实践"
        ],
        "draft_tip": "四角公式拆解：最广泛/最真实/最管用 + 科学民主立法 + 保障公民有序政治参与",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分，答出任意3点即可得满分）：<br>
① <b>民主特征维度（2分）</b>：全过程人民民主是社会主义民主政治的本质属性，是最广泛、最真实、最管用的民主。联系点畅通民意表达通道，使基层声音直达最高国家权力机关，彰显了民主的真实性与管用性；<br>
② <b>本质核心维度（2分）</b>：人民当家作主是社会主义民主政治的本质特征。联系点让普通百姓在家门口参与国家大政立法，保障了公民的知情权、参与权、表达权，使人民当家作主落实到国家治理各环节；<br>
③ <b>科学立法维度（2分）</b>：联系点开辟了民主立法、科学立法的新路径，广开言路、集思广益，使法律法规更好体现人民利益、反映人民意愿、增进人民福祉；<br>
④ <b>民主形式维度（2分）</b>：我国实行协商民主与选举民主相结合。基层立法联系点是践行全过程人民民主和基层协商民主的生动范例。""",
        "model_ans": """<p>上海长宁虹桥街道基层立法联系点生动展现了全过程人民民主的真谛：</p>
<p><b>① 展现了全过程人民民主“最真实、最管用”的特质</b>：联系点将百姓家门口的期盼与建议原汁原味送达最高立法机关并被写进法律条文，使民意真实转化为国家意志，解决了人民群众的实际关切。</p>
<p><b>② 充分保障了人民当家作主的民主权利</b>：人民当家作主是社会主义民主政治的本质特征。联系点搭建了公众参与平台，切实保障了公民的知情权、参与权和表达权，使人民有序参与国家治理落实到全过程各环节。</p>
<p><b>③ 推进了国家科学立法与民主立法进程</b>：立法听民意、聚民智，使制定出的法律更接地气、更有温度，增强了法律的权威与全社会的认同，是践行中国特色社会主义协商民主的生动范本。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：只答“全过程人民民主”而未结合联系点拆解“最广泛、最真实、最管用”扣2分。"
    })

    # Q14: 2024浦东一模真题·“人民城市人民建，人民城市为人民”
    questions.append({
        "id": "q-14",
        "tag": "cailiao",
        "meta_tags": [
            ("2024浦东一模真题", "tag-blue"),
            ("专项② 材料分析题", "tag-blue"),
            ("人民城市重要理念 · 民生福祉", "tag-amber")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
上海是“人民城市人民建，人民城市为人民”理念的首提地。近年来，上海深入推进“15分钟社区生活圈”建设，织密养老托育、文化体育、社区医疗服务网络；推进超千万平方米中心城区二级旧里以下房屋改造，解决大批群众“拎马桶”历史难题；在老旧小区加装电梯过程中，居委会搭建“加梯协商会”，由居民自主推选代表、自主商定出资方案，跑出上海城市更新加速度。""",
        "stem": "【设问】：请结合材料，运用所学九年级《道德与法治》知识，说明上海在城市建设中是如何践行“人民城市”重要理念的？（6分）",
        "chain": [
            "党的宗旨 ➔ 坚持立党为公、执政为民，始终坚持以人民为中心的发展思想",
            "民生目的 ➔ 增进民生福祉是发展的根本目的，织密便民网解决急难愁盼",
            "群众自治 ➔ 依靠人民建城市，健全基层群众自治与协商民主，激发城市活力"
        ],
        "draft_tip": "四角公式：人民为中心（理念） + 解决急难愁盼（举措） + 依靠人民共建（民主机制）",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分，三角度各2分）：<br>
① <b>发展思想维度（2分）</b>：坚持以人民为中心的发展思想。城市建设把人民对美好生活的向往作为奋斗目标，始终把人民利益放在第一位；<br>
② <b>发展根本目的维度（2分）</b>：增进民生福祉是发展的根本目的。上海通过推进社区生活圈与旧区改造，切实解决人民群众急难愁盼问题，提升人民群众的获得感、幸福感、安全感；<br>
③ <b>人民主体地位维度（2分）</b>：坚持人民城市人民建，依靠人民当家作主。上海在加装电梯等改造中坚持全过程人民民主，依托基层群众自治与协商民主，引导市民积极参与城市治理，共建共治共享幸福家园。""",
        "model_ans": """<p>上海在城市建设中践行“人民城市”理念体现在：</p>
<p><b>① 坚持以人民为中心的发展思想</b>：上海把增进民生福祉作为城市治理的出发点和落脚点，始终把群众最关切的住房、养老、医疗摆在突出位置，践行全心全意为人民服务的根本宗旨。</p>
<p><b>② 落实发展的根本目的是增进民生福祉</b>：通过织密“15分钟社区生活圈”和彻底解决旧里改造难题，补齐民生短板，切实提升了广大市民的获得感、幸福感和安全感。</p>
<p><b>③ 坚持人民主体地位，激发共建共治共享活力</b>：在加装电梯中推行基层协商民主与居民自主决策，落实了基层群众自治制度，体现了“城市建设依靠人民、治理成果由人民共享”的民主实践。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：容易遗漏“人民城市人民建（依靠人民参与治理）”这一半命题。"
    })

    # Q15: 2024徐汇一模真题·深海一号与中国航天大国重器
    questions.append({
        "id": "q-15",
        "tag": "cailiao",
        "meta_tags": [
            ("2024徐汇一模真题", "tag-blue"),
            ("专项② 材料分析题", "tag-blue"),
            ("大国重器 · 新型举国体制", "tag-purple")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
近年来，我国战略高技术领域捷报频传：全球首座10万吨级深水半潜式生产储油平台“深海一号”挺进深蓝，实现我国深水油气勘探开发跨越式突破；嫦娥六号在人类历史上首次实现月球背面采样返回，神舟十八号、十九号航天员顺利换岗。这些举世瞩目成就的背后，是国家集中财力物力打攻坚战，数千家科研院所、高校与骨干企业大力协同，几代科技工作者甘坐冷板凳、勇攀科学高峰的奋斗结晶。""",
        "stem": "【设问】：结合材料，综合运用所学九年级《道德与法治》知识，分析我国能够屡屡攻克关键核心技术、挺进科技强国的深层原因。（6分）",
        "chain": [
            "体制优势 ➔ 坚持中国共产党的全面领导，发挥集中力量办大事的新型举国体制优势",
            "国家战略 ➔ 坚定不移实施科教兴国、人才强国和创新驱动发展战略",
            "精神力量 ➔ 弘扬以爱国主义为核心的民族精神和改革创新为核心的时代精神（航天精神、科学家精神）"
        ],
        "draft_tip": "原因三维归纳法：党的领导与制度优势 + 国家发展战略支撑 + 精神动力与人才报国",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分，三方面各2分）：<br>
① <b>政治与制度优势（2分）</b>：坚持中国共产党的全面领导。发挥中国特色社会主义制度集中力量办大事的显著优势，健全新型举国体制，统筹全国科技攻坚资源；<br>
② <b>战略与综合国力支撑（2分）</b>：我国综合国力与经济实力持续增强，提供了强大的物质基础；坚定不移实施科教兴国战略、人才强国战略和创新驱动发展战略，走中国特色自主创新道路；<br>
③ <b>精神动力与人才支撑（2分）</b>：广大科研人员大力弘扬以爱国主义为核心的民族精神和以改革创新为核心的时代精神（科学家精神、载人航天精神），艰苦奋斗、开拓创新，展现了强烈的责任担当。""",
        "model_ans": """<p>我国屡屡攻克关键核心技术、挺进科技强国的原因在于：</p>
<p><b>① 坚持党的集中统一领导与制度优势</b>：发挥中国特色社会主义集中力量办大事的制度优越性，构建新型举国体制，实现全国一盘棋的高效协同攻关。</p>
<p><b>② 坚定实施创新驱动与科教兴国战略</b>：我国综合国力日益雄厚，国家持续加大科技研发投入，坚持科技自立自强，走出了一条中国特色自主创新道路。</p>
<p><b>③ 伟大民族精神与科学家精神的激励</b>：一代代科研人员弘扬以改革创新为核心的时代精神和载人航天精神，不畏艰难、勇攀高峰，汇聚起科技报国的磅礴伟力。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：若只提“科学家努力”，未上升到“党的集中领导与新型举国体制”，最高扣2分。"
    })

    # Q16: 2024松江一模真题·上海对口援疆“山海情”
    questions.append({
        "id": "q-16",
        "tag": "cailiao",
        "meta_tags": [
            ("2024松江一模真题", "tag-blue"),
            ("专项② 材料分析题", "tag-blue"),
            ("民族团结 · 共同繁荣", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
上海持续开展对口援疆工作，倾情帮扶新疆喀什四县。十余年来，上海累计投入对口援疆资金数百亿元，选派数批优秀教师、援疆医生与农科专家开展“组团式”帮扶；援建现代化工业园区、喀什第六人民医院、泽普上海实验学校；推进“喀品入沪”，助力当地特色农产品走进长三角高端商超，有力带动了边疆各族群众增收致富。""",
        "stem": "【设问】：请运用九年级上册“民族团结”和“共同富裕”的相关知识，分析上海深入开展对口援疆工作的重大意义。（6分）",
        "chain": [
            "民族关系 ➔ 巩固和发展平等团结互助和谐的社会主义民族关系，铸牢中华民族共同体意识",
            "发展格局 ➔ 缩小东西部差距，促进区域协调发展和各民族共同繁荣",
            "根本目的 ➔ 让各族人民共享改革发展成果，促进社会公平正义与边疆长治久安"
        ],
        "draft_tip": "四角公式意义维度：民族关系维度 + 经济协调/共同繁荣维度 + 民生与国家稳定维度",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分，三方面各2分）：<br>
① <b>民族团结与共同体维度（2分）</b>：有利于巩固和发展平等团结互助和谐的社会主义民族关系，铸牢中华民族共同体意识，促进各民族像石榴籽一样紧紧抱在一起；<br>
② <b>共同繁荣与协调发展维度（2分）</b>：有利于落实“民族平等、民族团结和各民族共同繁荣”的方针，推动东西部优势互补，促进区域协调发展，加快缩小城乡区域差距；<br>
③ <b>民生福祉与国家长治久安维度（2分）</b>：有利于改善边疆各族人民生活条件，促进共同富裕，维护边疆稳固、社会稳定和国家长治久安。""",
        "model_ans": """<p>上海深入推进对口援疆工作具有重大而深远的意义：</p>
<p><b>① 铸牢中华民族共同体意识</b>：深化了各民族交往交流交融，进一步巩固了平等团结互助和谐的社会主义新型民族关系，增强了中华民族凝聚力。</p>
<p><b>② 促进各民族共同繁荣与区域协调发展</b>：上海的技术、资金、人才优势与新疆的资源、区位优势紧密互补，有力带动边疆特色产业转型，促进各民族共同富裕。</p>
<p><b>③ 保障边疆民生福祉与国家长治久安</b>：改善了当地教育、医疗等公共服务水平，切实提升了各族群众的幸福感，为巩固国防安全和维护国家统一筑牢了坚实基石。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：必须准确写出“铸牢中华民族共同体意识”和“各民族共同繁荣”两项核心表述。"
    })

    # Q17: 2024杨浦一模真题·杨浦滨江工业锈带蝶变生活秀带
    questions.append({
        "id": "q-17",
        "tag": "cailiao",
        "meta_tags": [
            ("2024杨浦一模真题", "tag-blue"),
            ("专项② 材料分析题", "tag-blue"),
            ("生态文明 · 高质量发展", "tag-emerald")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【情境材料】</b><br>
曾经的杨浦滨江，机器轰鸣，密布着中国近代第一家水厂、造纸厂等老工业基地，被称为“工业锈带”，沿江岸线封闭阻隔。近年来，杨浦区践行生态绿色与城市更新理念，对工业遗存进行“留改拆”活化利用，保留厂房骨架与码头吊塔，打造连续不间断的滨江慢行道、跑步道和骑行道；建成多处“杨树浦驿站”，开辟生态绿地和口袋公园，实现“还江于民、还绿于民”，蝶变成为市民休闲健身的世界级“生活秀带”。""",
        "stem": "【设问】：结合材料，运用九年级上册“建设美丽中国”相关知识，说明杨浦滨江的蝶变是如何彰显人与自然和谐共生的？（6分）",
        "chain": [
            "绿色理念 ➔ 践行绿水青山就是金山银山理念，坚持节约资源和保护环境基本国策",
            "高质量转型 ➔ 摒弃高能耗粗放旧模式，推进城市绿色更新与历史文脉有机融合",
            "人民至上 ➔ 还江于民、还绿于民，打造良好生态环境作为最普惠民生福祉"
        ],
        "draft_tip": "四角公式：生态理念（两山理念） + 转变发展方式（绿色更新） + 民生福祉（良好生态最普惠）",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分，三方面各2分）：<br>
① <b>生态理念维度（2分）</b>：践行“绿水青山就是金山银山”理念，坚持节约优先、保护优先、自然恢复为主的方针，实现城市更新与生态修复有机统一；<br>
② <b>转变发展方式维度（2分）</b>：走绿色低碳循环的高质量发展之路。杨浦摈弃传统重工业高污染旧路径，保护历史工业文脉并注入现代绿色功能，实现生态效益、人文效益与社会效益的多赢；<br>
③ <b>以人为本民生维度（2分）</b>：坚持良好生态环境是最普惠的民生福祉。通过还江于民、建设绿道驿站，满足了人民群众对优美生态环境的高品质需求。""",
        "model_ans": """<p>杨浦滨江从“工业锈带”到“生活秀带”的蝶变展现了人与自然和谐共生的现代化新画卷：</p>
<p><b>① 践行绿水青山就是金山银山的生态文明理念</b>：杨浦转变城市治理模式，在更新中融入生态绿化与自然修复，实现了自然生态与城市建筑的共生共荣。</p>
<p><b>② 坚持走生态优先、绿色低碳的高质量发展道路</b>：对百年工业遗存活化利用而非大拆大建，保护了历史文化记忆，推动了岸线经济社会全面绿色转型。</p>
<p><b>③ 落实良好生态环境是最普惠的民生福祉</b>：坚持“还江于民、还绿于民”，将封闭工业岸线打造为百姓家门口的亲水乐园，让人民共享生态文明建设红利。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：缺少“良好生态环境是最普惠的民生福祉”金句将无法获得该维度2分。"
    })

    # ==================== MODULE D: 专项三 · 实践探究开放题（5题） ====================

    # Q18: 2024宝山一模真题·老旧小区加装电梯协商议事与倡议书
    questions.append({
        "id": "q-18",
        "tag": "kaifang",
        "meta_tags": [
            ("2024宝山一模真题", "tag-blue"),
            ("专项③ 实践探究开放题", "tag-emerald"),
            ("基层自治 · 协商民主 · 倡议书", "tag-red")
        ],
        "score_diff": "满分：8分 | 难度：★★★★☆",
        "material": """<b>【情境材料】</b><br>
某老公房小区推进加装电梯民心工程。高楼层居民特别是老年群体对加梯意愿迫切，但一二层居民担忧采光遮挡、运行噪音以及未来房屋贬值，邻里之间产生矛盾隔阂，甚至个别楼栋因此发生争吵，加梯工程一度停滞。为此，社区居委会决定召开一次由居民代表、物业、加梯企业共同参与的“加梯民主恳谈协商会”。""",
        "stem": "【设问】：<br>（1）请你作为居委会青年调解员，为本次加梯民主恳谈会设计一套规范的工作推进方案（含前期准备、现场协商、会后落实三阶段）。（4分）<br>（2）请你为一至六楼的邻居们拟写一段以“邻里和睦·换位思考”为主题的微型倡议寄语。（4分）",
        "chain": [
            "方案设计 ➔ 准备阶段（入户调研拟案） ➔ 实施阶段（面对面协商解答） ➔ 落实阶段（公示履约跟进）",
            "倡议撰写 ➔ 礼貌称呼 + 阐明换位思考重要性 + 提出协商共治倡导 + 语言真诚得体"
        ],
        "draft_tip": "探究题黄金三式：三阶方案要具实操性；倡议寄语要有情感温度与法理支撑",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分8分）：<br>
<b>（1）推进方案设计（4分）</b>：<br>
① 准备阶段（1分）：入户走访收集低楼层顾虑，与企业制定防噪采光补偿初步方案；<br>
② 实施阶段（2分）：召开多方民主恳谈会，专家现场答疑，邻里坦诚协商，形成公约草案；<br>
③ 会后落实（1分）：楼道公示表决结果，签订加梯协议，建立长效维护监督机制。<br>
<b>（2）倡议寄语撰写（4分）</b>：<br>
① 紧扣主题（换位思考、邻里守望相助，1分）；<br>
② 法治与道德结合（行使权利不得损害他人权益，众人的事情众人商量，2分）；<br>
③ 表达通畅真挚、符合倡议格式（1分）。""",
        "model_ans": """<p><b>（1）加梯民主恳谈会工作方案：</b><br>
<b>① 前期准备阶段</b>：联合楼组长逐户走访一、二层居民，详细记录其对采光、噪音、分摊费用的诉求；会同加梯公司制定透明遮光玻璃、低噪音主机及底层补偿草案。<br>
<b>② 现场协商阶段</b>：召开民主恳谈会，邀请街道法律顾问、工程师为居民客观解惑；高低楼层居民敞开心扉面对面协商，敲定费用分摊与补偿细则，达成共识。<br>
<b>③ 成果落实阶段</b>：将协商成果与加梯设计图纸在小区公示栏张贴公示，组织全楼业主正式签字确认，并建立后续运维管理委员会，监督施工进程。</p>
<p><b>（2）邻里互谅微倡议寄语：</b><br>
<b>亲爱的邻居们：</b><br>
远亲不如近邻，千金难买邻里情！高楼层老人的“下楼难”需要我们共同伸出援手，而底层居民对采光环境的关切同样需要体谅包容。民事不可盲，众人商量好。让我们多一分换位思考的温暖，少一分固执己见的隔阂，通过友好协商共同化解难题，携手建起方便全楼的幸福梯、连心梯！</p>""",
        "warning": "⚠️ <b>扣分警示</b>：方案设计空洞（只写“开会”、“签字”）而无具体专业内容会被扣2分。"
    })

    # Q19: 2024静安一模真题·“保护母亲河·守护一江碧水”环保活动
    questions.append({
        "id": "q-19",
        "tag": "kaifang",
        "meta_tags": [
            ("2024静安一模真题", "tag-blue"),
            ("专项③ 实践探究开放题", "tag-emerald"),
            ("生态环保 · 对偶标语 · 主体举措", "tag-amber")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【活动情境】</b><br>
为贯彻落实《中华人民共和国长江保护法》，学校团委与学生会联合开展“保护母亲河·守护一江碧水”青少年生态环保主题宣传周活动。""",
        "stem": "【设问】：<br>（1）请你为本次活动拟写两条对偶工整、富有号召力的宣传标语。（2分）<br>（2）请从“学校组织”和“学生个人”两个角度，各提出两条切实可行的落实举措。（4分）",
        "chain": [
            "对偶标语 ➔ 上句行动倡导 + 下句美好愿景（字数相等、结构工整）",
            "学校角度 ➔ 专题教育 + 实践研学活动",
            "个人角度 ➔ 日常节水守则 + 志愿宣讲践行"
        ],
        "draft_tip": "标语严禁散句凑字数；主体建议切合中学生与学校实际，拒绝假大空",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
<b>（1）宣传标语（2分，每条1分）</b>：要求字数对称、对仗工整、紧扣水环境保护主题。<br>
<b>（2）落实举措（4分，每条1分）</b>：<br>
① 学校组织角度（2分）：开设长江保护法法治班会或科普讲座；组织黄浦江水质取样监测研学实践活动；举办环保手抄报或微视频比赛；<br>
② 学生个人角度（2分）：在日常生活中节约用水，做到随手关水龙头、一水多用；不向河道倾倒垃圾或废弃物，践行垃圾分类；积极参加“巡河护绿”青少年志愿宣讲。""",
        "model_ans": """<p><b>（1）宣传标语：</b><br>
标语一：共护一江碧水长流，同筑绿色生态家园。<br>
标语二：点滴节水始于足下，守护母亲河驻在心中。</p>
<p><b>（2）落实举措：</b><br>
<b>【学校组织角度】：</b><br>
① 举办“长江保护与长江生态”法治科普专家讲座，普及水资源保护法律法规；<br>
② 组织“探秘滨江水系”科学社团研学活动，带领同学进行实地水质监测与考察。<br>
<b>【学生个人角度】：</b><br>
① 自觉践行绿色低碳生活方式，随手关闭水龙头，做到淘米水浇花等一水多用；<br>
② 积极报名社区“小小巡河员”志愿服务，劝阻向河道乱抛杂物的不文明行为。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：标语不对偶或个人角度写成“国家加大惩罚力度”错位扣分。"
    })

    # Q20: 2024黄浦一模真题·青少年网络法治素养与反诈防骗策划案
    questions.append({
        "id": "q-20",
        "tag": "kaifang",
        "meta_tags": [
            ("2024黄浦一模真题", "tag-blue"),
            ("专项③ 实践探究开放题", "tag-emerald"),
            ("网络法治 · 反诈防骗策划案", "tag-purple")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【现实背景】</b><br>
当前，部分不法分子盯上辨别能力较弱的青少年群体，通过“免费领游戏皮肤”、“充值返利”、“解除防沉迷限制”等网络套路实施电信网络诈骗，致使部分中学生财产受损甚至误入歧途。学校拟面向全体初三学生开展“提高网络素养·筑牢反诈防线”主题活动。""",
        "stem": "【设问】：<br>（1）请你为本次主题活动设计两个内容充实、形式新颖的互动环节。（2分）<br>（2）请运用“主体多元法”，分别给国家公安网信机关与青少年自身各提两条建议。（4分）",
        "chain": [
            "环节设计 ➔ 案例情境剖析 + 沉浸式模拟防骗剧场",
            "国家机关 ➔ 严格执法严打黑灰产 + 加强涉未成年网络安全技术反制",
            "青少年 ➔ 增强网络防范意识不贪便宜 + 遇险沉着留证并及时报警"
        ],
        "draft_tip": "互动环节要生动立体；主体法针对公安网信与青少年各有侧重",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
<b>（1）活动环节（2分，每环节1分）</b>：如“真实骗局微视频剖析”、“反诈模拟情景剧互动体验”等；<br>
<b>（2）主体对策（4分，每条1分）</b>：<br>
① 公安与网信部门（2分）：加大执法巡查力度，重拳打击侵害未成年人的涉网黑灰产业链；督导互联网平台压实主体责任，完善未成年人防沉迷与涉诈拦截算法；<br>
② 青少年自身（2分）：提高信息鉴别力与防范意识，坚决不轻信陌生中奖与充值返利信息；保管好个人及家长隐私信息与支付密码，遭遇可疑情况及时向老师家长报告并报警求助。""",
        "model_ans": """<p><b>（1）主题活动环节设计：</b><br>
<b>环节一：【迷雾重重·骗术大拆解】</b>：播放近期本市发生的“游戏皮肤诱导充值”典型真实案例短片，由法治副校长现场剖析骗局核心套路。<br>
<b>环节二：【慧眼识骗·情景沉浸演练】</b>：设计“收到虚假客服退款私信”模拟闯关互动，让同学通过手机端答题识破破绽，评选“反诈智多星”。</p>
<p><b>（2）主体对策建议：</b><br>
<b>【公安与网信机关】：</b><br>
① 严格执法，强化线上协同监测，依法严厉打击利用网络游戏、社交软件诈骗未成年人的违法犯罪行为；<br>
② 督促网络平台严格落实实名认证与未成年人保护模式，封堵涉诈引流网址与黑账号。<br>
<b>【青少年自身】：</b><br>
① 树立法治观念与防范意识，不贪图小便宜，不随意点击不明链接或扫描陌生二维码；<br>
② 严守个人信息底线，不向任何人透露家庭财产与支付密码，遇突发侵害第一时间留证并向家长报告报警。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：环节设计太笼统（如仅写“听讲座”、“写作业”）扣1分。"
    })

    # Q21: 2024普陀一模真题·“寻访身边非遗·讲好海派故事”调研方案与文创设计
    questions.append({
        "id": "q-21",
        "tag": "kaifang",
        "meta_tags": [
            ("2024普陀一模真题", "tag-blue"),
            ("专项③ 实践探究开放题", "tag-emerald"),
            ("海派文化 · 非遗传承创新", "tag-purple")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【文化情境】</b><br>
上海拥有丰富的非物质文化遗产，如海派撕纸、顾绣、龙华庙会、城隍庙老字号制作技艺等。某初中准备开展“寻访身边的海派非遗”跨学科综合探究研学活动。""",
        "stem": "【设问】：<br>（1）请你为本班设计一份条理清晰的非遗寻访调研步骤。（3分）<br>（2）请选择一项海派非遗，提出一个富有创意的“文化两创”（创造性转化与创新性发展）新点子。（3分）",
        "chain": [
            "调研步骤 ➔ 准备拟定提纲 ➔ 实地走访体验传承人 ➔ 整理撰写报告成果展",
            "文创点子 ➔ 具体非遗项目 + 现代审美/数字技术结合 + 市场或生活应用场景"
        ],
        "draft_tip": "步骤按“准备-实施-总结”三阶段；文创点子紧扣“创造性转化、创新性发展”",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
<b>（1）调研步骤（3分）</b>：<br>
① 准备阶段（1分）：选定探究非遗项目，搜集背景文献，制定安全调研计划与访谈提纲；<br>
② 实施阶段（1分）：实地探访非遗传承工坊或博物馆，现场观摩访谈传承人，亲自动手体验；<br>
③ 总结阶段（1分）：整理影像与采访笔记，撰写调研报告，在校内举办非遗摄影与作品展。<br>
<b>（2）文化两创点子（3分）</b>：<br>
① 明确具体非遗项目（1分）；<br>
② 运用现代科技、潮流审美或生活实用场景进行创新结合（1分）；<br>
③ 阐明促进传统文化传播推广的实际效果（1分）。""",
        "model_ans": """<p><b>（1）非遗寻访调研步骤：</b><br>
① <b>准备阶段</b>：确定“海派撕纸艺术传承”为调研主题，查阅历史文献，分组编制传承人采访问题提纲；<br>
② <b>实施阶段</b>：走访普陀区非遗工坊，与国家级传承人面对面交流记录口述历史，并在导师指导下亲手体验撕纸技法；<br>
③ <b>总结阶段</b>：将收集的照片与录音整理成调研报告，制作宣传展板并在校园文化节上举办“撕纸艺术互动体验坊”。</p>
<p><b>（2）文化创新点子设计：</b><br>
<b>项目名称：【海派撕纸 × 现代国潮数字文创】</b><br>
<b>创意方案</b>：将海派撕纸中的经典上海石库门、玉兰花图案进行矢量数字化建模，开发成手机壁纸、微信动态表情包以及国潮金属书签；同时推出“撕纸盲盒DIY材料包”，结合AR扫描技术让纸上图案在手机镜头中“动起来”。<br>
<b>价值说明</b>：这一创意把传统非遗技艺与现代生活审美深度融合，实现了中华优秀传统文化的创造性转化与创新性发展，让年轻人爱上非遗。</p>""",
        "warning": "⚠️ <b>扣分警示</b>：文创点子不可仅仅写“发传单”，必须体现“文化创造性转化与创新性发展”思维。"
    })

    # Q22: 2024长宁一模真题·“国家宪法日·尊崇宪法信仰”展板设计与宣誓词
    questions.append({
        "id": "q-22",
        "tag": "kaifang",
        "meta_tags": [
            ("2024长宁一模真题", "tag-blue"),
            ("专项③ 实践探究开放题", "tag-emerald"),
            ("宪法至上 · 根本大法 · 宣誓词", "tag-red")
        ],
        "score_diff": "满分：6分 | 难度：★★★☆☆",
        "material": """<b>【校园情境】</b><br>
每年的12月4日是国家宪法日。为了大力弘扬宪法精神，维护宪法权威，学校计划在校园主干道布置“尊崇宪法·伴我成长”主题展板长廊，并组织全体初三师生举行晨会宪法宣誓仪式。""",
        "stem": "【设问】：<br>（1）请你为主题展板设计三个层次分明、富有感染力的栏目名称。（3分）<br>（2）请你为宣誓仪式拟写中学生向宪法宣誓表态的核心誓词要点。（3分）",
        "chain": [
            "栏目设计 ➔ 根本大法定位 + 公民权利义务 + 弘扬宪法精神践行",
            "誓词要点 ➔ 忠于宪法权威 + 恪守法律底线 + 勇担强国时代使命"
        ],
        "draft_tip": "栏目按“认知-理解-践行”逻辑递进；誓词要点契合青少年法治素养要求",
        "rubric": """<b>【采分要点与赋分细则】</b>（满分6分）：<br>
<b>（1）展板栏目设计（3分，每个1分）</b>：要求结构清晰、层层递进、突出宪法地位（如：根本大法、权利基石、守法力行等）；<br>
<b>（2）宣誓誓词要点（3分，答出任意三点即可）</b>：<br>
① 尊崇宪法地位，维护宪法权威；<br>
② 学习宪法知识，弘扬宪法精神；<br>
③ 依法行使公民权利，自觉履行法定义务；<br>
④ 恪守法律红线，做社会主义法治的忠实崇尚者、自觉遵守者、坚定捍卫者。""",
        "model_ans": """<p><b>（1）主题展板三个栏目名称：</b><br>
<b>栏目一：【立国之基·根本大法】</b>——介绍我国宪法的根本地位、制定历程与核心原则；<br>
<b>栏目二：【生命之舟·一生守护】</b>——图解宪法如何从出生、受教育、成年到养老全生命周期保障公民基本权利；<br>
<b>栏目三：【信仰之火·法治力行】</b>——展示新时代公民维护宪法权威、积极遵规守法的青少年实践行动。</p>
<p><b>（2）宪法宣誓核心誓词要点：</b><br>
“我宣誓：忠于中华人民共和国宪法，维护宪法权威，履行法定职责！热爱祖国，热爱人民；刻苦学习，恪守校纪国法；依法行使权利，自觉履行义务；树立法治信仰，争做崇德守法的时代新人，为实现中华民族伟大复兴努力奋斗！”</p>""",
        "warning": "⚠️ <b>扣分警示</b>：展板名称口号化（如“第一块”、“第二块”）不给分，必须体现宪法核心原理。"
    })

    return questions

def render_question_html(q, index):
    meta_badges = "".join([f'<span class="q-tag {cls}">{txt}</span>' for txt, cls in q["meta_tags"]])
    chain_steps = []
    for i, step in enumerate(q["chain"]):
        chain_steps.append(f'<div class="chain-step">{step}</div>')
        if i < len(q["chain"]) - 1:
            chain_steps.append('<span class="chain-arrow">➔</span>')
    chain_html = "".join(chain_steps)

    html = f"""
      <!-- {q["id"]}: {q["meta_tags"][0][0]} -->
      <div class="question-card" data-tag="{q['tag']}">
        <div class="q-meta">
          <div class="q-tags">
            {meta_badges}
          </div>
          <div class="q-score">{q["score_diff"]}</div>
        </div>
        <div class="q-material">
          {q["material"]}
        </div>
        <div class="q-stem">
          {q["stem"]}
        </div>

        <div class="q-chain-box">
          <div class="chain-title"><span>💡</span> 官方标准审题与思维破题链 (材 ➔ 知)：</div>
          <div class="chain-flow">
            {chain_html}
          </div>
        </div>

        <div class="draft-box">
          <textarea class="draft-textarea" placeholder="✍️ 在此输入您的答题草稿思路（写完可点击下方按钮核对采分点）..." oninput="updateWordCount(this)"></textarea>
          <div class="draft-footer">
            <span>字数：<span class="wc-num">0</span> 字</span>
            <span>💡 提示：{q["draft_tip"]}</span>
          </div>
        </div>

        <button class="ans-toggle-btn" onclick="toggleAnswer('ans-{index+1}', this)">👁️ 查看本题官方答案与采分细则</button>
        <div class="ans-panel" id="ans-{index+1}">
          <div class="grading-points">
            {q["rubric"]}
          </div>
          <div class="full-answer-text">
            <b>【满分标准范文】</b>：
            {q["model_ans"]}
          </div>
          <div class="trap-warning">
            {q["warning"]}
          </div>
        </div>
      </div>
"""
    return html

def build_mega_daofa():
    head = get_html_head()
    tail = get_html_tail()

    questions = generate_questions()
    q_htmls = [render_question_html(q, i) for i, q in enumerate(questions)]

    full_html = head + "".join(q_htmls) + tail

    daofa_dir = "/Users/emily/Documents/Projects/owenlearining/daofa"
    
    # 1. daofa-special-bank.html (Question Bank Only)
    f_bank = os.path.join(daofa_dir, "daofa-special-bank.html")
    with open(f_bank, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Written: {f_bank} ({len(full_html)} bytes)")

    print(f"Successfully generated question bank with {len(questions)} authentic exam questions!")

if __name__ == "__main__":
    build_mega_daofa()
