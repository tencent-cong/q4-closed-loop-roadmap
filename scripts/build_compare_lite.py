import json
out = "/Users/congjiang/With/20260923/6fia/"
R = json.load(open(out + "q4_compare_items.json", encoding="utf-8"))
J = json.load(open(out + "q4_effective_days.json", encoding="utf-8"))
TR = {(r["商品消费链路"], r["track"]): r for r in J["track"]}
# 只保留排序用的整季日均，页面不展示任何消耗数字
order_meta = {f"{l}|{t}": TR[(l, t)]["在跑日耗万"] for l in ["直播", "小店"] for t in ["功效品", "清洁工具", "收纳用品", "厨具", "餐具水具", "家居家纺", "家居工艺品"]}
# 精简数据：去掉所有展示用的消耗字段，仅保留排序键
LR = [dict(track=r["track"], name=r["name"], node=r["node"], dy=int(r["dy_q4"] == 1 or r["dy_oct"] > 0), oct_new=int(r["dy_q4"] == 0 and r["dy_oct"] > 0 and r["live_days"] == 0 and r["shop_days"] == 0),
           live=int(r["live_days"] > 0), shop=int(r["shop_days"] > 0), live_old=int(r["live_old"] > 0), shop_old=int(r["shop_old"] > 0),
           oct_rank=r["dy_oct"], live_rank=r["live_daily"], shop_rank=r["shop_daily"]) for r in R]

html = r'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Q4 闭环 赛道 × 节点 机会地图</title>
<style>
:root{--navy:#102f4f;--ink:#1d2939;--muted:#667085;--line:#e4e9f0;--bg:#f5f7fb}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Arial,sans-serif}
.wrap{max-width:1700px;margin:auto;padding:16px 22px 20px}
.top{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}
.top h1{font-size:22px;margin:0;color:var(--navy)}.top .eyebrow{font-size:11px;letter-spacing:2px;color:#98a2b3;margin-bottom:4px}.top p{margin:6px 0 0;font-size:12.5px;color:var(--muted);line-height:1.6;max-width:900px}
.ctrl{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.tab{border:1px solid var(--line);background:#fff;border-radius:9px;padding:7px 16px;color:#475467;cursor:pointer;font-weight:700;font-size:13px}.tab.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;margin:10px 0 8px;font-size:11.5px;color:#475467}.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.table-wrap{border:1px solid var(--line);border-radius:14px;background:#fff;overflow:auto}table{border-collapse:separate;border-spacing:0;width:100%;table-layout:fixed;font-size:12px}
th{background:#153a5c;color:#fff;text-align:left;padding:8px 10px;white-space:nowrap;font-size:12.5px}th small{display:block;font-weight:400;opacity:.8;margin-top:1px;font-size:11px}th.tk{width:104px}
td{vertical-align:top;padding:7px 8px;border-bottom:1px solid var(--line);border-right:1px solid #f0f3f7;line-height:1.4}tr:last-child td{border-bottom:none}
.tk{background:#fafbfd;border-right:2px solid var(--line)!important}.tk b{display:block;color:var(--navy);font-size:13.5px}.tk .avg{font-size:10.5px;color:#98a2b3;margin-top:3px}
.chip{display:inline-block;padding:2px 7px;margin:2px 3px 0 0;border-radius:6px;font-size:11.5px;line-height:1.35;border:1px solid transparent;font-weight:600;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;vertical-align:top}
.inc{background:#fff4d6;color:#8a5a00;border-color:#e9b949}.stk{background:#eef2f7;color:#3b4a5e;border-color:#dde3ec;font-weight:550}
.sep{display:block;height:0;margin:3px 0 1px;border-top:1px dashed #e4e9f0}
.empty{color:#c0c7d2}
.note{font-size:11.5px;line-height:1.6;color:#667085;margin-top:8px}.note b{color:var(--navy)}
</style></head><body><div class="wrap">
<div class="top"><div><div class="eyebrow">Q4 CLOSED-LOOP · OPPORTUNITY MAP</div><h1>Q4 闭环：赛道 × 节点 机会地图</h1><p>每格上半部分为新增机会品（抖音在投、闭环未投放），下半部分为去年已跑爆品；每格最多 7 个。</p></div>
<div class="ctrl"><button class="tab active" data-l="live">直播</button><button class="tab" data-l="shop">小店（直购）</button></div></div>
<div class="legend"><span><i style="background:#fff4d6;border:1px solid #e9b949"></i>新增机会品</span><span><i style="background:#eef2f7;border:1px solid #dde3ec"></i>去年已跑爆品</span></div>
<div class="table-wrap"><table id="mx"><thead><tr><th class="tk">赛道</th><th>① 换季启动<small>寒露/霜降 10.01－10.20</small></th><th>② 双11<small>含重阳 10.21－11.11</small></th><th>③ 立冬/小雪<small>保暖峰值 11.12－11.30</small></th><th>④ 双12/大雪冬至<small>年终收官 12.01－12.22</small></th><th>⑤ 春节大扫除·年货<small>12.23－1月中</small></th></tr></thead><tbody id="mxb"></tbody></table></div>
<div class="note" id="mxnote"></div></div>
<script>
const R=__R__;const OM=__OM__;const CAP=7,INC_MAX=4;
const TRACKS=["功效品","清洁工具","收纳用品","厨具","餐具水具","家居家纺","家居工艺品","生活日用其他"];
let L="live";const O=()=>L==="live"?"shop":"live";const LN={live:"直播",shop:"小店"};
function st(r){if(r[L])return["去年已跑爆品","stk",1];
 if(r[L+"_old"])return null;
 return["新增机会品","inc",2]}
const chip=(r,[nm,cls])=>`<span class="chip ${cls}" title="${nm}｜${r.name}">${r.name}</span>`;
function render(){document.querySelectorAll("[data-l]").forEach(b=>b.classList.toggle("active",b.dataset.l===L));
 let h="";let cnt={s:0,i:0,si:0,ss:0};
 const PIN=["家居家纺","厨具"];const order=PIN.concat(TRACKS.filter(t=>!PIN.includes(t)&&OM[LN[L]+"|"+t]!==undefined).sort((a,b)=>OM[LN[L]+"|"+b]-OM[LN[L]+"|"+a])).concat(TRACKS.filter(t=>!PIN.includes(t)&&OM[LN[L]+"|"+t]===undefined));
 for(const t of order){h+=`<tr><td class="tk"><b>${t}</b>${OM[LN[L]+"|"+t]===undefined?`<div class="avg">仅竞媒在跑品</div>`:""}</td>`;
  for(let n=1;n<=5;n++){const rs=R.filter(r=>r.track===t&&r.node===n).map(r=>({r,s:st(r)})).filter(x=>x.s);
   const inc=rs.filter(x=>x.s[2]===2).sort((a,b)=>(b.r.oct_rank-a.r.oct_rank)||(b.r[O()+"_rank"]-a.r[O()+"_rank"]));const stock=rs.filter(x=>x.s[2]===1).sort((a,b)=>b.r[L+"_rank"]-a.r[L+"_rank"]);
   cnt.i+=inc.length;cnt.s+=stock.length;
   const nInc=Math.min(inc.length,Math.max(INC_MAX,CAP-stock.length));const nStk=Math.min(stock.length,CAP-nInc);
   const si=inc.slice(0,nInc),ss=stock.slice(0,nStk);cnt.si+=si.length;cnt.ss+=ss.length;
   h+=`<td>`;
   if(si.length)h+=si.map(x=>chip(x.r,x.s)).join("");
   if(si.length&&ss.length)h+=`<span class="sep"></span>`;
   if(ss.length)h+=ss.map(x=>chip(x.r,x.s)).join("");
   if(!si.length&&!ss.length)h+=`<span class="empty">—</span>`;h+=`</td>`}
  h+=`</tr>`}
 document.getElementById("mxb").innerHTML=h;
 document.getElementById("mxnote").innerHTML=`<b>${LN[L]}链路</b>：新增机会品 ${cnt.i} 个，去年已跑爆品 ${cnt.s} 个，每格最多展示 7 个 TOP 项。新增机会品 = 抖音在投、${LN[L]}链路未投放的品；去年已跑爆品 = ${LN[L]}链路去年 Q4 有有效消耗的品。完整清单见原版对比表。`}
document.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>{L=b.dataset.l;render()});
render();
</script></body></html>'''
html = html.replace("__R__", json.dumps(LR, ensure_ascii=False)).replace("__OM__", json.dumps(order_meta, ensure_ascii=False))
open(out + "q4-closed-loop-compare-lite.html", "w", encoding="utf-8").write(html)
print("ok", len(html))
