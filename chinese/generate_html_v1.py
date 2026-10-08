import json

with open('/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-data-V1.json', 'r', encoding='utf-8') as f:
    db_data = json.load(f)

json_data_str = json.dumps(db_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>中考名著阅读核心考点全书 (V1) | 39页扫描真迹全真提取</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700;900&family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-page: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --border-color: #E2E8F0;
      --border-hover: #CBD5E1;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --text-soft: #334155;
      
      --brand-red: #DC2626;
      --brand-red-light: #FEE2E2;
      --brand-red-text: #991B1B;
      
      --brand-blue: #2563EB;
      --brand-blue-light: #EFF6FF;
      --brand-blue-text: #1E40AF;
      
      --brand-emerald: #059669;
      --brand-emerald-light: #ECFDF5;
      --brand-emerald-text: #065F46;
      
      --brand-amber: #D97706;
      --brand-amber-light: #FFFBEB;
      --brand-amber-text: #92400E;

      --brand-purple: #7C3AED;
      --brand-purple-light: #F5F3FF;
      --brand-purple-text: #5B21B6;

      --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04);
      --shadow-xl: 0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 8px 10px -6px rgba(15, 23, 42, 0.05);

      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 20px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      background-color: var(--bg-page);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}

    /* 顶部导航 */
    header {{
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: var(--shadow-sm);
    }}
    .header-wrap {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }}
    .brand-group {{
      display: flex;
      align-items: center;
      gap: 1rem;
      text-decoration: none;
      color: inherit;
    }}
    .brand-icon {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, #DC2626, #EF4444);
      color: white;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.3rem;
      font-weight: 800;
      box-shadow: 0 4px 10px rgba(220, 38, 38, 0.25);
    }}
    .brand-info h1 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    }}
    .brand-info p {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 1px;
    }}
    .tag-ver {{
      background: var(--brand-red-light);
      color: var(--brand-red-text);
      font-size: 0.7rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 9999px;
      border: 1px solid #FECACA;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.55rem 1rem;
      border-radius: var(--radius-md);
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .btn-secondary {{
      background: white;
      border-color: var(--border-color);
      color: var(--text-soft);
    }}
    .btn-secondary:hover {{
      background: var(--bg-subtle);
      border-color: var(--border-hover);
      color: var(--text-main);
    }}
    .btn-primary {{
      background: var(--brand-red);
      color: white;
      box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
    }}
    .btn-primary:hover {{
      background: #B91C1C;
      transform: translateY(-1px);
    }}

    /* 主布局 */
    .app-layout {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 1.75rem 1.5rem 5rem 1.5rem;
      display: grid;
      grid-template-columns: 290px 1fr;
      gap: 2rem;
      align-items: start;
    }}

    /* 左侧控制栏与目录 */
    .sidebar {{
      position: sticky;
      top: 5rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      max-height: calc(100vh - 6rem);
      overflow-y: auto;
      padding-right: 0.5rem;
    }}
    .sidebar::-webkit-scrollbar {{
      width: 5px;
    }}
    .sidebar::-webkit-scrollbar-thumb {{
      background: #CBD5E1;
      border-radius: 4px;
    }}

    .control-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
    }}
    .control-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* 搜索栏 */
    .search-box {{
      position: relative;
      margin-bottom: 1rem;
    }}
    .search-input {{
      width: 100%;
      padding: 0.65rem 0.85rem 0.65rem 2.25rem;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      font-size: 0.86rem;
      background: var(--bg-subtle);
      transition: all 0.2s;
      outline: none;
    }}
    .search-input:focus {{
      background: white;
      border-color: var(--brand-red);
      box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
    }}
    .search-icon {{
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 0.9rem;
    }}

    /* 过滤分类药丸 */
    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      margin-bottom: 1rem;
    }}
    .pill {{
      padding: 0.35rem 0.65rem;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
      background: white;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s;
    }}
    .pill:hover {{
      border-color: #CBD5E1;
      color: var(--text-main);
    }}
    .pill.active {{
      background: var(--brand-red);
      border-color: var(--brand-red);
      color: white;
    }}

    /* 模式切换工具 */
    .mode-switch-group {{
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      margin-top: 0.5rem;
    }}
    .mode-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.55rem 0.75rem;
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-soft);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .mode-item:hover {{
      background: #E2E8F0;
    }}
    .mode-item.active {{
      background: var(--brand-blue-light);
      color: var(--brand-blue-text);
      border: 1px solid #BFDBFE;
    }}

    /* 目录列表 */
    .book-toc {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }}
    .toc-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.55rem 0.75rem;
      border-radius: var(--radius-md);
      text-decoration: none;
      color: var(--text-soft);
      font-size: 0.84rem;
      font-weight: 500;
      transition: all 0.15s;
    }}
    .toc-item:hover {{
      background: var(--bg-subtle);
      color: var(--brand-red);
      transform: translateX(3px);
    }}
    .toc-item.active {{
      background: var(--brand-red-light);
      color: var(--brand-red-text);
      font-weight: 700;
    }}
    .toc-badge {{
      font-size: 0.68rem;
      padding: 2px 6px;
      border-radius: 4px;
      background: #E2E8F0;
      color: var(--text-muted);
    }}

    /* 右侧主区域 */
    .main-content {{
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }}

    /* 顶部横幅 Banner */
    .hero-banner {{
      background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 50%, #FEF2F2 100%);
      border: 1px solid #FECACA;
      border-radius: var(--radius-xl);
      padding: 2.2rem 2.5rem;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.3rem 0.75rem;
      background: white;
      border: 1px solid #FECACA;
      border-radius: 9999px;
      color: var(--brand-red);
      font-size: 0.78rem;
      font-weight: 700;
      margin-bottom: 0.85rem;
    }}
    .hero-title {{
      font-family: 'Noto Serif SC', serif;
      font-size: 2rem;
      font-weight: 900;
      color: #7F1D1D;
      letter-spacing: -0.02em;
      line-height: 1.3;
      margin-bottom: 0.6rem;
    }}
    .hero-subtitle {{
      font-size: 0.95rem;
      color: var(--text-soft);
      max-width: 860px;
      line-height: 1.7;
    }}
    .hero-stats-row {{
      display: flex;
      gap: 2rem;
      margin-top: 1.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid rgba(220, 38, 38, 0.15);
      flex-wrap: wrap;
    }}
    .stat-card {{
      display: flex;
      flex-direction: column;
    }}
    .stat-val {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--brand-red);
      line-height: 1;
    }}
    .stat-label {{
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 0.3rem;
      font-weight: 600;
    }}

    /* 名著卡片 Card Container */
    .book-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      overflow: hidden;
      box-shadow: var(--shadow-md);
      transition: border-color 0.2s, box-shadow 0.2s;
      scroll-margin-top: 5.5rem;
    }}
    .book-card:hover {{
      border-color: #CBD5E1;
      box-shadow: var(--shadow-lg);
    }}

    /* 卡片头部 */
    .book-header {{
      padding: 1.5rem 2rem;
      background: #FAFAFA;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .book-title-wrap {{
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .book-num-tag {{
      width: 38px;
      height: 38px;
      border-radius: var(--radius-md);
      background: var(--brand-red-light);
      color: var(--brand-red-text);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.1rem;
      font-family: 'Outfit', sans-serif;
    }}
    .book-title {{
      font-family: 'Noto Serif SC', serif;
      font-size: 1.45rem;
      font-weight: 800;
      color: var(--text-main);
    }}
    .book-strategy {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--brand-red);
      background: white;
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid #FECACA;
      margin-left: 0.5rem;
    }}
    .book-meta-badges {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .badge-grade {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 9999px;
      background: #F1F5F9;
      color: var(--text-soft);
      border: 1px solid #E2E8F0;
    }}
    .badge-new {{
      background: #FEF3C7;
      color: #92400E;
      border-color: #FDE68A;
    }}

    /* 卡片主体 */
    .book-body {{
      padding: 2rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }}

    /* 考点亮点栏 Highlight Bar */
    .exam-highlight-box {{
      background: linear-gradient(to right, #FFFBEB, #FEF2F2);
      border: 1px solid #FDE68A;
      border-left: 4px solid var(--brand-amber);
      border-radius: var(--radius-md);
      padding: 1rem 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}
    .highlight-title {{
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--brand-amber-text);
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .highlight-content {{
      font-size: 0.88rem;
      color: var(--text-soft);
      font-weight: 500;
    }}
    .highlight-quote {{
      font-family: 'Noto Serif SC', serif;
      font-size: 0.86rem;
      color: #78350F;
      font-style: italic;
      border-top: 1px dashed rgba(217, 119, 6, 0.25);
      padding-top: 0.4rem;
      margin-top: 0.2rem;
    }}

    /* 档案栅格 Grid */
    .profile-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }}
    @media (max-width: 900px) {{
      .profile-grid {{ grid-template-columns: 1fr; }}
      .app-layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; max-height: none; }}
    }}
    .profile-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1.15rem;
    }}
    .profile-card-title {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--brand-blue);
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .profile-card-text {{
      font-size: 0.86rem;
      color: var(--text-soft);
      line-height: 1.65;
    }}

    /* 扫描件对照与完整原版文本折叠面板 */
    .accordion-section {{
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      overflow: hidden;
      background: white;
    }}
    .accordion-header {{
      padding: 0.85rem 1.25rem;
      background: #F8FAFC;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-main);
      user-select: none;
      transition: background 0.2s;
    }}
    .accordion-header:hover {{
      background: #F1F5F9;
    }}
    .accordion-content {{
      padding: 1.25rem;
      display: none;
      border-top: 1px solid var(--border-color);
    }}
    .accordion-content.open {{
      display: block;
    }}

    /* 逐页扫描缩略图展示 */
    .page-thumbs-row {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }}
    .page-thumb-item {{
      flex: 0 0 120px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      overflow: hidden;
      background: white;
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
      padding-bottom: 0.4rem;
    }}
    .page-thumb-item:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--brand-red);
    }}
    .page-thumb-item img {{
      width: 100%;
      height: 150px;
      object-fit: cover;
      display: block;
      border-bottom: 1px solid var(--border-color);
    }}
    .page-thumb-title {{
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-muted);
      margin-top: 0.35rem;
    }}

    /* 文本段落展示 */
    .full-lines-box {{
      background: #F8FAFC;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 1rem;
      font-size: 0.86rem;
      line-height: 1.75;
      color: #334155;
      max-height: 380px;
      overflow-y: auto;
      white-space: pre-wrap;
      font-family: inherit;
    }}

    /* 背诵遮罩高亮功能 */
    .recite-mask {{
      background: #E2E8F0;
      color: transparent;
      border-radius: 4px;
      padding: 0 4px;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s;
      display: inline-block;
      margin: 0 2px;
    }}
    .recite-mask:hover {{
      background: #CBD5E1;
    }}
    .recite-mask.revealed {{
      background: #FEF3C7;
      color: #92400E;
      font-weight: 600;
    }}

    /* 高清大图弹窗 Modal */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }}
    .modal-overlay.active {{
      display: flex;
    }}
    .modal-box {{
      background: white;
      border-radius: var(--radius-lg);
      max-width: 900px;
      width: 100%;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-xl);
      overflow: hidden;
    }}
    .modal-header {{
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .modal-header h3 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .modal-body {{
      padding: 1rem;
      overflow-y: auto;
      text-align: center;
      background: #F8FAFC;
    }}
    .modal-body img {{
      max-width: 100%;
      height: auto;
      box-shadow: var(--shadow-sm);
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }}
    .modal-footer {{
      padding: 0.85rem 1.5rem;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* 页脚 */
    footer {{
      background: white;
      border-top: 1px solid var(--border-color);
      padding: 2.5rem 1.5rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: 4rem;
    }}
  </style>
</head>
<body>

  <!-- 顶部导航 -->
  <header>
    <div class="header-wrap">
      <a href="chinese.html" class="brand-group">
        <div class="brand-icon">典</div>
        <div class="brand-info">
          <h1>中考名著阅读核心考点全书 <span class="tag-ver">V1 全真版</span></h1>
          <p>39页内部冲刺讲义全提取 · 统编初中语文16部核心名著（含新考纲新增）</p>
        </div>
      </a>
      <div class="header-actions">
        <button class="btn btn-secondary" id="toggleReciteBtn" onclick="toggleReciteMode()">
          <span>🧠</span> 背诵自测模式
        </button>
        <a href="chinese.html" class="btn btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          返回复习中心
        </a>
      </div>
    </div>
  </header>

  <!-- 页面主体容器 -->
  <div class="app-layout">

    <!-- 左侧控制面板与目录 -->
    <aside class="sidebar">
      
      <!-- 搜索与筛选控制 -->
      <div class="control-card">
        <div class="control-title">
          <span>考点速查检索</span>
          <span id="matchCountBadge" style="font-size: 0.72rem; color: var(--brand-red);">16 部</span>
        </div>
        
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="搜人物/情节/名著/考点..." oninput="handleSearch()">
        </div>

        <div class="filter-pills">
          <button class="pill active" onclick="filterGrade('all', this)">全部 16 部</button>
          <button class="pill" onclick="filterGrade('七年级', this)">七年级</button>
          <button class="pill" onclick="filterGrade('八年级', this)">八年级</button>
          <button class="pill" onclick="filterGrade('九年级', this)">九年级</button>
          <button class="pill" onclick="filterGrade('新增', this)">统编新增</button>
        </div>
      </div>

      <!-- 快速导航目录 -->
      <div class="control-card">
        <div class="control-title">
          <span>名著导航目录 (16部)</span>
          <span style="font-size: 0.72rem;">共39页</span>
        </div>
        <nav class="book-toc" id="tocContainer">
          <!-- 动态生成 TOC 链接 -->
        </nav>
      </div>

    </aside>

    <!-- 右侧内容主区 -->
    <main class="main-content">

      <!-- Hero Banner -->
      <section class="hero-banner">
        <div class="hero-badge">
          <span>📘</span> 统编版初中语文 2026 中考考纲重点
        </div>
        <h2 class="hero-title">中考名著阅读 39页核心考点全书</h2>
        <p class="hero-subtitle">
          依据《中考名著阅读考点整理（含新增）》全本39页高清扫描件无损提取，覆盖统编初中语文六册全部16部必读与选读名著，囊括作者简介、主要内容、核心人物谱系、典型情节梳理、艺术特色与中考高频真题考法。
        </p>
        <div class="hero-stats-row">
          <div class="stat-card">
            <span class="stat-val">39</span>
            <span class="stat-label">扫描讲义全真页码</span>
          </div>
          <div class="stat-card">
            <span class="stat-val">16</span>
            <span class="stat-label">部经典名著专栏</span>
          </div>
          <div class="stat-card">
            <span class="stat-val">31,700+</span>
            <span class="stat-label">提取考点字数</span>
          </div>
          <div class="stat-card">
            <span class="stat-val">2</span>
            <span class="stat-label">部统编新教材新增篇目</span>
          </div>
        </div>
      </section>

      <!-- 名著列表容器 -->
      <div id="booksContainer" style="display: flex; flex-direction: column; gap: 2rem;">
        <!-- JS 动态渲染各名著卡片 -->
      </div>

    </main>

  </div>

  <!-- 高清影印扫描件预览模态框 -->
  <div class="modal-overlay" id="pageModal" onclick="closeModal(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 id="modalTitle">原稿影印页查看</h3>
        <button class="btn btn-secondary" style="padding: 0.3rem 0.6rem;" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <img id="modalImg" src="" alt="原稿扫描件">
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="prevModalPage()">上一页</button>
        <span id="modalPageIndicator" style="font-size: 0.85rem; font-weight: 600; color: var(--text-muted);">第 1 / 39 页</span>
        <button class="btn btn-secondary" onclick="nextModalPage()">下一页</button>
      </div>
    </div>
  </div>

  <footer>
    <p>© 2026 初中语文复习中心 · 中考名著阅读核心考点全书 (V1)</p>
    <p style="margin-top: 4px; font-size: 0.78rem;">浅色商务风格 · 39页扫描真迹图文对照 · 支持离线全屏速记</p>
  </footer>

  <!-- 数据注入 -->
  <script>
    const DB = {json_data_str};
    let currentGradeFilter = 'all';
    let currentSearchTerm = '';
    let isReciteMode = false;
    let currentModalPage = 1;

    // 初始化渲染
    document.addEventListener('DOMContentLoaded', () => {{
      renderTOC();
      renderBooks();
    }});

    // 渲染 TOC 目录
    function renderTOC() {{
      const container = document.getElementById('tocContainer');
      container.innerHTML = DB.books.map((b, idx) => `
        <a href="#book-${{b.id}}" class="toc-item" data-grade="${{b.grade}}" id="toc-${{b.id}}">
          <span>${{b.index}}、${{b.title}}</span>
          <span class="toc-badge">${{b.grade}}</span>
        </a>
      `).join('');
    }}

    // 渲染名著卡片
    function renderBooks() {{
      const container = document.getElementById('booksContainer');
      const filtered = DB.books.filter(b => {{
        // 年级过滤
        let gradeMatch = true;
        if (currentGradeFilter === '七年级') gradeMatch = b.grade.includes('七');
        else if (currentGradeFilter === '八年级') gradeMatch = b.grade.includes('八') && !b.grade.includes('新增');
        else if (currentGradeFilter === '九年级') gradeMatch = b.grade.includes('九') && !b.grade.includes('新增');
        else if (currentGradeFilter === '新增') gradeMatch = b.grade.includes('新增');

        // 搜索过滤
        let searchMatch = true;
        if (currentSearchTerm) {{
          const term = currentSearchTerm.toLowerCase();
          const target = (b.title + b.author + b.full_text + (b.highlight ? b.highlight.focus : '')).toLowerCase();
          searchMatch = target.includes(term);
        }}
        return gradeMatch && searchMatch;
      }});

      document.getElementById('matchCountBadge').innerText = `${{filtered.length}} 部`;

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div style="background: white; border: 1px dashed var(--border-color); border-radius: var(--radius-lg); padding: 3rem; text-align: center; color: var(--text-muted);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <div style="font-size: 1rem; font-weight: 600;">未找到与 "${{currentSearchTerm}}" 相关的考点</div>
            <div style="font-size: 0.82rem; margin-top: 0.25rem;">建议缩短关键词或尝试角色名（如“保尔”、“范进”、“江姐”）</div>
          </div>
        `;
        return;
      }}

      container.innerHTML = filtered.map(b => {{
        const pagesText = b.pages.map(p => `P${{p < 10 ? '0' + p : p}}`).join('、');
        const thumbsHtml = b.pages_data.map(p => `
          <div class="page-thumb-item" onclick="openModal(${{p.page_num}})">
            <img src="${{p.image}}" alt="第${{p.page_num}}页影印件" loading="lazy">
            <div class="page-thumb-title">第 ${{p.page_num}} 页</div>
          </div>
        `).join('');

        const isNewBook = b.grade.includes('新增');

        return `
          <article class="book-card" id="book-${{b.id}}">
            <div class="book-header">
              <div class="book-title-wrap">
                <div class="book-num-tag">${{b.index}}</div>
                <div>
                  <span class="book-title">${{b.title}}</span>
                  <span class="book-strategy">${{b.subtitle}}</span>
                </div>
              </div>
              <div class="book-meta-badges">
                <span class="badge-grade ${{isNewBook ? 'badge-new' : ''}}">${{b.grade}}</span>
                <span class="badge-grade" style="background: white; border-color: #CBD5E1;">讲义 ${{pagesText}}</span>
                <button class="btn btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.78rem;" onclick="openModal(${{b.pages[0]}})">
                  📷 查看原稿图
                </button>
              </div>
            </div>

            <div class="book-body">
              ${{b.highlight ? `
                <div class="exam-highlight-box">
                  <div class="highlight-title">🎯 中考核心聚焦 · 提分必背</div>
                  <div class="highlight-content">${{applyReciteMask(b.highlight.focus)}}</div>
                  <div class="highlight-quote">${{applyReciteMask(b.highlight.quotes)}}</div>
                </div>
              ` : ''}}

              <div class="profile-grid">
                <div class="profile-card">
                  <div class="profile-card-title">
                    <span>✍️</span> 作者档案与文学常识
                  </div>
                  <div class="profile-card-text">
                    <strong>${{b.author}}</strong>：${{applyReciteMask(b.author_desc)}}
                  </div>
                </div>
                <div class="profile-card">
                  <div class="profile-card-title">
                    <span>📖</span> 考纲分类与阅读策略
                  </div>
                  <div class="profile-card-text">
                    <strong>体裁属性：</strong>${{b.category}}<br>
                    <strong>考纲要求：</strong>掌握《${{b.title}}》主要情节与经典人物，熟练运用“${{b.subtitle}}”阅读策略。
                  </div>
                </div>
              </div>

              <!-- 原稿影印件速查与完整提取文本面板 -->
              <div class="accordion-section">
                <div class="accordion-header" onclick="toggleAccordion(this)">
                  <span>🖼️ 本书原版 39 页高清影印件速查 (共 ${{b.pages.length}} 页)</span>
                  <span class="acc-arrow">▼</span>
                </div>
                <div class="accordion-content">
                  <div class="page-thumbs-row">
                    ${{thumbsHtml}}
                  </div>
                  <div style="font-size: 0.78rem; color: var(--text-muted);">
                    💡 点击任意缩略图可开启高清放大镜浏览原扫描稿。
                  </div>
                </div>
              </div>

              <!-- 全真逐行提取文字库折叠面板 -->
              <div class="accordion-section">
                <div class="accordion-header" onclick="toggleAccordion(this)">
                  <span>📑 本书 39 页原版逐行全真提取内容 (${{b.full_text.length}} 字)</span>
                  <span class="acc-arrow">▼</span>
                </div>
                <div class="accordion-content">
                  <div class="full-lines-box">${{applyReciteMask(b.full_text)}}</div>
                </div>
              </div>

            </div>
          </article>
        `;
      }}).join('');
    }}

    // 折叠展开
    function toggleAccordion(header) {{
      const content = header.nextElementSibling;
      const arrow = header.querySelector('.acc-arrow');
      content.classList.toggle('open');
      arrow.innerText = content.classList.contains('open') ? '▲' : '▼';
    }}

    // 分类筛选
    function filterGrade(grade, btn) {{
      currentGradeFilter = grade;
      document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      renderBooks();
    }}

    // 搜索输入
    function handleSearch() {{
      currentSearchTerm = document.getElementById('searchInput').value.trim();
      renderBooks();
    }}

    // 背诵挖空自测模式
    function toggleReciteMode() {{
      isReciteMode = !isReciteMode;
      const btn = document.getElementById('toggleReciteBtn');
      if (isReciteMode) {{
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
        btn.innerHTML = '<span>👀</span> 退出背诵模式';
      }} else {{
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
        btn.innerHTML = '<span>🧠</span> 背诵自测模式';
      }}
      renderBooks();
    }}

    // 应用挖空效果
    function applyReciteMask(text) {{
      if (!text) return '';
      if (!isReciteMode) return escapeHtml(text);

      // 提取核心关键词进行遮蔽
      const keywords = [
        '高尔基', '阿廖沙', '外祖父', '外祖母', '小茨冈', '好事情',
        '丹尼尔·笛福', '星期五', '鲁滨逊',
        '鲁迅', '百草园', '三味书屋', '阿长', '山海经', '藤野先生', '范爱农',
        '吴承恩', '孙悟空', '唐僧', '猪八戒', '沙僧', '白龙马',
        '老舍', '祥子', '虎妞', '小福子', '曹先生', '刘四爷',
        '凡尔纳', '尼摩船长', '诺第留斯号', '阿龙纳斯',
        '斯诺', '毛泽东', '周恩来', '彭德怀', '红军', '长征',
        '法布尔', '螳螂', '蟋蟀', '蝉',
        '朱自清', '说文解字', '春秋', '史记', '汉书',
        '保尔·柯察金', '奥斯特洛夫斯基', '冬妮亚', '丽达', '朱赫来',
        '艾青', '土地', '光明', '大堰河',
        '施耐庵', '鲁智深', '林冲', '宋江', '李逵', '武松',
        '吴敬梓', '范进', '周进', '严监生', '匡超人', '杜少卿',
        '夏洛蒂·勃朗特', '简·爱', '罗切斯特',
        '罗广斌', '杨益言', '江姐', '许云峰', '小萝卜头', '成岗', '绣红旗',
        '孙洙', '蘅塘退士', '唐诗三百首', '杜甫', '李白', '王维'
      ];

      let escaped = escapeHtml(text);
      keywords.forEach(kw => {{
        const reg = new RegExp(kw, 'g');
        escaped = escaped.replace(reg, `<span class="recite-mask" onclick="this.classList.toggle('revealed')">${{kw}}</span>`);
      }});
      return escaped;
    }}

    function escapeHtml(str) {{
      return str.replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
    }}

    // 高清弹窗查看
    function openModal(pageNum) {{
      currentModalPage = pageNum;
      updateModalView();
      document.getElementById('pageModal').classList.add('active');
    }}

    function closeModal(e) {{
      document.getElementById('pageModal').classList.remove('active');
    }}

    function updateModalView() {{
      const numStr = currentModalPage < 10 ? '0' + currentModalPage : '' + currentModalPage;
      document.getElementById('modalImg').src = `images/classic-reading/page-${{numStr}}.jpg`;
      document.getElementById('modalTitle').innerText = `《中考名著考点整理》第 ${{currentModalPage}} 页 扫描原稿`;
      document.getElementById('modalPageIndicator').innerText = `第 ${{currentModalPage}} / 39 页`;
    }}

    function prevModalPage() {{
      if (currentModalPage > 1) {{
        currentModalPage--;
        updateModalView();
      }}
    }}

    function nextModalPage() {{
      if (currentModalPage < 39) {{
        currentModalPage++;
        updateModalView();
      }}
    }}

    // 键盘支持
    document.addEventListener('keydown', (e) => {{
      if (document.getElementById('pageModal').classList.contains('active')) {{
        if (e.key === 'ArrowLeft') prevModalPage();
        if (e.key === 'ArrowRight') nextModalPage();
        if (e.key === 'Escape') closeModal();
      }}
    }});
  </script>
</body>
</html>
'''

output_file = '/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-V1.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated {output_file} successfully! File size: {len(html_content)} bytes")
