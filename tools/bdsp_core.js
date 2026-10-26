/* ---------- data helpers ---------- */
const ORDER = D.entries.slice().sort((a,b)=>a.n-b.n); // save-code bit order: National #001–#493 (never reorder)
const IDX = new Map(ORDER.map((e,i)=>[e.id,i]));
const BYN = {}; D.entries.forEach(e=>BYN[e.n]=e);
const state = {dex:new Set(), ver:0};
const $ = s=>document.querySelector(s);
const offVer = e=>!!(state.ver && e.ex && ((e.ex==="B"&&state.ver===2)||(e.ex==="S"&&state.ver===1)));

/* ---------- i18n ---------- */
let LANG = "en";
const T = ()=>I18N[LANG];
const EN = I18N.en;
function fill(str,p){ return String(str).replace(/\{([a-z0-9]+)\}/gi,(all,k)=>p && k in p ? p[k] : all); }
function t(key,p){ const v=(T().ui||{})[key]; return fill(v!=null ? v : EN.ui[key], p); }
const nm = n=>N.NAMES[LANG][n] || N.NAMES.en[n];
const item = id=>N.ITEMS[LANG][id] || N.ITEMS.en[id];
const move = id=>N.MOVES[LANG][id] || N.MOVES.en[id];
const lv = n=>fill(T().lv||EN.lv,{n});
const H = k=>{ const v=(T().how||{})[k]; return v!=null ? v : EN.how[k]; };
const C = k=>{ const v=(T().cond||{})[k]; return v!=null ? v : EN.cond[k]; };
const sep = ()=>T().sep||EN.sep;
const typeName = ty=>N.TYPES[LANG][ty] || ty;
function area(a){ // PokeAPI names (en/fr/de + a few CJK), else "Route N" by pattern, else English
  const x=(D.areas[a]||{})[LANG]; if(x) return x;
  const m=a.match(/^Route (\d+)$/), r=T().route; return m&&r ? fill(r,{n:m[1]}) : a;
}

const ITEM = {duskstone:"dusk-stone",firestone:"fire-stone",leafstone:"leaf-stone",moonstone:"moon-stone",shinystone:"shiny-stone",sunstone:"sun-stone",
  thunderstone:"thunder-stone",waterstone:"water-stone",upgrade:"upgrade",dubiousdisc:"dubious-disc",electirizer:"electirizer",magmarizer:"magmarizer",
  protector:"protector",reapercloth:"reaper-cloth",metalcoat:"metal-coat","king'srock":"kings-rock",kingsrock:"kings-rock",dragonscale:"dragon-scale",
  deepseatooth:"deep-sea-tooth",deepseascale:"deep-sea-scale",prismscale:"prism-scale"};
function cond(m){
  let r;
  if(!m) return C("special");
  if((r=m.match(/^l(\d+)$/))) return lv(r[1]);
  if((r=m.match(/^p[45]level(\d+)$/))) return lv(r[1]);
  if((r=m.match(/^l(day|night)(\d+)$/))) return lv(r[2])+C(r[1]);
  if((r=m.match(/^level([mf])(\d+)$/))) return lv(r[2])+C(r[1]==="m"?"male":"female");
  if(m==="trade") return C("trade");
  if((r=m.match(/^trade(.+)$/)) && ITEM[r[1]]) return fill(C("tradeItem"),{i:item(ITEM[r[1]])});
  if(ITEM[m]) return item(ITEM[m]);
  if(m==="maledawnstone") return item("dawn-stone")+" ♂";
  if(m==="femaledawnstone") return item("dawn-stone")+" ♀";
  if(m==="leveldayovalstone") return fill(C("holdLv"),{i:item("oval-stone")})+C("day");
  if(m==="levelnightrazorclaw") return fill(C("holdLv"),{i:item("razor-claw")})+C("night");
  if(m==="levelnightrazorfang") return fill(C("holdLv"),{i:item("razor-fang")})+C("night");
  if((r=m.match(/^level(ancientpower|doublehit|mimic|rollout)$/))) return fill(C("knows"),{m:move(r[1])});
  if(m==="levelcoronet") return C("coronet");
  if(m==="levelmossrock") return C("mossrock");
  if(m==="levelicerock") return C("icerock");
  if(m==="happiness") return C("friend");
  if(m==="happinessday") return C("friend")+C("day");
  if(m==="happinessnight") return C("friend")+C("night");
  if(m==="levelbeauty"||m==="levelpokeblock") return C("beauty");
  if(m==="levelremoraid223") return C("remoraid");
  if(m==="levelemptyspot") return C("shedinja");
  if(m==="levelpokeball20") return lv(20)+C("shedinja");
  if(m==="tyrogue20aed") return lv(20)+C("stats");
  return C("special");
}
function tokText(k,full){
  const a=k.slice(1);
  switch(k[0]){
    case "area": { const max=full?99:3, s=a[0].slice(0,max).map(area).join(sep()); return a[0].length>max ? s+fill(H("more"),{n:a[0].length-max}) : s; }
    case "gu": return fill(H("gu"),{m:H("ms"+a[0])});
    case "breed": return fill(H("breed"),{p:nm(a[0])});
    case "room": return fill(H("room"),{r:H("r_"+a[0].replace(/\W/g,""))});
    case "evo": return fill(H("evolve"),{p:nm(a[0]),c:cond(a[1])});
    case "x": { const v=(T().x||{})[a[0]]; return v!=null ? v : EN.x[a[0]]; }
  }
  return "";
}
const howText = e=>e.tok.map(k=>tokText(k,$("#dview").value==="zone")).join(H("join"));
const evoText = e=>e.evo.map(stage=>stage.map(([n,m])=>nm(n)+" ("+cond(m)+")").join(" / ")).join("  →  ");
function stopTitle(i){
  const d=EN.stopDefs[i], X=T().stopT||EN.stopT;
  return d[0]==="gym" ? fill(X.gym,{p:area(d[1]),t:typeName(d[2])}) : X[d[0]];
}
const stopTip = i=>{ const s=(T().tips||{})[i]; return s!=null ? s : (EN.tips[i]||""); };
const visStops = ()=>D.stops.map((_,i)=>i).filter(i=>D.entries.some(e=>e.stop===i));
function tagHTML(e){
  if(!e.ex) return "";
  if(offVer(e)) return `<span class="tag T">${esc(t(e.ex==="B"?"tradeB":"tradeS"))}</span>`;
  return `<span class="tag ${e.ex}">${esc(t(e.ex==="B"?"tagB":"tagS"))}</span>`;
}

/* ---------- encode / decode ---------- */
const LEN = 1+Math.ceil(ORDER.length/8);
function encode(){
  const b=new Uint8Array(LEN); b[0]=state.ver;
  state.dex.forEach(id=>{ const i=IDX.get(id); b[1+(i>>3)]|=1<<(i&7); });
  let bin=""; b.forEach(x=>bin+=String.fromCharCode(x));
  return "PBDSP1-"+btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
}
function decode(str){
  str=(str||"").trim().replace(/^#/,"");
  if(!str.startsWith("PBDSP1-")) throw new Error("bad prefix");
  let s=str.slice(7).replace(/-/g,"+").replace(/_/g,"/"); while(s.length%4) s+="=";
  const bin=atob(s); if(bin.length!==LEN) throw new Error("bad length");
  return {ver:Math.min(2,bin.charCodeAt(0)), dex:new Set(ORDER.filter((e,i)=>bin.charCodeAt(1+(i>>3))&(1<<(i&7))).map(e=>e.id))};
}

/* ---------- render ---------- */
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
const evoHTML = s=>s ? esc(s).replace(/\(([^)]*)\)/g,'<span style="color:var(--muted)">($1)</span>').split("  →  ").join('<span class="arr">→</span>') : "";
const headHTML = ()=>`<div class="head"><span></span><span>${esc(t("colDex"))}</span><span>${esc(t("colMon"))}</span><span>${esc(t("colHow"))}</span><span>${esc(t("colEvo"))}</span></div>`;
function rowHTML(e,withStop,label){
  const name=nm(e.n), how=howText(e), title=stopTitle(e.stop);
  const q=norm([N.NAMES.en[e.n],name,how,title].join(" "));
  return `<div class="row" data-id="${e.id}" data-q="${esc(q)}">
    <span class="cbw"><input type="checkbox" class="cb" data-dex="${e.id}" aria-label="${esc(name)}"></span>
    <span class="dex">${label||"#"+e.id}</span>
    <span class="main"><span class="nm">${esc(name)}${tagHTML(e)}</span>
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
  const open=new Set([...document.querySelectorAll("#stops .stop[open]")].map(d=>d.dataset.k));
  const first=!document.querySelector("#stops .stop") || $("#stops").dataset.view!==view;
  let html="";
  if(view==="num"){
    const sin=D.entries.filter(e=>e.sid).sort((a,b)=>a.sid-b.sid);
    html=card("dS",1,t("dexS"),"",sin.map(e=>rowHTML(e,true,"#"+String(e.sid).padStart(3,"0"))).join(""),first||open.has("dS"))
        +card("dN",2,t("dexN"),"",ORDER.map(e=>rowHTML(e,true)).join(""),open.has("dN"));
  } else if(view==="zone"){
    const groups={}; D.entries.forEach(e=>e.g.forEach(g=>(groups[g]=groups[g]||[]).push(e)));
    Object.keys(groups).sort((a,b)=>area(a).localeCompare(area(b),LANG,{numeric:true})).forEach((g,i)=>{
      html+=card("a:"+g,i+1,area(g),"",groups[g].slice().sort((a,b)=>a.n-b.n).map(e=>rowHTML(e,true)).join(""),first?i===0:open.has("a:"+g));
    });
  } else {
    visStops().forEach((s,k)=>{
      html+=card("s"+s,k+1,stopTitle(s),stopTip(s),D.entries.filter(e=>e.stop===s).map(e=>rowHTML(e,false)).join(""),first?k===0:open.has("s"+s));
    });
  }
  $("#stops").innerHTML=html; $("#stops").dataset.view=view;
}
function renderRooms(){ // Ramanas Park shares check-offs with the Pokédex
  let html="";
  D.rooms.forEach(r=>{
    html+=`<div class="loc-h">${esc(H("r_"+r.room.replace(/\W/g,"")))}${r.ver?` · ${esc(t(r.ver==="B"?"tagB":"tagS"))}`:""}<span class="loc-left"></span></div>`;
    r.mons.forEach(n=>{ const e=BYN[n];
      html+=`<label class="mcard" data-m="${e.id}" data-q="${esc(norm([N.NAMES.en[n],nm(n),r.room].join(" ")))}">
        <input type="checkbox" class="cb" data-dex="${e.id}"><span><span class="t">${esc(nm(n))}</span>${tagHTML(e)}
        <div class="s">#${e.id} · ${esc(fill(H("slate"),{r:H("r_"+r.room.replace(/\W/g,""))}))}</div></span></label>`; });
  });
  $("#mgrid").innerHTML=html;
}

/* ---------- sync UI with state ---------- */
function sync(){
  document.querySelectorAll("[data-dex]").forEach(cb=>{ const on=state.dex.has(cb.dataset.dex); cb.checked=on; (cb.closest(".row")||cb.closest(".mcard")).classList.toggle(cb.closest(".row")?"caught":"done",on); });
  document.querySelectorAll(".row").forEach(r=>r.classList.toggle("offver",offVer(ORDER[IDX.get(r.dataset.id)])));
  document.querySelectorAll(".stop[data-k]").forEach(d=>{
    const ids=[...new Set([...d.querySelectorAll(".row")].map(r=>r.dataset.id))], got=ids.filter(id=>state.dex.has(id)).length;
    d.querySelector(".count").textContent=`${got} / ${ids.length}`; d.classList.toggle("done",got===ids.length);
  });
  document.querySelectorAll(".loc-h").forEach(h=>{
    let el=h.nextElementSibling, left=0;
    while(el&&el.matches(".mcard")){ if(!state.dex.has(el.dataset.m)) left++; el=el.nextElementSibling; }
    h.querySelector(".loc-left").textContent = left ? t("locLeft",{n:left}) : t("locDone");
  });
  const sin=D.entries.filter(e=>e.sid), sg=sin.filter(e=>state.dex.has(e.id)).length, ng=state.dex.size;
  const rm=D.rooms.flatMap(r=>r.mons), rg=rm.filter(n=>state.dex.has(BYN[n].id)).length;
  $("#sSin").innerHTML=`${sg} <small>/ ${sin.length}</small>`; $("#bSin").style.width=sg/sin.length*100+"%";
  $("#sNat").innerHTML=`${ng} <small>/ ${ORDER.length}</small>`; $("#bNat").style.width=ng/ORDER.length*100+"%";
  $("#sRam").innerHTML=`${rg} <small>/ ${rm.length}</small>`; $("#bRam").style.width=rg/rm.length*100+"%";
  $("#ver").value=String(state.ver);
  applyFilter();
  const code=encode(); $("#code").textContent=code;
  try{ history.replaceState(null,"","#"+code); }catch(e){}
  try{ localStorage.setItem("pbdsp-code",code); }catch(e){}
}
function applyFilter(){
  const q=norm($("#q").value.trim()), hide=$("#hide").checked;
  document.querySelectorAll(".row").forEach(r=>{ r.hidden=(q&&!r.dataset.q.includes(q))||(hide&&state.dex.has(r.dataset.id)); });
  document.querySelectorAll("#stops .stop").forEach(d=>{ const any=[...d.querySelectorAll(".row")].some(r=>!r.hidden); d.hidden=!any; if(q&&any) d.open=true; });
  document.querySelectorAll(".mcard").forEach(c=>{ c.hidden=(q&&!c.dataset.q.includes(q))||(hide&&state.dex.has(c.dataset.m)); });
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
});
document.querySelectorAll(".tabs button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected",x===b));
  $("#tab-dex").hidden=b.dataset.tab!=="dex"; $("#tab-ram").hidden=b.dataset.tab!=="ram";
  try{localStorage.setItem("pbdsp-tab",b.dataset.tab)}catch(e){}
});
$("#q").oninput=applyFilter; $("#hide").onchange=applyFilter;
$("#ver").onchange=e=>{ state.ver=+e.target.value; renderStops(); renderRooms(); sync(); };
$("#dview").onchange=()=>{ renderStops(); sync(); };
$("#copy").onclick=async()=>{
  const code=encode();
  try{ await navigator.clipboard.writeText(code); toast(t("tCopied")); }
  catch(e){ const r=document.createRange(); r.selectNodeContents($("#code")); const s=getSelection(); s.removeAllRanges(); s.addRange(r); toast(t("tSel")); }
};
$("#loadBtn").onclick=()=>{ $("#loadRow").classList.toggle("show"); $("#loadIn").focus(); };
$("#loadGo").onclick=()=>{
  try{ const d=decode($("#loadIn").value); Object.assign(state,d); renderStops(); renderRooms(); sync(); $("#loadIn").value=""; $("#loadRow").classList.remove("show"); toast(t("tRest",{d:d.dex.size})); }
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
$("#lang").onchange=e=>{ LANG=e.target.value; try{localStorage.setItem("dex-lang",LANG)}catch(err){} applyLang(); renderStops(); renderRooms(); sync(); };

/* every game: copy all save codes at once; Load also accepts several codes and restores each game */
const PAGE_PREFIX="PBDSP1-", ALL_KEYS=[["PLZA1-","plza-code"],["PSV","psv-code"],["PLA1-","pla-code"],["PBDSP1-","pbdsp-code"],["PSWSH1-","pswsh-code"],["LGPE1-","lgpe-code"],["PUSUM1-","pusum-code"],["PSM1-","psm-code"],["PORAS1-","poras-code"],["PXY1-","pxy-code"],["PBW21-","pbw2-code"],["PBW1-","pbw-code"],["PHGSS1-","phgss-code"],["PDPPT1-","pdppt-code"],["PFRLG1-","pfrlg-code"],["PRSE1-","prse-code"],["PGSC1-","pgsc-code"],["PRBY1-","prby-code"]];
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
  let src=location.hash.slice(1);
  if(!src){ try{ src=localStorage.getItem("pbdsp-code")||""; }catch(e){} }
  if(src){ try{ Object.assign(state,decode(src)); }catch(e){} }
  ["serebii","pokeapi"].forEach((k,i)=>LINKS[k]=document.querySelectorAll("footer.src a")[i].outerHTML);
  try{ const lg=localStorage.getItem("dex-lang")||localStorage.getItem("lgpe-lang"); if(I18N[lg]) LANG=lg; }catch(e){}
  applyLang(); renderStops(); renderRooms(); sync();
  try{ if(localStorage.getItem("pbdsp-tab")==="ram") document.querySelector('[data-tab="ram"]').click(); }catch(e){}
})();
