/* ---------- data helpers ---------- */
const DEXK = {P:0,K:1,B:2};
const ORDER = D.entries.slice().sort((a,b)=>DEXK[a.id[0]]-DEXK[b.id[0]]||a.id.localeCompare(b.id)); // save-code bit order (never reorder)
const IDX = new Map(ORDER.map((e,i)=>[e.id,i]));
const BYN = {}; D.entries.forEach(e=>BYN[e.n]=e);
const STAKES = D.stakes; // save-code bit order: purple 1–8, yellow, blue, green
const DLC_STOP = 21, AREA_ZERO_STOP = 20;
const RAIDS = D.raids; // Mightiest Mark raids, oldest first (save-code bit order; new events are appended)
const state = {dex:new Set(), stk:new Set(), rd:new Set(), ver:0, dlc:true};
const $ = s=>document.querySelector(s);
const show = e=>state.dlc || !e.dlc;
const visStops = ()=>D.stops.map((_,i)=>i).filter(i=>(state.dlc || i<DLC_STOP) && D.entries.some(e=>e.stop===i && show(e))); // skip stops with no new Pokémon
const offVer = e=>!!(state.ver && e.ex && ((e.ex==="S"&&state.ver===2)||(e.ex==="V"&&state.ver===1)));

/* ---------- i18n ---------- */
let LANG = "en";
const T = ()=>I18N[LANG];
const EN = I18N.en;
function fill(str,p){ return String(str).replace(/\{([a-z0-9]+)\}/gi,(all,k)=>p && k in p ? p[k] : all); }
function t(key,p){ const v=(T().ui||{})[key]; return fill(v!=null ? v : EN.ui[key], p); }
const nm = n=>N.NAMES[LANG][n] || N.NAMES.en[n];
const item = id=>N.ITEMS[LANG][id] || N.ITEMS.en[id];
const typeName = ty=>N.TYPES[LANG][ty] || ty;
const lv = n=>fill(T().lv||EN.lv,{n});
const H = k=>{ const v=(T().how||{})[k]; return v!=null ? v : EN.how[k]; };
const C = k=>{ const v=(T().cond||{})[k]; return v!=null ? v : EN.cond[k]; };
const sep = ()=>T().sep||EN.sep;
const area = a=>(D.areas[a]||{})[LANG] || a;

const STONE_ITEM = {duskstone:"dusk-stone",firestone:"fire-stone",icestone:"ice-stone",leafstone:"leaf-stone",moonstone:"moon-stone",
  shinystone:"shiny-stone",sunstone:"sun-stone",thunderstone:"thunder-stone",waterstone:"water-stone",blackaugurite:"black-augurite",
  galaricacuff:"galarica-cuff",galaricawreath:"galarica-wreath",auspiciousarmor:"auspicious-armor",maliciousarmor:"malicious-armor",
  tartapple:"tart-apple",sweetapple:"sweet-apple",syrupyapple:"syrupy-apple",crackedpot:"cracked-pot",chippedpot:"chipped-pot",
  unremarkableteacup:"unremarkable-teacup",masterpieceteacup:"masterpiece-teacup",metalalloy:"metal-alloy",peatblock:"peat-block",
  ovalstone:"oval-stone",razorclaw:"razor-claw",razorfang:"razor-fang",linkingcord:"linking-cord",upgrade:"upgrade",dubiousdisc:"dubious-disc",
  electirizer:"electirizer",magmarizer:"magmarizer",protector:"protector",reapercloth:"reaper-cloth",kingsrock:"kings-rock",metalcoat:"metal-coat",
  dragonscale:"dragon-scale",prismscale:"prism-scale",sachet:"sachet",whippeddream:"whipped-dream"};
function cond(m){
  let r;
  if(!m) return C("special");
  if((r=m.match(/^l(\d+)$/))) return lv(r[1]);
  if((r=m.match(/^l(day|night)(\d+)$/))) return lv(r[2])+C(r[1]);
  if((r=m.match(/^l(\d+)(day|night)$/))) return lv(r[1])+C(r[2]);
  if(m==="l32dark") return lv(32)+C("dark");
  if(m==="l50rain") return lv(50)+C("rain");
  if(m==="nature30") return lv(30)+C("nature");
  if(m==="trade") return C("trade");
  if((r=m.match(/^trade(.+)$/)) && STONE_ITEM[r[1].replace("'","")]) return fill(C("tradeItem"),{i:item(STONE_ITEM[r[1].replace("'","")])});
  if(STONE_ITEM[m]) return item(STONE_ITEM[m]);
  if((r=m.match(/^level(day|night)(.+)$/)) && STONE_ITEM[r[2]]) return fill(C("holdLv"),{i:item(STONE_ITEM[r[2]])})+C(r[1]);
  if((r=m.match(/^level(ancientpower|doublehit|hyperdrill|stomp|twinbeam|taunt|mimic)$/))) return fill(C("knows"),{m:N.MOVES[LANG][r[1]]||N.MOVES.en[r[1]]});
  if((r=m.match(/^levelf(\d+)$/))) return lv(r[1])+C("female");
  if(m==="tandemaus25") return lv(25);
  if(m==="tyrogue20aed") return lv(20)+C("stats");
  if(m==="walk1000") return C("walk");
  if(m==="sweetspin") return C("spin");
  if(m==="maledawnstone") return item("dawn-stone")+" ♂";
  if(m==="femaledawnstone") return item("dawn-stone")+" ♀";
  if(m==="happiness") return C("friend");
  if(m==="happinessday") return C("friend")+C("day");
  if(m==="happinessnight") return C("friend")+C("night");
  const k={monamie:"monamie",gimmighoulcoin:"coins",ragefist:"ragefist",barbbarrge:"barb",lbattles:"crits"}[m];
  return C(k||"special");
}
function areaList(as){ const max=3, a=as.slice(0,max).map(area).join(sep()); return as.length>max ? a+fill(H("more"),{n:as.length-max}) : a; }
function tokText(k){
  const a=k.slice(1);
  switch(k[0]){
    case "area": return areaList(a[0]);
    case "raid": return H("raid")+" "+a[0].map(s=>"★"+s).join(" ");
    case "tm": return H("tm")+H("colon")+areaList(a[0]);
    case "id": return H("id")+H("colon")+areaList(a[0]);
    case "evo": return fill(H("evolve"),{p:nm(a[0]),c:cond(a[1])});
    case "trade": return fill(H("trade"),{p:nm(a[0]),place:area(a[1])});
    case "x": { const v=(T().x||{})[a[0]]; return v!=null ? v : EN.x[a[0]]; }
  }
  return "";
}
function howText(e){ let toks=e.tok.slice(); if(state.dlc && e.dlcTok && $("#dview").value==="zone") toks=toks.concat(e.dlcTok); return toks.map(tokText).join(H("join")); }
function evoText(e){
  return e.evo.map(stage=>stage.filter(([n])=>BYN[n]&&show(BYN[n])).map(([n,m])=>nm(n)+" ("+cond(m)+")").join(" / ")).filter(Boolean).join("  →  ");
}
function stopTitle(i){
  const s=EN.stopDefs[i], X=T().stopT||EN.stopT;
  if(s[0]==="gym") return fill(X.gym,{p:area(s[1]),t:typeName(s[2])});
  if(s[0]==="titan") return fill(X.titan,{m:s[1].map(nm).join(" / "),p:area(s[2])});
  if(s[0]==="squad") return fill(X.squad,{p:area(s[1]),t:typeName(s[2])});
  return X[s[0]];
}
const stopTip = i=>{ const s=(T().tips||{})[i]; return s!=null ? s : (EN.tips[i]||""); };
const dexLabel = e=>e.id[0]==="P" ? "#"+e.id.slice(1) : e.id;
function tagHTML(e){
  if(!e.ex) return "";
  if(offVer(e)) return `<span class="tag T">${esc(t(e.ex==="S"?"tradeS":"tradeV"))}</span>`;
  return `<span class="tag ${e.ex}">${esc(t(e.ex==="S"?"tagS":"tagV"))}</span>`;
}

/* ---------- encode / decode ----------
   PSV2- = the PSV1- layout plus 16 bytes for Mightiest Mark raids (room for 128, so new events don't change the format).
   PSV1- codes still load. */
const DEX_BYTES = Math.ceil(ORDER.length/8), STK_BYTES = Math.ceil(STAKES.length/8), LEN1 = 1+DEX_BYTES+STK_BYTES, RAID_BYTES = 16, LEN = LEN1+RAID_BYTES;
function encode(){
  const b=new Uint8Array(LEN); b[0]=state.ver;
  state.dex.forEach(id=>{ const i=IDX.get(id); b[1+(i>>3)]|=1<<(i&7); });
  STAKES.forEach((s,i)=>{ if(state.stk.has(s.id)) b[1+DEX_BYTES+(i>>3)]|=1<<(i&7); });
  RAIDS.forEach((r,i)=>{ if(state.rd.has(r.id)) b[LEN1+(i>>3)]|=1<<(i&7); });
  let bin=""; b.forEach(x=>bin+=String.fromCharCode(x));
  return "PSV2-"+btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
}
function decode(str){
  str=(str||"").trim().replace(/^#/,"");
  const v=str.startsWith("PSV2-")?2:str.startsWith("PSV1-")?1:0;
  if(!v) throw new Error("bad prefix");
  let s=str.slice(5).replace(/-/g,"+").replace(/_/g,"/"); while(s.length%4) s+="=";
  const bin=atob(s); if(bin.length!==(v===2?LEN:LEN1)) throw new Error("bad length");
  const dex=new Set(), stk=new Set(), rd=new Set();
  ORDER.forEach((e,i)=>{ if(bin.charCodeAt(1+(i>>3))&(1<<(i&7))) dex.add(e.id); });
  STAKES.forEach((st,i)=>{ if(bin.charCodeAt(1+DEX_BYTES+(i>>3))&(1<<(i&7))) stk.add(st.id); });
  if(v===2) RAIDS.forEach((r,i)=>{ if(bin.charCodeAt(LEN1+(i>>3))&(1<<(i&7))) rd.add(r.id); });
  return {ver:Math.min(2,bin.charCodeAt(0)),dex,stk,rd};
}

/* ---------- render: Pokédex ---------- */
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
const evoHTML = s=>s ? esc(s).replace(/\(([^)]*)\)/g,'<span style="color:var(--muted)">($1)</span>').split("  →  ").join('<span class="arr">→</span>') : "";
const headHTML = ()=>`<div class="head"><span></span><span>${esc(t("colDex"))}</span><span>${esc(t("colMon"))}</span><span>${esc(t("colHow"))}</span><span>${esc(t("colEvo"))}</span></div>`;
function rowHTML(e,withStop,label){
  const name=nm(e.n), how=howText(e), title=stopTitle(e.stop);
  const q=norm([N.NAMES.en[e.n],name,how,title].join(" "));
  return `<div class="row" data-id="${e.id}" data-q="${esc(q)}">
    <span class="cbw"><input type="checkbox" class="cb" data-dex="${e.id}" aria-label="${esc(name)}"></span>
    <span class="dex">${label||dexLabel(e)}</span>
    <span class="main"><span class="nm">${esc(name)}${tagHTML(e)}${e.dlc?`<span class="tag T">${esc(t("tagDLC"))}</span>`:""}</span>
    <span class="how">${esc(how)}${withStop?`<span class="tag T" title="${esc(title)}">${esc(t("stopN",{n:visStops().indexOf(e.stop)+1}))}</span>`:""}</span>
    <span class="evo">${evoHTML(evoText(e))}</span></span>
  </div>`;
}
function card(key,num,title,tip,rows,open){
  return `<details class="stop" data-k="${key}" ${open?"open":""}>
    <summary><span class="num">${num}</span><h2>${esc(title)}</h2><span class="count"></span><span class="chev">›</span></summary>
    ${tip?`<p class="tip">${esc(tip)}</p>`:""}
    <div class="rows">${headHTML()}${rows}</div></details>`;
}
function renderStops(){
  const view=$("#dview").value;
  const open=new Set([...document.querySelectorAll(".stop[open]")].map(d=>d.dataset.k));
  const first=!document.querySelector(".stop") || $("#stops").dataset.view!==view;
  let html="";
  if(view==="num"){
    [["P",t("dexP")],["K",t("dexK")],["B",t("dexB")]].forEach(([k,label],i)=>{
      if(k!=="P" && !state.dlc) return;
      const list=D.entries.filter(e=>e.dex[k]).sort((a,b)=>a.dex[k]-b.dex[k]);
      html+=card("d"+k,i+1,label,"",list.map(e=>rowHTML(e,true,(k==="P"?"#":k)+String(e.dex[k]).padStart(3,"0"))).join(""),first?i===0:open.has("d"+k));
    });
  } else if(view==="zone"){
    const groups={};
    D.entries.filter(show).forEach(e=>e.g.forEach(g=>(groups[g]=groups[g]||[]).push(e)));
    const names=Object.keys(groups).sort((a,b)=>area(a).localeCompare(area(b),LANG));
    names.forEach((g,i)=>{
      const list=groups[g].slice().sort((a,b)=>IDX.get(a.id)-IDX.get(b.id));
      html+=card("a:"+g,i+1,area(g),"",list.map(e=>rowHTML(e,true)).join(""),first?i===0:open.has("a:"+g));
    });
  } else {
    visStops().forEach((s,k)=>{
      const list=D.entries.filter(e=>e.stop===s && show(e));
      html+=card("s"+s,k+1,stopTitle(s),stopTip(s),list.map(e=>rowHTML(e,false)).join(""),first?k===0:open.has("s"+s));
    });
  }
  $("#stops").innerHTML=html; $("#stops").dataset.view=view;
}

/* ---------- render: Ominous Stakes ---------- */
const SHRINE = {Purple:"Grasswither Shrine",Yellow:"Icerend Shrine",Blue:"Firescourge Shrine",Green:"Groundblight Shrine"};
function renderStakes(){
  let html="", last=null;
  STAKES.forEach(s=>{
    if(s.color!==last){ last=s.color; html+=`<div class="loc-h">${esc(fill(H("shrineH"),{s:area(SHRINE[s.color]),p:nm(s.n),c:H("c"+s.color)}))}<span class="loc-left"></span></div>`; }
    html+=`<label class="mcard" data-m="${s.id}" data-q="${esc(norm([s.color,H("c"+s.color),s.area,area(s.area),N.NAMES.en[s.n],nm(s.n)].join(" ")))}">
      <input type="checkbox" class="cb" data-stk="${s.id}">
      <span><span class="t">${esc(fill(H("stakeN"),{c:H("c"+s.color),n:s.no}))}</span>
      <div class="s">${esc(area(s.area))}</div></span></label>`;
  });
  $("#mgrid").innerHTML=html;
}

/* ---------- render: Mightiest Mark raids ---------- */
function renderRaids(){ // newest first, grouped by year
  const fmt=d=>{ try{ return new Intl.DateTimeFormat(LANG,{year:"numeric",month:"long"}).format(new Date(d+"-15")); }catch(e){ return d; } };
  let html="", year=null;
  RAIDS.slice().reverse().forEach(r=>{
    const y=r.date.slice(0,4);
    if(y!==year){ year=y; html+=`<div class="loc-h">${y}<span class="loc-left"></span></div>`; }
    const name=r.form ? fill(H("hisuian"),{p:nm(r.n)}) : nm(r.n), off=state.ver&&r.ex&&((r.ex==="S"&&state.ver===2)||(r.ex==="V"&&state.ver===1));
    const tag=r.ex ? `<span class="tag ${off?"T":r.ex}">${esc(t(r.ex==="S"?"tagS":"tagV"))}</span>` : "";
    html+=`<label class="mcard" data-m="${r.id}" data-q="${esc(norm([N.NAMES.en[r.n],nm(r.n),name,r.tera,typeName(r.tera)].join(" ")))}">
      <input type="checkbox" class="cb" data-rd="${r.id}">
      <span><span class="t">${esc(name)}</span>${tag}
      <div class="s">${esc(fill(H("teraT"),{t:typeName(r.tera)}))} · ${esc(fmt(r.date))}</div></span></label>`;
  });
  $("#rgrid").innerHTML=html;
}

/* ---------- sync UI with state ---------- */
function sync(){
  document.querySelectorAll("[data-dex]").forEach(cb=>{ const on=state.dex.has(cb.dataset.dex); cb.checked=on; cb.closest(".row").classList.toggle("caught",on); });
  document.querySelectorAll("[data-stk]").forEach(cb=>{ const on=state.stk.has(cb.dataset.stk); cb.checked=on; cb.closest(".mcard").classList.toggle("done",on); });
  document.querySelectorAll("[data-rd]").forEach(cb=>{ const on=state.rd.has(cb.dataset.rd); cb.checked=on; cb.closest(".mcard").classList.toggle("done",on); });
  document.querySelectorAll(".row").forEach(r=>r.classList.toggle("offver",offVer(ORDER[IDX.get(r.dataset.id)])));
  document.querySelectorAll(".stop[data-k]").forEach(d=>{
    const ids=[...new Set([...d.querySelectorAll(".row")].map(r=>r.dataset.id))], got=ids.filter(id=>state.dex.has(id)).length;
    d.querySelector(".count").textContent=`${got} / ${ids.length}`; d.classList.toggle("done",got===ids.length);
  });
  document.querySelectorAll(".loc-h").forEach(h=>{
    let el=h.nextElementSibling, left=0;
    while(el&&el.matches(".mcard")){ if(!el.querySelector(".cb").checked) left++; el=el.nextElementSibling; }
    h.querySelector(".loc-left").textContent = left ? t("locLeft",{n:left}) : t("locDone");
  });
  const dexAll=ORDER.filter(show), got=dexAll.filter(e=>state.dex.has(e.id)).length;
  const sgot=STAKES.filter(s=>state.stk.has(s.id)).length;
  const stops=visStops(), sdone=stops.filter(s=>D.entries.filter(e=>e.stop===s&&show(e)).every(e=>state.dex.has(e.id))).length;
  $("#sDex").innerHTML=`${got} <small>/ ${dexAll.length}</small>`; $("#bDex").style.width=got/dexAll.length*100+"%";
  $("#sStk").innerHTML=`${sgot} <small>/ ${STAKES.length}</small>`; $("#bStk").style.width=sgot/STAKES.length*100+"%";
  $("#sStop").innerHTML=`${sdone} <small>/ ${stops.length}</small>`; $("#bStop").style.width=sdone/stops.length*100+"%";
  const b=$("#stkBadge"); b.classList.toggle("won",sgot===STAKES.length);
  b.textContent = sgot===STAKES.length ? t("won") : t("badge",{n:sgot,t:STAKES.length});
  const rgot=state.rd.size, rb=$("#rdBadge"); rb.classList.toggle("won",rgot===RAIDS.length);
  rb.textContent = rgot===RAIDS.length ? t("rdWon") : t("rdBadge",{n:rgot,t:RAIDS.length});
  $("#ver").value=String(state.ver);
  applyFilter();
  const code=encode(); $("#code").textContent=code;
  try{ history.replaceState(null,"","#"+code); }catch(e){}
  try{ localStorage.setItem("psv-code",code); }catch(e){}
}
function applyFilter(){
  const q=norm($("#q").value.trim()), hide=$("#hide").checked;
  document.querySelectorAll(".row").forEach(r=>{ r.hidden=(q&&!r.dataset.q.includes(q))||(hide&&state.dex.has(r.dataset.id)); });
  document.querySelectorAll(".stop").forEach(d=>{ const any=[...d.querySelectorAll(".row")].some(r=>!r.hidden); d.hidden=!any; if(q&&any&&d.tagName==="DETAILS") d.open=true; });
  document.querySelectorAll(".mcard").forEach(c=>{ c.hidden=(q&&!c.dataset.q.includes(q))||(hide&&c.querySelector(".cb").checked); });
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
  if(x.dataset.stk){ x.checked?state.stk.add(x.dataset.stk):state.stk.delete(x.dataset.stk); sync(); }
  if(x.dataset.rd){ x.checked?state.rd.add(x.dataset.rd):state.rd.delete(x.dataset.rd); sync(); }
});
document.querySelectorAll(".tabs button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected",x===b));
  ["dex","stk","rd"].forEach(k=>$("#tab-"+k).hidden=b.dataset.tab!==k);
  try{localStorage.setItem("psv-tab",b.dataset.tab)}catch(e){}
});
$("#q").oninput=applyFilter; $("#hide").onchange=applyFilter;
$("#ver").onchange=e=>{ state.ver=+e.target.value; renderStops(); sync(); };
$("#dlc").onchange=e=>{ state.dlc=e.target.checked; try{localStorage.setItem("psv-dlc",state.dlc?"1":"0")}catch(err){} renderStops(); sync(); };
$("#dview").onchange=()=>{ renderStops(); sync(); };
$("#copy").onclick=async()=>{
  const code=encode();
  try{ await navigator.clipboard.writeText(code); toast(t("tCopied")); }
  catch(e){ const r=document.createRange(); r.selectNodeContents($("#code")); const s=getSelection(); s.removeAllRanges(); s.addRange(r); toast(t("tSel")); }
};
$("#loadBtn").onclick=()=>{ $("#loadRow").classList.toggle("show"); $("#loadIn").focus(); };
$("#loadGo").onclick=()=>{
  try{ const d=decode($("#loadIn").value); Object.assign(state,d); renderStops(); renderStakes(); renderRaids(); sync(); $("#loadIn").value=""; $("#loadRow").classList.remove("show"); toast(t("tRest",{d:d.dex.size,m:d.stk.size})+(d.rd.size?" · "+t("rdBadge",{n:d.rd.size,t:RAIDS.length}):"")); }
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
$("#lang").onchange=e=>{ LANG=e.target.value; try{localStorage.setItem("dex-lang",LANG)}catch(err){} applyLang(); renderStops(); renderStakes(); renderRaids(); sync(); };

/* every game: copy all save codes at once; Load also accepts several codes and restores each game */
const PAGE_PREFIX="PSV", ALL_KEYS=[["PLZA1-","plza-code"],["PSV","psv-code"],["PLA1-","pla-code"],["PBDSP1-","pbdsp-code"],["PSWSH1-","pswsh-code"],["LGPE1-","lgpe-code"],["PUSUM1-","pusum-code"],["PSM1-","psm-code"],["PORAS1-","poras-code"],["PXY1-","pxy-code"],["PBW21-","pbw2-code"],["PBW1-","pbw-code"],["PHGSS1-","phgss-code"],["PDPPT1-","pdppt-code"],["PFRLG1-","pfrlg-code"],["PRSE1-","prse-code"],["PGSC1-","pgsc-code"],["PRBY1-","prby-code"]];
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
  try{ if(localStorage.getItem("psv-dlc")==="0") state.dlc=false; }catch(e){}
  $("#dlc").checked=state.dlc;
  let src=location.hash.slice(1);
  if(!src){ try{ src=localStorage.getItem("psv-code")||""; }catch(e){} }
  if(src){ try{ Object.assign(state,decode(src)); }catch(e){} }
  ["serebii","pokestop","imore","pokeapi"].forEach((k,i)=>LINKS[k]=document.querySelectorAll("footer.src a")[i].outerHTML);
  try{ const lg=localStorage.getItem("dex-lang")||localStorage.getItem("lgpe-lang"); if(I18N[lg]) LANG=lg; }catch(e){}
  applyLang(); renderStops(); renderStakes(); renderRaids(); sync();
  try{ const tb=localStorage.getItem("psv-tab"); if(tb&&tb!=="dex") document.querySelector(`[data-tab="${tb}"]`).click(); }catch(e){}
})();
