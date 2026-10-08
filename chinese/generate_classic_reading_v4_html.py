# -*- coding: utf-8 -*-
import json
import os
import html

# Load V4 data
with open('chinese/classic-reading-v4-full.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

books = db['books']

# Build HTML
html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>中考名著阅读核心考点全景比对表 (V4 100%无损还原版)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-card-sub: #F1F5F9;
      --border-color: #E2E8F0;
      --border-dark: #CBD5E1;
      --text-main: #0F172A;
      --text-secondary: #334155;
      --text-muted: #64748B;
      --primary: #2563EB;
      --primary-hover: #1D4ED8;
      --primary-light: #EFF6FF;
      --accent: #0284C7;
      --accent-light: #E0F2FE;
      --badge-bg: #EEF2F6;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.06), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      padding-bottom: 80px;
    }

    /* Top Sticky Header */
    .top-navbar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
    }

    .nav-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .brand-title {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text-main);
    }

    .brand-badge {
      background: linear-gradient(135deg, #2563EB, #1D4ED8);
      color: white;
      font-weight: 700;
      font-size: 13px;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }

    .brand-text {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
      font-family: 'Noto Serif SC', serif;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .search-box {
      position: relative;
      width: 280px;
    }

    .search-input {
      width: 100%;
      padding: 8px 12px 8px 36px;
      border: 1px solid var(--border-dark);
      border-radius: 8px;
      font-size: 14px;
      background: var(--bg-main);
      transition: all 0.2s;
    }

    .search-input:focus {
      outline: none;
      border-color: var(--primary);
      background: #FFFFFF;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }

    .search-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
    }

    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
      background: white;
      border: 1px solid var(--border-dark);
      border-radius: 8px;
      text-decoration: none;
      transition: all 0.2s;
      cursor: pointer;
    }

    .nav-btn:hover {
      background: var(--bg-card-sub);
      color: var(--primary);
      border-color: var(--primary);
    }

    .nav-btn.primary {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }

    .nav-btn.primary:hover {
      background: var(--primary-hover);
    }

    /* Sub-Navigation for 16 Books */
    .books-subnav {
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-color);
      overflow-x: auto;
      white-space: nowrap;
      padding: 8px 24px;
    }

    .books-pill-list {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      gap: 8px;
      list-style: none;
      align-items: center;
    }

    .book-pill-link {
      display: inline-block;
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-secondary);
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      text-decoration: none;
      transition: all 0.15s ease;
    }

    .book-pill-link:hover, .book-pill-link.active {
      background: var(--primary-light);
      color: var(--primary);
      border-color: #93C5FD;
      font-weight: 600;
    }

    /* Main Container */
    .main-wrapper {
      max-width: 1400px;
      margin: 24px auto;
      padding: 0 24px;
    }

    /* Hero Banner */
    .hero-card {
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 24px 32px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      overflow: hidden;
    }

    .hero-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 6px;
      height: 100%;
      background: linear-gradient(180deg, #2563EB, #0284C7);
    }

    .hero-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }

    .hero-title {
      font-size: 26px;
      font-weight: 700;
      color: var(--text-main);
      font-family: 'Noto Serif SC', serif;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .hero-version-tag {
      font-size: 12px;
      padding: 3px 8px;
      background: #EFF6FF;
      color: #1D4ED8;
      border: 1px solid #BFDBFE;
      border-radius: 6px;
      font-family: sans-serif;
    }

    .hero-desc {
      font-size: 15px;
      color: var(--text-secondary);
      line-height: 1.7;
    }

    .hero-stats {
      display: flex;
      gap: 24px;
      margin-top: 6px;
      padding-top: 14px;
      border-top: 1px solid var(--border-color);
      flex-wrap: wrap;
    }

    .stat-item {
      display: flex;
      flex-direction: column;
    }

    .stat-val {
      font-size: 20px;
      font-weight: 700;
      color: var(--primary);
    }

    .stat-lbl {
      font-size: 12px;
      color: var(--text-muted);
    }

    /* Book Section */
    .book-section {
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      margin-bottom: 36px;
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      scroll-margin-top: 110px;
    }

    .book-header {
      padding: 20px 28px;
      background: linear-gradient(to right, #FFFFFF, #F8FAFC);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }

    .book-heading {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .book-index-tag {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--primary-light);
      color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 15px;
    }

    .book-main-title {
      font-size: 22px;
      font-weight: 700;
      color: var(--text-main);
      font-family: 'Noto Serif SC', serif;
    }

    .book-subtitle {
      font-size: 14px;
      color: var(--text-muted);
      margin-left: 6px;
    }

    .book-meta-badges {
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }

    .meta-badge {
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 500;
      background: var(--bg-card-sub);
      color: var(--text-secondary);
      border: 1px solid var(--border-color);
    }

    .meta-badge.blue {
      background: #EFF6FF;
      color: #1D4ED8;
      border-color: #DBEAFE;
    }

    .meta-badge.orange {
      background: #FFF7ED;
      color: #C2410C;
      border-color: #FFEDD5;
    }

    /* Book Info Grid */
    .book-overview-grid {
      padding: 24px 28px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 18px;
      background: #FAFCFF;
      border-bottom: 1px solid var(--border-color);
    }

    .info-card {
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px 20px;
    }

    .info-card-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .info-card-text {
      font-size: 14px;
      color: var(--text-secondary);
      line-height: 1.65;
    }

    /* Table Container */
    .table-section {
      padding: 24px 28px;
    }

    .table-title-bar {
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }

    .table-heading {
      font-size: 17px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: 'Noto Serif SC', serif;
    }

    .table-row-count {
      font-size: 13px;
      color: var(--text-muted);
      background: var(--bg-card-sub);
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 500;
    }

    .table-responsive-box {
      width: 100%;
      overflow-x: auto;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      background: #FFFFFF;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 14px;
    }

    table.data-table th {
      background: #F1F5F9;
      color: #1E293B;
      font-weight: 700;
      padding: 14px 16px;
      border-bottom: 2px solid var(--border-dark);
      white-space: nowrap;
      position: sticky;
      top: 0;
    }

    table.data-table td {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-secondary);
      line-height: 1.6;
      vertical-align: top;
    }

    table.data-table tbody tr:nth-child(even) {
      background-color: #F8FAFC;
    }

    table.data-table tbody tr:hover {
      background-color: #EFF6FF;
    }

    .row-key-col {
      font-weight: 700;
      color: #0F172A;
      white-space: nowrap;
      min-width: 120px;
    }

    .cell-content-formatted {
      white-space: pre-line;
    }

    /* Handout / Scan Scroller at Bottom of each Book */
    .scan-gallery-box {
      padding: 20px 28px;
      background: #F8FAFC;
      border-top: 1px solid var(--border-color);
    }

    .scan-gallery-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .scan-gallery-items {
      display: flex;
      gap: 12px;
      overflow-x: auto;
      padding-bottom: 6px;
    }

    .scan-item-card {
      flex: 0 0 150px;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 6px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
    }

    .scan-item-card:hover {
      border-color: var(--primary);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .scan-item-img {
      width: 100%;
      height: 180px;
      object-fit: cover;
      border-radius: 4px;
      border: 1px solid var(--border-color);
    }

    .scan-item-label {
      font-size: 12px;
      color: var(--text-secondary);
      margin-top: 6px;
      font-weight: 600;
    }

    /* Lightbox Modal */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 2000;
      padding: 24px;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-dialog {
      background: #FFFFFF;
      border-radius: 12px;
      max-width: 900px;
      width: 100%;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: var(--shadow-lg);
    }

    .modal-header {
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
    }

    .modal-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
    }

    .modal-close-btn {
      background: none;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: var(--text-muted);
    }

    .modal-body {
      padding: 16px;
      overflow-y: auto;
      text-align: center;
    }

    .modal-img-full {
      max-width: 100%;
      max-height: 75vh;
      border-radius: 6px;
      box-shadow: var(--shadow-sm);
    }

    /* Back to Top Floating Button */
    .back-top-btn {
      position: fixed;
      bottom: 30px;
      right: 30px;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 1px solid var(--border-dark);
      box-shadow: var(--shadow-md);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--primary);
      font-size: 20px;
      cursor: pointer;
      transition: all 0.2s;
      z-index: 999;
      text-decoration: none;
    }

    .back-top-btn:hover {
      background: var(--primary);
      color: white;
      transform: translateY(-3px);
    }

    @media (max-width: 768px) {
      .nav-container {
        flex-direction: column;
        align-items: stretch;
      }
      .search-box {
        width: 100%;
      }
      .hero-title {
        font-size: 20px;
      }
      .book-overview-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>

  <!-- Top Fixed Header -->
  <header class="top-navbar">
    <div class="nav-container">
      <a href="chinese.html" class="brand-title">
        <span class="brand-badge">语文文库</span>
        <span class="brand-text">中考名著考点全景比对表</span>
      </a>

      <div class="nav-actions">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="输入篇目/人物/考点关键字检索...">
        </div>
        <a href="chinese.html" class="nav-btn">返回语文主页</a>
        <a href="classic-reading-ocr-raw-V1.json" target="_blank" class="nav-btn">查看OCR生肉</a>
      </div>
    </div>

    <!-- 16 Books Sub-Navigation Pills -->
    <nav class="books-subnav">
      <ul class="books-pill-list" id="booksPills">
"""

for b in books:
    html_content += f"""        <li><a href="#book-{b['id']}" class="book-pill-link">{b['title']}</a></li>\n"""

html_content += """      </ul>
    </nav>
  </header>

  <!-- Main Content Container -->
  <main class="main-wrapper">

    <!-- Hero Card -->
    <section class="hero-card">
      <div class="hero-title-row">
        <h1 class="hero-title">
          <span>中考名著阅读核心考点全景整理</span>
          <span class="hero-version-tag">V4 100%无损表格还原版</span>
        </h1>
        <div class="hero-meta-right">
          <span class="meta-badge blue">部编版初中语文 · 16部必读名著</span>
        </div>
      </div>
      <p class="hero-desc">
        严格对照《39页中考名著阅读考点整理（含新增）（内部）》扫描版PDF逐页还原。彻底解决表格缺失与概括缩减问题，原汁原味还原包含《鲁滨逊漂流记》14大典型事件在内的全部结构化对比表，每部名著均附原版影印手稿印证。
      </p>
      <div class="hero-stats">
        <div class="stat-item">
          <span class="stat-val">16 部</span>
          <span class="stat-lbl">必读名著全收录</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">39 页</span>
          <span class="stat-lbl">原版讲义逐页精校</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">25 张</span>
          <span class="stat-lbl">高频结构化对比表</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">100%</span>
          <span class="stat-lbl">无删减考点无损呈现</span>
        </div>
      </div>
    </section>

    <!-- Books Sections -->
"""

# Render each book
for b in books:
    html_content += f"""
    <!-- Book: {b['title']} -->
    <article class="book-section" id="book-{b['id']}" data-book-title="{html.escape(b['title'])}">
      <!-- Book Header -->
      <header class="book-header">
        <div class="book-heading">
          <div class="book-index-tag">{b['index']}</div>
          <div>
            <h2 class="book-main-title">{b['title']}<span class="book-subtitle">{b.get('subtitle', '')}</span></h2>
          </div>
        </div>
        <div class="book-meta-badges">
          <span class="meta-badge blue">{b['grade']}</span>
          <span class="meta-badge orange">{b['category']}</span>
          <span class="meta-badge">讲义第 {b['pages'][0]:02d}-{b['pages'][-1]:02d} 页</span>
        </div>
      </header>

      <!-- Book Overview Grid -->
      <div class="book-overview-grid">
        <div class="info-card">
          <div class="info-card-title">✍️ 作者与文学常识</div>
          <p class="info-card-text"><strong>{html.escape(b['author'])}</strong>：{html.escape(b['author_desc'])}</p>
        </div>
        <div class="info-card">
          <div class="info-card-title">📖 作品主要内容概述</div>
          <p class="info-card-text">{html.escape(b['main_content'])}</p>
        </div>
        <div class="info-card">
          <div class="info-card-title">💡 主题思想与阅读策略</div>
          <p class="info-card-text">{html.escape(b['structure_summary'])}</p>
        </div>
      </div>

      <!-- Book Tables -->
      <div class="table-section">
"""
    for t in b.get('tables', []):
        html_content += f"""
        <div class="table-title-bar">
          <h3 class="table-heading">{html.escape(t['name'])}</h3>
          <span class="table-row-count">共 {len(t['rows'])} 项核心考点</span>
        </div>
        <div class="table-responsive-box">
          <table class="data-table">
            <thead>
              <tr>
"""
        for h in t['headers']:
            html_content += f"                <th>{html.escape(h)}</th>\n"
        html_content += """              </tr>
            </thead>
            <tbody>
"""
        for row in t['rows']:
            html_content += "              <tr>\n"
            for col_idx, col in enumerate(row):
                if col_idx == 0:
                    html_content += f"                <td class=\"row-key-col\">{html.escape(col)}</td>\n"
                else:
                    col_formatted = html.escape(col).replace('\n', '<br>')
                    html_content += f"                <td><div class=\"cell-content-formatted\">{col_formatted}</div></td>\n"
            html_content += "              </tr>\n"
        html_content += """            </tbody>
          </table>
        </div>
        <div style="margin-bottom: 24px;"></div>
"""

    # Handout Scan Showcase
    html_content += f"""
      </div>

      <!-- Scan Showcase Gallery -->
      <footer class="scan-gallery-box">
        <div class="scan-gallery-title">📄 对应原版讲义高清影印（点击查看大图核验）：</div>
        <div class="scan-gallery-items">
"""
    for p_num in b['pages']:
        img_path = f"images/classic-reading/page-{p_num:02d}.jpg"
        html_content += f"""          <div class="scan-item-card" onclick="openModal('{img_path}', '原讲义第 {p_num:02d} 页高清影印')">
            <img src="{img_path}" alt="Page {p_num:02d}" class="scan-item-img" loading="lazy">
            <div class="scan-item-label">第 {p_num:02d} 页</div>
          </div>\n"""

    html_content += """        </div>
      </footer>
    </article>
"""

html_content += """
  </main>

  <!-- Back to Top Button -->
  <a href="#" class="back-top-btn" title="返回顶部">↑</a>

  <!-- Lightbox Modal -->
  <div class="modal-overlay" id="imageModal" onclick="closeModal(event)">
    <div class="modal-dialog" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h4 class="modal-title" id="modalTitle">原版讲义影印</h4>
        <button class="modal-close-btn" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <img src="" id="modalImg" class="modal-img-full" alt="Full Preview">
      </div>
    </div>
  </div>

  <script>
    // Lightbox modal logic
    function openModal(imgSrc, title) {
      document.getElementById('modalImg').src = imgSrc;
      document.getElementById('modalTitle').textContent = title;
      document.getElementById('imageModal').classList.add('active');
    }

    function closeModal() {
      document.getElementById('imageModal').classList.remove('active');
    }

    // Escape key closes modal
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeModal();
    });

    // Real-time Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function(e) {
      const q = e.target.value.trim().toLowerCase();
      const sections = document.querySelectorAll('.book-section');

      sections.forEach(sec => {
        if (!q) {
          sec.style.display = 'block';
          // unhighlight
          return;
        }
        const text = sec.textContent.toLowerCase();
        if (text.includes(q)) {
          sec.style.display = 'block';
        } else {
          sec.style.display = 'none';
        }
      });
    });

    // Highlight active pill on scroll
    window.addEventListener('scroll', function() {
      const sections = document.querySelectorAll('.book-section');
      const pills = document.querySelectorAll('.book-pill-link');
      let currentId = '';

      sections.forEach(sec => {
        const top = sec.getBoundingClientRect().top;
        if (top <= 160) {
          currentId = sec.id;
        }
      });

      pills.forEach(pill => {
        if (pill.getAttribute('href') === '#' + currentId) {
          pill.classList.add('active');
        } else {
          pill.classList.remove('active');
        }
      });
    });
  </script>
</body>
</html>
"""

with open('chinese/classic-reading-V4.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated chinese/classic-reading-V4.html!")
