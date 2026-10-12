import json
J = json.load(open("/Users/congjiang/With/20260923/6fia/q4_effective_days.json", encoding="utf-8"))
html = r'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Q4 闭环类目有效跑量周期与在跑日耗</title>
<style>
:root{--navy:#102f4f;--ink:#1d2939;--muted:#667085;--line:#e4e9f0;--bg:#f5f7fb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Arial,sans-serif}.wrap{max-width:1560px;margin:auto;padding:26px}
.hero{border-radius:22px;padding:34px 40px;color:#fff;background:linear-gradient(120deg,#0e2945,#155a8c 60%,#2775d8)}.hero h1{font-size:29px;margin:8px 0}.hero p{max-width:1080px;color:#dbeafe;line-height:1.75;margin:0}.eyebrow{font-size:12px;letter-spacing:2px;opacity:.72}.src{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.src span{font-size:12px;padding:6px 11px;border:1px solid rgba(255,255,255,.25);border-radius:99px;background:rgba(255,255,255,.08)}
.section{margin-top:18px;padding:22px;background:#fff;border:1px solid var(--line);border-radius:18px}.section h2{font-size:19px;color:var(--navy);margin:0}.sub{color:var(--muted);font-size:13px;margin-top:6px;line-height:1.6}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}.card{padding:16px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(180deg,#fff,#f9fbfe)}.card .k{font-size:12px;color:var(--muted)}.card .v{font-size:24px;color:var(--navy);font-weight:750;margin:6px 0 3px}.card .n{font-size:12px;color:var(--muted);line-height:1.5}
.tabs{display:flex;gap:8px;margin:16px 0 0;flex-wrap:wrap;align-items:center}.tabs .lab{font-size:12px;color:var(--muted);margin-right:4px}.tab{border:1px solid var(--line);background:#fff;border-radius:10px;padding:7px 14px;color:#475467;cursor:pointer;font-weight:650;font-size:13px}.tab.active{background:var(--navy);color:#fff;border-color:var(--navy)}.tab.sm{padding:5px 10px;font-size:12px;font-weight:550}.tab.sm.active{background:#2563eb;border-color:#2563eb}
.chk{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:#475467;margin-left:14px;cursor:pointer}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:14px;margin-top:14px}table{border-collapse:separate;border-spacing:0;width:100%;font-size:12.5px}th{background:#153a5c;color:#fff;text-align:left;padding:10px 12px;position:sticky;top:0;z-index:2;white-space:nowrap;cursor:pointer;user-select:none}th small{display:block;font-weight:400;opacity:.8;margin-top:2px}td{vertical-align:middle;padding:9px 12px;border-bottom:1px solid var(--line);line-height:1.45;white-space:nowrap}tr:hover td{background:#f8fbff}.num{text-align:right;font-variant-numeric:tabular-nums}
.tl{position:relative;width:260px;height:14px;background:#eef2f7;border-radius:4px;overflow:hidden}.tl i{position:absolute;top:0;height:100%;background:#2563eb;opacity:.85}.tl .pk{position:absolute;top:0;width:2px;height:100%;background:#d92d20}.tl .nd{position:absolute;top:0;height:100%;border-left:1px dashed rgba(16,47,79,.35)}
.tag{display:inline-block;padding:3px 7px;border-radius:6px;font-size:11px;font-weight:650}.t1{background:#e8f7ef;color:#08783e}.t2{background:#e9f0ff;color:#2457a7}.t3{background:#fff1dd;color:#9a5800}.t4{background:#f2f4f7;color:#667085}
.svgbox{margin-top:14px;border:1px solid var(--line);border-radius:14px;padding:12px;background:#fafcff}
.ntab{width:100%;min-width:900px}.ntab td,.ntab th{text-align:right}.ntab td:first-child,.ntab th:first-child{text-align:left}.hi{background:#edf5ff!important;font-weight:700;color:var(--navy)}
.note{font-size:12.5px;line-height:1.75;color:#475467;padding:15px;background:#f8fafc;border-radius:12px;margin-top:14px}.note b{color:var(--navy)}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}.co{border:1px solid #d5e4fa;background:#f1f7ff;border-radius:14px;padding:17px}.co.o{border-color:#f5d6a3;background:#fff8eb}.co.p{border-color:#cdbcf3;background:#f7f3ff}.co h3{margin:0 0 8px;color:var(--navy);font-size:15px}.co ul{margin:0;padding-left:18px;color:#475467;font-size:13px;line-height:1.75}
.footer{text-align:center;color:#98a2b3;font-size:11px;padding:20px}
@media(max-width:900px){.wrap{padding:12px}.cards,.grid3{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<section class="hero"><div class="eyebrow">Q4 CLOSED-LOOP · EFFECTIVE RUNNING DAYS</div><h1>Q4 闭环类目：有效跑量周期 × 在跑日耗</h1><p>整季平均会把只跑了两周的品摊薄到 92 天，看不出真实规模。本页改用按天数据：一个类目当天消耗 ≥ 2000 元记为一个“有效日”，只统计有效日的天数、首末日和期间日均消耗，一天都没达到 2000 元的类目直接剔除。</p><div class="src"><span>数据：去年 Q4 闭环 by 天（10.01－12.31，92 天）</span><span>链路：直播 + 小店</span><span>有效日阈值：≥ 2000 元/天</span><span>赛道口径：情报台</span></div></section>

<section class="section"><h2>口径与大盘</h2><div class="sub">剔除后保留 452 个类目×链路（直播 192、小店 260），覆盖映射赛道消耗的 99.1%；剔除 876 个类目×链路，合计仅 169.6 万元。</div>
<div class="cards"><div class="card"><div class="k">有效天数</div><div class="v">天</div><div class="n">该类目当日消耗 ≥ 2000 元的天数，衡量跑量持续性</div></div><div class="card"><div class="k">在跑日耗</div><div class="v">万/天</div><div class="n">仅对有效日取平均，代表类目“跑起来时”的真实规模</div></div><div class="card"><div class="k">跨度 / 连续性</div><div class="v">首末日</div><div class="n">首个到末个有效日的日历天数，连续性 = 有效天数 ÷ 跨度</div></div><div class="card"><div class="k">跑量形态</div><div class="v">4 档</div><div class="n">常青 ≥ 75 天；阶段性 14～74 天；短波 4～13 天；脉冲 ≤ 3 天</div></div></div>
<div class="svgbox" id="dailySvg"></div>
<div class="table-wrap"><table class="ntab"><thead><tr><th style="cursor:default">链路 / 节点日耗（万/天）</th><th style="cursor:default">①换季启动<small>10.01－10.20</small></th><th style="cursor:default">②双11<small>10.21－11.11</small></th><th style="cursor:default">③立冬小雪<small>11.12－11.30</small></th><th style="cursor:default">④双12冬至<small>12.01－12.22</small></th><th style="cursor:default">⑤年末<small>12.23－12.31</small></th><th style="cursor:default">整季日均</th></tr></thead><tbody>
<tr><td>直播 合计</td><td>173.7</td><td class="hi">177.5</td><td>163.8</td><td>156.1</td><td>142.5</td><td>165.3</td></tr>
<tr><td>小店 合计</td><td>33.5</td><td>44.4</td><td>54.0</td><td>73.2</td><td class="hi">86.3</td><td>55.0</td></tr></tbody></table></div>
<div class="note"><b>大盘信号。</b>直播在双11 见顶后逐节点回落，年末只有 142.5 万/天；小店则一路爬升，年末 86.3 万/天是 10 月初的 2.6 倍，增量来自清洁工具（2.0 → 16.7，物理清洁口径）、家居工艺品（6.6 → 21.5）和餐具水具（8.6 → 16.3）。两条链路节奏相反，说明直播缺 12 月接棒品，小店缺 10 月启动品。</div></section>

<section class="section"><h2>赛道级：节点日耗与有效周期</h2><div class="sub">赛道日耗按节点内日均计算。每个赛道全季 92 天都有 ≥ 2000 元消耗，所以赛道层面的差异体现在节点节奏，而非天数。</div>
<div class="tabs"><span class="lab">链路</span><button class="tab active" data-l="直播" onclick="setTL('直播')">直播</button><button class="tab" data-l="小店" onclick="setTL('小店')">小店</button></div>
<div class="table-wrap"><table class="ntab" id="trackTab"></table></div></section>

<section class="section"><h2>类目明细：有效跑量周期与在跑日耗</h2><div class="sub">点击表头可排序。时间轴为 10.01－12.31，蓝色为有效日所在区间（按首末日绘制，深浅不代表密度），红线为峰值日，虚线为五个节点分界。</div>
<div class="tabs"><span class="lab">链路</span><button class="tab active" data-g="l" data-v="直播">直播</button><button class="tab" data-g="l" data-v="小店">小店</button><span class="lab" style="margin-left:14px">赛道</span><span id="trackBtns"></span><label class="chk"><input type="checkbox" id="hidePulse" checked> 隐藏脉冲（≤3 天）</label><label class="chk"><input type="checkbox" id="onlyTop"> 只看在跑日耗 ≥ 1 万</label></div>
<div class="table-wrap"><table id="detail"><thead><tr><th data-k="track">赛道</th><th data-k="leaf">类目</th><th data-k="shape">形态</th><th data-k="days" class="num">有效天数</th><th data-k="span" class="num">跨度</th><th data-k="cont" class="num">连续性</th><th data-k="daily" class="num">在跑日耗<small>万/天</small></th><th data-k="peak" class="num">峰值日耗<small>万/天 · 日期</small></th><th data-k="a">有效区间</th><th>时间轴 10.01 ─ 12.31</th><th data-k="tot" class="num">Q4 累计<small>万元</small></th><th>有效消耗节点分布</th></tr></thead><tbody id="dtb"></tbody></table></div>
<div class="note" id="cnt"></div></section>

<section class="section"><h2>重点结论</h2><div class="grid3">
<div class="co"><h3>直播：常青品撑盘，但不少高日耗品其实只跑了两周</h3><ul><li>常青（≥75 天）且在跑日耗 ≥ 2 万的只有 13 个：炒锅 28.6、床单 12.4、拖把 8.0、足浴桶 4.6（已归清洁工具）、床品套件 7.5、菜刀 6.7、枕芯 5.6、高压锅 3.9、记忆棉枕 3.7、纤维被 3.6、睡袋 3.1、运动护腰 3.1、剪刀 3.0、羽绒被 3.0。</li><li>被整季平均严重低估的阶段品：艾灸贴 12.19－12.31 共 13 天、在跑 4.9 万/天（整季均值仅 0.7）；发热保暖护具 10.01－10.20 共 20 天、3.3 万/天；暖宫贴 10.20－11.02 共 14 天、2.4 万/天；锅盖 10 月 23 天、3.2 万/天。</li><li>这些品说明直播存在明确的“节点窗口”，Road Map 上应按首末日而非整季排布。</li></ul></div>
<div class="co o"><h3>小店：12 月才起量，年末清洁与礼赠是真实爆点</h3><ul><li>常青品只有装饰摆件 4.7、保温杯 4.1、线香 2.5、装饰画 2.6、菜刀 2.2、炒锅 1.7 万/天，其余多为 12 月集中起量。</li><li>12 月清洁脉冲明显：拖把配件 12.17 起 15 天、6.3 万/天；拖把 12 月 54%+33% 的消耗在④⑤；垃圾袋峰值 12.20 达 19.7 万；卫生间用刷 12.16 起 14 天、1.4 万/天。春节大扫除节点在小店侧已被数据验证。</li><li>礼赠在 12 月中旬爆发：装饰摆件、装饰画 12.15 同日峰值 15.7 / 13.2 万，台历 12.19 起 13 天 1.4 万/天，喜字剪纸 12.21 起，冰箱贴 12.01 起。</li></ul></div>
<div class="co p"><h3>对 Road Map 的修正建议</h3><ul><li>功效品直播窗口清晰：①发热护具、③④眼罩（48 天，峰值 12.04）、⑤艾灸贴，暖宫贴卡在双11 前两周。今年可按此窗口提前 10 天起量。</li><li>家纺直播全部常青但权重前移：床单 36%、床褥 37%、记忆棉枕 39% 的消耗落在①换季启动，羽绒被 42% 在双11，枕芯 57% 在④双12冬至，说明被芯→枕头有明确的接力顺序。</li><li>小店 10－11 月是空档：功效品①仅 1.4 万/天、收纳①仅 1.7 万/天。直播在①已跑通的发热护具、黏毛器（52% 消耗在①）、床褥、衣物收纳箱可直接前置复制到小店。</li></ul></div></div></section>
<div class="footer">去年 Q4 闭环 by 天数据（10.01－12.31）× 情报台赛道口径 ｜ 有效日阈值 2000 元/天 ｜ 清洁工具 = 物理清洁 + 洗浴工具（泡脚桶/沐浴桶/搓澡），化学清洁已剔除 ｜ 手霜/足霜等个护类目已删除 ｜ 保鲜袋/保鲜膜归收纳用品</div></div>
<script>
const J=__JSON__;
const NODES=[["①换季启动","10.01","10.20",20],["②双11","10.21","11.11",22],["③立冬小雪","11.12","11.30",19],["④双12冬至","12.01","12.22",22],["⑤年末","12.23","12.31",9]];
const DAYS=Object.keys(J.daily["直播"]); const di=d=>DAYS.indexOf(d);
function shape(d){return d>=75?["常青","t1"]:d>=14?["阶段性","t2"]:d>=4?["短波","t3"]:["脉冲","t4"]}
// daily svg
(function(){const W=1480,H=190,P=40;const L=J.daily["直播"],S=J.daily["小店"];const mx=Math.max(...Object.values(L));const x=i=>P+i*(W-2*P)/91,y=v=>H-24-(v/mx)*(H-50);
let s=`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto"><text x="${P}" y="14" font-size="12" fill="#102f4f" font-weight="700">大盘日消耗（万/天）　<tspan fill="#2563eb">● 直播</tspan>　<tspan fill="#f59e0b">● 小店</tspan></text>`;
let cum=0;NODES.forEach((n,k)=>{const a=cum;cum+=n[3];s+=`<rect x="${x(a)}" y="22" width="${x(cum)-x(a)}" height="${H-46}" fill="${k%2?'#f1f5fa':'#fff'}"/><text x="${(x(a)+x(cum))/2}" y="${H-6}" font-size="11" fill="#667085" text-anchor="middle">${n[0]} ${n[1]}－${n[2]}</text>`});
const path=(o,c)=>`<polyline fill="none" stroke="${c}" stroke-width="2" points="${DAYS.map((d,i)=>x(i)+','+y(o[d])).join(' ')}"/>`;
s+=path(L,'#2563eb')+path(S,'#f59e0b');
[0,100,200].forEach(v=>{if(v<=mx)s+=`<text x="${P-6}" y="${y(v)+4}" font-size="10" fill="#98a2b3" text-anchor="end">${v}</text>`});
s+=`</svg>`;document.getElementById("dailySvg").innerHTML=s})();
// track table
function setTL(l){document.querySelectorAll("[data-l]").forEach(b=>b.classList.toggle("active",b.dataset.l===l));
 const PIN=["家居家纺","厨具"];const rows=J.track.filter(r=>r["商品消费链路"]===l).sort((a,b)=>{const pa=PIN.indexOf(a.track),pb=PIN.indexOf(b.track);if(pa!==pb)return(pa<0?9:pa)-(pb<0?9:pb);return b["在跑日耗万"]-a["在跑日耗万"]});
 let h=`<thead><tr><th style="cursor:default">赛道</th><th style="cursor:default">整季日均</th>${NODES.map(n=>`<th style="cursor:default">${n[0]}</th>`).join("")}<th style="cursor:default">峰值日耗 · 日期</th><th style="cursor:default">常青类目数</th><th style="cursor:default">阶段/短波数</th><th style="cursor:default">脉冲数</th></tr></thead><tbody>`;
 rows.forEach(r=>{const tn=J.track_node.find(x=>x["商品消费链路"]===l&&x.track===r.track);const vals=NODES.map(n=>tn[n[0]]);const m=Math.max(...vals);const it=(J.items[l]||{})[r.track]||[];const c1=it.filter(i=>i.days>=75).length,c2=it.filter(i=>i.days>=4&&i.days<75).length,c3=it.filter(i=>i.days<=3).length;
  h+=`<tr><td>${r.track}</td><td>${r["在跑日耗万"].toFixed(1)}</td>${vals.map(v=>`<td class="${v===m?'hi':''}">${v.toFixed(1)}</td>`).join("")}<td>${r["峰值日耗万"]} · ${r["峰值日"]}</td><td>${c1}</td><td>${c2}</td><td>${c3}</td></tr>`});
 document.getElementById("trackTab").innerHTML=h+"</tbody>"}
setTL("直播");
// detail
let L="直播",T="全部",sortK="daily",sortD=-1;
const TRACKS=["功效品","清洁工具","收纳用品","厨具","餐具水具","家居家纺","家居工艺品"];
document.getElementById("trackBtns").innerHTML=["全部",...TRACKS].map(t=>`<button class="tab sm ${t==="全部"?"active":""}" data-g="t" data-v="${t}">${t}</button>`).join("");
document.querySelectorAll(".tab[data-g]").forEach(b=>b.onclick=()=>{document.querySelectorAll(`.tab[data-g=${b.dataset.g}]`).forEach(x=>x.classList.remove("active"));b.classList.add("active");if(b.dataset.g==="l")L=b.dataset.v;else T=b.dataset.v;render()});
document.getElementById("hidePulse").onchange=render;document.getElementById("onlyTop").onchange=render;
document.querySelectorAll("#detail th[data-k]").forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sortK===k)sortD*=-1;else{sortK=k;sortD=(k==="track"||k==="leaf"||k==="shape"||k==="a")?1:-1}render()});
function tl(it){const a=di(it.a),b=di(it.b),p=di(it.peakd);let s=`<div class="tl">`;let c=0;NODES.slice(0,4).forEach(n=>{c+=n[3];s+=`<span class="nd" style="left:${c/92*100}%"></span>`});s+=`<i style="left:${a/92*100}%;width:${Math.max((b-a+1)/92*100,1.2)}%"></i><span class="pk" style="left:${p/92*100}%"></span></div>`;return s}
function render(){
 const hp=document.getElementById("hidePulse").checked,ot=document.getElementById("onlyTop").checked;
 let rows=[];for(const t of TRACKS){if(T!=="全部"&&t!==T)continue;((J.items[L]||{})[t]||[]).forEach(i=>rows.push({...i,track:t,cont:+(i.days/i.span).toFixed(2),shape:shape(i.days)[0]}))}
 const total=rows.length;if(hp)rows=rows.filter(r=>r.days>3);if(ot)rows=rows.filter(r=>r.daily>=1);
 rows.sort((x,y)=>{const a=x[sortK],b=y[sortK];return (typeof a==="string"?a.localeCompare(b,"zh"):a-b)*sortD});
 document.getElementById("dtb").innerHTML=rows.map(r=>{const [sn,sc]=shape(r.days);return `<tr><td>${r.track}</td><td><b>${r.leaf}</b></td><td><span class="tag ${sc}">${sn}</span></td><td class="num">${r.days}</td><td class="num">${r.span}</td><td class="num">${r.cont.toFixed(2)}</td><td class="num"><b>${r.daily.toFixed(2)}</b></td><td class="num">${r.peak.toFixed(2)} · ${r.peakd}</td><td>${r.a} － ${r.b}</td><td>${tl(r)}</td><td class="num">${r.tot.toFixed(1)}</td><td style="white-space:normal;max-width:300px;font-size:11.5px;color:#667085">${r.nd}</td></tr>`}).join("");
 document.getElementById("cnt").innerHTML=`<b>${L} · ${T}</b>：显示 ${rows.length} / ${total} 个类目。在跑日耗为有效日均值，与整季平均（累计 ÷ 92）相比，阶段性与短波类目会明显放大，这才是该品在跑期间的真实量级；累计列可用于核对整季贡献。`}
render();
</script></body></html>'''
open("/Users/congjiang/With/20260923/6fia/q4-closed-loop-effective-days.html","w",encoding="utf-8").write(html.replace("__JSON__",json.dumps(J,ensure_ascii=False)))
print("ok")
