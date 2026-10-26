/* ---------- data helpers ---------- */
const ORDER = D.entries.slice().sort((a,b)=>(a.dlc-b.dlc)||a.id.localeCompare(b.id)); // save-code bit order: L001…L232, H001…H132 (never reorder)
const IDX = new Map(ORDER.map((e,i)=>[e.id,i]));
const BYN = {}; D.entries.forEach(e=>BYN[e.n]=e);
const STONES = D.stones; // save-code bit order (never reorder; append new stones at the end)
const LUMIOSE = ORDER.filter(e=>!e.dlc).length, DLC_STOP = 11;
const state = {dex:new Set(), meg:new Set(), dlc:true};
const $ = s=>document.querySelector(s);
const show = e=>state.dlc || !e.dlc;
const visStops = ()=>D.stops.map((_,i)=>i).filter(i=>state.dlc || i<DLC_STOP);

/* ---------- i18n ---------- */
let LANG = "en";
const T = ()=>I18N[LANG];
const EN = I18N.en;
function fill(str,p){ return String(str).replace(/\{([a-z0-9]+)\}/gi,(all,k)=>p && k in p ? p[k] : all); }
function t(key,p){ const v=(T().ui||{})[key]; return fill(v!=null ? v : EN.ui[key], p); }
const nm = n=>N.NAMES[LANG][n] || N.NAMES.en[n];
const item = id=>N.ITEMS[LANG][id] || N.ITEMS.en[id];
const typeName = ty=>ty==="Special" ? (T().how.special||EN.how.special) : (N.TYPES[LANG][ty] || ty);
const lv = n=>fill(T().lv||EN.lv,{n});
const H = k=>{ const v=(T().how||{})[k]; return v!=null ? v : EN.how[k]; };
const C = k=>{ const v=(T().cond||{})[k]; return v!=null ? v : EN.cond[k]; };
const sep = ()=>T().sep||EN.sep;

const STONE_ITEM = {duskstone:"dusk-stone",firestone:"fire-stone",icestone:"ice-stone",leafstone:"leaf-stone",moonstone:"moon-stone",
  shinystone:"shiny-stone",sunstone:"sun-stone",thunderstone:"thunder-stone",waterstone:"water-stone",blackaugurite:"black-augurite",
  galaricacuff:"galarica-cuff",galaricawreath:"galarica-wreath",auspiciousarmor:"auspicious-armor",maliciousarmor:"malicious-armor"};
const TRADE_ITEM = {tradeupgrade:"upgrade",tradedubiousdisc:"dubious-disc","tradeking'srock":"kings-rock",trademetalcoat:"metal-coat",
  tradesachet:"sachet",tradewhippeddream:"whipped-dream"};
function cond(m){
  let r;
  if(!m) return C("special");
  if((r=m.match(/^l(\d+)$/))) return lv(r[1]);
  if((r=m.match(/^l(day|night)(\d+)$/))) return lv(r[2])+C(r[1]);
  if(m==="l30night") return lv(30)+C("night");
  if(m==="l32dark") return lv(32)+C("dark");
  if(m==="l50rain") return lv(50)+C("rain");
  if(m==="nature30") return lv(30)+C("nature");
  if(m==="trade") return C("trade");
  if(TRADE_ITEM[m]) return fill(C("tradeItem"),{i:item(TRADE_ITEM[m])});
  if(STONE_ITEM[m]) return item(STONE_ITEM[m]);
  if(m==="maledawnstone") return item("dawn-stone")+" ♂";
  if(m==="femaledawnstone") return item("dawn-stone")+" ♀";
  if(m==="happiness") return C("friend");
  if(m==="happinessday") return C("friend")+C("day");
  if(m==="happinessnight") return C("friend")+C("night");
  const k={monamie:"monamie",gimmighoulcoin:"coins",ragefist:"ragefist",barbbarrge:"barb",lbattles:"crits",leveltaunt:"taunt",levelmimic:"mimic"}[m];
  return C(k||"special");
}
const wz = zs=>(T().wz||EN.wz)(zs);
function tokText(k){
  const a=k.slice(1);
  switch(k[0]){
    case "wz": return wz(a[0]);
    case "streets": return a[0]===1 ? H("streets") : fill(H("streetsSome"),{d:a[0].join(sep())});
    case "sewers": case "labs": case "oldhouse": return H(k[0]);
    case "hs": return H("hs")+H("colon")+a[0].map(([ty,ss])=>typeName(ty)+" "+ss.map(s=>"★"+s).join(" ")).join(sep());
    case "evo": return fill(H("evolve"),{p:nm(a[0]),c:cond(a[1])});
    case "sm": return fill(H("sm"),{n:a[0]});
    case "trade": return fill(H("trade"),{p:nm(a[0]),n:a[1]});
    case "x": { const v=(T().x||{})[a[0]]; return v!=null ? v : EN.x[a[0]]; }
  }
  return "";
}
function howText(e){ // base-game Pokémon's Hyperspace spawns only show in the Wild Zone view
  let toks=e.tok.slice(); if(state.dlc && e.hs && $("#dview").value==="zone") toks=toks.concat(e.hs);
  return toks.map(tokText).join(H("join"));
}
function evoText(e){
  return e.evo.map(stage=>stage.filter(([n])=>show(BYN[n])).map(([n,m])=>nm(n)+" ("+cond(m)+")").join(" / ")).filter(Boolean).join("  →  ");
}
const stopTitle = i=>{ const s=(T().stops||[])[i]; return s ? s : EN.stops[i]; };
const stopTip = i=>{ const s=(T().tips||{})[i]; return s!=null ? s : (EN.tips[i]||""); };
const dexLabel = e=>(e.dlc?"H":"#")+e.id.slice(1);

/* ---------- encode / decode ---------- */
const DEX_BYTES = Math.ceil(ORDER.length/8), MEG_BYTES = Math.ceil(STONES.length/8), LEN = 1+DEX_BYTES+MEG_BYTES;
function encode(){
  const b=new Uint8Array(LEN);
  state.dex.forEach(id=>{ const i=IDX.get(id); b[1+(i>>3)]|=1<<(i&7); });
  STONES.forEach((s,i)=>{ if(state.meg.has(s.id)) b[1+DEX_BYTES+(i>>3)]|=1<<(i&7); });
  let bin=""; b.forEach(x=>bin+=String.fromCharCode(x));
  return "PLZA1-"+btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
}
function decode(str){
  str=(str||"").trim().replace(/^#/,"");
  if(!str.startsWith("PLZA1-")) throw new Error("bad prefix");
  let s=str.slice(6).replace(/-/g,"+").replace(/_/g,"/"); while(s.length%4) s+="=";
  const bin=atob(s); if(bin.length!==LEN) throw new Error("bad length");
  const dex=new Set(), meg=new Set();
  ORDER.forEach((e,i)=>{ if(bin.charCodeAt(1+(i>>3))&(1<<(i&7))) dex.add(e.id); });
  STONES.forEach((st,i)=>{ if(bin.charCodeAt(1+DEX_BYTES+(i>>3))&(1<<(i&7))) meg.add(st.id); });
  return {dex,meg};
}

/* ---------- render: Pokédex ---------- */
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
const evoHTML = s=>s ? esc(s).replace(/\(([^)]*)\)/g,'<span style="color:var(--muted)">($1)</span>').split("  →  ").join('<span class="arr">→</span>') : "";
const headHTML = ()=>`<div class="head"><span></span><span>${esc(t("colDex"))}</span><span>${esc(t("colMon"))}</span><span>${esc(t("colHow"))}</span><span>${esc(t("colEvo"))}</span></div>`;
function rowHTML(e,withStop){
  const name=nm(e.n), how=howText(e), title=stopTitle(e.stop);
  const q=norm([N.NAMES.en[e.n],name,how,EN.stops[e.stop],title].join(" "));
  return `<div class="row" data-id="${e.id}" data-q="${esc(q)}">
    <span class="cbw"><input type="checkbox" class="cb" data-dex="${e.id}" aria-label="${esc(name)}"></span>
    <span class="dex">${dexLabel(e)}</span>
    <span class="main"><span class="nm">${esc(name)}${e.dlc?`<span class="tag T">${esc(t("tagDLC"))}</span>`:""}</span>
    <span class="how">${esc(how)}${withStop?`<span class="tag T" title="${esc(title)}">${esc(t("stopN",{n:e.stop+1}))}</span>`:""}</span>
    <span class="evo">${evoHTML(evoText(e))}</span></span>
  </div>`;
}
function card(key,num,title,tip,rows,open){
  return `<details class="stop" data-k="${key}" ${open?"open":""}>
    <summary><span class="num">${num}</span><h2>${esc(title)}</h2><span class="count"></span><span class="chev">›</span></summary>
    ${tip?`<p class="tip">${esc(tip)}</p>`:""}
    <div class="rows">${headHTML()}${rows}</div></details>`;
}
const GROUP_ORDER = [...Array(20)].map((_,i)=>"wz"+(i+1)).concat(["streets","sewers","labs","oldhouse","gift"],
  ["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy","Special"].map(x=>"hs-"+x),["evo"]);
function groupLabel(g){
  if(g.startsWith("wz")) return wz([+g.slice(2)]);
  if(g.startsWith("hs-")) return H("hs")+H("colon")+typeName(g.slice(3));
  return H("g_"+g);
}
function renderStops(){
  const view=$("#dview").value;
  const open=new Set([...document.querySelectorAll(".stop[open]")].map(d=>d.dataset.k));
  const first=!document.querySelector(".stop") || $("#stops").dataset.view!==view;
  let html="";
  if(view==="num"){
    html=`<div class="stop"><div class="rows">${headHTML()}${ORDER.filter(show).map(e=>rowHTML(e,true)).join("")}</div></div>`;
  } else if(view==="zone"){
    const groups={};
    D.entries.filter(show).forEach(e=>{
      let g=e.g.slice(); if(state.dlc && e.hs) e.hs.forEach(h=>h[1].forEach(([ty])=>g.push("hs-"+ty)));
      [...new Set(g)].forEach(k=>(groups[k]=groups[k]||[]).push(e));
    });
    let n=0;
    GROUP_ORDER.forEach(g=>{ if(!groups[g]) return; n++;
      const list=groups[g].slice().sort((a,b)=>IDX.get(a.id)-IDX.get(b.id));
      html+=card(g,n,groupLabel(g),"",list.map(e=>rowHTML(e,true)).join(""),first?n===1:open.has(g));
    });
  } else {
    visStops().forEach((s,k)=>{
      const list=D.entries.filter(e=>e.stop===s && show(e));
      html+=card("s"+s,s+1,stopTitle(s),stopTip(s),list.map(e=>rowHTML(e,false)).join(""),first?k===0:open.has("s"+s));
    });
  }
  $("#stops").innerHTML=html; $("#stops").dataset.view=view;
}

/* ---------- render: Mega Stones ---------- */
function stoneCat(loc){
  if(/^Shop Quasartico|^Quasartico/.test(loc)) return "quasartico";
  if(/Vernal Avenue/.test(loc)) return "vernal";
  if(/^(Vert|Bleu|Magenta|Rouge|Jaune) District/.test(loc)) return "d:"+loc.split(" ")[0];
  if(/^Hyperspace/.test(loc)) return "hyper";
  if(/^Side Mission/.test(loc)) return "sm";
  if(/Ranked|Battle Club/.test(loc)) return "online";
  if(/Mystery Gift/.test(loc)) return "gift";
  return "other";
}
const SCAT_ORDER = ["quasartico","vernal","d:Vert","d:Bleu","d:Magenta","d:Rouge","d:Jaune","other","sm","hyper","online","gift"];
function scatLabel(c){ return c.startsWith("d:") ? c.slice(2)+" District" : H("s_"+c); }
function stoneLoc(loc){
  let r;
  if((r=loc.match(/^Shop (.+)$/))) return fill(H("shop"),{p:r[1]==="Vernal Avenue"?r[1]:H("quasar")});
  if(loc==="Hotel Z Shop Vernal Avenue") return H("hotelz");
  if(loc==="Quasartico Inc.") return H("quasar");
  if((r=loc.match(/^Side Mission (\d+): (.+)$/))) return fill(H("smName"),{n:r[1],name:r[2]});
  if(loc==="Ranked Battle Rank-up reward") return H("s_ranked");
  if(loc==="Z-A Battle Club Ranked Reward") return H("s_club");
  if(loc==="Mystery Gift") return H("s_gift");
  if((r=loc.match(/^Hyperspace Lumiose( \(Event\))?$/))) return H("hs")+(r[1]?H("event"):"");
  if((r=loc.match(/^Hyperspace (.+)$/))) return H("hs")+H("colon")+r[1];
  return loc;
}
function renderMega(){
  const sort=$("#msort").value;
  const list=STONES.map((s,i)=>({...s,i})).filter(s=>state.dlc || !s.dlc);
  const key=s=>IDX.get(BYN[s.n].id);
  let html="";
  const cardHTML=s=>{ const holder=nm(s.n), sn=N.STN[LANG][s.i]||N.STN.en[s.i];
    return `<label class="mcard" data-m="${s.id}" data-q="${esc(norm([s.name,sn,N.NAMES.en[s.n],holder,s.loc,stoneLoc(s.loc)].join(" ")))}">
      <input type="checkbox" class="cb" data-meg="${s.id}" aria-label="${esc(sn)}">
      <span><span class="t">${esc(sn)}</span>${s.dlc?`<span class="pill opt">${esc(t("tagDLC"))}</span>`:""}
      <div class="s">${esc(holder)} · ${esc(stoneLoc(s.loc))}</div>
      <div class="w" data-warn="${BYN[s.n].id}">${esc(t("warn"))}</div></span></label>`; };
  if(sort==="loc"){
    const cats={}; list.forEach(s=>(cats[stoneCat(s.loc)]=cats[stoneCat(s.loc)]||[]).push(s));
    SCAT_ORDER.forEach(c=>{ if(!cats[c]) return;
      html+=`<div class="loc-h">${esc(scatLabel(c))}<span class="loc-left"></span></div>`;
      cats[c].sort((a,b)=>key(a)-key(b)).forEach(s=>html+=cardHTML(s));
    });
  } else list.sort((a,b)=>key(a)-key(b)||a.i-b.i).forEach(s=>html+=cardHTML(s));
  $("#mgrid").innerHTML=html;
}

/* ---------- sync UI with state ---------- */
function sync(){
  document.querySelectorAll("[data-dex]").forEach(cb=>{ const on=state.dex.has(cb.dataset.dex); cb.checked=on; cb.closest(".row").classList.toggle("caught",on); });
  document.querySelectorAll("[data-meg]").forEach(cb=>{ const on=state.meg.has(cb.dataset.meg); cb.checked=on; cb.closest(".mcard").classList.toggle("done",on); });
  document.querySelectorAll("[data-warn]").forEach(w=>w.hidden=state.dex.has(w.dataset.warn));
  document.querySelectorAll(".stop[data-k]").forEach(d=>{
    const ids=[...new Set([...d.querySelectorAll(".row")].map(r=>r.dataset.id))], got=ids.filter(id=>state.dex.has(id)).length;
    d.querySelector(".count").textContent=`${got} / ${ids.length}`; d.classList.toggle("done",got===ids.length);
  });
  document.querySelectorAll(".loc-h").forEach(h=>{
    let el=h.nextElementSibling, left=0;
    while(el&&el.matches(".mcard")){ if(!state.meg.has(el.dataset.m)) left++; el=el.nextElementSibling; }
    h.querySelector(".loc-left").textContent = left ? t("locLeft",{n:left}) : t("locDone");
  });
  const dexAll=ORDER.filter(show), got=dexAll.filter(e=>state.dex.has(e.id)).length;
  const stones=STONES.filter(s=>state.dlc||!s.dlc), sgot=stones.filter(s=>state.meg.has(s.id)).length;
  const stops=visStops(), sdone=stops.filter(s=>D.entries.filter(e=>e.stop===s&&show(e)).every(e=>state.dex.has(e.id))).length;
  $("#sDex").innerHTML=`${got} <small>/ ${dexAll.length}</small>`; $("#bDex").style.width=got/dexAll.length*100+"%";
  $("#sMeg").innerHTML=`${sgot} <small>/ ${stones.length}</small>`; $("#bMeg").style.width=sgot/stones.length*100+"%";
  $("#sStop").innerHTML=`${sdone} <small>/ ${stops.length}</small>`; $("#bStop").style.width=sdone/stops.length*100+"%";
  const b=$("#megBadge"); b.classList.toggle("won",sgot===stones.length);
  b.textContent = sgot===stones.length ? t("won") : t("badge",{n:sgot,t:stones.length});
  applyFilter();
  const code=encode(); $("#code").textContent=code;
  try{ history.replaceState(null,"","#"+code); }catch(e){}
  try{ localStorage.setItem("plza-code",code); }catch(e){}
}
function applyFilter(){
  const q=norm($("#q").value.trim()), hide=$("#hide").checked;
  document.querySelectorAll(".row").forEach(r=>{ r.hidden=(q&&!r.dataset.q.includes(q))||(hide&&state.dex.has(r.dataset.id)); });
  document.querySelectorAll(".stop").forEach(d=>{ const any=[...d.querySelectorAll(".row")].some(r=>!r.hidden); d.hidden=!any; if(q&&any&&d.tagName==="DETAILS") d.open=true; });
  document.querySelectorAll(".mcard").forEach(c=>{ c.hidden=(q&&!c.dataset.q.includes(q))||(hide&&state.meg.has(c.dataset.m)); });
  document.querySelectorAll(".loc-h").forEach(h=>{
    let el=h.nextElementSibling, any=false;
    while(el&&!el.matches(".loc-h")){ if(el.matches(".mcard")&&!el.hidden) any=true; el=el.nextElementSibling; }
    h.hidden=!any;
  });
}

/* ---------- events ---------- */
document.addEventListener("click",e=>{
  const row=e.target.closest(".row");
  if(row && !e.target.matches(".cb")){ const id=row.dataset.id; state.dex.has(id)?state.dex.delete(id):state.dex.add(id); sync(); }
});
document.addEventListener("change",e=>{
  const x=e.target;
  if(x.dataset.dex){ x.checked?state.dex.add(x.dataset.dex):state.dex.delete(x.dataset.dex); sync(); }
  if(x.dataset.meg){ x.checked?state.meg.add(x.dataset.meg):state.meg.delete(x.dataset.meg); sync(); }
});
document.querySelectorAll(".tabs button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected",x===b));
  $("#tab-dex").hidden=b.dataset.tab!=="dex"; $("#tab-meg").hidden=b.dataset.tab!=="meg";
  try{localStorage.setItem("plza-tab",b.dataset.tab)}catch(e){}
});
$("#q").oninput=applyFilter; $("#hide").onchange=applyFilter;
$("#dlc").onchange=e=>{ state.dlc=e.target.checked; try{localStorage.setItem("plza-dlc",state.dlc?"1":"0")}catch(err){} renderStops(); renderMega(); sync(); };
$("#dview").onchange=()=>{ renderStops(); sync(); };
$("#msort").onchange=()=>{ renderMega(); sync(); };
$("#copy").onclick=async()=>{
  const code=encode();
  try{ await navigator.clipboard.writeText(code); toast(t("tCopied")); }
  catch(e){ const r=document.createRange(); r.selectNodeContents($("#code")); const s=getSelection(); s.removeAllRanges(); s.addRange(r); toast(t("tSel")); }
};
$("#loadBtn").onclick=()=>{ $("#loadRow").classList.toggle("show"); $("#loadIn").focus(); };
$("#loadGo").onclick=()=>{
  try{ const d=decode($("#loadIn").value); Object.assign(state,d); renderStops(); renderMega(); sync(); $("#loadIn").value=""; $("#loadRow").classList.remove("show"); toast(t("tRest",{d:d.dex.size,m:d.meg.size})); }
  catch(e){ toast(t("tBad")); }
};
$("#loadIn").onkeydown=e=>{ if(e.key==="Enter") $("#loadGo").click(); };
$("#theme").onclick=()=>{
  const cur=document.documentElement.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");
  const nxt=cur==="dark"?"light":"dark"; document.documentElement.dataset.theme=nxt;
  try{localStorage.setItem("dex-theme",nxt)}catch(e){}
};
let tt; function toast(m){ const x=$("#toast"); x.textContent=m; x.classList.add("show"); clearTimeout(tt); tt=setTimeout(()=>x.classList.remove("show"),2200); }
const norm = s=>String(s).toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g,"").replace(/[ぁ-ゖ]/g,c=>String.fromCharCode(c.charCodeAt(0)+0x60));

/* static text: English comes from the HTML itself, saved on first run */
const LINKS={}, I18N_ATTR={i18n:"textContent","i18n-html":"innerHTML","i18n-ph":"placeholder","i18n-aria":"aria-label","i18n-title":"title"};
function applyLang(){
  document.documentElement.lang=LANG;
  Object.entries(I18N_ATTR).forEach(([a,prop])=>document.querySelectorAll(`[data-${a}]`).forEach(el=>{
    const k=el.getAttribute("data-"+a), attr=prop!=="textContent"&&prop!=="innerHTML";
    if(!(k in EN.ui)) EN.ui[k]=attr?el.getAttribute(prop):el[prop];
    const v=LANG==="en"?EN.ui[k]:t(k,LINKS);
    if(attr) el.setAttribute(prop,v); else el[prop]=v;
  }));
  document.title=t("title"); $("#lang").value=LANG;
}
/* game picker in the top bar (games listed newest release first) */
const gamesel=document.getElementById("gamesel"), gameCur=gamesel.value;
gamesel.onchange=e=>{ if(e.target.value) location.href=e.target.value; };
addEventListener("pageshow",()=>gamesel.value=gameCur);
$("#lang").innerHTML=LANGS.map(([k,n])=>`<option value="${k}">${n}</option>`).join("");
$("#lang").onchange=e=>{ LANG=e.target.value; try{localStorage.setItem("dex-lang",LANG)}catch(err){} applyLang(); renderStops(); renderMega(); sync(); };

/* every game: copy all save codes at once; Load also accepts several codes and restores each game */
const PAGE_PREFIX="PLZA1-", ALL_KEYS=[["PLZA1-","plza-code"],["PSV","psv-code"],["PLA1-","pla-code"],["PBDSP1-","pbdsp-code"],["PSWSH1-","pswsh-code"],["LGPE1-","lgpe-code"],["PUSUM1-","pusum-code"],["PSM1-","psm-code"],["PORAS1-","poras-code"],["PXY1-","pxy-code"],["PBW21-","pbw2-code"],["PBW1-","pbw-code"],["PHGSS1-","phgss-code"],["PDPPT1-","pdppt-code"],["PFRLG1-","pfrlg-code"],["PRSE1-","prse-code"],["PGSC1-","pgsc-code"],["PRBY1-","prby-code"]];
// each game's code has a fixed length, so codes are found even when pasted without separators
const CODE_RE=/(LGPE1-[A-Za-z0-9_-]{55}|PLZA1-[A-Za-z0-9_-]{79}|PSV1-[A-Za-z0-9_-]{118}|PSV2-[A-Za-z0-9_-]{139}|PLA1-[A-Za-z0-9_-]{67}|PBDSP1-[A-Za-z0-9_-]{83}|PSWSH1-[A-Za-z0-9_-]{130}|PUSUM1-[A-Za-z0-9_-]{87}|PSM1-[A-Za-z0-9_-]{70}|PORAS1-[A-Za-z0-9_-]{50}|PXY1-[A-Za-z0-9_-]{84}|PBW21-[A-Za-z0-9_-]{55}|PBW1-[A-Za-z0-9_-]{28}|PHGSS1-[A-Za-z0-9_-]{46}|PDPPT1-[A-Za-z0-9_-]{40}|PFRLG1-[A-Za-z0-9_-]{28}|PRSE1-[A-Za-z0-9_-]{38}|PGSC1-[A-Za-z0-9_-]{44}|PRBY1-[A-Za-z0-9_-]{27})/g;
function allCodes(){ return ALL_KEYS.map(([,k])=>{ try{ return localStorage.getItem(k)||""; }catch(e){ return ""; } }).filter(Boolean); }
function storeAll(text){ let n=0; (String(text).match(CODE_RE)||[]).forEach(c=>{ const m=ALL_KEYS.find(([p])=>c.startsWith(p)); if(m){ try{ localStorage.setItem(m[1],c); n++; }catch(e){} } }); return n; }
$("#copyAll").onclick=async()=>{
  const codes=allCodes();
  try{ await navigator.clipboard.writeText(codes.join("\n")); toast(t("tCopiedAll",{n:codes.length})); }
  catch(e){ $("#loadRow").classList.add("show"); $("#loadIn").value=codes.join(" "); $("#loadIn").select(); toast(t("tSel")); }
};
const loadOne=$("#loadGo").onclick;
$("#loadGo").onclick=()=>{
  const raw=$("#loadIn").value, codes=raw.match(CODE_RE)||[];
  if(codes.length>1 || (codes.length===1 && !codes[0].startsWith(PAGE_PREFIX))){
    const n=storeAll(raw); if(!n){ toast(t("tBad")); return; }
    try{ sessionStorage.setItem("dex-toast",t("tRestAll",{n})); }catch(e){}
    const mine=codes.find(c=>c.startsWith(PAGE_PREFIX)); location.hash=mine?mine:""; location.reload(); return;
  }
  loadOne();
};
try{ const m=sessionStorage.getItem("dex-toast"); if(m){ sessionStorage.removeItem("dex-toast"); setTimeout(()=>toast(m),300); } }catch(e){}

/* ---------- boot ---------- */
(function(){
  try{ const th=localStorage.getItem("dex-theme")||localStorage.getItem("lgpe-theme"); if(th) document.documentElement.dataset.theme=th; }catch(e){}
  try{ if(localStorage.getItem("plza-dlc")==="0") state.dlc=false; }catch(e){}
  $("#dlc").checked=state.dlc;
  let src=location.hash.slice(1);
  if(!src){ try{ src=localStorage.getItem("plza-code")||""; }catch(e){} }
  if(src){ try{ Object.assign(state,decode(src)); }catch(e){} }
  ["serebii","pokeapi"].forEach((k,i)=>LINKS[k]=document.querySelectorAll("footer.src a")[i].outerHTML);
  try{ const lg=localStorage.getItem("dex-lang")||localStorage.getItem("lgpe-lang"); if(I18N[lg]) LANG=lg; }catch(e){}
  applyLang(); renderStops(); renderMega(); sync();
  try{ if(localStorage.getItem("plza-tab")==="meg") document.querySelector('[data-tab="meg"]').click(); }catch(e){}
})();
