import json
import re

with open('/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-data-V1.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 编写精美 HTML 生成器
def build_html():
    books_json = json.dumps(db['books'], ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>初中语文中考名著阅读核心考点全书 (V1) | 39页讲义全真提取</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700;900&family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-page: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --border-color: #E2E8F0;
      --border-focus: #CBD5E1;
      --text-main: #0F172A;
      --text-soft: #334155;
      --text-muted: #64748B;
      
      --brand-red: #DC2626;
      --brand-red-light: #FEF2F2;
      --brand-red-border: #FEE2E2;
      
      --brand-blue: #2563EB;
      --brand-blue-light: #EFF6FF;
      --brand-blue-border: #DBEAFE;
      
      --brand-amber: #D97706;
      --brand-amber-light: #FFFBEB;
      --brand-amber-border: #FEF3C7;

      --brand-emerald: #059669;
      --brand-emerald-light: #ECFDF5;
      --brand-emerald-border: #A7F3D0;

      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
      --shadow-md: 0 4px 10px -2px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
      --shadow-lg: 0 12px 24px -4px rgba(15, 23, 42, 0.08);

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

    /* 顶栏 */
    header {{
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: var(--shadow-sm);
    }}
    .nav-wrap {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }}
    .brand-link {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
      text-decoration: none;
      color: inherit;
    }}
    .brand-icon {{
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #DC2626, #EF4444);
      color: white;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      font-weight: 800;
      box-shadow: 0 4px 10px rgba(220, 38, 38, 0.22);
    }}
    .brand-text h1 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-family: 'Outfit', sans-serif;
    }}
    .brand-text p {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 1px;
    }}
    .ver-badge {{
      background: var(--brand-red-light);
      color: var(--brand-red);
      border: 1px solid var(--brand-red-border);
      font-size: 0.7rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 9999px;
    }}

    .header-btns {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.55rem 1.05rem;
      border-radius: var(--radius-md);
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.18s ease;
    }}
    .btn-secondary {{
      background: white;
      border-color: var(--border-color);
      color: var(--text-soft);
    }}
    .btn-secondary:hover {{
      background: var(--bg-subtle);
      border-color: var(--border-focus);
      color: var(--text-main);
    }}
    .btn-primary {{
      background: var(--brand-red);
      color: white;
    }}
    .btn-primary:hover {{
      background: #B91C1C;
      transform: translateY(-1px);
    }}

    /* 主布局 */
    .app-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 2rem 1.5rem 5rem 1.5rem;
      display: grid;
      grid-template-columns: 310px 1fr;
      gap: 2rem;
      align-items: start;
    }}

    /* 侧边栏 */
    .sidebar {{
      position: sticky;
      top: 5rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
      max-height: calc(100vh - 6.5rem);
      overflow-y: auto;
      padding-right: 0.35rem;
    }}
    .sidebar::-webkit-scrollbar {{
      width: 4px;
    }}
    .sidebar::-webkit-scrollbar-thumb {{
      background: #CBD5E1;
      border-radius: 4px;
    }}

    .panel-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
    }}
    .panel-header {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* 搜索框 */
    .search-wrap {{
      position: relative;
      margin-bottom: 0.85rem;
    }}
    .search-input {{
      width: 100%;
      padding: 0.65rem 0.85rem 0.65rem 2.2rem;
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
      box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.08);
    }}
    .search-icon {{
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 0.88rem;
    }}

    /* 过滤分类药丸 */
    .filter-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
    }}
    .filter-btn {{
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
    .filter-btn:hover {{
      border-color: #CBD5E1;
      color: var(--text-main);
    }}
    .filter-btn.active {{
      background: var(--brand-red);
      border-color: var(--brand-red);
      color: white;
    }}

    /* 目录列表 */
    .toc-list {{
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
    }}
    .toc-node {{
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
    .toc-node:hover {{
      background: var(--bg-subtle);
      color: var(--brand-red);
      transform: translateX(2px);
    }}
    .toc-node.active {{
      background: var(--brand-red-light);
      color: var(--brand-red);
      font-weight: 700;
    }}
    .toc-tag {{
      font-size: 0.68rem;
      padding: 2px 6px;
      border-radius: 4px;
      background: var(--bg-subtle);
      color: var(--text-muted);
    }}

    /* 内容主区 */
    .content-area {{
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }}

    /* Hero Banner */
    .hero-box {{
      background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 45%, #FEF2F2 100%);
      border: 1px solid #FECACA;
      border-radius: var(--radius-xl);
      padding: 2.2rem 2.5rem;
      box-shadow: var(--shadow-sm);
      position: relative;
    }}
    .hero-top-badge {{
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
    .hero-headline {{
      font-family: 'Noto Serif SC', serif;
      font-size: 2.1rem;
      font-weight: 900;
      color: #7F1D1D;
      letter-spacing: -0.01em;
      line-height: 1.25;
      margin-bottom: 0.6rem;
    }}
    .hero-desc {{
      font-size: 0.95rem;
      color: var(--text-soft);
      max-width: 900px;
      line-height: 1.7;
    }}
    .hero-metrics {{
      display: flex;
      gap: 2.5rem;
      margin-top: 1.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid rgba(220, 38, 38, 0.12);
      flex-wrap: wrap;
    }}
    .metric-col {{
      display: flex;
      flex-direction: column;
    }}
    .metric-num {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--brand-red);
      line-height: 1;
    }}
    .metric-label {{
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 0.35rem;
      font-weight: 600;
    }}

    /* 快捷功能悬浮条 */
    .action-bar {{
      background: white;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 0.85rem 1.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: var(--shadow-sm);
      flex-wrap: wrap;
      gap: 0.75rem;
    }}
    .action-bar-left {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-soft);
    }}

    /* 名著卡片 */
    .book-block {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      scroll-margin-top: 5rem;
    }}
    .book-block:hover {{
      border-color: #CBD5E1;
      box-shadow: var(--shadow-md);
    }}

    .book-block-header {{
      padding: 1.5rem 2rem;
      background: #FAFAFA;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .book-title-cell {{
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .book-index-badge {{
      width: 40px;
      height: 40px;
      border-radius: var(--radius-md);
      background: var(--brand-red-light);
      color: var(--brand-red);
      border: 1px solid var(--brand-red-border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.15rem;
      font-family: 'Outfit', sans-serif;
    }}
    .book-name {{
      font-family: 'Noto Serif SC', serif;
      font-size: 1.45rem;
      font-weight: 900;
      color: var(--text-main);
    }}
    .book-tactic {{
      font-size: 0.84rem;
      font-weight: 600;
      color: var(--brand-red);
      background: white;
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid #FECACA;
      margin-left: 0.4rem;
    }}
    .book-header-right {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .tag-bubble {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 9999px;
      background: var(--bg-subtle);
      color: var(--text-soft);
      border: 1px solid var(--border-color);
    }}
    .tag-bubble-new {{
      background: var(--brand-amber-light);
      color: var(--brand-amber);
      border-color: var(--brand-amber-border);
    }}

    .book-block-body {{
      padding: 2rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }}

    /* 重点考点摘要 */
    .focus-card {{
      background: linear-gradient(to right, #FFFBEB, #FEF2F2);
      border: 1px solid #FDE68A;
      border-left: 4px solid var(--brand-amber);
      border-radius: var(--radius-md);
      padding: 1.1rem 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }}
    .focus-title {{
      font-size: 0.82rem;
      font-weight: 800;
      color: #92400E;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .focus-desc {{
      font-size: 0.88rem;
      color: var(--text-soft);
      font-weight: 500;
      line-height: 1.6;
    }}
    .focus-quote {{
      font-family: 'Noto Serif SC', serif;
      font-size: 0.86rem;
      color: #78350F;
      font-style: italic;
      border-top: 1px dashed rgba(217, 119, 6, 0.2);
      padding-top: 0.45rem;
      margin-top: 0.15rem;
    }}

    /* 档案栅格 */
    .info-dual-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }}
    .info-cell {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1.25rem;
    }}
    .info-cell-title {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--brand-blue);
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .info-cell-content {{
      font-size: 0.86rem;
      color: var(--text-soft);
      line-height: 1.65;
    }}

    /* 逐页影印件与全真文本卡片 */
    .expand-card {{
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      overflow: hidden;
      background: white;
    }}
    .expand-head {{
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
      transition: background 0.15s;
    }}
    .expand-head:hover {{
      background: #F1F5F9;
    }}
    .expand-body {{
      padding: 1.25rem;
      display: none;
      border-top: 1px solid var(--border-color);
    }}
    .expand-body.open {{
      display: block;
    }}

    .scans-row {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-bottom: 0.75rem;
    }}
    .scan-item {{
      flex: 0 0 125px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      overflow: hidden;
      background: white;
      cursor: pointer;
      transition: all 0.2s;
      text-align: center;
      padding-bottom: 0.4rem;
    }}
    .scan-item:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--brand-red);
    }}
    .scan-item img {{
      width: 100%;
      height: 155px;
      object-fit: cover;
      display: block;
      border-bottom: 1px solid var(--border-color);
    }}
    .scan-item-label {{
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-muted);
      margin-top: 0.35rem;
    }}

    .raw-text-view {{
      background: #F8FAFC;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 1rem 1.25rem;
      font-size: 0.86rem;
      line-height: 1.8;
      color: #334155;
      max-height: 420px;
      overflow-y: auto;
      white-space: pre-wrap;
    }}

    /* 背诵挖空交互 */
    .recite-blank {{
      background: #E2E8F0;
      color: transparent;
      border-radius: 4px;
      padding: 0 4px;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s;
      display: inline-block;
      margin: 0 2px;
      font-weight: 600;
    }}
    .recite-blank:hover {{
      background: #CBD5E1;
    }}
    .recite-blank.opened {{
      background: #FEF3C7;
      color: #92400E;
    }}

    /* 模态弹窗 */
    .img-modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(5px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}
    .img-modal-backdrop.show {{
      display: flex;
    }}
    .img-modal-window {{
      background: white;
      border-radius: var(--radius-lg);
      max-width: 960px;
      width: 100%;
      max-height: 92vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
      overflow: hidden;
    }}
    .img-modal-top {{
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .img-modal-top h3 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
    }}
    .img-modal-body {{
      padding: 1.25rem;
      overflow-y: auto;
      text-align: center;
      background: #F1F5F9;
    }}
    .img-modal-body img {{
      max-width: 100%;
      height: auto;
      border-radius: var(--radius-sm);
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border-color);
    }}
    .img-modal-bar {{
      padding: 0.85rem 1.5rem;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    footer {{
      background: white;
      border-top: 1px solid var(--border-color);
      padding: 2.5rem 1.5rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: 4rem;
    }}

    @media (max-width: 1024px) {{
      .app-container {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; max-height: none; }}
      .info-dual-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <!-- 顶部导航 -->
  <header>
    <div class="nav-wrap">
      <a href="chinese.html" class="brand-link">
        <div class="brand-icon">典</div>
        <div class="brand-text">
          <h1>中考名著阅读核心考点全书 <span class="ver-badge">V1 全真版</span></h1>
          <p>39页讲义全部提取 · 统编初中语文16部名著全面覆盖（含新教材新增）</p>
        </div>
      </a>
      <div class="header-btns">
        <button class="btn btn-secondary" id="reciteSwitch" onclick="toggleReciteMode()">
          <span>🧠</span> 背诵自测模式
        </button>
        <a href="chinese.html" class="btn btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          返回复习中心
        </a>
      </div>
    </div>
  </header>

  <!-- 主体区域 -->
  <div class="app-container">

    <!-- 侧边栏控制面板 -->
    <aside class="sidebar">
      
      <div class="panel-card">
        <div class="panel-header">
          <span>考点速查与检索</span>
          <span id="statFound" style="color: var(--brand-red); font-size: 0.72rem;">16 部名著</span>
        </div>
        
        <div class="search-wrap">
          <span class="search-icon">🔍</span>
          <input type="text" id="filterInput" class="search-input" placeholder="输入人物/情节/名著/考点..." oninput="onSearchChange()">
        </div>

        <div class="filter-group">
          <button class="filter-btn active" onclick="setGradeFilter('all', this)">全部 (16)</button>
          <button class="filter-btn" onclick="setGradeFilter('七年级', this)">七年级</button>
          <button class="filter-btn" onclick="setGradeFilter('八年级', this)">八年级</button>
          <button class="filter-btn" onclick="setGradeFilter('九年级', this)">九年级</button>
          <button class="filter-btn" onclick="setGradeFilter('新增', this)">统编新增</button>
        </div>
      </div>

      <div class="panel-card">
        <div class="panel-header">
          <span>16 部名著考点导航</span>
          <span style="font-size: 0.72rem;">全书 39 页</span>
        </div>
        <nav class="toc-list" id="tocWrapper">
          <!-- 动态渲染导航项 -->
        </nav>
      </div>

    </aside>

    <!-- 主展示区 -->
    <main class="content-area">

      <!-- 顶部 Banner -->
      <section class="hero-box">
        <div class="hero-top-badge">
          <span>🎯</span> 2026 中考语文冲刺核心考点图谱
        </div>
        <h2 class="hero-headline">中考名著阅读 39页全真考点全书</h2>
        <p class="hero-desc">
          本库依据《【语文】39页中考名著阅读考点整理（含新增）（内部）》扫描原件进行全真数字化提取。包含统编初中语文全六册16本中考必考名著，逐字逐句提炼作者档案、主要内容、人物辨识与形象分析、经典回目情节、思想主题、艺术特色与中考高频考向。支持背诵自测与高清原稿图文对照。
        </p>
        <div class="hero-metrics">
          <div class="metric-col">
            <span class="metric-num">39</span>
            <span class="metric-label">扫描讲义全真页码</span>
          </div>
          <div class="metric-col">
            <span class="metric-num">16</span>
            <span class="metric-label">部经典名著专栏</span>
          </div>
          <div class="metric-col">
            <span class="metric-num">31,700+</span>
            <span class="metric-label">提取考点字数</span>
          </div>
          <div class="metric-col">
            <span class="metric-num">2</span>
            <span class="metric-label">部统编新教材新增篇目</span>
          </div>
        </div>
      </section>

      <!-- 快捷操作栏 -->
      <div class="action-bar">
        <div class="action-bar-left">
          <span>📖 复习模式：</span>
          <span id="modeDescription" style="color: var(--brand-red);">全景考点精研 + 原版讲义随时对照</span>
        </div>
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;" onclick="expandAllSections(true)">
            全部展开
          </button>
          <button class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;" onclick="expandAllSections(false)">
            全部折叠
          </button>
        </div>
      </div>

      <!-- 名著列表 -->
      <div id="booksWrapper" style="display: flex; flex-direction: column; gap: 2rem;">
        <!-- JS 动态渲染各名著卡片 -->
      </div>

    </main>

  </div>

  <!-- 原版扫描件全屏大图预览弹窗 -->
  <div class="img-modal-backdrop" id="imgModal" onclick="closeImgModal(event)">
    <div class="img-modal-window" onclick="event.stopPropagation()">
      <div class="img-modal-top">
        <h3 id="modalPageTitle">原版扫描件对照预览</h3>
        <button class="btn btn-secondary" style="padding: 0.3rem 0.6rem;" onclick="closeImgModal()">✕</button>
      </div>
      <div class="img-modal-body">
        <img id="modalPagePic" src="" alt="扫描件">
      </div>
      <div class="img-modal-bar">
        <button class="btn btn-secondary" onclick="stepModalPage(-1)">上一页</button>
        <span id="modalPageNum" style="font-size: 0.86rem; font-weight: 600; color: var(--text-muted);">第 1 / 39 页</span>
        <button class="btn btn-secondary" onclick="stepModalPage(1)">下一页</button>
      </div>
    </div>
  </div>

  <footer>
    <p>© 2026 初中语文复习中心 · 中考名著阅读核心考点全书 (V1)</p>
    <p style="margin-top: 4px; font-size: 0.78rem;">浅色商务风格 · 39页讲义全真提取 · 支持中考离线全景背诵与原稿对照</p>
  </footer>

  <script>
    const BOOKS_DB = {books_json};
    let activeGrade = 'all';
    let searchKeyword = '';
    let isReciting = false;
    let modalPage = 1;

    document.addEventListener('DOMContentLoaded', () => {{
      renderTocNav();
      renderBooksList();
    }});

    function renderTocNav() {{
      const el = document.getElementById('tocWrapper');
      el.innerHTML = BOOKS_DB.map(b => `
        <a href="#book-${{b.id}}" class="toc-node" data-grade="${{b.grade}}" id="toc-item-${{b.id}}">
          <span>${{b.index}}、${{b.title}}</span>
          <span class="toc-tag">${{b.grade}}</span>
        </a>
      `).join('');
    }}

    function renderBooksList() {{
      const wrapper = document.getElementById('booksWrapper');
      const filtered = BOOKS_DB.filter(b => {{
        let gOk = true;
        if (activeGrade === '七年级') gOk = b.grade.includes('七');
        else if (activeGrade === '八年级') gOk = b.grade.includes('八') && !b.grade.includes('新增');
        else if (activeGrade === '九年级') gOk = b.grade.includes('九') && !b.grade.includes('新增');
        else if (activeGrade === '新增') gOk = b.grade.includes('新增');

        let sOk = true;
        if (searchKeyword) {{
          const term = searchKeyword.toLowerCase();
          const bag = (b.title + b.author + b.full_text + (b.highlight ? b.highlight.focus : '')).toLowerCase();
          sOk = bag.includes(term);
        }}
        return gOk && sOk;
      }});

      document.getElementById('statFound').innerText = `${{filtered.length}} 部名著`;

      if (filtered.length === 0) {{
        wrapper.innerHTML = `
          <div style="background: white; border: 1px dashed var(--border-color); border-radius: var(--radius-lg); padding: 3rem; text-align: center; color: var(--text-muted);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <div style="font-size: 1rem; font-weight: 600;">未找到与 "${{searchKeyword}}" 相关的名著考点</div>
            <div style="font-size: 0.82rem; margin-top: 0.35rem;">请尝试搜索人物（如保尔、范进、鲁智深、江姐、阿廖沙）或名著名</div>
          </div>
        `;
        return;
      }}

      wrapper.innerHTML = filtered.map(b => {{
        const pageListText = b.pages.map(p => `P${{p < 10 ? '0' + p : p}}`).join('、');
        const thumbs = b.pages_data.map(p => `
          <div class="scan-item" onclick="openScanModal(${{p.page_num}})">
            <img src="${{p.image}}" alt="第${{p.page_num}}页扫描件" loading="lazy">
            <div class="scan-item-label">第 ${{p.page_num}} 页</div>
          </div>
        `).join('');

        const isNew = b.grade.includes('新增');

        return `
          <article class="book-block" id="book-${{b.id}}">
            <div class="book-block-header">
              <div class="book-title-cell">
                <div class="book-index-badge">${{b.index}}</div>
                <div>
                  <span class="book-name">${{b.title}}</span>
                  <span class="book-tactic">${{b.subtitle}}</span>
                </div>
              </div>
              <div class="book-header-right">
                <span class="tag-bubble ${{isNew ? 'tag-bubble-new' : ''}}">${{b.grade}}</span>
                <span class="tag-bubble" style="background: white;">讲义 ${{pageListText}}</span>
                <button class="btn btn-secondary" style="padding: 0.32rem 0.75rem; font-size: 0.78rem;" onclick="openScanModal(${{b.pages[0]}})">
                  📷 讲义图
                </button>
              </div>
            </div>

            <div class="book-block-body">
              ${{b.highlight ? `
                <div class="focus-card">
                  <div class="focus-title">🎯 中考核心聚焦 · 提分必背</div>
                  <div class="focus-desc">${{maskText(b.highlight.focus)}}</div>
                  <div class="focus-quote">${{maskText(b.highlight.quotes)}}</div>
                </div>
              ` : ''}}

              <div class="info-dual-grid">
                <div class="info-cell">
                  <div class="info-cell-title">
                    <span>✍️</span> 作者档案与文学常识
                  </div>
                  <div class="info-cell-content">
                    <strong>${{b.author}}</strong>：${{maskText(b.author_desc)}}
                  </div>
                </div>
                <div class="info-cell">
                  <div class="info-cell-title">
                    <span>📖</span> 考纲分类与阅读策略
                  </div>
                  <div class="info-cell-content">
                    <strong>体裁属性：</strong>${{b.category}}<br>
                    <strong>阅读策略：</strong>运用“${{b.subtitle}}”方法，熟练掌握《${{b.title}}》的核心人物、关键情节与主题意蕴。
                  </div>
                </div>
              </div>

              <!-- 讲义影印件预览 -->
              <div class="expand-card">
                <div class="expand-head" onclick="toggleExpand(this)">
                  <span>🖼️ 本书 39 页原版高清扫描讲义 (共 ${{b.pages.length}} 页)</span>
                  <span class="exp-icon">▼</span>
                </div>
                <div class="expand-body">
                  <div class="scans-row">${{thumbs}}</div>
                  <p style="font-size: 0.78rem; color: var(--text-muted);">
                    💡 点击任意页面缩略图即可进入高清全屏逐页浏览。
                  </p>
                </div>
              </div>

              <!-- 全真逐行提取文字库折叠面板 -->
              <div class="expand-card">
                <div class="expand-head" onclick="toggleExpand(this)">
                  <span>📑 本书 39 页原版全真提取考点内容 (${{b.full_text.length}} 字)</span>
                  <span class="exp-icon">▼</span>
                </div>
                <div class="expand-body">
                  <div class="raw-text-view">${{maskText(b.full_text)}}</div>
                </div>
              </div>

            </div>
          </article>
        `;
      }}).join('');
    }}

    function toggleExpand(head) {{
      const body = head.nextElementSibling;
      const icon = head.querySelector('.exp-icon');
      body.classList.toggle('open');
      icon.innerText = body.classList.contains('open') ? '▲' : '▼';
    }}

    function expandAllSections(open) {{
      document.querySelectorAll('.expand-body').forEach(b => {{
        if (open) b.classList.add('open');
        else b.classList.remove('open');
      }});
      document.querySelectorAll('.exp-icon').forEach(i => {{
        i.innerText = open ? '▲' : '▼';
      }});
    }}

    function setGradeFilter(g, btn) {{
      activeGrade = g;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderBooksList();
    }}

    function onSearchChange() {{
      searchKeyword = document.getElementById('filterInput').value.trim();
      renderBooksList();
    }}

    function toggleReciteMode() {{
      isReciting = !isReciting;
      const btn = document.getElementById('reciteSwitch');
      if (isReciting) {{
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
        btn.innerHTML = '<span>👀</span> 退出背诵模式';
        document.getElementById('modeDescription').innerText = '背诵自测中：点击黄色遮罩揭晓答案';
      }} else {{
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
        btn.innerHTML = '<span>🧠</span> 背诵自测模式';
        document.getElementById('modeDescription').innerText = '全景考点精研 + 原版讲义随时对照';
      }}
      renderBooksList();
    }}

    function maskText(str) {{
      if (!str) return '';
      if (!isReciting) return escapeMarkup(str);

      const keys = [
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

      let res = escapeMarkup(str);
      keys.forEach(k => {{
        const reg = new RegExp(k, 'g');
        res = res.replace(reg, `<span class="recite-blank" onclick="this.classList.toggle('opened')">${{k}}</span>`);
      }});
      return res;
    }}

    function escapeMarkup(str) {{
      return str.replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
    }}

    function openScanModal(pNum) {{
      modalPage = pNum;
      refreshModal();
      document.getElementById('imgModal').classList.add('show');
    }}

    function closeImgModal(e) {{
      document.getElementById('imgModal').classList.remove('show');
    }}

    function refreshModal() {{
      const numFormatted = modalPage < 10 ? '0' + modalPage : '' + modalPage;
      document.getElementById('modalPagePic').src = `images/classic-reading/page-${{numFormatted}}.jpg`;
      document.getElementById('modalPageTitle').innerText = `《中考名著考点整理》第 ${{modalPage}} 页 (扫描讲义原稿)`;
      document.getElementById('modalPageNum').innerText = `第 ${{modalPage}} / 39 页`;
    }}

    function stepModalPage(delta) {{
      const next = modalPage + delta;
      if (next >= 1 && next <= 39) {{
        modalPage = next;
        refreshModal();
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (document.getElementById('imgModal').classList.contains('show')) {{
        if (e.key === 'ArrowLeft') stepModalPage(-1);
        if (e.key === 'ArrowRight') stepModalPage(1);
        if (e.key === 'Escape') closeImgModal();
      }}
    }});
  </script>
</body>
</html>
'''
    return html

html_text = build_html()
out_file = '/Users/emily/Developer/Projects/owenlearining/chinese/classic-reading-V1.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(html_text)

print(f"Generated {out_file} successfully! Length: {len(html_text)} characters")
