/* ---------- data helpers ---------- */
const ORDER = D.entries.slice().sort((a,b)=>a.dex-b.dex); // save-code bit order: Alola Pokédex number (never reorder)
const IDX = new Map(ORDER.map((e,i)=>[e.id,i]));
const STK = D.cells;                                     // bit order: Z001–Z100 (5 Cores, then 95 Cells)
const BYN = {}; D.entries.forEach(e=>BYN[e.n]=e);
const state = {dex:new Set(), stk:new Set(), ver:0};
const $ = s=>document.querySelector(s);
const offVer = e=>!!(state.ver && e.ex && ((e.ex==="S"&&state.ver===2)||(e.ex==="M"&&state.ver===1)));

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
const area = a=>{ const d=D.areas[a]||{}; return d[LANG]||d.en||a; }; // Serebii area slug -> PokeAPI name in every language

const ITEM = {duskstone:"dusk-stone",firestone:"fire-stone",icestone:"ice-stone",leafstone:"leaf-stone",moonstone:"moon-stone",shinystone:"shiny-stone",
  sunstone:"sun-stone",thunderstone:"thunder-stone",waterstone:"water-stone",upgrade:"upgrade",dubiousdisc:"dubious-disc",electirizer:"electirizer",
  magmarizer:"magmarizer",protector:"protector",reapercloth:"reaper-cloth",metalcoat:"metal-coat","king'srock":"kings-rock",dragonscale:"dragon-scale",
  prismscale:"prism-scale",deepseatooth:"deep-sea-tooth",deepseascale:"deep-sea-scale",sachet:"sachet",whippeddream:"whipped-dream"};
function cond(m){
  let r;
  if(!m) return C("special");
  if((r=m.match(/^l(\d+)$/))) return lv(r[1]);
  if((r=m.match(/^l(day|night)(\d+)$/))) return lv(r[2])+C(r[1]);
  if((r=m.match(/^l(\d+)(night|day|dark|rain|dusk)$/))) return lv(r[1])+C(r[2]);
  if((r=m.match(/^levelf(\d+)$/))) return lv(r[1])+C("female");
  if((r=m.match(/^levelm(\d+)$/))) return lv(r[1])+C("male");
  if(m==="trade") return C("trade");
  if(m==="trade588"||m==="trade616") return fill(C("tradeFor"),{p:nm(m==="trade588"?616:588)});
  if((r=m.match(/^trade(.+)$/)) && ITEM[r[1]]) return fill(C("tradeItem"),{i:item(ITEM[r[1]])});
  if(ITEM[m]) return item(ITEM[m]);
  if(m==="maledawnstone") return item("dawn-stone")+" ♂";
  if(m==="femaledawnstone") return item("dawn-stone")+" ♀";
  if(m==="leveldayovalstone") return fill(C("holdLv"),{i:item("oval-stone")})+C("day");
  if(m==="levelnightrazorclaw") return fill(C("holdLv"),{i:item("razor-claw")})+C("night");
  if(m==="levelnightrazorfang") return fill(C("holdLv"),{i:item("razor-fang")})+C("night");
  if((r=m.match(/^level(ancientpower|doublehit|mimic|rollout|stomp|taunt)$/))) return fill(C("knows"),{m:move(r[1])});
  if(m==="happiness") return C("friend");
  if(m==="happinessday") return C("friend")+C("day");
  if(m==="happinessnight") return C("friend")+C("night");
  if(m==="fairyfriend") return C("fairy");
  if(m==="levelremoraid223") return C("remoraid");
  if(m==="levelpokeball20") return lv(20)+C("shedinja");
  if(m==="tyrogue20aed") return lv(20)+C("stats");
  if(m==="l303ds") return lv(30)+C("upside");
  if(m==="levelcoronet") return fill(C("magnetic"),{a:area("blushmountain"),b:area("vastponicanyon")});
  if(m==="snow") return fill(C("lanakila"),{a:area("mountlanakila")});
  if(m==="mossrock") return fill(C("mossrock"),{a:area("lushjungle")});
  if(m==="icerock") return fill(C("icerock"),{a:area("mountlanakila")});
  if(m==="levelbeauty"||m==="levelpokeblock") return C("beauty");
  return C("special");
}
function list(a,full){ const max=full?99:3, s=a.slice(0,max).map(area).join(sep()); return a.length>max ? s+fill(H("more"),{n:a.length-max}) : s; }
function tokText(k,full){
  const a=k.slice(1);
  switch(k[0]){
    case "area": return list(a[0],full);
    case "sos": return H("sos")+H("colon")+list(a[0],full);
    case "scan": return H("scan")+H("colon")+list(a[0],full);
    case "evo": return fill(H("evolve"),{p:nm(a[0]),c:cond(a[1])});
    case "x": { const v=(T().x||{})[a[0]]; return v!=null ? v : EN.x[a[0]]; }
  }
  return "";
}
const howText = e=>e.tok.map(k=>tokText(k,$("#dview").value==="zone")).join(H("join"));
const evoText = e=>e.evo.map(stage=>stage.map(([n,m])=>nm(n)+" ("+cond(m)+")").join(" / ")).join("  →  ");
function stopTitle(i){
  const d=EN.stopDefs[i], X=T().stopT||EN.stopT;
  return d[0]==="trial" ? fill(X.trial,{p:area(d[1]),t:typeName(d[2])}) : d[0]==="grand" ? fill(X.grand,{p:t("cap_"+d[1])}) : fill(X[d[0]],{a:area("ikitown"),b:area("verdantcavern")});
}
const stopTip = i=>{ const s=(T().tips||{})[i]; return fill(s!=null ? s : (EN.tips[i]||""),{a:area("mountlanakila"),b:area("pokemonleague")}); };
const visStops = ()=>D.stops.map((_,i)=>i).filter(i=>D.entries.some(e=>e.stop===i)); // skip stops with no new Pokémon
function tagHTML(e){
  if(!e.ex) return "";
  return offVer(e) ? `<span class="tag T">${esc(t(e.ex==="S"?"tradeS":"tradeM"))}</span>` : `<span class="tag ${e.ex}">${esc(t(e.ex==="S"?"tagS":"tagM"))}</span>`;
}

/* ---------- encode / decode ---------- */
const NB = Math.ceil(ORDER.length/8), SB = Math.ceil(STK.length/8);
const LEN = 1+NB+SB;
function encode(){
  const b=new Uint8Array(LEN); b[0]=state.ver;
  state.dex.forEach(id=>{ const i=IDX.get(id); b[1+(i>>3)]|=1<<(i&7); });
  STK.forEach((s,i)=>{ if(state.stk.has(s.id)) b[1+NB+(i>>3)]|=1<<(i&7); });
  let bin=""; b.forEach(x=>bin+=String.fromCharCode(x));
  return "PSM1-"+btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
}
function decode(str){
  str=(str||"").trim().replace(/^#/,"");
  if(!str.startsWith("PSM1-")) throw new Error("bad prefix");
  let s=str.slice(5).replace(/-/g,"+").replace(/_/g,"/"); while(s.length%4) s+="=";
  const bin=atob(s); if(bin.length!==LEN) throw new Error("bad length");
  const bit=(o,i)=>bin.charCodeAt(o+(i>>3))&(1<<(i&7));
  return {ver:Math.min(2,bin.charCodeAt(0)), dex:new Set(ORDER.filter((e,i)=>bit(1,i)).map(e=>e.id)), stk:new Set(STK.filter((s,i)=>bit(1+NB,i)).map(s=>s.id))};
}

/* ---------- render ---------- */
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
const evoHTML = s=>s ? esc(s).replace(/\(([^)]*)\)/g,'<span style="color:var(--muted)">($1)</span>').split("  →  ").join('<span class="arr">→</span>') : "";
const headHTML = ()=>`<div class="head"><span></span><span>${esc(t("colDex"))}</span><span>${esc(t("colMon"))}</span><span>${esc(t("colHow"))}</span><span>${esc(t("colEvo"))}</span></div>`;
function rowHTML(e,withStop){
  const name=nm(e.n), how=howText(e), title=stopTitle(e.stop);
  const q=norm([N.NAMES.en[e.n],name,how,title].join(" "));
  return `<div class="row" data-id="${e.id}" data-q="${esc(q)}">
    <span class="cbw"><input type="checkbox" class="cb" data-dex="${e.id}" aria-label="${esc(name)}"></span>
    <span class="dex">#${e.id}</span>
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
    html=card("dA",1,t("dexA"),"",ORDER.map(e=>rowHTML(e,true)).join(""),first||open.has("dA"));
  } else if(view==="zone"){
    const groups={}; D.entries.forEach(e=>e.g.forEach(g=>(groups[g]=groups[g]||[]).push(e)));
    Object.keys(groups).sort((a,b)=>area(a).localeCompare(area(b),LANG,{numeric:true})).forEach((g,i)=>{
      html+=card("a:"+g,i+1,area(g),"",groups[g].slice().sort((a,b)=>a.dex-b.dex).map(e=>rowHTML(e,true)).join(""),first?i===0:open.has("a:"+g));
    });
  } else {
    visStops().forEach((s,k)=>{
      html+=card("s"+s,k+1,stopTitle(s),stopTip(s),D.entries.filter(e=>e.stop===s).map(e=>rowHTML(e,false)).join(""),first?k===0:open.has("s"+s));
    });
  }
  $("#stops").innerHTML=html; $("#stops").dataset.view=view;
}
function renderStickers(){ // Zygarde Cores and Cells, grouped by island then area
  let html="", groups={};
  STK.forEach(s=>{ const k=s.island+"|"+s.area; (groups[k]=groups[k]||[]).push(s); });
  Object.keys(groups).forEach(k=>{
    const [isl,a]=k.split("|");
    html+=`<div class="loc-h">${esc(t("isl_"+isl))} · ${esc(area(a))}<span class="loc-left"></span></div>`;
    groups[k].forEach((s,i)=>{
      const sub=[s.sub, s.kind==="cell"&&s.note ? (T().notes||EN.notes)[s.note] || s.note : ""].filter(Boolean).join(" · ");
      const title=s.kind==="core" ? fill(t("coreN"),{m:move(s.note.toLowerCase().replace(/ /g,"-"))}) : fill(t("stkN"),{n:+s.id.slice(1)-5});
      html+=`<label class="mcard" data-m="${s.id}" data-q="${esc(norm([a,area(a),s.sub,s.note,t("isl_"+isl)].join(" ")))}">
        <input type="checkbox" class="cb" data-stk="${s.id}"><span><span class="t">${esc(title)}</span>
        <div class="s">${esc(area(a))}${sub?" · "+esc(sub):""}</div></span></label>`;
    });
  });
  $("#mgrid").innerHTML=html;
}
const renderAll = ()=>{ renderStops(); renderStickers(); sync(); };

/* ---------- sync UI with state ---------- */
function stat(id,got,tot){ $("#s"+id).innerHTML=`${got} <small>/ ${tot}</small>`; $("#b"+id).style.width=(tot?got/tot*100:0)+"%"; }
function sync(){
  document.querySelectorAll("[data-dex]").forEach(cb=>{ const on=state.dex.has(cb.dataset.dex); cb.checked=on; cb.closest(".row").classList.toggle("caught",on); });
  document.querySelectorAll("[data-stk]").forEach(cb=>{ const on=state.stk.has(cb.dataset.stk); cb.checked=on; cb.closest(".mcard").classList.toggle("done",on); });
  document.querySelectorAll(".row").forEach(r=>r.classList.toggle("offver",offVer(ORDER[IDX.get(r.dataset.id)])));
  document.querySelectorAll(".stop[data-k]").forEach(d=>{
    const ids=[...new Set([...d.querySelectorAll(".row")].map(r=>r.dataset.id))], got=ids.filter(id=>state.dex.has(id)).length;
    d.querySelector(".count").textContent=`${got} / ${ids.length}`; d.classList.toggle("done",got===ids.length);
  });
  document.querySelectorAll(".loc-h").forEach(h=>{
    let el=h.nextElementSibling, left=0;
    while(el&&el.matches(".mcard")){ if(!state.stk.has(el.dataset.m)) left++; el=el.nextElementSibling; }
    h.querySelector(".loc-left").textContent = left ? t("locLeft",{n:left}) : t("locDone");
  });
  stat("Dex",state.dex.size,ORDER.length); stat("Stk",state.stk.size,STK.length);
  const vs=visStops(), done=vs.filter(s=>D.entries.filter(e=>e.stop===s).every(e=>state.dex.has(e.id))).length; stat("Stop",done,vs.length);
  const b=$("#stkBadge"), sg=state.stk.size; b.classList.toggle("won",sg===STK.length);
  b.textContent = sg===STK.length ? t("won") : t("badge",{n:sg,t:STK.length});
  $("#ver").value=String(state.ver);
  applyFilter();
  const code=encode(); $("#code").textContent=code;
  try{ history.replaceState(null,"","#"+code); }catch(e){}
  try{ localStorage.setItem("psm-code",code); }catch(e){}
}
function applyFilter(){
  const q=norm($("#q").value.trim()), hide=$("#hide").checked;
  document.querySelectorAll(".row").forEach(r=>{ r.hidden=(q&&!r.dataset.q.includes(q))||(hide&&state.dex.has(r.dataset.id)); });
  document.querySelectorAll("#stops .stop").forEach(d=>{ const any=[...d.querySelectorAll(".row")].some(r=>!r.hidden); d.hidden=!any; if(q&&any) d.open=true; });
  document.querySelectorAll(".mcard").forEach(c=>{ c.hidden=(q&&!c.dataset.q.includes(q))||(hide&&state.stk.has(c.dataset.m)); });
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
  const x=e.target, k=["dex","stk"].find(k=>x.dataset[k]);
  if(k){ x.checked?state[k].add(x.dataset[k]):state[k].delete(x.dataset[k]); sync(); }
});
document.querySelectorAll(".tabs button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected",x===b));
  $("#tab-dex").hidden=b.dataset.tab!=="dex"; $("#tab-stk").hidden=b.dataset.tab!=="stk";
  try{localStorage.setItem("psm-tab",b.dataset.tab)}catch(e){}
});
$("#q").oninput=applyFilter; $("#hide").onchange=applyFilter;
$("#ver").onchange=e=>{ state.ver=+e.target.value; renderStops(); sync(); };
$("#dview").onchange=()=>{ renderStops(); sync(); };
$("#copy").onclick=async()=>{
  const code=encode();
  try{ await navigator.clipboard.writeText(code); toast(t("tCopied")); }
  catch(e){ const r=document.createRange(); r.selectNodeContents($("#code")); const s=getSelection(); s.removeAllRanges(); s.addRange(r); toast(t("tSel")); }
};
$("#loadBtn").onclick=()=>{ $("#loadRow").classList.toggle("show"); $("#loadIn").focus(); };
$("#loadGo").onclick=()=>{
  try{ const d=decode($("#loadIn").value); Object.assign(state,d); renderAll(); $("#loadIn").value=""; $("#loadRow").classList.remove("show"); toast(t("tRest",{d:d.dex.size,s:d.stk.size})); }
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
  document.documentElement.lang=LANG; LINKS.heahea=area("heaheacity");
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
$("#lang").onchange=e=>{ LANG=e.target.value; try{localStorage.setItem("dex-lang",LANG)}catch(err){} applyLang(); renderAll(); };

/* every game: copy all save codes at once; Load also accepts several codes and restores each game */
const PAGE_PREFIX="PSM1-", ALL_KEYS=[["PLZA1-","plza-code"],["PSV","psv-code"],["PLA1-","pla-code"],["PBDSP1-","pbdsp-code"],["PSWSH1-","pswsh-code"],["LGPE1-","lgpe-code"],["PUSUM1-","pusum-code"],["PSM1-","psm-code"],["PORAS1-","poras-code"],["PXY1-","pxy-code"],["PBW21-","pbw2-code"],["PBW1-","pbw-code"],["PHGSS1-","phgss-code"],["PDPPT1-","pdppt-code"],["PFRLG1-","pfrlg-code"],["PRSE1-","prse-code"],["PGSC1-","pgsc-code"],["PRBY1-","prby-code"]];
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
  if(!src){ try{ src=localStorage.getItem("psm-code")||""; }catch(e){} }
  if(src){ try{ Object.assign(state,decode(src)); }catch(e){} }
  ["serebii","pokeapi"].forEach((k,i)=>LINKS[k]=document.querySelectorAll("footer.src a")[i].outerHTML);
  try{ const lg=localStorage.getItem("dex-lang")||localStorage.getItem("lgpe-lang"); if(I18N[lg]) LANG=lg; }catch(e){}
  applyLang(); renderAll();
  try{ if(localStorage.getItem("psm-tab")==="stk") document.querySelector('[data-tab="stk"]').click(); }catch(e){}
})();
