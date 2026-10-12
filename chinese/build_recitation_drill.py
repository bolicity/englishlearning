#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 86 篇理解性默写自测工具页 chinese/recitation-drill-V1.html
数据源: chinese/recitation-data-V1.json（86 篇 / 8 册 / 568 易错字条目）
风格: 与 chinese/recitation-bank-V1.html 一致（左侧可折叠栏 + 学习模式）
"""
import json, re, io, os

BASE = '/Users/emily/Developer/Projects/owenlearining/chinese'
data = json.load(open(f'{BASE}/recitation-data-V1.json', encoding='utf-8'))

# 把数据内联进页面，避免 file:// 下 fetch 被 CORS 拦
payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
payload = payload.replace('</', '<\\/')

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>理解性默写自测· 86篇全册 | 上海中考27届</title>
<style>
:root{
  --bg:#F8FAFC; --card:#FFFFFF; --subtle:#F1F5F9; --border:#E2E8F0;
  --tx:#0F172A; --tx2:#475569; --mut:#64748B;
  --red:#DC2626; --red-l:#EF4444; --red-bg:#FEF2F2;
  --green:#059669; --green-bg:#ECFDF5; --amber:#D97706; --amber-bg:#FFFBEB;
  --blue:#1D4ED8; --blue-bg:#EFF6FF; --violet:#7C3AED; --violet-bg:#F5F3FF;
  --serif:"Songti SC","STSong","Noto Serif SC","SimSun",serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:-apple-system,"PingFang SC","Segoe UI",sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;display:flex}

/* ---------- 左侧目录 ---------- */
#sidebar{width:276px;flex:none;background:var(--card);border-right:1px solid var(--border);
  display:flex;flex-direction:column;height:100vh;position:sticky;top:0;transition:margin-left .25s ease;z-index:40}
body.collapsed #sidebar{margin-left:-276px}
#side-head{padding:1rem 1rem .8rem;border-bottom:1px solid var(--border);position:relative}
#side-head h1{font-size:1rem;font-weight:800;color:var(--red);letter-spacing:-.01em}
#side-head p{font-size:.72rem;color:var(--mut);margin-top:.15rem}
#fold{position:absolute;right:.7rem;top:1rem;background:var(--subtle);border:1px solid var(--border);
  border-radius:7px;width:30px;height:30px;cursor:pointer;font-size:.8rem;color:var(--tx2);display:flex;align-items:center;justify-content:center}
#fold:hover{background:var(--red-bg);border-color:var(--red-l);color:var(--red)}
#sec-list{flex:1;overflow-y:auto;padding:.5rem}
.vol{margin-bottom:.35rem}
.vol-head{display:flex;align-items:center;gap:.45rem;padding:.42rem .55rem;border-radius:8px;cursor:pointer;user-select:none}
.vol-head:hover{background:var(--subtle)}
.vol-dot{width:7px;height:7px;border-radius:50%;background:var(--border);flex:none}
.vol-dot.full{background:var(--green)}
.vol-dot.half{background:var(--amber)}
.vol-name{flex:1;font-size:.8rem;font-weight:700;color:var(--tx2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vol-n{font-size:.68rem;color:var(--mut);flex:none;font-variant-numeric:tabular-nums}
.vol-items{display:none;padding:.1rem 0 .3rem .55rem}
.vol.open .vol-items{display:block}
.pi{display:flex;align-items:center;gap:.4rem;padding:.3rem .5rem;border-radius:7px;cursor:pointer;font-size:.78rem;color:var(--tx2)}
.pi:hover{background:var(--subtle)}
.pi.active{background:var(--red-bg);color:var(--red);font-weight:600}
.pi-t{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pi-ok{font-size:.68rem;color:var(--green);flex:none}
.pi-no{font-size:.66rem;color:var(--mut);flex:none;font-variant-numeric:tabular-nums}
.pi-type{font-size:.6rem;padding:.05rem .28rem;border-radius:4px;background:var(--subtle);color:var(--mut);flex:none}
.pi-type.wy{background:var(--violet-bg);color:var(--violet)}
#side-foot{padding:.7rem 1rem;border-top:1px solid var(--border);font-size:.72rem;color:var(--mut)}
#progress-line{height:6px;border-radius:3px;background:var(--subtle);margin-top:.45rem;overflow:hidden}
#progress-fill{height:100%;background:linear-gradient(90deg,var(--red),var(--red-l));width:0;transition:width .3s}

/* ---------- 主区 ---------- */
main{flex:1;min-width:0;display:flex;flex-direction:column}
header{background:var(--card);border-bottom:1px solid var(--border);padding:.9rem 1.4rem;position:sticky;top:0;z-index:30}
.hrow{display:flex;align-items:center;justify-content:space-between;gap:1rem;max-width:940px;margin:0 auto;flex-wrap:wrap}
#crumb{font-size:.8rem;color:var(--mut)}
#crumb a{color:var(--mut);text-decoration:none}
#crumb a:hover{color:var(--red)}
#crumb b{color:var(--red);font-weight:700}
#crumb .pl{color:var(--blue);font-weight:600}
.hbtns{display:flex;gap:.4rem;align-items:center;flex-wrap:wrap}
.btn{font:inherit;font-size:.76rem;font-weight:600;padding:.42rem .75rem;border-radius:8px;border:1px solid var(--border);
  background:var(--subtle);color:var(--tx2);cursor:pointer;white-space:nowrap}
.btn:hover{background:var(--red-bg);border-color:var(--red-l);color:var(--red)}
.btn.on{background:var(--red);border-color:var(--red);color:#fff}
.btn.g{border-color:var(--green);color:var(--green);background:var(--green-bg)}
.btn.g.on{background:var(--green);color:#fff}
.btn.b{border-color:var(--blue);color:var(--blue);background:var(--blue-bg)}
.btn.b.on{background:var(--blue);color:#fff}

.wrap{max-width:940px;margin:0 auto;padding:1.3rem 1.4rem 4rem;flex:1}
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.15rem 1.25rem;margin-bottom:1rem}
.title-row{display:flex;align-items:baseline;gap:.6rem;flex-wrap:wrap;margin-bottom:.15rem}
.t-no{font-size:.72rem;color:var(--mut);font-variant-numeric:tabular-nums}
.t-name{font-family:var(--serif);font-size:1.32rem;font-weight:700;letter-spacing:.01em}
.t-au{font-size:.82rem;color:var(--mut)}
.t-meta{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.9rem}
.chip{font-size:.68rem;padding:.16rem .5rem;border-radius:20px;background:var(--subtle);color:var(--tx2);font-weight:600}
.chip.wy{background:var(--violet-bg);color:var(--violet)}
.chip.ci{background:var(--blue-bg);color:var(--blue)}
.chip.lv{background:var(--green-bg);color:var(--green)}

.passage{font-family:var(--serif);font-size:1.06rem;line-height:2.15;color:var(--tx);margin-bottom:1rem}
.passage p{margin-bottom:.55rem}
.cue{background:var(--amber-bg);color:var(--amber);padding:0 .18rem;border-radius:3px;font-weight:700}
.ell{color:var(--mut);font-weight:400}
.blank{display:inline-block;min-width:4em;border-bottom:2px solid var(--red);background:var(--red-bg);
  border-radius:3px 3px 0 0;cursor:pointer;vertical-align:baseline;transition:background .15s;
  text-align:center;letter-spacing:.05em;color:transparent;min-height:1.5em;line-height:1.5;padding:0 .2em}
.blank:hover{background:#FEE2E2}
.blank.filled{color:var(--red);background:var(--subtle);border-color:var(--mut)}
.blank.right{color:var(--green);background:var(--green-bg);border-color:var(--green)}
.blank.wrong{color:var(--red);background:#FEF2F2;border-color:var(--red)}
.blank input{font:inherit;width:100%;border:none;background:transparent;color:var(--tx);
  text-align:center;letter-spacing:.05em;outline:none;padding:0}

.hardbox{background:var(--amber-bg);border:1px solid #FDE68A;border-radius:10px;padding:.75rem .9rem;margin-bottom:1rem}
.hardbox h4{font-size:.78rem;color:var(--amber);margin-bottom:.45rem;font-weight:700}
.hz{display:inline-flex;align-items:baseline;gap:.2rem;margin:.16rem .35rem .16rem 0;padding:.2rem .5rem;background:var(--card);
  border:1px solid #FDE68A;border-radius:7px;font-size:.86rem}
.hz b{font-family:var(--serif);font-weight:700}
.hz span{font-size:.7rem;color:var(--mut);font-variant-numeric:tabular-nums}

.judge{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;padding-top:.9rem;border-top:1px dashed var(--border)}
.res{font-size:.86rem;font-weight:700}
.res.ok{color:var(--green)} .res.no{color:var(--red)}
.score{font-size:.74rem;color:var(--mut);margin-left:auto}

.note{background:var(--blue-bg);border:1px solid #BFDBFE;border-radius:10px;padding:.75rem .9rem;
  font-size:.8rem;color:#1E40AF;margin-bottom:1rem}
.note b{font-weight:700}
.hint{font-size:.8rem;color:var(--mut);margin-bottom:.8rem}

/* 背诵模式：逐句遮盖 */
.recite{font-family:var(--serif);font-size:1.1rem;line-height:2.3}
.rline{display:block;padding:.18rem .4rem;border-radius:6px;margin-bottom:.1rem;cursor:pointer;transition:background .15s}
.rline:hover{background:var(--subtle)}
.rline.hidden{color:transparent;background:var(--red-bg);user-select:none}
.rline.hidden::after{content:"点击显示";font-family:-apple-system,sans-serif;font-size:.72rem;color:var(--red-l)}
.rline.hi{background:var(--amber-bg)}

.overview{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:.6rem}
.ov{background:var(--card);border:1px solid var(--border);border-radius:11px;padding:.7rem .8rem}
.ov b{display:block;font-size:1.5rem;font-weight:800;color:var(--red);line-height:1.2;font-variant-numeric:tabular-nums}
.ov span{font-size:.7rem;color:var(--mut)}
.ov.g b{color:var(--green)} .ov.b b{color:var(--blue)} .ov.a b{color:var(--amber)}

.warn{background:#FEF2F2;border:1px solid #FECACA;border-radius:10px;padding:.8rem .95rem;font-size:.8rem;color:#991B1B;margin-bottom:1rem}
.warn b{font-weight:700}
table{width:100%;border-collapse:collapse;font-size:.8rem;margin-bottom:.4rem}
th,td{padding:.45rem .55rem;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
th{background:var(--subtle);font-weight:700;font-size:.76rem;color:var(--tx2)}
td.c{text-align:center;font-variant-numeric:tabular-nums}
.tblwrap{overflow-x:auto}

@media(max-width:760px){
  #sidebar{position:fixed;left:0;top:0;bottom:0;box-shadow:0 0 30px rgba(0,0,0,.12)}
  body.collapsed #sidebar{margin-left:-276px}
  .wrap{padding:1rem .9rem 3rem}
}
@media print{#sidebar,header,.judge{display:none}body{display:block}.wrap{max-width:100%}}
</style>
</head>
<body>
<aside id="sidebar">
  <div id="side-head">
    <h1>理解性默写 · 86篇</h1>
    <p>上海中考 27 届 · 六至九年级全册</p>
    <button id="fold" title="折叠/展开目录">«</button>
  </div>
  <div id="sec-list"></div>
  <div id="side-foot">
    <div><span id="doneN">0</span> / 86 篇连续默写无误</div>
    <div id="progress-line"><div id="progress-fill"></div></div>
  </div>
</aside>

<main>
  <header>
    <div class="hrow">
      <div class="crumb"><a href="../index.html">学习中心</a> · <a href="chinese.html">初中语文</a> · <b>理解性默写自测</b> · <a class="pl" href="chinese-repair-plan-V1.html">8 个月补习计划 ↗</a></div>
      <div class="hbtns">
        <button class="btn on" id="mHide">填空默写</button>
        <button class="btn" id="mRecite">背诵模式</button>
        <button class="btn g" id="mReview">易错字表</button>
        <button class="btn b" id="mStat">进度总览</button>
        <button class="btn" id="mReset">清空记录</button>
      </div>
    </div>
  </header>

  <div class="wrap" id="view"></div>
</main>

<script>
const DATA = __PAYLOAD__;
const KEY = 'yw-moshou-drill-v1';
let MODE = 'hide';
let CUR = {v:0,ii:0};
let STATE = {};   // key -> {n:连续无错次数, ok:日期}
try{ STATE = JSON.parse(localStorage.getItem(KEY)||'{}'); }catch(e){ STATE={}; }

const FLAT = [];
DATA.forEach((v,vi)=>v.items.forEach((it,ii)=>FLAT.push({v,vi,ii,it})));

function save(){ try{ localStorage.setItem(KEY, JSON.stringify(STATE)); }catch(e){} }
function k(vi,ii){ return vi+'-'+ii; }
function streak(vi,ii){ return (STATE[k(vi,ii)]||{}).n||0; }

/* ---------------- 侧栏 ---------------- */
function buildSide(){
  const el=document.getElementById('sec-list');
  el.innerHTML = DATA.map((v,vi)=>{
    const done = v.items.filter((_,ii)=>streak(vi,ii)>=3).length;
    const cls = done===v.items.length?'full':(done>0?'half':'');
    return `<div class="vol" data-v="${vi}">
      <div class="vol-head"><span class="vol-dot ${cls}"></span>
        <span class="vol-name">${v.volume}</span><span class="vol-n">${done}/${v.items.length}</span></div>
      <div class="vol-items">${v.items.map((it,ii)=>{
        const s=streak(vi,ii);
        const ok = s>=3 ? '<span class="pi-ok">✓</span>' : (s>0?`<span class="pi-no">${s}</span>`:'');
        const t = it.type==='文言文'?'wy':'';
        return `<div class="pi" data-v="${vi}" data-i="${ii}">
          <span class="pi-t">${it.no}. ${it.title}</span>
          <span class="pi-type ${t}">${it.type}</span>${ok}</div>`;
      }).join('')}</div></div>`;
  }).join('');
  el.querySelectorAll('.vol-head').forEach(h=>{
    h.onclick=()=>h.parentElement.classList.toggle('open');
  });
  el.querySelectorAll('.pi').forEach(p=>{
    p.onclick=()=>{ CUR={v:+p.dataset.v,ii:+p.dataset.i}; openVol(+p.dataset.v); render(); };
  });
  updFoot();
}
function openVol(vi){
  document.querySelectorAll('.vol').forEach(e=>e.classList.toggle('open', +e.dataset.v===vi));
  document.querySelectorAll('.pi').forEach(e=>{
    e.classList.toggle('active', +e.dataset.v===CUR.v && +e.dataset.i===CUR.ii);
  });
}
function updFoot(){
  const done = FLAT.filter(x=>streak(x.vi,x.ii)>=3).length;
  document.getElementById('doneN').textContent = done;
  document.getElementById('progress-fill').style.width = (done/86*100)+'%';
}

/* ---------------- 填空默写（逐句给提示挖句） ---------------- */
function pickCue(it, para){
  // 真实理解性默写是「给一句语境，写一句」，所以只挖该段最后一句，前文作提示
  const parts = para.split(/(?<=[。！？])/).filter(Boolean);
  if(parts.length<2) return null;
  const cueAll = parts.slice(0,-1).join('');
  const target = parts[parts.length-1];
  const n = target.replace(/[，。！？；：、""''《》（）·…—\s]/g,'').length;
  // 长段（文言文常一整段）只保留末尾语境，前面省略，避免整屏高亮
  const cueLen = cueAll.replace(/[，。！？；：、""''《》（）·…—\s]/g,'').length;
  const cue = cueLen>40 ? '<span class="ell">……</span>'+parts.slice(-3,-1).join('') : cueAll;
  return '<span class="cue">'+cue+'</span><span class="blank" data-ans="'+target+'">'+
         '＿'.repeat(Math.min(14, Math.max(4, n)))+'</span>';
}
function countCues(it){
  return it.paras.reduce((s,p)=>s+(pickCue(it,p)?1:0),0);
}
function renderHide(){
  const {v,ii} = CUR, vol=DATA[v], it=vol.items[ii];
  const cues = it.paras.map(p=>pickCue(it,p)).filter(Boolean);
  const nCue = cues.length;
  const hz = it.hardList.length ? `<div class="hardbox"><h4>本篇易错字（先看这行再默写）</h4>${
    it.hardList.map(h=>`<span class="hz"><b>${h.zi}</b><span>${h.py}</span></span>`).join('')}</div>` : '';
  document.getElementById('view').innerHTML = `
    <div class="note"><b>怎么用：</b>读橙色提示句，在横线上默写缺失的一句——点横线即可输入，按<b>回车</b>下一空。判卷按字比对，<b>错一字该空不得分</b>。同一句连续 3 次写对才算过关，左栏出现 ✓。</div>
    <div class="card">
      <div class="title-row">
        <span class="t-no">${vol.volume} · 第${it.no}篇</span>
        <span class="t-name">${it.title}</span>
        <span class="t-au">${it.author||''}</span>
      </div>
      <div class="t-meta">
        <span class="chip">${it.type}</span>
        <span class="chip lv">${it.len} 字</span>
        <span class="chip">${nCue} 空待默</span>
        ${streak(v,ii)>0?`<span class="chip">连续 ${streak(v,ii)} 次</span>`:''}
      </div>
      ${hz}
      <div class="passage">${cues.map(c=>`<p>${c}</p>`).join('')}</div>
      <div class="judge">
        <button class="btn g" id="check">判卷</button>
        <button class="btn" id="resetWrong" hidden>清空重做</button>
        <button class="btn" id="pass">全对（跳过填写）</button>
        <button class="btn" id="fail">有错</button>
        <button class="btn" id="showAll">显示全文对照</button>
        <span class="res" id="res"></span>
        <span class="score" id="score"></span>
      </div>
    </div>
    <div class="card" id="ansCard" style="display:none">
      <div class="title-row"><span class="t-name" style="font-size:1.05rem">全文对照</span></div>
      <div class="passage">${it.paras.map(p=>`<p>${p}</p>`).join('')}</div>
    </div>
    <div class="hbtns">
      <button class="btn" id="prev">← 上一篇</button>
      <button class="btn" id="next">下一篇 →</button>
      <button class="btn b" id="toStat">看总进度</button>
    </div>`;
  const sc=document.getElementById('score');
  const upd=()=>{ sc.textContent = `进度：${FLAT.filter(x=>streak(x.vi,x.ii)>=3).length}/86 篇过关 · 位置 ${v+1}册${it.no}`; };
  upd();

  // 点击横线 → 变成输入框；回车提交并跳下一空
  const blanks=[...document.querySelectorAll('.blank')];
  function resetBlank(el){
    el.textContent = el.dataset.orig;
    el.classList.remove('filled','right','wrong');
    el.title = '';
    bindBlank(el);
  }
  function bindBlank(el){
    el.onclick = ()=>{
      if(el.querySelector('input')) return;
      const ans = el.dataset.ans;
      el.classList.remove('right','wrong');
      el.classList.add('filled');
      el.textContent = '';
      const inp = document.createElement('input');
      inp.placeholder = '默写这句';
      el.appendChild(inp); inp.focus();
      el.onclick = null;
      const submit = ()=>{
        if(inp.readOnly) return;
        const val = inp.value.trim();
        if(!val){ inp.remove(); el.textContent=el.dataset.orig; el.classList.remove('filled'); bindBlank(el); return; }
        inp.readOnly = true;
        const ok = norm(val)===norm(ans);
        el.classList.remove('filled'); el.classList.add(ok?'right':'wrong');
        el.title = ok ? '✓ 正确' : '✗ 应为：'+ans;
        if(!ok) resetWrongBtn.hidden = false;
      };
      inp.onblur = submit;
      inp.onkeydown = e=>{
        if(e.key==='Enter'){ e.preventDefault(); submit();
          const nx = blanks[blanks.indexOf(el)+1]; if(nx) nx.click(); }
        if(e.key==='Escape'){ e.preventDefault(); inp.remove(); resetBlank(el); }
      };
    };
  }
  blanks.forEach(el=>{ el.dataset.orig = el.textContent; bindBlank(el); });
  function norm(s){ return s.replace(/[\s，。！？；：、"''《》（）·…—]/g,''); }

  const resetWrongBtn = document.getElementById('resetWrong');
  if(resetWrongBtn) resetWrongBtn.onclick = ()=>{ blanks.forEach(resetBlank); resetWrongBtn.hidden = true; };
  document.getElementById('showAll').onclick=()=>{
    const c=document.getElementById('ansCard');
    c.style.display='block';
    c.scrollIntoView({behavior:'smooth',block:'start'});
  };
  document.getElementById('check').onclick=()=>{
    // 没填的空算错
    let ok=0, total=blanks.length;
    blanks.forEach(el=>{
      if(el.classList.contains('right')) ok++;
      else if(!el.classList.contains('filled')){ el.classList.add('wrong'); el.title='✗ 未作答'; }
    });
    judge(ok===total, ok===total?'':`${total-ok} / ${total} 空有错`);
  };
  document.getElementById('pass').onclick=()=>judge(true);
  document.getElementById('fail').onclick=()=>judge(false);
  document.getElementById('prev').onclick=()=>move(-1);
  document.getElementById('next').onclick=()=>move(1);
  document.getElementById('toStat').onclick=()=>{ MODE='stat'; syncBtn(); render(); };
  function judge(ok, detail){
    const kk=k(v,ii); STATE[kk]=STATE[kk]||{n:0,ok:''};
    const r=document.getElementById('res');
    if(ok){ STATE[kk].n=(STATE[kk].n||0)+1; STATE[kk].ok=new Date().toISOString().slice(0,10);
      r.className='res ok';
      r.textContent = STATE[kk].n>=3 ? '✓ 过关（连续3次全对）' : `✓ 记一次，还差 ${3-STATE[kk].n} 次`;
    } else { STATE[kk].n=0; r.className='res no';
      r.textContent='✗ 连续次数归零'+ (detail?'（'+detail+'）':'') + '，明天重来'; }
    save(); buildSide(); openVol(v); upd();
  }
}

/* ---------------- 背诵模式：逐句遮挡 ---------------- */
function renderRecite(){
  const {v,ii} = CUR, vol=DATA[v], it=vol.items[ii];
  const hz = it.hardList.length ? `<div class="hardbox"><h4>易错字</h4>${
    it.hardList.map(h=>`<span class="hz"><b>${h.zi}</b><span>${h.py}</span></span>`).join('')}</div>` : '';
  const body = it.paras.map(p=>p.split(/(?<=[。！？])/).filter(Boolean)
    .map(s=>`<span class="rline hidden">${s}</span>`).join('')).join('');
  document.getElementById('view').innerHTML=`
    <div class="hint">逐句自测：先在心里接下一句，点句子看答案。长按拖选可给重点句高亮。</div>
    <div class="card">
      <div class="title-row">
        <span class="t-no">${vol.volume} · 第${it.no}篇</span>
        <span class="t-name">${it.title}</span>
        <span class="t-au">${it.author||''}</span>
      </div>
      <div class="t-meta"><span class="chip">${it.type}</span><span class="chip lv">${it.len} 字</span></div>
      ${hz}
      <div class="recite" id="reciteBox">${body}</div>
    </div>
    <div class="hbtns">
      <button class="btn" id="revealAll">全部显示</button>
      <button class="btn" id="hideAll">全部遮住</button>
      <button class="btn" id="prev">← 上一篇</button>
      <button class="btn" id="next">下一篇 →</button>
    </div>`;
  document.querySelectorAll('.rline').forEach(el=>{
    el.onclick=()=>el.classList.toggle('hidden');
    el.oncontextmenu=e=>{ e.preventDefault(); el.classList.toggle('hi'); };
  });
  document.getElementById('revealAll').onclick=()=>document.querySelectorAll('.rline').forEach(e=>e.classList.remove('hidden'));
  document.getElementById('hideAll').onclick=()=>document.querySelectorAll('.rline').forEach(e=>e.classList.add('hidden'));
  document.getElementById('prev').onclick=()=>move(-1);
  document.getElementById('next').onclick=()=>move(1);
}

/* ---------------- 易错字表 ---------------- */
function renderReview(){
  const map = new Map();
  FLAT.forEach(({v,ii,it})=>it.hardList.forEach(h=>{
    if(!map.has(h.zi)) map.set(h.zi,{py:h.py,titles:[]});
    map.get(h.zi).titles.push(it.title);
  }));
  const rows=[...map.entries()].sort((a,b)=>b[1].titles.length-a[1].titles.length);
  document.getElementById('view').innerHTML=`
    <div class="note"><b>共 ${map.size} 个易错字</b>，来自 86 篇默写。排在前面的字跨篇重复出现，默写命中率最高，优先背。左栏点任一篇可回该篇练习。</div>
    <div class="card"><div class="tblwrap"><table>
      <thead><tr><th style="width:64px">字</th><th style="width:96px">读音</th><th style="width:56px" class="c">出现篇数</th><th>涉及篇目</th></tr></thead>
      <tbody>${rows.map(([z,info])=>`<tr>
        <td style="font-family:var(--serif);font-size:1.1rem;font-weight:700">${z}</td>
        <td style="color:var(--mut);font-size:.76rem">${info.py}</td>
        <td class="c"><b style="color:${info.titles.length>2?'var(--red)':'var(--tx)'}">${info.titles.length}</b></td>
        <td style="color:var(--tx2);font-size:.76rem">${[...new Set(info.titles)].join('、')}</td></tr>`).join('')}</tbody>
    </table></div></div>`;
}

/* ---------------- 进度总览 ---------------- */
function renderStat(){
  const done = FLAT.filter(x=>streak(x.vi,x.ii)>=3).length;
  const started = FLAT.filter(x=>streak(x.vi,x.ii)>0).length;
  const byv = DATA.map((v,vi)=>({v, done:v.items.filter((_,ii)=>streak(vi,ii)>=3).length, n:v.items.length}));
  const hzTotal = new Set(); FLAT.forEach(({it})=>it.hardList.forEach(h=>hzTotal.add(h.zi)));
  document.getElementById('view').innerHTML=`
    <div class="warn"><b>为什么只盯默写不够：</b>27 届上海中考语文已改三大板块——积累与运用约 20 分（默写仅 6 分）、阅读 70 分、作文 60 分。默写从旧卷约 12 分缩到 6 分，光背诗最多值 6 分。默写要「零错字」保住这 6 分，但提分主力在阅读和作文，见 <a href="chinese-repair-plan-V1.html">8个月补习计划</a>。</div>
    <div class="card">
      <div class="overview">
        <div class="ov"><b>${done}</b><span>篇连续 3 次无错（过关）</span></div>
        <div class="ov b"><b>${started}</b><span>篇已开始练习</span></div>
        <div class="ov"><b>${86-done}</b><span>篇待完成</span></div>
        <div class="ov a"><b>${hzTotal.size}</b><span>个易错字需掌握</span></div>
        <div class="ov g"><b>${26}</b><span>篇文言文（课内 16 分的地基）</span></div>
      </div>
    </div>
    <div class="card">
      <div class="title-row"><span class="t-name" style="font-size:1.05rem">按册过关情况</span></div>
      <div class="tblwrap"><table>
        <thead><tr><th>册次</th><th style="width:74px" class="c">篇数</th><th style="width:150px">进度</th><th style="width:74px" class="c">过关</th></tr></thead>
        <tbody>${byv.map(b=>`<tr><td>${b.v.volume}</td><td class="c">${b.n}</td>
          <td><div style="height:8px;background:var(--subtle);border-radius:4px;overflow:hidden">
            <div style="height:100%;width:${b.done/b.n*100}%;background:linear-gradient(90deg,var(--red),var(--red-l))"></div></div></td>
          <td class="c"><b>${b.done}/${b.n}</b></td></tr>`).join('')}</tbody>
      </table></div>
    </div>
    <div class="card">
      <div class="title-row"><span class="t-name" style="font-size:1.05rem">判卷标准</span></div>
      <table><tbody>
        <tr><td style="width:96px"><b>过关</b></td><td>同一篇连续 3 次默写无错字。左栏该篇出现 ✓。</td></tr>
        <tr><td><b>归零</b></td><td>错 1 字即连续次数归 0（理解性默写按字给分，错一字该空不得分）。</td></tr>
        <tr><td><b>周抽检</b></td><td>每周日随机抽 3 篇已过关的默写，错了重新背该篇。</td></tr>
      </tbody></table>
    </div>`;
}

/* ---------------- 导航 ---------------- */
function move(d){
  const idx = FLAT.findIndex(x=>x.vi===CUR.v && x.ii===CUR.ii);
  const n = Math.min(FLAT.length-1, Math.max(0, idx+d));
  CUR={v:FLAT[n].vi, ii:FLAT[n].ii};
  openVol(CUR.v); render(); window.scrollTo(0,0);
}
function syncBtn(){
  const m={'hide':'mHide','recite':'mRecite','review':'mReview','stat':'mStat'};
  for(const k in m) document.getElementById(m[k]).classList.toggle('on', MODE===k);
}
function render(){
  syncBtn();
  if(MODE==='hide') renderHide();
  else if(MODE==='recite') renderRecite();
  else if(MODE==='review') renderReview();
  else renderStat();
}
document.getElementById('mHide').onclick=()=>{MODE='hide';render();};
document.getElementById('mRecite').onclick=()=>{MODE='recite';render();};
document.getElementById('mReview').onclick=()=>{MODE='review';render();};
document.getElementById('mStat').onclick=()=>{MODE='stat';render();};
document.getElementById('mReset').onclick=()=>{
  if(confirm('清空全部默写进度记录？此操作不可撤销。')){ STATE={}; save(); buildSide(); render(); }
};
document.getElementById('fold').onclick=()=>document.body.classList.toggle('collapsed');

buildSide(); openVol(CUR.v); render();
</script>
</body>
</html>
'''

HTML = HTML.replace('__PAYLOAD__', payload)
out = f'{BASE}/recitation-drill-V1.html'
io.open(out, 'w', encoding='utf-8').write(HTML)
print('written', out, os.path.getsize(out)//1024, 'KB')