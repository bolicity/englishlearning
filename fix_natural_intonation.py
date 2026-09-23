import json

with open('english/unit_data_v1.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

json_str = js_content.split('window.UNIT_KNOWLEDGE_BASE = ')[1].strip().rstrip(';')
unit_data = json.loads(json_str)

hub_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>高中英语必背知识点读中心 V2</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --border-color: #E2E8F0;
      --border-hover: #CBD5E1;
      --text-main: #0F172A;
      --text-secondary: #334155;
      --text-muted: #64748B;
      --primary: #2563EB;
      --primary-hover: #1D4ED8;
      --primary-soft: #EFF6FF;
      --accent-green: #059669;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      padding: 16px;
      max-width: 1100px;
      margin: 0 auto;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }

    header {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }

    .back-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--primary);
      background: var(--primary-soft);
      border: 1px solid rgba(37, 99, 235, 0.15);
      padding: 8px 16px;
      border-radius: 9999px;
      font-weight: 600;
      font-size: 0.9rem;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .back-btn:hover {
      background: var(--primary);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .header-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .controls-wrapper {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .mode-toggle {
      display: flex;
      align-items: center;
      background: var(--bg-subtle);
      border-radius: 9999px;
      padding: 4px;
      border: 1px solid var(--border-color);
    }

    .mode-btn {
      padding: 6px 14px;
      border-radius: 9999px;
      border: none;
      background: transparent;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .mode-btn.active {
      background: var(--bg-card);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    .unit-tabs-wrapper {
      margin-bottom: 20px;
      overflow-x: auto;
      padding-bottom: 4px;
    }
    .unit-tabs {
      display: flex;
      gap: 8px;
      min-width: max-content;
    }
    .unit-tab {
      padding: 10px 18px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      font-size: 0.92rem;
      font-weight: 700;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 2px;
    }
    .unit-tab .sub-text {
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--text-muted);
    }
    .unit-tab:hover {
      border-color: var(--primary);
      color: var(--primary);
    }
    .unit-tab.active {
      background: var(--primary);
      color: #FFFFFF;
      border-color: var(--primary);
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }
    .unit-tab.active .sub-text {
      color: rgba(255, 255, 255, 0.85);
    }

    .filter-bar {
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 8px;
      overflow-x: auto;
    }
    .filter-btn {
      padding: 8px 16px;
      background: transparent;
      border: none;
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      position: relative;
      transition: color 0.2s ease;
    }
    .filter-btn.active {
      color: var(--primary);
    }
    .filter-btn.active::after {
      content: '';
      position: absolute;
      bottom: -10px;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--primary);
      border-radius: 3px 3px 0 0;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-left: 4px;
    }
    .section-title {
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .section-badge {
      background: var(--primary-soft);
      color: var(--primary);
      font-size: 0.8rem;
      font-weight: 700;
      padding: 2px 10px;
      border-radius: 9999px;
    }

    .words-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
      margin-bottom: 28px;
    }

    .word-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .word-card:hover {
      border-color: var(--primary);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }
    .word-info { flex: 1; padding-right: 12px; }
    .word-top { display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px; }
    .word-target { font-size: 1.15rem; font-weight: 800; color: var(--text-main); letter-spacing: -0.01em; }
    .word-phonetic { font-size: 0.85rem; color: var(--text-muted); }
    .word-trans { font-size: 0.9rem; color: var(--text-secondary); font-weight: 500; }

    /* 默写模式遮罩：隐藏英文，显示中文 */
    body.mask-mode .en-text {
      background: #E2E8F0;
      color: transparent !important;
      border-radius: 4px;
      user-select: none;
      text-shadow: none !important;
    }
    body.mask-mode .word-card:hover .en-text,
    body.mask-mode .phrase-card:hover .en-text,
    body.mask-mode .sentence-card:hover .en-text {
      background: transparent;
      color: var(--primary) !important;
    }

    .audio-btn {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      flex-shrink: 0;
      transition: all 0.2s ease;
    }
    .word-card:hover .audio-btn,
    .phrase-card:hover .audio-btn,
    .sentence-card:hover .audio-btn {
      background: var(--primary);
      color: #FFFFFF;
      border-color: var(--primary);
    }

    .audio-btn.playing {
      background: var(--accent-green) !important;
      color: #FFFFFF !important;
      border-color: var(--accent-green) !important;
      animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
      70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
      100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .phrases-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 12px;
      margin-bottom: 28px;
    }
    .phrase-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .phrase-card:hover {
      border-color: var(--primary);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }
    .phrase-en { font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-bottom: 2px; }
    .phrase-cn { font-size: 0.88rem; color: var(--text-secondary); }

    .sentences-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 28px;
    }
    .sentence-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .sentence-card:hover {
      box-shadow: var(--shadow-md);
      border-left-color: var(--primary-hover);
      transform: translateX(2px);
    }
    .sentence-content { flex: 1; }
    .sentence-en { font-size: 1.05rem; font-weight: 600; color: var(--text-main); margin-bottom: 6px; line-height: 1.5; }
    .sentence-cn { font-size: 0.9rem; color: var(--text-muted); font-weight: 500; }

    .grammar-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 28px;
    }
    .grammar-title { font-size: 1.1rem; font-weight: 800; color: var(--primary); margin-bottom: 10px; }
    .grammar-desc { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; white-space: pre-line; }

    #toast {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #0F172A;
      color: #FFFFFF;
      padding: 10px 20px;
      border-radius: 9999px;
      font-size: 0.88rem;
      font-weight: 600;
      transition: transform 0.3s ease;
      z-index: 1000;
    }
    #toast.show { transform: translateX(-50%) translateY(0); }

    @media (max-width: 640px) {
      body { padding: 12px; }
      header { flex-direction: column; align-items: stretch; gap: 10px; }
      .header-title { font-size: 1.1rem; justify-content: center; }
      .controls-wrapper { justify-content: center; }
      .words-grid, .phrases-grid { grid-template-columns: 1fr; }
      .sentence-card { flex-direction: column; align-items: flex-start; }
      .sentence-card .audio-btn { align-self: flex-end; }
    }
  </style>
</head>
<body>

  <header>
    <a href="english-hub.html" class="back-btn">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      返回英语中心
    </a>

    <div class="header-title">
      <span>高中英语必背知识点读中心</span>
    </div>

    <div class="controls-wrapper">
      <div class="mode-toggle">
        <button class="mode-btn active" id="btnAccentUK" onclick="setAccent('1')">🇬🇧 英音</button>
        <button class="mode-btn" id="btnAccentUS" onclick="setAccent('2')">🇺🇸 美音</button>
      </div>

      <div class="mode-toggle">
        <button class="mode-btn active" id="btnRecite" onclick="setMode('recite')">📖 背诵</button>
        <button class="mode-btn" id="btnMask" onclick="setMode('mask')">🙈 默写</button>
      </div>
    </div>
  </header>

  <div class="unit-tabs-wrapper">
    <div class="unit-tabs" id="unitTabsContainer"></div>
  </div>

  <div class="filter-bar">
    <button class="filter-btn active" onclick="filterSection('all', this)">全量展示</button>
    <button class="filter-btn" onclick="filterSection('words', this)">核心词汇</button>
    <button class="filter-btn" onclick="filterSection('phrases', this)">必备短语</button>
    <button class="filter-btn" onclick="filterSection('sentences', this)">经典例句</button>
    <button class="filter-btn" onclick="filterSection('grammar', this)">语法讲解</button>
  </div>

  <main id="mainContainer">
    <section id="wordsSec">
      <div class="section-header">
        <div class="section-title">
          <span>📝 核心词汇</span>
          <span class="section-badge" id="wordsCount">0</span>
        </div>
      </div>
      <div class="words-grid" id="wordsGrid"></div>
    </section>

    <section id="phrasesSec">
      <div class="section-header">
        <div class="section-title">
          <span>💡 必备短语</span>
          <span class="section-badge" id="phrasesCount">0</span>
        </div>
      </div>
      <div class="phrases-grid" id="phrasesGrid"></div>
    </section>

    <section id="sentencesSec">
      <div class="section-header">
        <div class="section-title">
          <span>🗣️ 经典例句</span>
          <span class="section-badge" id="sentencesCount">0</span>
        </div>
      </div>
      <div class="sentences-list" id="sentencesList"></div>
    </section>

    <section id="grammarSec">
      <div class="section-header">
        <div class="section-title">
          <span>📘 语法与结构分析</span>
        </div>
      </div>
      <div id="grammarContent"></div>
    </section>
  </main>

  <div id="toast">提示信息</div>

  <script>
    window.UNIT_KNOWLEDGE_BASE = __DATA_PLACEHOLDER__;
  </script>

  <script>
    let currentUnitId = 1;
    let currentAccent = '1';
    let globalAudio = new Audio();
    let audioUnlocked = false;

    function unlockAudio() {
      if (audioUnlocked) return;
      try {
        globalAudio.play().catch(() => {});
        globalAudio.pause();
        audioUnlocked = true;
      } catch(e) {}
    }
    document.addEventListener('touchstart', unlockAudio, { once: true });
    document.addEventListener('click', unlockAudio, { once: true });

    document.addEventListener('DOMContentLoaded', () => {
      renderUnitTabs();
      loadUnit(1);

      if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
          speechSynthesis.onvoiceschanged = () => { window.speechSynthesis.getVoices(); };
        }
      }
    });

    function setAccent(accent) {
      currentAccent = accent;
      document.getElementById('btnAccentUK').classList.toggle('active', accent === '1');
      document.getElementById('btnAccentUS').classList.toggle('active', accent === '2');
      showToast(accent === '1' ? '已切换为 🇬🇧 标准英式发音 (UK Accent)' : '已切换为 🇺🇸 标准美式发音 (US Accent)');
    }

    function renderUnitTabs() {
      const container = document.getElementById('unitTabsContainer');
      container.innerHTML = window.UNIT_KNOWLEDGE_BASE.map(u => `
        <button class="unit-tab ${u.unit_id === currentUnitId ? 'active' : ''}" onclick="switchUnit(${u.unit_id})">
          <span>Unit ${u.unit_id}</span>
          <span class="sub-text">${u.title.replace('Unit ' + u.unit_id, '').trim()}</span>
        </button>
      `).join('');
    }

    function switchUnit(unitId) {
      currentUnitId = unitId;
      renderUnitTabs();
      loadUnit(unitId);
    }

    function loadUnit(unitId) {
      const unit = window.UNIT_KNOWLEDGE_BASE.find(u => u.unit_id === unitId);
      if (!unit) return;

      // 1. 核心词汇
      const wordsGrid = document.getElementById('wordsGrid');
      document.getElementById('wordsCount').innerText = (unit.words || []).length;
      wordsGrid.innerHTML = (unit.words || []).map(w => `
        <div class="word-card" onclick="playAudio('${escapeQuote(w.word)}', this)">
          <div class="word-info">
            <div class="word-top">
              <span class="word-target en-text">${w.word}</span>
              ${w.phonetic ? `<span class="word-phonetic">${w.phonetic}</span>` : ''}
            </div>
            <div class="word-trans">
              ${w.pos ? `<span style="color:var(--primary); font-weight:700; margin-right:4px;">${w.pos}</span>` : ''}${w.trans || w.cn || ''}
            </div>
          </div>
          <div class="audio-btn" title="点击发音">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
          </div>
        </div>
      `).join('');

      // 2. 必备短语
      const phrasesGrid = document.getElementById('phrasesGrid');
      document.getElementById('phrasesCount').innerText = (unit.phrases || []).length;
      phrasesGrid.innerHTML = (unit.phrases || []).map(p => {
        const pEn = p.en || p.phrase || '';
        const pCn = p.cn || p.trans || '';
        return `
        <div class="phrase-card" onclick="playAudio('${escapeQuote(pEn)}', this)">
          <div>
            <div class="phrase-en en-text">${pEn}</div>
            <div class="phrase-cn">${pCn}</div>
          </div>
          <div class="audio-btn" title="点击发音">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
          </div>
        </div>
      `}).join('');

      // 3. 经典例句
      const sentencesList = document.getElementById('sentencesList');
      document.getElementById('sentencesCount').innerText = (unit.sentences || []).length;
      sentencesList.innerHTML = (unit.sentences || []).map(s => `
        <div class="sentence-card" onclick="playAudio('${escapeQuote(s.en)}', this)">
          <div class="sentence-content">
            <div class="sentence-en en-text">${s.en}</div>
            <div class="sentence-cn">${s.cn || s.trans || ''}</div>
          </div>
          <div class="audio-btn" title="点击发音">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
          </div>
        </div>
      `).join('');

      // 4. 语法讲解
      const grammarContent = document.getElementById('grammarContent');
      if (unit.grammar && unit.grammar.length > 0) {
        grammarContent.innerHTML = unit.grammar.map(g => `
          <div class="grammar-card">
            <div class="grammar-title">${g.title || '语法重点'}</div>
            <div class="grammar-desc">${g.content || g.desc || ''}</div>
          </div>
        `).join('');
      } else {
        grammarContent.innerHTML = '<div class="grammar-card"><div class="grammar-desc">暂无详细语法说明</div></div>';
      }
    }

    function escapeQuote(str) {
      if (!str) return '';
      return str.replace(/'/g, "\\'");
    }

    function setMode(mode) {
      document.getElementById('btnRecite').classList.toggle('active', mode === 'recite');
      document.getElementById('btnMask').classList.toggle('active', mode === 'mask');
      if (mode === 'mask') {
        document.body.classList.add('mask-mode');
        showToast('已开启默写模式：隐藏英文，看中文默写');
      } else {
        document.body.classList.remove('mask-mode');
        showToast('已开启背诵模式：英文中文全显');
      }
    }

    function filterSection(sec, btn) {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const secWords = document.getElementById('wordsSec');
      const secPhrases = document.getElementById('phrasesSec');
      const secSentences = document.getElementById('sentencesSec');
      const secGrammar = document.getElementById('grammarSec');

      if (sec === 'all') {
        secWords.style.display = 'block';
        secPhrases.style.display = 'block';
        secSentences.style.display = 'block';
        secGrammar.style.display = 'block';
      } else {
        secWords.style.display = (sec === 'words') ? 'block' : 'none';
        secPhrases.style.display = (sec === 'phrases') ? 'block' : 'none';
        secSentences.style.display = (sec === 'sentences') ? 'block' : 'none';
        secGrammar.style.display = (sec === 'grammar') ? 'block' : 'none';
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);
    }

    // ----------------------------------------------------
    // 自然和谐、标准原声语调例句与单词点读系统
    // ----------------------------------------------------
    function playAudio(text, element) {
      unlockAudio();

      try { globalAudio.pause(); } catch(e){}
      if ('speechSynthesis' in window) {
        try { window.speechSynthesis.cancel(); } catch(e){}
      }

      // 1. 彻底保持天然标点与文本，绝不强加无意义空间替换
      let cleanText = text.replace(/[\r\n\t]+/g, ' ').trim();
      if (!cleanText) return;

      if (element) {
        document.querySelectorAll('.audio-btn.playing').forEach(el => el.classList.remove('playing'));
        const btn = element.querySelector('.audio-btn') || element;
        btn.classList.add('playing');
      }

      const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

      // 移动端：直接在物理点击函数主线程内【同步零延迟】朗读原生标准音调
      if (isMobile) {
        playDirectSyncMobileSpeech(cleanText, element);
      } else {
        // 桌面端：走在线高保真音频
        playOnlineAudioPC(cleanText, element);
      }
    }

    function playDirectSyncMobileSpeech(cleanText, element) {
      if (!('speechSynthesis' in window)) {
        playOnlineAudioPC(cleanText, element);
        return;
      }

      try {
        if (window.speechSynthesis.paused) window.speechSynthesis.resume();
        window.speechSynthesis.cancel();

        const u = new SpeechSynthesisUtterance(cleanText);
        u.lang = (currentAccent === '1') ? 'en-GB' : 'en-US';
        
        // 关键！将 u.rate 恢复为 1.0（标准自然人声原速），取消一切人为降速引起的拉伸失真与变音！
        u.rate = 1.0;
        u.pitch = 1.0;

        const bestVoice = getBestNaturalVoice();
        if (bestVoice) u.voice = bestVoice;

        const clearPlaying = () => {
          if (element) {
            const btn = element.querySelector('.audio-btn') || element;
            btn.classList.remove('playing');
          }
        };

        u.onend = clearPlaying;
        u.onerror = clearPlaying;

        window.speechSynthesis.speak(u);
      } catch(e) {
        playOnlineAudioPC(cleanText, element);
      }
    }

    function playOnlineAudioPC(cleanText, element) {
      const wordCount = cleanText.split(' ').length;
      const encodedText = encodeURIComponent(cleanText);

      let primaryUrl = (wordCount <= 4)
        ? 'https://dict.youdao.com/dictvoice?audio=' + encodedText + '&type=' + currentAccent
        : 'https://fanyi.baidu.com/gettts?lan=' + (currentAccent === '1' ? 'uk' : 'en') + '&text=' + encodedText + '&spd=3&source=web';

      globalAudio.src = primaryUrl;

      const clearPlaying = () => {
        if (element) {
          const btn = element.querySelector('.audio-btn') || element;
          btn.classList.remove('playing');
        }
      };

      globalAudio.onended = clearPlaying;
      globalAudio.onerror = () => { playDirectSyncMobileSpeech(cleanText, element); };

      globalAudio.play().catch(() => {
        playDirectSyncMobileSpeech(cleanText, element);
      });
    }

    function getBestNaturalVoice() {
      if (!('speechSynthesis' in window)) return null;
      const voices = window.speechSynthesis.getVoices();
      if (!voices || voices.length === 0) return null;

      const targetLang = (currentAccent === '1') ? 'en-GB' : 'en-US';

      const topVoice = voices.find(v => 
        v.lang && (v.lang === targetLang || v.lang.replace('_', '-').startsWith(targetLang)) &&
        (v.name.includes('Natural') || v.name.includes('Premium') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Jenny') || v.name.includes('Aria') || v.name.includes('Oliver') || v.name.includes('Kate'))
      );
      if (topVoice) return topVoice;

      const accentVoice = voices.find(v => v.lang && (v.lang === targetLang || v.lang.replace('_', '-').startsWith(targetLang)));
      if (accentVoice) return accentVoice;

      return voices.find(v => v.lang && v.lang.startsWith('en')) || null;
    }
  </script>
</body>
</html>
'''

final_html = hub_template.replace('__DATA_PLACEHOLDER__', json.dumps(unit_data, ensure_ascii=False, indent=2))

with open('english/unit-study-hub-V1.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open('english/unit-study-hub-V2.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Natural intonation fix applied to unit-study-hub-V1.html and V2.html!")
