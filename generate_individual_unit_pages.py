import json

with open('english/unit_data_v1.js', 'r', encoding='utf-8') as f:
    text = f.read().replace('window.UNIT_KNOWLEDGE_BASE = ', '').rstrip(';')
    units = json.loads(text)

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - 纯净网页版（高清发音）</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --border-color: #E2E8F0;
      --text-main: #0F172A;
      --text-secondary: #334155;
      --text-muted: #64748B;
      --primary: #2563EB;
      --primary-soft: #EFF6FF;
      --accent-green: #16A34A;
      --accent-green-soft: #F0FDF4;
      --radius-md: 12px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      padding: 20px;
      max-width: 1000px;
      margin: 0 auto;
      line-height: 1.5;
    }}
    header {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .back-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      color: var(--primary);
      font-weight: 700;
      font-size: 14px;
    }}
    h1 {{ font-size: 22px; font-weight: 800; color: #1E40AF; }}
    p.sub {{ font-size: 14px; color: var(--text-muted); font-weight: 500; margin-top: 4px; }}
    
    .ctrl-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .ctrl-btn {{
      padding: 8px 16px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-secondary);
      cursor: pointer;
      outline: none;
    }}
    .ctrl-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}

    .section-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .sec-title {{
      font-size: 18px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .grid-words {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 12px;
    }}
    .item-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .item-card:hover {{ border-color: var(--primary); background: var(--primary-soft); }}
    .item-card.playing {{ border-color: var(--accent-green); background: var(--accent-green-soft); }}
    
    .item-en {{ font-weight: 700; font-size: 16px; color: var(--text-main); margin-bottom: 4px; display: flex; justify-content: space-between; }}
    .item-cn {{ font-size: 13px; color: var(--text-muted); font-weight: 500; transition: filter 0.2s; }}

    body.mask-mode .item-cn {{ filter: blur(5px); user-select: none; }}
    body.mask-mode .item-card:hover .item-cn {{ filter: blur(0); }}
    body.mask-mode .list-row:hover .item-cn {{ filter: blur(0); }}

    .list-phrases, .list-sentences {{ display: flex; flex-direction: column; gap: 10px; }}
    .list-row {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 14px 18px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s;
    }}
    .list-row:hover {{ border-color: var(--primary); background: var(--primary-soft); }}
    .list-row.playing {{ border-color: var(--accent-green); background: var(--accent-green-soft); }}
    
    .row-left {{ display: flex; align-items: center; gap: 12px; }}
    .num-badge {{ font-size: 12px; font-weight: 700; color: var(--text-muted); background: white; padding: 2px 8px; border-radius: 4px; }}
  </style>
</head>
<body>
  <header>
    <div>
      <a href="unit-study-hub-V1.html" class="back-link">← 返回英语单元总中心</a>
      <h1 style="margin-top:8px;">{title}</h1>
      <p class="sub">{subtitle} · 原生网页点读版（无PDF）</p>
    </div>
    <div>
      <span style="font-size:13px; background:var(--accent-green-soft); color:var(--accent-green); border:1px solid #BBF7D0; padding:6px 14px; border-radius:20px; font-weight:700;">🔊 清晰真人语音模式</span>
    </div>
  </header>

  <div class="ctrl-bar">
    <button class="ctrl-btn" id="maskBtn" onclick="toggleMask()">🙈 默写遮罩模式: 关</button>
    <select class="ctrl-btn" id="audioEngineSelect">
      <option value="dict">🔊 高音质在线发音 (推荐)</option>
      <option value="speech">🤖 浏览器原生发音</option>
    </select>
  </div>

  <!-- 单词 -->
  <div class="section-box">
    <div class="sec-title">🔤 重点词汇 ({words_count}个)</div>
    <div class="grid-words">
      {words_html}
    </div>
  </div>

  <!-- 短语 -->
  <div class="section-box">
    <div class="sec-title">🗣️ 核心短语 ({phrases_count}条)</div>
    <div class="list-phrases">
      {phrases_html}
    </div>
  </div>

  <!-- 句型 -->
  <div class="section-box">
    <div class="sec-title">💬 重点句型与经典例句 ({sentences_count}句)</div>
    <div class="list-sentences">
      {sentences_html}
    </div>
  </div>

  <script>
    let isMask = false;
    let activeAudio = null;

    // 高声音质播放引擎 (解决杂音问题)
    function playAudio(text, element) {{
      if (activeAudio) {{
        activeAudio.pause();
        activeAudio = null;
      }}
      if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
      }}

      // 清理非发音字符
      const cleanText = text.replace(/[^a-zA-Z0-9\\s,'\\.\\?!\\-]/g, '').trim();
      if (!cleanText) return;

      const engine = document.getElementById('audioEngineSelect').value;

      if (element) {{
        document.querySelectorAll('.playing').forEach(el => el.classList.remove('playing'));
        element.classList.add('playing');
      }}

      if (engine === 'dict') {{
        // 高保真在线字典真人发音接口
        const audioUrl = 'https://dict.youdao.com/dictvoice?audio=' + encodeURIComponent(cleanText) + '&type=2';
        const audio = new Audio(audioUrl);
        activeAudio = audio;

        audio.play().then(() => {{
          audio.onended = () => {{ if (element) element.classList.remove('playing'); }};
          audio.onerror = () => {{ playWebSpeech(cleanText, element); }};
        }}).catch(() => {{
          // 网络失败备选
          playWebSpeech(cleanText, element);
        }});
      }} else {{
        playWebSpeech(cleanText, element);
      }}
    }}

    function playWebSpeech(text, element) {{
      if (!('speechSynthesis' in window)) return;
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-US';
      u.rate = 0.9;
      u.pitch = 1.0;

      const voices = window.speechSynthesis.getVoices();
      const usVoice = voices.find(v => v.lang.includes('en-US') || v.lang.includes('en-GB') || v.name.includes('Samantha') || v.name.includes('Alex'));
      if (usVoice) u.voice = usVoice;

      u.onend = () => {{ if (element) element.classList.remove('playing'); }};
      u.onerror = () => {{ if (element) element.classList.remove('playing'); }};

      window.speechSynthesis.speak(u);
    }}

    function toggleMask() {{
      isMask = !isMask;
      document.body.classList.toggle('mask-mode', isMask);
      document.getElementById('maskBtn').textContent = isMask ? '🙈 默写遮罩模式: 开' : '🙈 默写遮罩模式: 关';
      document.getElementById('maskBtn').classList.toggle('active', isMask);
    }}
  </script>
</body>
</html>
"""

for u in units:
    uid = u['unit_id']
    words_html = ""
    for w in u.get('words', []):
        word_escaped = w['word'].replace("'", "\\'")
        words_html += f"""
        <div class="item-card" onclick="playAudio('{word_escaped}', this)">
          <div class="item-en"><span>{w['word']}</span><span>🔊</span></div>
          <div style="font-size:12px; color:var(--text-muted);">{w.get('phonetic','')} {w.get('pos','')}</div>
          <div class="item-cn">{w['trans']}</div>
        </div>
        """
    
    phrases_html = ""
    for p in u.get('phrases', []):
        phrase_escaped = p['en'].replace("'", "\\'")
        phrases_html += f"""
        <div class="list-row" onclick="playAudio('{phrase_escaped}', this)">
          <div class="row-left">
            <span class="num-badge">{p['id']}</span>
            <span style="font-weight:700;">{p['en']}</span>
          </div>
          <div>
            <span class="item-cn" style="margin-right:10px;">{p['cn']}</span>
            <span>🔊</span>
          </div>
        </div>
        """

    sentences_html = ""
    for s in u.get('sentences', []):
        sentence_escaped = s['en'].replace("'", "\\'")
        sentences_html += f"""
        <div class="list-row" style="flex-direction:column; align-items:flex-start; gap:6px;" onclick="playAudio('{sentence_escaped}', this)">
          <div style="display:flex; justify-content:space-between; width:100%;">
            <span style="font-weight:700; font-size:16px; color:var(--text-main);"><span class="num-badge">{s['id']}</span> {s['en']}</span>
            <span>🔊</span>
          </div>
          <div class="item-cn" style="font-size:14px;">{s['cn']}</div>
        </div>
        """

    page_html = template.format(
        title=u['title'],
        subtitle=u['subtitle'],
        words_count=len(u.get('words', [])),
        phrases_count=len(u.get('phrases', [])),
        sentences_count=len(u.get('sentences', [])),
        words_html=words_html,
        phrases_html=phrases_html,
        sentences_html=sentences_html
    )

    filename = f"english/unit-{uid}.html"
    with open(filename, 'w', encoding='utf-8') as out_f:
        out_f.write(page_html)
    print(f"Successfully created: {filename}")

