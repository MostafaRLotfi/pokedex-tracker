/* ---------- data helpers ---------- */
const ORDER = D.entries.slice().sort((a,b)=>a.id.localeCompare(b.id)); // save-code bit order: Hisui #001–#242 (never reorder)
const IDX = new Map(ORDER.map((e,i)=>[e.id,i]));
const BYN = {}; D.entries.forEach(e=>BYN[e.n]=e);
const WISPS = D.wisps, UNOWN = D.unown; // save-code bit order (never reorder)
const AREAS = ["Jubilife Village","Obsidian Fieldlands","Crimson Mirelands","Cobalt Coastlands","Coronet Highlands","Alabaster Icelands"];
const state = {dex:new Set(), wsp:new Set(), unw:new Set()};
const $ = s=>document.querySelector(s);

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
const area = a=>(D.areas[a]||{})[LANG] || a;

const ITEM = {duskstone:"dusk-stone",firestone:"fire-stone",leafstone:"leaf-stone",moonstone:"moon-stone",shinystone:"shiny-stone",sunstone:"sun-stone",
  thunderstone:"thunder-stone",waterstone:"water-stone",icestone:"ice-stone",blackaugurite:"black-augurite",peatblock:"peat-block",
  upgrade:"upgrade",dubiousdisc:"dubious-disc",electirizer:"electirizer",magmarizer:"magmarizer",protector:"protector",reapercloth:"reaper-cloth",metalcoat:"metal-coat"};
function cond(m){ // Legends: Arceus: trade evolutions use a Linking Cord, and trade items are used directly
  let r;
  if(!m) return C("special");
  if((r=m.match(/^l(\d+)$/))) return lv(r[1]);
  if((r=m.match(/^p[45]level(\d+)$/))) return lv(r[1]);
  if(m==="l50rain") return lv(50)+C("rain");
  if((r=m.match(/^level([mf])(\d+)$/))) return lv(r[2])+C(r[1]==="m"?"male":"female");
  if(m==="trade") return item("linking-cord");
  if((r=m.match(/^trade(.+)$/)) && ITEM[r[1]]) return item(ITEM[r[1]]);
  if(m==="levelcoronet") return item("thunder-stone");
  if(ITEM[m]) return item(ITEM[m]);
  if(m==="maledawnstone") return item("dawn-stone")+" ♂";
  if(m==="femaledawnstone") return item("dawn-stone")+" ♀";
  if(m==="leveldayovalstone") return fill(C("holdLv"),{i:item("oval-stone")})+C("day");
  if(m==="levelnightrazorclaw") return fill(C("holdLv"),{i:item("razor-claw")})+C("night");
  if(m==="levelnightrazorfang") return fill(C("holdLv"),{i:item("razor-fang")})+C("night");
  if(m==="razorclawday") return item("razor-claw")+C("day");
  if(m==="peatblock") return item("peat-block")+C("fullmoon");
  if((r=m.match(/^level(ancientpower|doublehit|mimic|rollout)$/))) return fill(C("knows"),{m:move(r[1])});
  if(m==="psyshieldbash") return fill(C("use20"),{m:move("psyshieldbash")});
  if(m==="barbbarrge") return fill(C("use20"),{m:move("barbbarrage")});
  if(m==="happiness") return C("friend");
  if(m==="happinessday") return C("friend")+C("day");
  if(m==="happinessnight") return C("friend")+C("night");
  if(m==="recoil") return C("recoil");
  if(m==="levelremoraid223") return C("remoraid");
  return C("special");
}
function tokText(k){
  const a=k.slice(1);
  switch(k[0]){
    case "area": return area(a[0])+(a[1].length?H("colon")+a[1].map(area).join(sep()):"");
    case "dist": return fill(H("dist"),{a:area(a[0])});
    case "mmo": return fill(H("mmo"),{a:area(a[0])});
    case "evo": return fill(H("evolve"),{p:nm(a[0]),c:cond(a[1])});
    case "x": { const v=(T().x||{})[a[0]]; return v!=null ? v : EN.x[a[0]]; }
  }
  return "";
}
function howText(e){ // route view: first two areas, then "+N more"; the area view shows everything
  const full=$("#dview").value==="zone", areas=e.tok.filter(k=>k[0]==="area"), rest=e.tok.filter(k=>k[0]!=="area");
  const shown=full?areas:areas.slice(0,2), more=areas.length-shown.length;
  return shown.map(tokText).join(H("join"))+(more?fill(H("more"),{n:more}):"")+(rest.length?(shown.length?H("join"):"")+rest.map(tokText).join(H("join")):"");
}
const evoText = e=>e.evo.map(stage=>stage.map(([n,m])=>nm(n)+" ("+cond(m)+")").join(" / ")).join("  →  ");
function stopTitle(i){
  const s=D.stops[i], X=T().stopT||EN.stopT;
  if(AREAS.includes(s)) return fill(X.area,{a:area(s),m:(T().missions||EN.missions)[i]});
  return fill(X[s],{a:area("Jubilife Village")});
}
const stopTip = i=>{ const s=(T().tips||{})[i]; return s!=null ? s : (EN.tips[i]||""); };
const visStops = ()=>D.stops.map((_,i)=>i).filter(i=>D.entries.some(e=>e.stop===i));

/* ---------- encode / decode ---------- */
const DB = Math.ceil(ORDER.length/8), WB = Math.ceil(WISPS.length/8), UB = Math.ceil(UNOWN.length/8), LEN = 1+DB+WB+UB;
function encode(){
  const b=new Uint8Array(LEN);
  state.dex.forEach(id=>{ const i=IDX.get(id); b[1+(i>>3)]|=1<<(i&7); });
  WISPS.forEach((w,i)=>{ if(state.wsp.has(w.id)) b[1+DB+(i>>3)]|=1<<(i&7); });
  UNOWN.forEach((u,i)=>{ if(state.unw.has(u.id)) b[1+DB+WB+(i>>3)]|=1<<(i&7); });
  let bin=""; b.forEach(x=>bin+=String.fromCharCode(x));
  return "PLA1-"+btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
}
function decode(str){
  str=(str||"").trim().replace(/^#/,"");
  if(!str.startsWith("PLA1-")) throw new Error("bad prefix");
  let s=str.slice(5).replace(/-/g,"+").replace(/_/g,"/"); while(s.length%4) s+="=";
  const bin=atob(s); if(bin.length!==LEN) throw new Error("bad length");
  const bit=(off,i)=>bin.charCodeAt(off+(i>>3))&(1<<(i&7));
  return {dex:new Set(ORDER.filter((e,i)=>bit(1,i)).map(e=>e.id)), wsp:new Set(WISPS.filter((w,i)=>bit(1+DB,i)).map(w=>w.id)),
          unw:new Set(UNOWN.filter((u,i)=>bit(1+DB+WB,i)).map(u=>u.id))};
}

/* ---------- render: Pokédex ---------- */
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
const evoHTML = s=>s ? esc(s).replace(/\(([^)]*)\)/g,'<span style="color:var(--muted)">($1)</span>').split("  →  ").join('<span class="arr">→</span>') : "";
const headHTML = ()=>`<div class="head"><span></span><span>${esc(t("colDex"))}</span><span>${esc(t("colMon"))}</span><span>${esc(t("colHow"))}</span><span>${esc(t("colEvo"))}</span></div>`;
function rowHTML(e,withStop){
  const name=nm(e.n), how=howText(e), title=stopTitle(e.stop);
  const q=norm([N.NAMES.en[e.n],name,how,title].join(" "));
  return `<div class="row" data-id="${e.id}" data-q="${esc(q)}">
    <span class="cbw"><input type="checkbox" class="cb" data-dex="${e.id}" aria-label="${esc(name)}"></span>
    <span class="dex">#${e.id}</span>
    <span class="main"><span class="nm">${esc(name)}</span>
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
    html=`<div class="stop"><div class="rows">${headHTML()}${ORDER.map(e=>rowHTML(e,true)).join("")}</div></div>`;
  } else if(view==="zone"){
    const groups={}; D.entries.forEach(e=>e.g.forEach(g=>(groups[g]=groups[g]||[]).push(e)));
    const order=AREAS.flatMap(a=>[a,"dist|"+a]).filter(g=>groups[g]);
    order.forEach((g,i)=>{
      const label=g.startsWith("dist|") ? fill(H("dist"),{a:area(g.slice(5))}) : area(g);
      const list=groups[g].slice().sort((a,b)=>IDX.get(a.id)-IDX.get(b.id));
      html+=card("g:"+g,i+1,label,"",list.map(e=>rowHTML(e,true)).join(""),first?i===0:open.has("g:"+g));
    });
  } else {
    visStops().forEach((s,k)=>{
      const list=D.entries.filter(e=>e.stop===s);
      html+=card("s"+s,k+1,stopTitle(s),stopTip(s),list.map(e=>rowHTML(e,false)).join(""),first?k===0:open.has("s"+s));
    });
  }
  $("#stops").innerHTML=html; $("#stops").dataset.view=view;
}

/* ---------- render: wisps & Unown ---------- */
function renderWisps(){
  let html="", last=null;
  WISPS.forEach(w=>{
    if(w.area!==last){ last=w.area; html+=`<div class="loc-h">${esc(area(w.area))}<span class="loc-left"></span></div>`; }
    html+=`<label class="mcard" data-m="${w.id}" data-set="wsp" data-q="${esc(norm([w.area,area(w.area),w.loc,area(w.loc)].join(" ")))}">
      <input type="checkbox" class="cb" data-wsp="${w.id}"><span><span class="t">${esc(fill(H("wispN"),{n:w.no}))}</span>
      <div class="s">${esc(area(w.loc))}</div></span></label>`;
  });
  $("#wgrid").innerHTML=html;
}
function renderUnown(){
  $("#ugrid").innerHTML=UNOWN.map(u=>`<label class="mcard" data-m="${u.id}" data-set="unw" data-q="${esc(norm(["unown",nm(201),u.form,u.loc,area(u.loc)].join(" ")))}">
      <input type="checkbox" class="cb" data-unw="${u.id}"><span><span class="t">${esc(fill(H("unownN"),{p:nm(201),f:u.form}))}</span>
      <div class="s">${esc(area(u.loc))}</div></span></label>`).join("");
}

/* ---------- sync UI with state ---------- */
function sync(){
  document.querySelectorAll("[data-dex]").forEach(cb=>{ const on=state.dex.has(cb.dataset.dex); cb.checked=on; cb.closest(".row").classList.toggle("caught",on); });
  document.querySelectorAll("[data-wsp]").forEach(cb=>{ const on=state.wsp.has(cb.dataset.wsp); cb.checked=on; cb.closest(".mcard").classList.toggle("done",on); });
  document.querySelectorAll("[data-unw]").forEach(cb=>{ const on=state.unw.has(cb.dataset.unw); cb.checked=on; cb.closest(".mcard").classList.toggle("done",on); });
  document.querySelectorAll(".stop[data-k]").forEach(d=>{
    const ids=[...new Set([...d.querySelectorAll(".row")].map(r=>r.dataset.id))], got=ids.filter(id=>state.dex.has(id)).length;
    d.querySelector(".count").textContent=`${got} / ${ids.length}`; d.classList.toggle("done",got===ids.length);
  });
  document.querySelectorAll(".loc-h").forEach(h=>{
    let el=h.nextElementSibling, left=0;
    while(el&&el.matches(".mcard")){ if(!state.wsp.has(el.dataset.m)) left++; el=el.nextElementSibling; }
    h.querySelector(".loc-left").textContent = left ? t("locLeft",{n:left}) : t("locDone");
  });
  const got=state.dex.size, wg=state.wsp.size, ug=state.unw.size;
  const stops=visStops(), sdone=stops.filter(s=>D.entries.filter(e=>e.stop===s).every(e=>state.dex.has(e.id))).length;
  $("#sDex").innerHTML=`${got} <small>/ ${ORDER.length}</small>`; $("#bDex").style.width=got/ORDER.length*100+"%";
  $("#sWsp").innerHTML=`${wg} <small>/ ${WISPS.length}</small>`; $("#bWsp").style.width=wg/WISPS.length*100+"%";
  $("#sUnw").innerHTML=`${ug} <small>/ ${UNOWN.length}</small>`; $("#bUnw").style.width=ug/UNOWN.length*100+"%";
  const b1=$("#wspBadge"); b1.classList.toggle("won",wg===WISPS.length); b1.textContent = wg===WISPS.length ? t("wonW") : t("badgeW",{n:wg,t:WISPS.length});
  const b2=$("#unwBadge"); b2.classList.toggle("won",ug===UNOWN.length); b2.textContent = ug===UNOWN.length ? t("wonU") : t("badgeU",{n:ug,t:UNOWN.length});
  applyFilter();
  const code=encode(); $("#code").textContent=code;
  try{ history.replaceState(null,"","#"+code); }catch(e){}
  try{ localStorage.setItem("pla-code",code); }catch(e){}
}
function applyFilter(){
  const q=norm($("#q").value.trim()), hide=$("#hide").checked;
  document.querySelectorAll(".row").forEach(r=>{ r.hidden=(q&&!r.dataset.q.includes(q))||(hide&&state.dex.has(r.dataset.id)); });
  document.querySelectorAll(".stop").forEach(d=>{ const any=[...d.querySelectorAll(".row")].some(r=>!r.hidden); d.hidden=!any; if(q&&any&&d.tagName==="DETAILS") d.open=true; });
  document.querySelectorAll(".mcard").forEach(c=>{ c.hidden=(q&&!c.dataset.q.includes(q))||(hide&&state[c.dataset.set].has(c.dataset.m)); });
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
  if(x.dataset.wsp){ x.checked?state.wsp.add(x.dataset.wsp):state.wsp.delete(x.dataset.wsp); sync(); }
  if(x.dataset.unw){ x.checked?state.unw.add(x.dataset.unw):state.unw.delete(x.dataset.unw); sync(); }
});
document.querySelectorAll(".tabs button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".tabs button").forEach(x=>x.setAttribute("aria-selected",x===b));
  ["dex","wsp","unw"].forEach(k=>$("#tab-"+k).hidden=b.dataset.tab!==k);
  try{localStorage.setItem("pla-tab",b.dataset.tab)}catch(e){}
});
$("#q").oninput=applyFilter; $("#hide").onchange=applyFilter;
$("#dview").onchange=()=>{ renderStops(); sync(); };
$("#copy").onclick=async()=>{
  const code=encode();
  try{ await navigator.clipboard.writeText(code); toast(t("tCopied")); }
  catch(e){ const r=document.createRange(); r.selectNodeContents($("#code")); const s=getSelection(); s.removeAllRanges(); s.addRange(r); toast(t("tSel")); }
};
$("#loadBtn").onclick=()=>{ $("#loadRow").classList.toggle("show"); $("#loadIn").focus(); };
$("#loadGo").onclick=()=>{
  try{ const d=decode($("#loadIn").value); Object.assign(state,d); renderStops(); renderWisps(); renderUnown(); sync(); $("#loadIn").value=""; $("#loadRow").classList.remove("show"); toast(t("tRest",{d:d.dex.size,w:d.wsp.size,u:d.unw.size})); }
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
$("#lang").onchange=e=>{ LANG=e.target.value; try{localStorage.setItem("dex-lang",LANG)}catch(err){} applyLang(); renderStops(); renderWisps(); renderUnown(); sync(); };

/* every game: copy all save codes at once; Load also accepts several codes and restores each game */
const PAGE_PREFIX="PLA1-", ALL_KEYS=[["PLZA1-","plza-code"],["PSV","psv-code"],["PLA1-","pla-code"],["PBDSP1-","pbdsp-code"],["PSWSH1-","pswsh-code"],["LGPE1-","lgpe-code"],["PUSUM1-","pusum-code"],["PSM1-","psm-code"],["PORAS1-","poras-code"],["PXY1-","pxy-code"],["PBW21-","pbw2-code"],["PBW1-","pbw-code"],["PHGSS1-","phgss-code"],["PDPPT1-","pdppt-code"],["PFRLG1-","pfrlg-code"],["PRSE1-","prse-code"],["PGSC1-","pgsc-code"],["PRBY1-","prby-code"]];
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
  if(!src){ try{ src=localStorage.getItem("pla-code")||""; }catch(e){} }
  if(src){ try{ Object.assign(state,decode(src)); }catch(e){} }
  ["serebii","pokeapi"].forEach((k,i)=>LINKS[k]=document.querySelectorAll("footer.src a")[i].outerHTML);
  try{ const lg=localStorage.getItem("dex-lang")||localStorage.getItem("lgpe-lang"); if(I18N[lg]) LANG=lg; }catch(e){}
  applyLang(); renderStops(); renderWisps(); renderUnown(); sync();
  try{ const tb=localStorage.getItem("pla-tab"); if(tb&&tb!=="dex") document.querySelector(`[data-tab="${tb}"]`).click(); }catch(e){}
})();
