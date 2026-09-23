import re
import os

# Ultra-clean audio playback engine for sentences & phrases
clean_audio_js = """
    let activeAudio = null;

    // 清亮级多音源高保真发音引擎（解决长句子破音/嘈杂/杂音问题）
    function playAudio(text, element) {
      if (activeAudio) {
        activeAudio.pause();
        activeAudio = null;
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }

      // 1. 过滤任何非英文标点与特殊乱码字符
      const cleanText = text.replace(/[^a-zA-Z0-9\\s,'\\.\\?!\\-]/g, ' ').replace(/\\s+/g, ' ').trim();
      if (!cleanText) return;

      if (element) {
        document.querySelectorAll('.playing').forEach(el => el.classList.remove('playing'));
        element.classList.add('playing');
      }

      // 音频选择引擎:
      // 音源1: 微软/有道高保真真人发音 API (短句/单词最优)
      // 音源2: 百度高清广播级英文发音 API (长句/复杂例句最优)
      const encodedText = encodeURIComponent(cleanText);
      const isLongSentence = cleanText.split(' ').length > 4;

      let primaryUrl = isLongSentence 
        ? 'https://fanyi.baidu.com/gettts?lan=en&text=' + encodedText + '&spd=3&source=web'
        : 'https://dict.youdao.com/dictvoice?audio=' + encodedText + '&type=2';
      
      let backupUrl = isLongSentence
        ? 'https://dict.youdao.com/dictvoice?audio=' + encodedText + '&type=2'
        : 'https://fanyi.baidu.com/gettts?lan=en&text=' + encodedText + '&spd=3&source=web';

      const audio = new Audio(primaryUrl);
      activeAudio = audio;

      audio.play().then(() => {
        audio.onended = () => { if (element) element.classList.remove('playing'); };
        audio.onerror = () => { tryBackupAudio(backupUrl, cleanText, element); };
      }).catch(() => {
        tryBackupAudio(backupUrl, cleanText, element);
      });
    }

    function tryBackupAudio(backupUrl, cleanText, element) {
      const bAudio = new Audio(backupUrl);
      activeAudio = bAudio;
      bAudio.play().then(() => {
        bAudio.onended = () => { if (element) element.classList.remove('playing'); };
        bAudio.onerror = () => { playCleanWebSpeech(cleanText, element); };
      }).catch(() => {
        playCleanWebSpeech(cleanText, element);
      });
    }

    // 绝无杂音的硬核 WebSpeech 发音人绑定 (只挑选 Samantha / Alex / Daniel 等高清发音人)
    function playCleanWebSpeech(text, element) {
      if (!('speechSynthesis' in window)) return;
      
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-US';
      u.rate = 0.88; // 适当降低语速，确保长句极其清晰无爆音
      u.pitch = 1.0;
      u.volume = 1.0;

      const voices = window.speechSynthesis.getVoices();
      // 在 macOS/iOS/Windows/Android 上强行绑定最高质量的声音
      const topVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Samantha') || v.name.includes('Alex') || v.name.includes('Daniel') || v.name.includes('Google US English') || v.name.includes('Natural'))) 
                    || voices.find(v => v.lang.startsWith('en'));
      
      if (topVoice) u.voice = topVoice;

      u.onend = () => { if (element) element.classList.remove('playing'); };
      u.onerror = () => { if (element) element.classList.remove('playing'); };

      window.speechSynthesis.speak(u);
    }
"""

# Update english/unit-1.html to english/unit-6.html and english/unit-study-hub-V1.html
unit_files = [f'english/unit-{i}.html' for i in range(1, 7)] + ['english/unit-study-hub-V1.html']

for filepath in unit_files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace existing playAudio or playSpeech function
    content = re.sub(r'function playAudio\(text, element\) \{[\s\S]*?\}\s*function playWebSpeech[\s\S]*?\}', clean_audio_js, content)
    content = re.sub(r'let activeAudio = null;[\s\S]*?function fallbackWebSpeech[\s\S]*?\}', clean_audio_js, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated clean sentence audio engine in: {filepath}")

