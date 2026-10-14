import json
out = "/Users/congjiang/With/20260923/6fia/"
R = json.load(open(out + "q4_compare_items.json", encoding="utf-8"))
J = json.load(open(out + "q4_effective_days.json", encoding="utf-8"))
TR = {(r["商品消费链路"], r["track"]): r for r in J["track"]}
# 只保留排序用的整季日均，页面不展示任何消耗数字
order_meta = {f"{l}|{t}": TR[(l, t)]["在跑日耗万"] for l in ["直播", "小店"] for t in ["功效品", "清洁工具", "收纳用品", "厨具", "餐具水具", "家居家纺", "家居工艺品"]}
# 精简数据：去掉所有消耗/指数字段
LR = [dict(track=r["track"], name=r["name"], node=r["node"], dy=int(r["dy_q4"] == 1 or r["dy_oct"] > 0), oct_new=int(r["dy_q4"] == 0 and r["dy_oct"] > 0 and r["live_days"] == 0 and r["shop_days"] == 0),
           live=int(r["live_days"] > 0), shop=int(r["shop_days"] > 0), live_old=int(r["live_old"] > 0), shop_old=int(r["shop_old"] > 0), oct_rank=r["dy_oct"]) for r in R]

html = r'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Q4 闭环 赛道 × 节点 对比表（精简版）</title>
<style>
:root{--navy:#102f4f;--ink:#1d2939;--muted:#667085;--line:#e4e9f0;--bg:#f5f7fb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Arial,sans-serif}.wrap{max-width:1640px;margin:auto;padding:26px}
.hero{border-radius:22px;padding:28px 36px;color:#fff;background:linear-gradient(120deg,#0e2945,#155a8c 60%,#2775d8)}.hero h1{font-size:26px;margin:8px 0}.hero p{max-width:1100px;color:#dbeafe;line-height:1.75;margin:0}.eyebrow{font-size:12px;letter-spacing:2px;opacity:.72}.src{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.src span{font-size:12px;padding:6px 11px;border:1px solid rgba(255,255,255,.25);border-radius:99px;background:rgba(255,255,255,.08)}
.section{margin-top:18px;padding:22px;background:#fff;border:1px solid var(--line);border-radius:18px}.section h2{font-size:19px;color:var(--navy);margin:0}.sub{color:var(--muted);font-size:13px;margin-top:6px;line-height:1.6}
.tabs{display:flex;gap:8px;margin:16px 0 0;flex-wrap:wrap;align-items:center}.lab{font-size:12px;color:var(--muted);margin-right:2px}.tab{border:1px solid var(--line);background:#fff;border-radius:10px;padding:8px 18px;color:#475467;cursor:pointer;font-weight:700;font-size:14px}.tab.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.chk{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:#475467;margin-left:14px;cursor:pointer}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;margin-top:12px;font-size:12px;color:#475467}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-2px}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:14px;margin-top:14px}table{border-collapse:separate;border-spacing:0;width:100%;font-size:12.5px}th{background:#153a5c;color:#fff;text-align:left;padding:10px 12px;position:sticky;top:0;z-index:2;white-space:nowrap}th small{display:block;font-weight:400;opacity:.8;margin-top:2px}td{vertical-align:top;padding:10px 10px;border-bottom:1px solid var(--line);border-right:1px solid #f0f3f7;line-height:1.5}
.tk{position:sticky;left:0;background:#fff;z-index:1;min-width:130px;border-right:2px solid var(--line)!important}.tk b{display:block;color:var(--navy);font-size:14px}.tk .avg{font-size:11.5px;color:#98a2b3;margin-top:4px}
.cell{min-width:215px}.grp{font-size:11px;font-weight:700;color:#475467;margin:6px 0 3px;letter-spacing:.5px}.grp.inc{color:#b54708}.grp.stk{border-top:1px dashed #e4e9f0;padding-top:6px}
.chip{display:inline-block;padding:3px 9px;margin:3px 4px 0 0;border-radius:7px;font-size:12px;line-height:1.35;border:1px solid transparent;font-weight:600;max-width:200px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;vertical-align:top}
.s1{background:#e8f7ef;color:#08783e;border-color:#c6ecd6}.s2{background:#e9f0ff;color:#2457a7;border-color:#cfdcf9}.s3{background:#fff1dd;color:#9a5800;border-color:#f7dfb3}.s4{background:#fff7ed;color:#9a5800;border:1px dashed #e9a23b}.s5{background:#f3eefc;color:#6b3fc0;border-color:#dccdf6}
.more{font-size:11px;color:#2563eb;cursor:pointer;margin-top:4px;display:inline-block}
.note{font-size:12.5px;line-height:1.75;color:#475467;padding:15px;background:#f8fafc;border-radius:12px;margin-top:14px}.note b{color:var(--navy)}
.footer{text-align:center;color:#98a2b3;font-size:11px;padding:20px}
</style></head><body><div class="wrap">
<section class="hero"><div class="eyebrow">Q4 CLOSED-LOOP · INCREMENT × STOCK BY NODE · LITE</div><h1>Q4 闭环：赛道 × 节点 增量机会品 / 存量品 对比表</h1><p>每个单元格先列该链路竞媒在跑、闭环未投放的增量机会品，再列该链路去年 Q4 已跑的存量品。直播与小店（直购）分两个 tab，每条链路独立判定。本版不展示消耗数据，仅看品的分布与机会方向。</p><div class="src"><span>闭环：去年 Q4 by 天数据</span><span>竞媒：抖音 Q4 TOP1500 + 2026.10 月榜</span><span>赛道口径：情报台</span><span>清洁工具 = 物理清洁 + 洗浴工具，化学清洁已剔除</span><span>手霜/足霜等个护类目已删除</span><span>保鲜袋/保鲜膜归收纳用品</span></div></section>

<section class="section"><h2>赛道 × 节点 对比表</h2><div class="sub">默认每格增量品取 TOP 5、存量品取 TOP 6，点“更多”展开全部，或勾选“全部展开”。鼠标悬停可查看品的状态说明。</div>
<div class="tabs"><span class="lab">链路</span><button class="tab active" data-l="live">直播</button><button class="tab" data-l="shop">小店（直购）</button><label class="chk"><input type="checkbox" id="expandAll"> 全部展开</label></div>
<div class="legend"><span><i style="background:#f7dfb3"></i>增量 · 抖音在投，闭环未投放</span><span><i style="background:#fff7ed;border:1px dashed #e9a23b"></i>增量 · 另一链路已跑，可直接复制</span><span><i style="background:#dccdf6"></i>增量 · 10 月榜新增机会品</span><span><i style="background:#c6ecd6"></i>存量 · 抖音也在跑</span><span><i style="background:#cfdcf9"></i>存量 · 闭环独有</span></div>
<div class="table-wrap"><table id="mx"><thead><tr><th class="tk" style="z-index:3">赛道</th><th>①换季启动<small>寒露/霜降 10.01－10.20</small></th><th>②双11<small>含重阳 10.21－11.11</small></th><th>③立冬/小雪<small>保暖峰值 11.12－11.30</small></th><th>④双12/大雪冬至<small>年终收官 12.01－12.22</small></th><th>⑤春节大扫除·年货<small>12.23－1月中</small></th></tr></thead><tbody id="mxb"></tbody></table></div>
<div class="note" id="mxnote"></div></section>
<div class="footer">去年 Q4 闭环 × 抖音 Q4 TOP1500 / 2026.10 月榜 ｜ 情报台赛道口径 ｜ 精简版不含消耗数据</div></div>
<script>
const R=__R__;const OM=__OM__;
const TRACKS=["功效品","清洁工具","收纳用品","厨具","餐具水具","家居家纺","家居工艺品","生活日用其他"];
let L="live";const O=()=>L==="live"?"shop":"live";const LN={live:"直播",shop:"小店"};
function st(r){if(r[L])return r.dy?["存量 · 抖音也在跑","s1",1]:["存量 · 闭环独有","s2",1];
 if(r[L+"_old"])return null;
 if(r.oct_new)return["增量 · 10 月榜新增机会品","s5",2];
 if(r[O()])return["增量 · "+LN[O()]+"链路已跑，可直接复制","s4",2];
 return["增量 · 抖音在投，闭环未投放","s3",2]}
const chip=(r,[nm,cls])=>`<span class="chip ${cls}" title="${nm}｜${r.name}">${r.name}</span>`;
function render(){document.querySelectorAll("[data-l]").forEach(b=>b.classList.toggle("active",b.dataset.l===L));
 const ex=document.getElementById("expandAll").checked;let h="";let cnt={s:0,i:0};
 const PIN=["家居家纺","厨具"];const order=PIN.concat(TRACKS.filter(t=>!PIN.includes(t)&&OM[LN[L]+"|"+t]!==undefined).sort((a,b)=>OM[LN[L]+"|"+b]-OM[LN[L]+"|"+a])).concat(TRACKS.filter(t=>!PIN.includes(t)&&OM[LN[L]+"|"+t]===undefined));
 for(const t of order){h+=`<tr><td class="tk"><b>${t}</b>${OM[LN[L]+"|"+t]===undefined?`<div class="avg">仅竞媒在跑品</div>`:""}</td>`;
  for(let n=1;n<=5;n++){const rs=R.filter(r=>r.track===t&&r.node===n).map(r=>({r,s:st(r)})).filter(x=>x.s);
   const inc=rs.filter(x=>x.s[2]===2).sort((a,b)=>(b.r.oct_rank-a.r.oct_rank)||a.r.name.localeCompare(b.r.name,"zh"));const stock=rs.filter(x=>x.s[2]===1).sort((a,b)=>a.r.name.localeCompare(b.r.name,"zh"));
   cnt.s+=stock.length;cnt.i+=inc.length;
   const lim=(arr,k)=>{if(ex||arr.length<=k)return arr.map(x=>chip(x.r,x.s)).join("");return arr.slice(0,k).map(x=>chip(x.r,x.s)).join("")+`<br><span class="more" onclick="this.outerHTML=this.dataset.rest" data-rest="${arr.slice(k).map(x=>chip(x.r,x.s)).join("").replace(/"/g,'&quot;')}">更多 ${arr.length-k} 个 ▾</span>`};
   h+=`<td class="cell">`;
   if(inc.length)h+=`<div class="grp inc">增量机会 ${inc.length}</div>${lim(inc,5)}`;
   if(stock.length)h+=`<div class="grp ${inc.length?"stk":""}">存量 ${stock.length}</div>${lim(stock,6)}`;
   if(!stock.length&&!inc.length)h+=`<span style="color:#c0c7d2">—</span>`;h+=`</td>`}
  h+=`</tr>`}
 document.getElementById("mxb").innerHTML=h;
 document.getElementById("mxnote").innerHTML=`<b>${LN[L]}链路</b>：增量机会品 ${cnt.i} 个、存量品 ${cnt.s} 个。增量品中虚线框的在${LN[O()]}链路已跑通，是最容易复制投放的一批；紫色为 10 月榜新上榜、去年两边都没跑的真增量；橙色为抖音在投、两条链路都空白。存量品绿色表示抖音也在跑，蓝色为闭环独有心智。`}
document.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>{L=b.dataset.l;render()});document.getElementById("expandAll").onchange=render;
render();
</script></body></html>'''
html = html.replace("__R__", json.dumps(LR, ensure_ascii=False)).replace("__OM__", json.dumps(order_meta, ensure_ascii=False))
open(out + "q4-closed-loop-compare-lite.html", "w", encoding="utf-8").write(html)
print("ok", len(html))
