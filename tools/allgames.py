# Adds "Copy all games" to every game page (save bar) + multi-code Load. Idempotent.
import re,sys
S,R=sys.argv[1],sys.argv[2]
TR={'en':('Copy all games','Copy the save codes of every game you track here, to paste into your notes','Copied the save codes of {n} games. Paste them into your notes.','Restored {n} games.'),
 'ja':('全ゲームをコピー','このサイトで記録している全ゲームのセーブコードをまとめてコピー','{n}本のゲームのセーブコードをコピーしました。メモに貼り付けてください。','{n}本のゲームを復元しました。'),
 'fr':('Copier tous les jeux','Copier les codes de sauvegarde de tous les jeux suivis ici','Codes de {n} jeux copiés. Collez-les dans vos notes.','{n} jeux restaurés.'),
 'de':('Alle Spiele kopieren','Speichercodes aller hier verfolgten Spiele kopieren','Speichercodes von {n} Spielen kopiert. Füge sie in deine Notizen ein.','{n} Spiele wiederhergestellt.'),
 'ko':('모든 게임 복사','여기서 기록 중인 모든 게임의 세이브 코드를 한꺼번에 복사','게임 {n}개의 세이브 코드를 복사했습니다. 메모에 붙여 넣으세요.','게임 {n}개를 복원했습니다.'),
 'zh-Hant':('複製所有遊戲','一次複製這裡記錄的所有遊戲存檔代碼','已複製{n}款遊戲的存檔代碼，請貼到記事本中。','已還原{n}款遊戲。'),
 'zh-Hans':('复制所有游戏','一次复制这里记录的所有游戏存档代码','已复制{n}款游戏的存档代码，请粘贴到备忘录中。','已还原{n}款游戏。')}
BTN='<button class="btn ghost" id="copyAll" data-i18n="copyAll" title="Copy the save codes of every game you track here, to paste into your notes" data-i18n-title="copyAllT">Copy all games</button>'
def js(prefix): return '''
/* every game: copy all save codes at once; Load also accepts several codes and restores each game */
const PAGE_PREFIX="%s", ALL_KEYS=[["PLZA1-","plza-code"],["PSV","psv-code"],["PLA1-","pla-code"],["PBDSP1-","pbdsp-code"],["PSWSH1-","pswsh-code"],["LGPE1-","lgpe-code"],["PUSUM1-","pusum-code"],["PSM1-","psm-code"],["PORAS1-","poras-code"],["PXY1-","pxy-code"],["PBW21-","pbw2-code"],["PBW1-","pbw-code"],["PHGSS1-","phgss-code"],["PDPPT1-","pdppt-code"],["PFRLG1-","pfrlg-code"],["PRSE1-","prse-code"],["PGSC1-","pgsc-code"],["PRBY1-","prby-code"]];
const CODE_RE=/(LGPE1-[A-Za-z0-9_-]{55}|PLZA1-[A-Za-z0-9_-]{79}|PSV1-[A-Za-z0-9_-]{118}|PSV2-[A-Za-z0-9_-]{139}|PLA1-[A-Za-z0-9_-]{67}|PBDSP1-[A-Za-z0-9_-]{83}|PSWSH1-[A-Za-z0-9_-]{130}|PUSUM1-[A-Za-z0-9_-]{87}|PSM1-[A-Za-z0-9_-]{70}|PORAS1-[A-Za-z0-9_-]{50}|PXY1-[A-Za-z0-9_-]{84}|PBW21-[A-Za-z0-9_-]{55}|PBW1-[A-Za-z0-9_-]{28}|PHGSS1-[A-Za-z0-9_-]{46}|PDPPT1-[A-Za-z0-9_-]{40}|PFRLG1-[A-Za-z0-9_-]{28}|PRSE1-[A-Za-z0-9_-]{38}|PGSC1-[A-Za-z0-9_-]{44}|PRBY1-[A-Za-z0-9_-]{27})/g;
function allCodes(){ return ALL_KEYS.map(([,k])=>{ try{ return localStorage.getItem(k)||""; }catch(e){ return ""; } }).filter(Boolean); }
function storeAll(text){ let n=0; (String(text).match(CODE_RE)||[]).forEach(c=>{ const m=ALL_KEYS.find(([p])=>c.startsWith(p)); if(m){ try{ localStorage.setItem(m[1],c); n++; }catch(e){} } }); return n; }
$("#copyAll").onclick=async()=>{
  const codes=allCodes();
  try{ await navigator.clipboard.writeText(codes.join("\\n")); toast(t("tCopiedAll",{n:codes.length})); }
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
''' % prefix
def add_btn(s):
  if 'id="copyAll"' in s: return s
  a='<button class="btn ghost" id="loadBtn" data-i18n="load">Load</button>'
  assert s.count(a)==1; return s.replace(a,a+'\n    '+BTN)
def add_keys(s,anchor=r'tBad:\s*"[^"]*"'):
  if 'tCopiedAll' in s: return s
  ms=list(re.finditer(anchor,s)); out=s
  # map each match to its language by the nearest preceding language header
  for m in reversed(ms):
    head=s[:m.start()]
    pos={k:max(head.rfind('\n'+k+':{'),head.rfind('"'+k+'":{'),head.rfind(' '+k+':{')) for k in TR}
    lang=max(pos,key=pos.get)
    c,ct,tc,tr=TR[lang]
    ins=',copyAll:"%s",copyAllT:"%s",tCopiedAll:"%s",tRestAll:"%s"'%(c,ct,tc,tr) if lang!='en' else ',tCopiedAll:"%s",tRestAll:"%s"'%(tc,tr)
    out=out[:m.end()]+ins+out[m.end():]
  return out
# --- Let's Go page (edited in place) ---
p=R+'/letsgo/index.html'; s=open(p).read()
s=add_btn(s); s=add_keys(s)
if 'PAGE_PREFIX' not in s: s=s.replace('\n/* ---------- boot ---------- */',js('LGPE1-')+'\n/* ---------- boot ---------- */',1)
open(p,'w').write(s)
# --- generated pages: patch their sources ---
for g,prefix,i18n in (('za','PLZA1-',['za_i18n_en.js','za_i18n_jafr.js','za_i18n_deko.js','za_i18n_zh.js']),('sv','PSV1-',['sv_i18n.js']),('la','PLA1-',['la_i18n.js']),('bdsp','PBDSP1-',['bdsp_i18n.js'])):
  p=f'{S}/{g}_template.html'; s=open(p).read(); open(p,'w').write(add_btn(s))
  p=f'{S}/{g}_core.js'; s=open(p).read()
  if 'PAGE_PREFIX' not in s: s=s.replace('\n/* ---------- boot ---------- */',js(prefix)+'\n/* ---------- boot ---------- */',1)
  open(p,'w').write(s)
  for f in i18n:
    p=f'{S}/{f}'; s=open(p).read(); open(p,'w').write(add_keys(s))
print('patched')
