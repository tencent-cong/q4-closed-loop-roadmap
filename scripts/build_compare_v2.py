import json
out = "/Users/congjiang/With/20260923/6fia/"
R = json.load(open(out + "q4_compare_items.json", encoding="utf-8"))
J = json.load(open(out + "q4_effective_days.json", encoding="utf-8"))
TR = {(r["商品消费链路"], r["track"]): r for r in J["track"]}
TN = {(r["商品消费链路"], r["track"]): r for r in J["track_node"]}
track_meta = {}
for l in ["直播", "小店"]:
    for t in ["功效品", "清洁工具", "收纳用品", "厨具", "餐具水具", "家居家纺", "家居工艺品"]:
        a = TR[(l, t)]; n = TN[(l, t)]
        track_meta[f"{l}|{t}"] = dict(avg=a["在跑日耗万"], nodes=[n["①换季启动"], n["②双11"], n["③立冬小雪"], n["④双12冬至"], n["⑤年末"]])

html = r'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Q4 闭环 存量 × 增量 节点对比表（有效日口径）</title>
<style>
:root{--navy:#102f4f;--ink:#1d2939;--muted:#667085;--line:#e4e9f0;--bg:#f5f7fb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Arial,sans-serif}.wrap{max-width:1640px;margin:auto;padding:26px}
.hero{border-radius:22px;padding:32px 40px;color:#fff;background:linear-gradient(120deg,#0e2945,#155a8c 60%,#2775d8)}.hero h1{font-size:28px;margin:8px 0}.hero p{max-width:1100px;color:#dbeafe;line-height:1.75;margin:0}.eyebrow{font-size:12px;letter-spacing:2px;opacity:.72}.src{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.src span{font-size:12px;padding:6px 11px;border:1px solid rgba(255,255,255,.25);border-radius:99px;background:rgba(255,255,255,.08)}
.section{margin-top:18px;padding:22px;background:#fff;border:1px solid var(--line);border-radius:18px}.section h2{font-size:19px;color:var(--navy);margin:0}.sub{color:var(--muted);font-size:13px;margin-top:6px;line-height:1.6}
.tabs{display:flex;gap:8px;margin:16px 0 0;flex-wrap:wrap;align-items:center}.lab{font-size:12px;color:var(--muted);margin-right:2px}.tab{border:1px solid var(--line);background:#fff;border-radius:10px;padding:8px 18px;color:#475467;cursor:pointer;font-weight:700;font-size:14px}.tab.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.chk{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:#475467;margin-left:14px;cursor:pointer}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;margin-top:12px;font-size:12px;color:#475467}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-2px}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:14px;margin-top:14px}table{border-collapse:separate;border-spacing:0;width:100%;font-size:12.5px}th{background:#153a5c;color:#fff;text-align:left;padding:10px 12px;position:sticky;top:0;z-index:2;white-space:nowrap}th small{display:block;font-weight:400;opacity:.8;margin-top:2px}td{vertical-align:top;padding:10px 10px;border-bottom:1px solid var(--line);border-right:1px solid #f0f3f7;line-height:1.5}
.tk{position:sticky;left:0;background:#fff;z-index:1;min-width:150px;border-right:2px solid var(--line)!important}.tk b{display:block;color:var(--navy);font-size:14px}.tk .avg{font-size:12px;color:var(--muted);margin-top:3px}.tk .nd{font-size:11px;color:#98a2b3;margin-top:4px;line-height:1.6}
.cell{min-width:235px}.nday{font-size:11px;color:#98a2b3;margin-bottom:5px}.grp{font-size:11px;font-weight:700;color:#475467;margin:6px 0 3px;letter-spacing:.5px}.grp.inc{color:#b54708;border-top:1px dashed #e4e9f0;padding-top:6px}
.chip{display:flex;justify-content:space-between;gap:8px;padding:4px 8px;margin:3px 0;border-radius:7px;font-size:12px;line-height:1.35;border:1px solid transparent}.chip .nm{font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:150px}.chip .mt{white-space:nowrap;font-variant-numeric:tabular-nums;font-size:11.5px;opacity:.9}
.s1{background:#e8f7ef;color:#08783e;border-color:#c6ecd6}.s2{background:#e9f0ff;color:#2457a7;border-color:#cfdcf9}.s3{background:#fff1dd;color:#9a5800;border-color:#f7dfb3}.s4{background:#fff7ed;color:#9a5800;border:1px dashed #e9a23b}.s5{background:#f3eefc;color:#6b3fc0;border-color:#dccdf6}.s0{background:#f2f4f7;color:#98a2b3}
.more{font-size:11px;color:#2563eb;cursor:pointer;margin-top:4px;display:inline-block}
.note{font-size:12.5px;line-height:1.75;color:#475467;padding:15px;background:#f8fafc;border-radius:12px;margin-top:14px}.note b{color:var(--navy)}
.flat td{white-space:nowrap;vertical-align:middle}.flat th{cursor:pointer;user-select:none}.num{text-align:right;font-variant-numeric:tabular-nums}.tag{display:inline-block;padding:3px 7px;border-radius:6px;font-size:11px;font-weight:650}
.footer{text-align:center;color:#98a2b3;font-size:11px;padding:20px}
</style></head><body><div class="wrap">
<section class="hero"><div class="eyebrow">Q4 CLOSED-LOOP · STOCK × INCREMENT BY NODE</div><h1>Q4 闭环：赛道 × 节点 存量品 / 增量机会品 对比表</h1><p>恢复此前的赛道×节点对比表，并把每个品的数据换成按天口径：有效天数（当日消耗 ≥ 2000 元的天数）与在跑日耗（仅有效日的日均，万/天）。同一单元格里，上半部分是该链路去年 Q4 已跑的存量品，下半部分是竞媒在跑、该链路未投放的增量机会品。直播与小店（直购）分两个 tab，每条链路独立判定存量/增量。</p><div class="src"><span>闭环：去年 Q4 by 天数据（10.01－12.31）</span><span>竞媒：抖音 Q4 TOP1500 + 2026.10 月榜</span><span>有效日阈值 ≥ 2000 元/天</span><span>赛道口径：情报台</span><span>清洁工具 = 物理清洁 + 洗浴工具（泡脚桶/沐浴桶/搓澡），化学清洁已剔除</span><span>手霜/足霜等个护类目已删除</span><span>保鲜袋/保鲜膜归收纳用品</span><span>行序：家纺、厨具置顶，其余按日耗倒序</span></div></section>

<section class="section"><h2>赛道 × 节点 对比表</h2><div class="sub">默认每格存量品按在跑日耗取 TOP 6，增量品按抖音 10 月榜销售额指数取 TOP 5，点“更多”展开全部。存量品标注「在跑日耗 · 有效天数」，增量品标注抖音 10 月榜销售额指数（万）或另一链路的在跑日耗。</div>
<div class="tabs"><span class="lab">链路</span><button class="tab active" data-l="live">直播</button><button class="tab" data-l="shop">小店（直购）</button><label class="chk"><input type="checkbox" id="showTiny"> 显示未达有效日的微量品（&lt;2000 元/天）</label><label class="chk"><input type="checkbox" id="expandAll"> 全部展开</label></div>
<div class="legend"><span><i style="background:#c6ecd6"></i>存量 · 抖音也在跑</span><span><i style="background:#cfdcf9"></i>存量 · 闭环独有</span><span><i style="background:#f7dfb3"></i>增量 · 抖音在投，闭环未投放</span><span><i style="background:#fff7ed;border:1px dashed #e9a23b"></i>增量 · 另一链路已跑，可直接复制</span><span><i style="background:#dccdf6"></i>增量 · 10 月榜新增机会品</span><span><i style="background:#f2f4f7"></i>微量 · 有消耗但未达有效日</span></div>
<div class="table-wrap"><table id="mx"><thead><tr><th class="tk" style="z-index:3">赛道<small>整季日均 / 各节点日耗 万/天</small></th><th>①换季启动<small>寒露/霜降 10.01－10.20</small></th><th>②双11<small>含重阳 10.21－11.11</small></th><th>③立冬/小雪<small>保暖峰值 11.12－11.30</small></th><th>④双12/大雪冬至<small>年终收官 12.01－12.22</small></th><th>⑤春节大扫除·年货<small>12.23－1月中（数据至 12.31）</small></th></tr></thead><tbody id="mxb"></tbody></table></div>
<div class="note" id="mxnote"></div></section>

<section class="section"><h2>当前链路 明细清单</h2><div class="sub">与上表同一份数据的平铺视图，点表头排序，便于核对单品。</div>
<div class="tabs"><span class="lab">状态</span><span id="stBtns"></span></div>
<div class="table-wrap"><table class="flat" id="flat"><thead><tr><th data-k="track">赛道</th><th data-k="node">节点</th><th data-k="name">品</th><th data-k="st">状态</th><th data-k="days" class="num">有效天数</th><th data-k="daily" class="num">在跑日耗<small>万/天</small></th><th data-k="peak" class="num">峰值<small>万/天</small></th><th data-k="a">有效区间</th><th>有效消耗节点分布</th><th data-k="dy_oct" class="num">抖音10月榜<small>销售额指数 万</small></th><th data-k="dy_q4">抖音Q4<small>TOP1500</small></th><th data-k="odaily" class="num">另一链路<small>日耗 · 天数</small></th></tr></thead><tbody id="fb"></tbody></table></div></section>
<div class="footer">去年 Q4 闭环 by 天 × 抖音 Q4 TOP1500 / 2026.10 月榜 ｜ 情报台赛道口径 ｜ 清洁工具仅含物理清洁 ｜ 有效日阈值 2000 元/天</div></div>
<script>
const R=__R__;const TM=__TM__;
const TRACKS=["功效品","清洁工具","收纳用品","厨具","餐具水具","家居家纺","家居工艺品","生活日用其他"];
const NODE=["①换季启动","②双11","③立冬小雪","④双12冬至","⑤年末"];
let L="live";const O=()=>L==="live"?"shop":"live";const LN={live:"直播",shop:"小店"};
function st(r){const days=r[L+"_days"],old=r[L+"_old"],dy=r.dy_q4===1||r.dy_oct>0;
 if(days>0)return dy?["存量·抖音也在跑","s1",1]:["存量·闭环独有","s2",1];
 if(old>0)return["微量·未达有效日","s0",0];
 if(r.dy_q4===0&&r.dy_oct>0&&r.live_days===0&&r.shop_days===0)return["增量·10月榜新增","s5",2];
 if(r[O()+"_days"]>0)return["增量·另一链路已跑","s4",2];
 return["增量·抖音在投闭环未投","s3",2]}
function chip(r,[nm,cls,kind]){let mt;if(kind===1)mt=`${r[L+"_daily"].toFixed(1)}万 · ${r[L+"_days"]}d`;else if(kind===0)mt=`峰值${r[L+"_peak"].toFixed(2)}万`;else if(cls==="s4")mt=`${LN[O()]} ${r[O()+"_daily"].toFixed(1)}万 · ${r[O()+"_days"]}d`;else mt=r.dy_oct>0?`抖10月 ${Math.round(r.dy_oct)}`:`抖Q4榜`;
 return `<div class="chip ${cls}" title="${nm}｜${r.name}｜匹配闭环类目：${r.matched||'无'}"><span class="nm">${r.name}</span><span class="mt">${mt}</span></div>`}
function renderMx(){document.querySelectorAll("[data-l]").forEach(b=>b.classList.toggle("active",b.dataset.l===L));
 const tiny=document.getElementById("showTiny").checked,ex=document.getElementById("expandAll").checked;let h="";let cnt={s:0,i:0};
 const PIN=["家居家纺","厨具"];const order=PIN.concat(TRACKS.filter(t=>!PIN.includes(t)&&TM[LN[L]+"|"+t]).sort((a,b)=>TM[LN[L]+"|"+b].avg-TM[LN[L]+"|"+a].avg)).concat(TRACKS.filter(t=>!PIN.includes(t)&&!TM[LN[L]+"|"+t]));
 for(const t of order){const m=TM[LN[L]+"|"+t];
  h+=`<tr><td class="tk"><b>${t}</b>${m?`<div class="avg">整季日均 ${m.avg.toFixed(1)} 万/天</div><div class="nd">${m.nodes.map((v,i)=>`${"①②③④⑤"[i]} ${v.toFixed(1)}`).join(" · ")}</div>`:`<div class="avg">CSV 未拉取该赛道闭环类目</div>`}</td>`;
  for(let n=1;n<=5;n++){const rs=R.filter(r=>r.track===t&&r.node===n).map(r=>({r,s:st(r)}));
   let stock=rs.filter(x=>x.s[2]===1).sort((a,b)=>b.r[L+"_daily"]-a.r[L+"_daily"]);let inc=rs.filter(x=>x.s[2]===2).sort((a,b)=>(b.r.dy_oct-a.r.dy_oct)||(b.r[O()+"_daily"]-a.r[O()+"_daily"]));let tn=rs.filter(x=>x.s[2]===0);
   cnt.s+=stock.length;cnt.i+=inc.length;
   const lim=(arr,k,id)=>{if(ex||arr.length<=k)return arr.map(x=>chip(x.r,x.s)).join("");return arr.slice(0,k).map(x=>chip(x.r,x.s)).join("")+`<span class="more" onclick="this.outerHTML=this.dataset.rest" data-rest="${arr.slice(k).map(x=>chip(x.r,x.s)).join("").replace(/"/g,'&quot;')}">更多 ${arr.length-k} 个 ▾</span>`};
   h+=`<td class="cell">${m?`<div class="nday">赛道节点日耗 ${m.nodes[n-1].toFixed(1)} 万/天</div>`:""}`;
   if(stock.length)h+=`<div class="grp">存量 ${stock.length}</div>${lim(stock,6)}`;
   if(inc.length)h+=`<div class="grp inc">增量机会 ${inc.length}</div>${lim(inc,5)}`;
   if(tiny&&tn.length)h+=`<div class="grp" style="color:#98a2b3">微量 ${tn.length}</div>${tn.map(x=>chip(x.r,x.s)).join("")}`;
   if(!stock.length&&!inc.length&&!(tiny&&tn.length))h+=`<span style="color:#c0c7d2">—</span>`;h+=`</td>`}
  h+=`</tr>`}
 document.getElementById("mxb").innerHTML=h;
 document.getElementById("mxnote").innerHTML=`<b>${LN[L]}链路</b>：存量品 ${cnt.s} 个、增量机会品 ${cnt.i} 个。存量品的“万 · d”为在跑日耗与有效天数，例如 4.9万 · 13d 表示该品在 13 个有效日里日均 4.9 万，而不是摊到 92 天的均值。增量品中带虚线框的在另一链路已有有效消耗，是最容易复制的一批；紫色为 10 月榜新上榜、去年两边都没跑的真增量。`;renderFlat()}
let F="全部",sk="daily",sd=-1;
const STS=["全部","存量·抖音也在跑","存量·闭环独有","增量·抖音在投闭环未投","增量·另一链路已跑","增量·10月榜新增"];
document.getElementById("stBtns").innerHTML=STS.map(s=>`<button class="tab ${s==="全部"?"active":""}" style="padding:5px 10px;font-size:12px;font-weight:550" data-s="${s}">${s}</button>`).join("");
document.querySelectorAll("[data-s]").forEach(b=>b.onclick=()=>{document.querySelectorAll("[data-s]").forEach(x=>x.classList.remove("active"));b.classList.add("active");F=b.dataset.s;renderFlat()});
document.querySelectorAll("#flat th[data-k]").forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sk===k)sd*=-1;else{sk=k;sd=["track","node","name","st","a"].includes(k)?1:-1}renderFlat()});
function renderFlat(){const tiny=document.getElementById("showTiny").checked;
 let rows=R.map(r=>{const s=st(r);return{...r,st:s[0],cls:s[1],kind:s[2],days:r[L+"_days"],daily:r[L+"_daily"],peak:r[L+"_peak"],a:r[L+"_a"],b:r[L+"_b"],nd:r[L+"_nd"],odaily:r[O()+"_daily"],odays:r[O()+"_days"]}}).filter(r=>tiny||r.kind!==0).filter(r=>F==="全部"||r.st===F);
 rows.sort((x,y)=>{const a=x[sk],b=y[sk];return(typeof a==="string"?a.localeCompare(b,"zh"):a-b)*sd});
 document.getElementById("fb").innerHTML=rows.map(r=>`<tr><td>${r.track}</td><td>${NODE[r.node-1]}</td><td><b>${r.name}</b></td><td><span class="tag ${r.cls}">${r.st}</span></td><td class="num">${r.days||""}</td><td class="num"><b>${r.days?r.daily.toFixed(2):""}</b></td><td class="num">${r.peak?r.peak.toFixed(2):""}</td><td>${r.a?r.a+" － "+r.b:""}</td><td style="font-size:11.5px;color:#667085">${r.nd}</td><td class="num">${r.dy_oct>0?Math.round(r.dy_oct):""}</td><td>${r.dy_q4?"命中":""}</td><td class="num">${r.odays?r.odaily.toFixed(2)+" · "+r.odays+"d":""}</td></tr>`).join("")}
document.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>{L=b.dataset.l;renderMx()});document.getElementById("showTiny").onchange=renderMx;document.getElementById("expandAll").onchange=renderMx;
renderMx();
</script></body></html>'''
html = html.replace("__R__", json.dumps(R, ensure_ascii=False)).replace("__TM__", json.dumps(track_meta, ensure_ascii=False))
open(out + "q4-closed-loop-compare-v2.html", "w", encoding="utf-8").write(html)
print("ok", len(html))
