# -*- coding: utf-8 -*-
import os, sys, re

CSS_ADDITIONS = """
/* ---------- 快速选题面板与答题卡 (Picker Modal) ---------- */
.picker-pill{
  display:inline-flex;align-items:center;gap:.4rem;padding:.36rem .85rem;
  border:1px solid var(--border);border-radius:99px;background:var(--subtle);
  font-size:.82rem;font-weight:700;color:var(--tx);cursor:pointer;transition:all .15s;
}
.picker-pill:hover{background:var(--red-bg);border-color:var(--red-l);color:var(--red)}
.picker-pill-sub{
  font-size:.7rem;color:var(--mut);font-weight:600;padding:.08rem .45rem;
  border-radius:99px;background:#fff;border:1px solid var(--border);
}
.picker-pill:hover .picker-pill-sub{color:var(--red);border-color:#FECACA}

.pos-banner{
  background:var(--blue-bg);border:1px solid #BFDBFE;border-radius:10px;
  padding:.5rem .85rem;margin-bottom:.7rem;display:flex;align-items:center;
  justify-content:space-between;gap:.6rem;font-size:.78rem;color:var(--blue);
  animation:fadeSlideIn .25s ease;
}
.pos-banner b{font-weight:700}
.pos-banner-btn{
  border:1px solid #BFDBFE;background:#fff;color:var(--blue);border-radius:6px;
  padding:.18rem .5rem;font-size:.72rem;font-weight:700;cursor:pointer;flex:none;
}
.pos-banner-btn:hover{background:var(--blue);color:#fff}
.pos-banner-close{border:0;background:transparent;color:var(--blue);cursor:pointer;font-size:1rem;line-height:1;padding:0 .2rem}

.modal-mask{
  position:fixed;top:0;left:0;right:0;bottom:0;
  background:rgba(15,23,42,.5);backdrop-filter:blur(3px);
  z-index:999;display:none;align-items:center;justify-content:center;
  padding:1rem;opacity:0;transition:opacity .2s ease;
}
.modal-mask.show{display:flex;opacity:1}
.modal-box{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  width:100%;max-width:700px;max-height:86vh;
  box-shadow:0 20px 25px -5px rgba(0,0,0,.18), 0 8px 10px -6px rgba(0,0,0,.1);
  display:flex;flex-direction:column;overflow:hidden;
  animation:modalScale .2s cubic-bezier(.16,1,.3,1);
}
@keyframes modalScale{from{transform:scale(.95);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes fadeSlideIn{from{transform:translateY(-6px);opacity:0}to{transform:translateY(0);opacity:1}}

.modal-head{
  padding:.85rem 1.15rem;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;gap:.5rem;
  background:#fff;flex:none;
}
.modal-head h3{font-size:1.02rem;font-weight:800;color:var(--tx);display:flex;align-items:center;gap:.4rem}
.modal-head p{font-size:.74rem;color:var(--mut);margin-top:1px}
.modal-close-btn{
  border:0;background:var(--subtle);border-radius:8px;
  width:32px;height:32px;font-size:1.15rem;color:var(--mut);cursor:pointer;
  display:inline-flex;align-items:center;justify-content:center;transition:all .15s;
}
.modal-close-btn:hover{background:#FEE2E2;color:var(--red)}

.modal-tools{
  padding:.75rem 1.15rem;background:var(--bg);border-bottom:1px solid var(--border);
  display:flex;flex-direction:column;gap:.55rem;flex:none;
}
.jump-row{display:flex;align-items:center;gap:.45rem;flex-wrap:wrap}
.jump-input-box{
  display:inline-flex;align-items:center;gap:.3rem;background:#fff;
  border:1px solid var(--border);border-radius:8px;padding:.2rem .5rem;
}
.jump-input-box input{
  width:55px;border:none;outline:none;font-size:.88rem;
  font-weight:700;color:var(--tx);text-align:center;
}
.jump-submit{
  border:0;background:var(--red);color:#fff;border-radius:8px;
  padding:.38rem .75rem;font-size:.78rem;font-weight:700;cursor:pointer;
}
.jump-submit:hover{background:var(--red-l)}
.jump-quick{
  border:1px solid var(--border);background:#fff;color:var(--tx2);
  border-radius:8px;padding:.35rem .6rem;font-size:.75rem;font-weight:600;cursor:pointer;
}
.jump-quick:hover{border-color:var(--blue);color:var(--blue);background:var(--blue-bg)}

.filter-row{display:flex;align-items:center;justify-content:space-between;gap:.5rem;flex-wrap:wrap}
.picker-sec-select{
  border:1px solid var(--border);background:#fff;border-radius:8px;
  padding:.32rem .55rem;font-size:.78rem;font-weight:600;color:var(--tx);outline:none;
}
.picker-tabs{display:flex;gap:.25rem}
.ptab{
  border:1px solid var(--border);background:#fff;border-radius:7px;
  padding:.28rem .55rem;font-size:.74rem;font-weight:600;color:var(--tx2);cursor:pointer;
}
.ptab.active{background:var(--red);border-color:var(--red);color:#fff}

.modal-body{flex:1;overflow-y:auto;padding:.9rem 1.15rem}
.picker-grid{
  display:grid;grid-template-columns:repeat(auto-fill, minmax(46px, 1fr));gap:.45rem;
}
.q-btn{
  position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;
  aspect-ratio:1;border-radius:9px;border:1px solid var(--border);background:#fff;
  font-size:.82rem;font-weight:700;color:var(--tx2);cursor:pointer;
  transition:all .12s ease;user-select:none;padding:.15rem;
}
.q-btn:hover{border-color:var(--red-l);transform:translateY(-1px);box-shadow:0 2px 4px rgba(0,0,0,.08)}
.q-btn.current{
  border-color:var(--red);background:var(--red-bg);color:var(--red);font-weight:800;
  box-shadow:0 0 0 2px rgba(239,68,68,.3);
}
.q-btn.known{
  background:var(--green-bg);border-color:#A7F3D0;color:var(--green);
}
.q-btn.known.current{
  box-shadow:0 0 0 2px var(--green);border-color:var(--green);
}
.q-btn-sub{
  font-size:.56rem;font-weight:600;line-height:1;margin-top:1px;color:inherit;opacity:.75;
}
.q-btn-dot{
  position:absolute;top:3px;right:3px;width:5px;height:5px;border-radius:50%;
  background:var(--green);
}
.q-btn.current .q-btn-dot{background:var(--red)}

.modal-foot{
  padding:.6rem 1.15rem;border-top:1px solid var(--border);background:#fff;
  display:flex;align-items:center;justify-content:space-between;gap:.5rem;
  font-size:.72rem;color:var(--mut);flex-wrap:wrap;flex:none;
}
.legend-group{display:flex;gap:.7rem;align-items:center}
.legend-item{display:inline-flex;align-items:center;gap:.3rem}
.legend-dot{width:7px;height:7px;border-radius:50%;display:inline-block}
.legend-dot.cur{background:var(--red)}
.legend-dot.kn{background:var(--green)}
.legend-dot.un{background:var(--border)}
"""

MODAL_HTML = """
<div id="picker-modal" class="modal-mask" onclick="closePickerModal()">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-head">
      <div>
        <h3 id="picker-title">📋 题库选题卡 · 快速跳题</h3>
        <p id="picker-subtitle">全部板块 · 共 1055 题 · 已熟 0 / 1055</p>
      </div>
      <button class="modal-close-btn" id="picker-close-btn" title="关闭 (Esc)">✕</button>
    </div>
    <div class="modal-tools">
      <div class="jump-row">
        <div class="jump-input-box">
          <span style="font-size:0.75rem;color:var(--mut)">跳至第</span>
          <input type="number" id="jump-val" min="1" placeholder="题号">
          <span style="font-size:0.75rem;color:var(--mut)">题</span>
        </div>
        <button class="jump-submit" id="jump-submit-btn">前往</button>
        <button class="jump-quick" id="jump-first-unmastered">首个未背熟</button>
        <button class="jump-quick" id="jump-first-btn">第 1 题</button>
        <button class="jump-quick" id="jump-last-btn">末题</button>
      </div>
      <div class="filter-row">
        <div style="display:flex;align-items:center;gap:4px">
          <label for="picker-sec-select" style="font-size:0.74rem;color:var(--mut);font-weight:600">板块：</label>
          <select id="picker-sec-select" class="picker-sec-select"></select>
        </div>
        <div class="picker-tabs">
          <button class="ptab active" data-tab="all" id="tab-all">全部 <span id="cnt-all">(0)</span></button>
          <button class="ptab" data-tab="todo" id="tab-todo">未背 <span id="cnt-todo">(0)</span></button>
          <button class="ptab" data-tab="done" id="tab-done">已背 <span id="cnt-done">(0)</span></button>
        </div>
      </div>
    </div>
    <div class="modal-body">
      <div class="picker-grid" id="picker-grid"></div>
    </div>
    <div class="modal-foot">
      <div class="legend-group">
        <span class="legend-item"><span class="legend-dot cur"></span> 当前学习</span>
        <span class="legend-item"><span class="legend-dot kn"></span> 已背熟</span>
        <span class="legend-item"><span class="legend-dot un"></span> 未背熟</span>
      </div>
      <div>支持快捷键 <kbd>G</kbd> 开启 · <kbd>Esc</kbd> 关闭</div>
    </div>
  </div>
</div>
"""

JS_LOGIC = """
const IMGPH = "data:image/svg+xml," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="8" height="6"><rect width="8" height="6" fill="#e2e8f0"/></svg>');
const LSKEY = "8shang-recite-v1";
const POSKEY = "8shang-recite-pos-map";
const SECKEY = "8shang-recite-cursec";

let known = {};
try{ known = JSON.parse(localStorage.getItem(LSKEY) || "{}"); }catch(e){ known = {}; }

let secPos = {};
try{ secPos = JSON.parse(localStorage.getItem(POSKEY) || "{}"); }catch(e){ secPos = {}; }

let mode="recite", curSec="all", cursor=0, qOnly=false, imgOnly=false, query="";
let alwaysAns=true;
try{ alwaysAns = localStorage.getItem("8shang-recite-ans") !== "0"; }catch(e){}
let showJy=true;
try{ showJy = localStorage.getItem("8shang-recite-jx") !== "0"; }catch(e){}
document.body.classList.toggle("nojx", !showJy);
const byId = {}; DATA.questions.forEach(q=>byId[q.id]=q);

// 恢复上次学习板块与题号
let savedSec = localStorage.getItem(SECKEY);
if (savedSec && (savedSec === "all" || DATA.sections.some(s => s.sid === savedSec))) {
  curSec = savedSec;
}

let showPosRestoreBanner = false;

function filtered(){
  return DATA.questions.filter(q=>{
    if(curSec!=="all" && q.sid!==curSec) return false;
    if(qOnly && known[q.id]) return false;
    if(imgOnly && !q.ph) return false;
    if(query){
      const s=q.stem+"\\n"+q.ans;
      if(!s.toLowerCase().includes(query)) return false;
    }
    return true;
  });
}

// 初始化光标定位
const fInit = filtered();
const targetQid = secPos[curSec] || secPos["all"];
if (targetQid) {
  const initIdx = fInit.findIndex(q => q.id === targetQid);
  if (initIdx > 0) {
    cursor = initIdx;
    showPosRestoreBanner = true;
  }
}

function save(){ try{ localStorage.setItem(LSKEY, JSON.stringify(known)); }catch(e){} }
function totalKnown(){ return DATA.questions.filter(q=>known[q.id]).length; }

// 记录当前题号与板块位置
function recordPos(){
  const f = filtered();
  if (f[cursor]) {
    const qid = f[cursor].id;
    secPos[curSec] = qid;
    secPos["all"] = qid;
    try {
      localStorage.setItem(POSKEY, JSON.stringify(secPos));
      localStorage.setItem(SECKEY, curSec);
    } catch(e){}
    const topNum = document.getElementById("top-qnum");
    if (topNum) topNum.textContent = (cursor + 1);
  }
}

// 切换板块
function switchSection(sid, targetQid){
  curSec = sid;
  const f = filtered();
  let idx = -1;
  if (targetQid) {
    idx = f.findIndex(q => q.id === targetQid);
  } else if (secPos[curSec]) {
    idx = f.findIndex(q => q.id === secPos[curSec]);
  }
  if (idx < 0) {
    const fi = f.findIndex(q => !known[q.id]);
    idx = fi >= 0 ? fi : 0;
  }
  cursor = Math.max(0, idx);
  recordPos();
  renderSidebar();
  render();
}

/* ---------------- 侧栏 ---------------- */
function renderSidebar(){
  const box=document.getElementById("sec-list");
  const tot=DATA.questions.length;
  let h=`<div class="sec ${curSec==="all"?"active":""}" data-sid="all">
    <div class="sec-row"><span class="sec-dot ${totalKnown()>=tot?"full":""}"></span>
    <span class="sec-name">全部板块</span><span class="sec-n">${tot}</span></div></div>`;
  for(const s of DATA.sections){
    const qs=DATA.questions.filter(q=>q.sid===s.sid);
    const k=qs.filter(q=>known[q.id]).length;
    h+=`<div class="sec ${curSec===s.sid?"active":""}" data-sid="${s.sid}">
      <div class="sec-row"><span class="sec-dot ${k>=qs.length&&qs.length>0?"full":""}"></span>
      <span class="sec-name">${s.s}</span><span class="sec-n">${k}/${qs.length}</span></div></div>`;
  }
  box.innerHTML=h;
  box.querySelectorAll(".sec").forEach(el=>{
    el.onclick=()=>{
      showPosRestoreBanner = false;
      switchSection(el.dataset.sid);
    };
  });
  const t=totalKnown();
  document.getElementById("foot-label").textContent=`总进度 ${t} / ${DATA.questions.length}`;
  document.getElementById("progress-fill").style.width=(t/DATA.questions.length*100)+"%";
  const jl=document.getElementById("jx-label");
  if(jl) jl.textContent=`含解析 ${DATA.jxN} / ${DATA.total} 题`;
}

/* ---------------- 工具 ---------------- */
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function hl(text){
  if(text==null) return "";
  const e=esc(text).replace(/\\*\\*([^*]+)\\*\\*/g,'<b class="k">$1</b>');
  if(!query) return e;
  return e.replace(new RegExp("("+query.replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&")+")","gi"),"<mark>$1</mark>");
}
/* 选择题：高亮正确选项 */
function optHl(stem, ans){
  if(!/^[A-D]{1,4}$/.test(ans.trim())) return null;
  const lines=stem.split("\\n");
  const idx=lines.map((L,i)=>{
    const m=L.match(/^\\s*[·•]?\\s*([A-D])[.、．]/);
    return m && ans.includes(m[1]) ? i : -1;
  }).filter(i=>i>=0);
  if(!idx.length) return null;
  return lines.map((L,i)=>{
    let e=esc(L);
    if(idx.includes(i)) e="<mark>"+e+"</mark>";
    return e;
  }).join("\\n");
}
function stemHtml(q, hlMode){
  let body;
  if(hlMode){ body=optHl(q.stem,q.ans)||hl(q.stem); }
  else{
    body=esc(q.stem)
      .replace(/_{2,}/g,'<span class="blank">＿＿＿＿</span>')
      .replace(/\\n/g,"\\n");
  }
  return body;
}
function ansText(q){
  if(q.ph && !q.ans || (q.ans.startsWith("请对照")||q.ans.startsWith("请查看"))) return null;
  return q.ans;
}

/* ---------------- 背诵模式 ---------------- */
function renderRecite(){
  const f=filtered(), view=document.getElementById("view");
  if(!f.length){ view.innerHTML='<div class="empty">没有符合条件的题目</div>'; return; }
  if(cursor>=f.length) cursor=f.length-1; if(cursor<0) cursor=0;
  recordPos();
  const q=f[cursor], at=ansText(q);
  const knownOn=!!known[q.id];
  const bar=`<div id="cardbar"><div id="cardbar-f" style="width:${f.length?((cursor+1)/f.length*100):0}%"></div></div>`;
  let answerHtml;
  if(at){
    answerHtml=`<div class="atext">${hl(at).replace(/ ｜ /g,'<br>')}</div>`;
    if(q.aimg) answerHtml+=`<img loading="lazy" src="${q.aimg}" alt="参考答案图">`;
  }else if(q.aimg){
    answerHtml=`<div class="atext">对照下方参考答案原图自评</div><img loading="lazy" src="${q.aimg}" alt="参考答案图">`;
  }else{
    answerHtml=`<div class="atext">⚠️ 原仓库未提供本题答案（原书答案页可查：板块内“原资料页”）</div>`;
  }

  let posBannerHtml = "";
  if (showPosRestoreBanner && cursor > 0) {
    posBannerHtml = `<div class="pos-banner" id="pos-banner">
      <span>📖 已自动恢复上次学习进度：<b>${q.s} · 第 ${q.n} 题</b>（第 ${cursor+1} / ${f.length} 题）</span>
      <div style="display:flex;align-items:center;gap:6px">
        <button class="pos-banner-btn" onclick="cursor=0;recordPos();showPosRestoreBanner=false;renderRecite();">从第1题重新开始</button>
        <button class="pos-banner-close" onclick="showPosRestoreBanner=false;document.getElementById('pos-banner')?.remove()" title="关闭提示">×</button>
      </div>
    </div>`;
  }

  view.innerHTML=`<div id="card-wrap">${posBannerHtml}${bar}
    <div class="card">
      <div class="meta">
        <span class="chip">${q.s}</span>
        <span class="chip gray">第 ${q.n} 题</span>
        <span class="chip gray">${q.t}</span>
        ${q.tag?`<span class="chip gray">${q.tag}</span>`:""}
        ${q.ph?`<span class="chip" style="background:var(--amber-bg);color:var(--amber)">需看原题图</span>`:""}
        ${q.jx?`<span class="chip" style="background:var(--blue-bg);color:var(--blue)">有解析</span>`:""}
      </div>
      ${q.ph?`<div class="imgbox show"><img loading="lazy" src="${q.img}" alt="原题图"></div>`
            :`<div class="stem">${stemHtml(q,true)}</div>
              ${q.img?`<button class="fchip" style="margin-top:.8rem" onclick="this.nextElementSibling.classList.toggle('show');this.textContent=this.textContent.includes('题')?'收起题图':'看题图'">看题图</button><div class="imgbox"><img loading="lazy" src="${q.img}"></div>`:""}`}
      ${q.ph&&q.src?`<button class="fchip" style="margin-top:.5rem" onclick="this.nextElementSibling.classList.toggle('show')">看原资料页</button><div class="imgbox"><img loading="lazy" src="${q.src}"></div>`:""}
      ${alwaysAns?"":'<button id="reveal-btn">显示答案（空格）</button>'}
      <div class="answer${alwaysAns?" show":""}" id="ansbox"><div class="alabel">答案</div>${answerHtml}
        ${q.jx?`<div class="jx"><div class="jxlabel">解析 · 为什么是这个答案</div><div class="jxtext">${hl(q.jx)}</div></div>`:""}
      </div>
      <div class="ops">
        <button class="know ${knownOn?"on":""}" id="know-btn">${knownOn?"✓ 已背熟（点击取消）":"标记为已背熟"}</button>
      </div>
    </div>
    <div class="navrow">
      <button id="prev-btn" title="上一题 (←)">← 上一题</button>
      <button id="open-picker-btn" class="picker-pill" title="点击打开选题答题卡，快速跳题 (快捷键 G)">
        <span>第 <b>${cursor+1}</b> / ${f.length} 题</span>
        <span class="picker-pill-sub">📋 选题 ▾</span>
      </button>
      <button id="next-btn" title="下一题 (→ 或 空格)">下一题 →</button>
    </div>
    <div class="hint"><kbd>空格</kbd> 答案/下题 · <kbd>G</kbd> 选题卡 · <kbd>M</kbd> 熟记 · <kbd>←</kbd><kbd>→</kbd> 翻题 · <kbd>Shift+←/→</kbd> 快翻10题 · <kbd>/</kbd> 搜索</div>
  </div>`;
  const rb=document.getElementById("reveal-btn");
  if(rb) rb.onclick=()=>{
    document.getElementById("ansbox").classList.add("show");
    rb.style.display="none";
  };
  document.getElementById("know-btn").onclick=()=>{
    if(known[q.id]) delete known[q.id]; else known[q.id]=1;
    save(); renderSidebar(); renderRecite();
  };
  document.getElementById("prev-btn").onclick=()=>{cursor--;showPosRestoreBanner=false;recordPos();renderRecite()};
  document.getElementById("next-btn").onclick=()=>{cursor++;showPosRestoreBanner=false;recordPos();renderRecite()};
  document.getElementById("open-picker-btn").onclick=openPickerModal;
  document.getElementById("view").scrollTop=0;
}

/* ---------------- 速览模式 ---------------- */
function renderBrowse(){
  const f=filtered(), view=document.getElementById("view");
  if(!f.length){ view.innerHTML='<div class="empty">没有符合条件的题目</div>'; return; }
  let h='<div id="list">';
  f.forEach(q=>{
    const at=ansText(q);
    const body=optHl(q.stem,q.ans)||hl(q.stem).replace(/_{2,}/g,'<span class="blank">＿＿＿＿</span>');
    let ans="";
    if(at) ans=`<div class="li-ans">${hl(at).replace(/ ｜ /g,'<br>')}</div>`;
    else if(q.aimg) ans=`<div class="li-ans">对照参考答案原图自评 ↓<img class="qimg" loading="lazy" src="${q.aimg}"></div>`;
    else ans=`<div class="li-ans" style="background:var(--amber-bg);color:var(--amber)">原仓库未提供本题答案</div>`;
    h+=`<div class="li" data-id="${q.id}">
      <div class="li-head">
        <span class="li-n">#${q.n}</span>
        <span class="li-sect">${q.s}${q.tag?" · "+q.tag:""}</span>
        ${known[q.id]?'<span class="li-know">已背熟 ✓</span>':""}
      </div>
      ${q.ph?`<img class="qimg" loading="lazy" src="${q.img}">`:`<div class="li-stem">${body}</div>`}
      ${ans}
      ${q.jx?`<div class="li-jx"><div style="font-size:0.75rem;font-weight:700;color:var(--blue);margin-bottom:2px">解析 · 为什么是这个答案</div>${hl(q.jx)}</div>`:""}
    </div>`;
  });
  h+='</div>';
  view.innerHTML=h;
  view.scrollTop=0;
  view.querySelectorAll(".li").forEach(el=>{
    el.onclick=()=>{
      const id=el.dataset.id, f2=filtered();
      const i=f2.findIndex(q=>q.id===id);
      if(i>=0){ mode="recite"; cursor=i; recordPos(); setMode(); }
    };
  });
}

function render(){ mode==="recite"?renderRecite():renderBrowse(); renderSidebar(); }
function setMode(){
  document.getElementById("m-recite").classList.toggle("on",mode==="recite");
  document.getElementById("m-browse").classList.toggle("on",mode==="browse");
  render();
}

/* ---------------- 选题面板 (Picker Modal) ---------------- */
let pickerTab = "all";

function openPickerModal(){
  const modal = document.getElementById("picker-modal");
  if (!modal) return;
  modal.classList.add("show");
  populatePickerSecSelect();
  renderPickerGrid();
  setTimeout(()=>{
    const inp = document.getElementById("jump-val");
    if(inp){ inp.value = cursor + 1; inp.select(); }
  }, 100);
}

function closePickerModal(){
  const modal = document.getElementById("picker-modal");
  if (modal) modal.classList.remove("show");
}

function populatePickerSecSelect(){
  const sel = document.getElementById("picker-sec-select");
  if (!sel) return;
  let opt = `<option value="all" ${curSec==="all"?"selected":""}>全部板块 (${DATA.questions.length}题)</option>`;
  for (const s of DATA.sections) {
    opt += `<option value="${s.sid}" ${curSec===s.sid?"selected":""}>${s.s} (${s.n}题)</option>`;
  }
  sel.innerHTML = opt;
  sel.onchange = (e) => {
    switchSection(e.target.value);
    populatePickerSecSelect();
    renderPickerGrid();
  };
}

function renderPickerGrid(){
  const f = filtered();
  const curQ = f[cursor];
  const grid = document.getElementById("picker-grid");
  const sub = document.getElementById("picker-subtitle");
  
  const secName = curSec === "all" ? "全部板块" : (DATA.sections.find(s=>s.sid===curSec)?.s || "当前板块");
  const knownCount = f.filter(q=>known[q.id]).length;
  if (sub) {
    sub.textContent = `${secName} · 共 ${f.length} 题 · 已背熟 ${knownCount} / ${f.length}`;
  }

  const allCount = f.length;
  const todoCount = allCount - knownCount;
  const cntAll = document.getElementById("cnt-all"); if(cntAll) cntAll.textContent = `(${allCount})`;
  const cntTodo = document.getElementById("cnt-todo"); if(cntTodo) cntTodo.textContent = `(${todoCount})`;
  const cntDone = document.getElementById("cnt-done"); if(cntDone) cntDone.textContent = `(${knownCount})`;

  let displayList = [];
  f.forEach((q, idx) => {
    const isDone = !!known[q.id];
    if (pickerTab === "todo" && isDone) return;
    if (pickerTab === "done" && !isDone) return;
    displayList.push({ q, idx, isDone, isCur: (curQ && curQ.id === q.id) });
  });

  if (!displayList.length) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:2.5rem 1rem;color:var(--mut);font-size:0.85rem">该筛选分类下暂无题目</div>';
    return;
  }

  let h = "";
  displayList.forEach(item => {
    const { q, idx, isDone, isCur } = item;
    const numDisplay = curSec === "all" ? (idx + 1) : q.n;
    const subText = curSec === "all" ? q.s.substring(0, 2) : "";
    let cls = "q-btn";
    if (isDone) cls += " known";
    if (isCur) cls += " current";
    
    h += `<button class="${cls}" data-idx="${idx}" title="${q.s} 第${q.n}题 (${idx+1}/${f.length}) ${isDone?'[已背熟]':''}">
      <span>${numDisplay}</span>
      ${subText ? `<span class="q-btn-sub">${subText}</span>` : ""}
      ${isDone ? `<span class="q-btn-dot"></span>` : ""}
    </button>`;
  });
  grid.innerHTML = h;

  grid.querySelectorAll(".q-btn").forEach(btn => {
    btn.onclick = () => {
      const idx = parseInt(btn.dataset.idx, 10);
      if (!isNaN(idx) && idx >= 0 && idx < f.length) {
        showPosRestoreBanner = false;
        cursor = idx;
        recordPos();
        closePickerModal();
        if (mode !== "recite") {
          mode = "recite";
          setMode();
        } else {
          renderRecite();
        }
      }
    };
  });
}

function doJump(){
  const f = filtered();
  const inp = document.getElementById("jump-val");
  if (!inp) return;
  const val = parseInt(inp.value.trim(), 10);
  if (isNaN(val) || val < 1 || val > f.length) {
    alert(`请输入 1 到 ${f.length} 之间的有效题号`);
    return;
  }
  showPosRestoreBanner = false;
  cursor = val - 1;
  recordPos();
  closePickerModal();
  if (mode !== "recite") {
    mode = "recite";
    setMode();
  } else {
    renderRecite();
  }
}

function jumpFirstUnmastered(){
  const f = filtered();
  const fi = f.findIndex(q => !known[q.id]);
  if (fi < 0) {
    alert("🎉 恭喜！当前筛选范围内所有题目均已背熟！");
    return;
  }
  showPosRestoreBanner = false;
  cursor = fi;
  recordPos();
  closePickerModal();
  if (mode !== "recite") {
    mode = "recite";
    setMode();
  } else {
    renderRecite();
  }
}

function jumpFirst(){
  showPosRestoreBanner = false;
  cursor = 0;
  recordPos();
  closePickerModal();
  if (mode !== "recite") { mode = "recite"; setMode(); } else { renderRecite(); }
}

function jumpLast(){
  const f = filtered();
  showPosRestoreBanner = false;
  cursor = Math.max(0, f.length - 1);
  recordPos();
  closePickerModal();
  if (mode !== "recite") { mode = "recite"; setMode(); } else { renderRecite(); }
}

/* ---------------- 事件绑定 ---------------- */
document.getElementById("m-recite").onclick=()=>{mode="recite";setMode()};
document.getElementById("m-browse").onclick=()=>{mode="browse";setMode()};
document.getElementById("burger").onclick=()=>document.body.classList.toggle("collapsed");
document.getElementById("search").oninput=e=>{query=e.target.value.trim().toLowerCase();cursor=0;render()};
document.getElementById("f-todo").onclick=e=>{qOnly=!qOnly;e.target.classList.toggle("on",qOnly);cursor=0;render()};
document.getElementById("f-img").onclick=e=>{imgOnly=!imgOnly;e.target.classList.toggle("on",imgOnly);cursor=0;render()};

const topPicker = document.getElementById("top-picker-btn");
if (topPicker) topPicker.onclick = openPickerModal;

document.getElementById("picker-close-btn").onclick = closePickerModal;
document.getElementById("jump-submit-btn").onclick = doJump;
document.getElementById("jump-first-unmastered").onclick = jumpFirstUnmastered;
document.getElementById("jump-first-btn").onclick = jumpFirst;
document.getElementById("jump-last-btn").onclick = jumpLast;
document.getElementById("jump-val").onkeydown = (e) => { if(e.key === "Enter") doJump(); };

// 选题面板分类 Tab
document.querySelectorAll(".ptab").forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll(".ptab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    pickerTab = tab.dataset.tab;
    renderPickerGrid();
  };
});

function syncAnsBtn(){
  const b=document.getElementById("f-ans");
  b.classList.toggle("ans-on",alwaysAns);
  b.classList.toggle("on",!alwaysAns);
  b.textContent=alwaysAns?"答案默认展开":"答案手动展开";
}
document.getElementById("f-ans").onclick=()=>{
  alwaysAns=!alwaysAns;
  try{ localStorage.setItem("8shang-recite-ans",alwaysAns?"1":"0"); }catch(e){}
  syncAnsBtn(); renderRecite();
};
function syncJyBtn(){
  const b=document.getElementById("f-jx");
  b.classList.toggle("jx-on",showJy);
  b.classList.toggle("on",!showJy);
  b.textContent=showJy?"显示解析":"隐藏解析";
}
document.getElementById("f-jx").onclick=()=>{
  showJy=!showJy;
  try{ localStorage.setItem("8shang-recite-jx",showJy?"1":"0"); }catch(e){}
  document.body.classList.toggle("nojx",!showJy);
  syncJyBtn();
};

/* 题图 / 答案图 点击看大图 */
document.getElementById("view").addEventListener("click",e=>{
  const t=e.target;
  if(t&&t.tagName==="IMG"&&t.closest(".imgbox")&&t.src){
    e.stopPropagation(); e.preventDefault(); window.open(t.src,"_blank");
  }
},true);

document.addEventListener("keydown",e=>{
  const tag=(e.target.tagName||"").toLowerCase();
  if(tag==="input"||tag==="textarea"||tag==="select"){
    if(e.key==="Escape") {
      e.target.blur();
      closePickerModal();
    }
    return;
  }
  if(e.key==="Escape"){ closePickerModal(); return; }
  if(e.key==="/"){ e.preventDefault(); document.getElementById("search").focus(); return; }
  if(e.key==="g"||e.key==="G"){ e.preventDefault(); openPickerModal(); return; }
  if(mode!=="recite") return;
  const f=filtered(); if(!f.length) return;
  const ansShown=document.getElementById("ansbox")?.classList.contains("show");
  
  if(e.shiftKey && e.key==="ArrowRight" || e.key==="PageDown"){
    e.preventDefault();
    cursor=Math.min(cursor+10, f.length-1);
    recordPos();
    renderRecite();
    return;
  }
  if(e.shiftKey && e.key==="ArrowLeft" || e.key==="PageUp"){
    e.preventDefault();
    cursor=Math.max(cursor-10, 0);
    recordPos();
    renderRecite();
    return;
  }
  if(e.code==="Space"){
    e.preventDefault();
    if(!ansShown){ document.getElementById("ansbox")?.classList.add("show"); const b=document.getElementById("reveal-btn"); if(b)b.style.display="none"; }
    else{ cursor=(cursor+1)%f.length; recordPos(); renderRecite(); }
  }else if(e.key==="ArrowRight"){
    cursor=Math.min(cursor+1,f.length-1); recordPos(); renderRecite();
  }else if(e.key==="ArrowLeft"){
    cursor=Math.max(cursor-1,0); recordPos(); renderRecite();
  }else if(e.key==="m"||e.key==="M"){
    const q=f[cursor]; if(known[q.id]) delete known[q.id]; else known[q.id]=1;
    save(); renderRecite();
  }
});

syncAnsBtn(); syncJyBtn(); renderSidebar(); render();
"""

def upgrade_file(filepath):
    print(f"Upgrading {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS if not present
    if "/* ---------- 快速选题面板与答题卡 (Picker Modal) ---------- */" not in content:
        content = content.replace("</style>", CSS_ADDITIONS + "\n</style>", 1)

    # 2. Add Topbar button if not present
    top_btn = '<button class="fchip" id="top-picker-btn" title="选题答题卡 / 快速跳题 (快捷键 G)">📋 选题 (第<span id="top-qnum">1</span>题)</button>'
    if 'id="top-picker-btn"' not in content:
        content = content.replace(
            '<div class="modes">\n      <button id="m-recite" class="on">背诵</button>\n      <button id="m-browse">速览</button>\n    </div>',
            '<div class="modes">\n      <button id="m-recite" class="on">背诵</button>\n      <button id="m-browse">速览</button>\n    </div>\n    ' + top_btn
        )

    # 3. Add Modal HTML if not present
    if 'id="picker-modal"' not in content:
        content = content.replace('</div>\n\n<script>', '</div>\n' + MODAL_HTML + '\n<script>')

    # 4. Replace script logic from const IMGPH to </script>
    script_start = content.find('const IMGPH = ')
    script_end = content.find('</script>', script_start)
    if script_start != -1 and script_end != -1:
        content = content[:script_start] + JS_LOGIC.strip() + "\n" + content[script_end:]
    else:
        print("Warning: could not locate script boundaries in", filepath)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully upgraded {filepath}! Size: {os.path.getsize(filepath) / 1024:.1f} KB")

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target1 = os.path.join(ROOT, "chinese", "recitation-bank-V1.html")
    upgrade_file(target1)

    target2 = os.path.join(ROOT, "资料索引", "8shang_yuwen_jichu", "导出", "背诵版.html")
    if os.path.exists(target2):
        upgrade_file(target2)
