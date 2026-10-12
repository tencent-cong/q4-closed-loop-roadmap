import pandas as pd, re, json

DAYS = 92
csv_path = "/Users/congjiang/Downloads/通用分析数据集 (44).csv"
dy_path = "/Users/congjiang/Downloads/抖音蝉妈妈-日用百货 25 年Q4数据.xlsx"
map_path = "/Users/congjiang/Downloads/拆商品类目划分赛道明细.xlsx"

d = pd.read_csv(csv_path)
d["s"] = pd.to_numeric(d["消耗(元)"].replace({"~": "0"}), errors="coerce").fillna(0)
d = d[d["商品消费链路"].isin(["直播", "小店"])].copy()
m = pd.read_excel(map_path, sheet_name="最新表").iloc[:8].copy(); m["赛道"] = m["赛道"].ffill()
lk = {}
for _, r in m.iterrows():
    if r["子赛道"] == "其他": continue
    for c in str(r["商品统一类目v2"]).splitlines():
        if c.strip(): lk[c.strip()] = r["子赛道"]
d["track"] = d["类目"].map(lk)
d["leaf"] = d["类目"].str.split("-").str[-1]

def classify(c):
    c = str(c)
    if c.startswith("家居家纺-"): return "家居家纺"
    if any(x in c for x in ["摆件","香薰","线香","装饰画","工艺品","香囊"]): return "家居工艺品"
    if any(x in c for x in ["炒锅","煎锅","平底锅","汤锅","蒸锅","奶锅","炖锅","压力锅","菜刀","砧板","菜板","剪刀","瓜果刀","刨","锅具"]): return "厨具"
    if any(x in c for x in ["餐具","水具","保温杯","保温壶","马克杯","玻璃杯","塑杯","筷子","饭盒","保温桶","茶具","酒杯","碗"]): return "餐具水具"
    if any(x in c for x in ["收纳","衣架","晾晒","置物架","鞋架","压缩袋","防尘罩","挂钩","粘钩","储物"]): return "收纳用品"
    if any(x in c for x in ["清洁","拖把","抹布","垃圾袋","垃圾桶","花洒","马桶","扫把","刷子","粘毛","黏毛","家务手套","除尘掸","洗衣膏"]): return "清洁工具"
    if any(x in c for x in ["艾灸","足贴","眼罩","护腰","护膝","护肩","护颈","暖宝宝","保暖","热水袋","按摩","足浴","泡脚","修脚","护理贴","暖腹","暖手贴","暖脚"]): return "功效品"
    return "其他"

dy = pd.read_excel(dy_path)
dy["track"] = dy["所属类目"].map(classify)
dy["leaf"] = dy["所属类目"].astype(str).str.split("-").str[-1]
dyg = dy.groupby(["track","leaf"]).agg(sku=("商品","size"), idx=("销售额-指数","sum")).reset_index()

def toks(x):
    x = re.sub(r"[（(].*?[)）]", "", str(x))
    out = set()
    for p in re.split(r"[/、 ]", x):
        p = p.strip()
        if len(p) >= 2 and p not in ("其他",): out.add(p)
    return out

def find_csv_spend(track, leaf):
    sub = d[d["track"] == track]
    t = toks(leaf)
    key = leaf.replace("粘毛","黏毛")
    hit = sub[sub["leaf"].apply(lambda l: (l == leaf) or (l == key) or bool(toks(l) & t) or any(k in l for k in t) or any(k in leaf for k in toks(l)))]
    live = hit.loc[hit["商品消费链路"] == "直播", "s"].sum()
    shop = hit.loc[hit["商品消费链路"] == "小店", "s"].sum()
    return live, shop, "；".join(hit.loc[hit.s > 0, "leaf"].drop_duplicates().tolist()[:4])

node_rules = [
 ("换季启动", ["压缩袋","收纳袋","防尘罩","床单","床笠","枕","床品","四件套","艾灸","眼罩","眼贴","肚脐","居家鞋","拖鞋","浴巾","地垫","毛巾","香薰","线香","衣架","收纳箱"]),
 ("双11爆发", ["炒锅","菜刀","砧板","菜板","平底锅","煎锅","刀具","剪刀","拖把","抹布","垃圾袋","清洁刷","花洒","暖宝宝","暖身贴","保暖贴","自发热","暖手","置物架","鞋架","收纳柜","餐具","筷子","玻璃杯","塑杯","马克杯","纤维被","棉花被","化纤被","被子","家务手套"]),
 ("立冬/小雪", ["羽绒被","羊毛被","蚕丝被","毛毯","毛巾被","绒","保暖","热水袋","暖宫","足贴","暖足","护腰","护膝","护肩","护颈","肩颈","骨贴","透骨","黑膏","膏药","保温杯","保温壶","焖烧","汤锅","蒸锅","炖锅","高压锅","压力锅","砂锅","电热毯","坐垫","椅垫"]),
 ("双12/冬至", ["足浴","泡脚","泡澡","按摩","修毛","修剪","剃须","理发","黏毛","粘毛","除尘","玻璃","窗","烘鞋","暖脚","暖手宝","保鲜","汤锅","火锅"]),
 ("年末/春节前置", ["摆件","装饰画","香","节日","礼","扫把","垃圾桶","缝隙","油污","去油","洗衣机清洁","茶具","茶壶","酒杯","锅具套装","刀具套装","床褥","床垫"]),
]
def node_of(leaf):
    for n, kws in node_rules:
        if any(k in leaf for k in kws): return n
    return "双11爆发"

rows = []
for _, r in dyg.iterrows():
    if r["track"] == "其他": continue
    live, shop, matched = find_csv_spend(r["track"], r["leaf"])
    rows.append(dict(赛道=r["track"], 抖音细分类目=r["leaf"], 节点=node_of(r["leaf"]), 抖音SKU=int(r["sku"]), 抖音销售额指数=round(r["idx"],1),
        直播日耗万=round(live/DAYS/1e4,2), 小店日耗万=round(shop/DAYS/1e4,2), 匹配闭环类目=matched))
cross = pd.DataFrame(rows)
cross["直播状态"] = cross["直播日耗万"].apply(lambda v: "闭环有消耗" if v > 0 else "抖音有消耗，闭环未投放")
cross["小店状态"] = cross["小店日耗万"].apply(lambda v: "闭环有消耗" if v > 0 else "抖音有消耗，闭环未投放")
cross = cross.sort_values(["赛道","节点","抖音销售额指数"], ascending=[True,True,False])
cross.to_csv("/Users/congjiang/With/20260923/6fia/q4_track_cross_detail.csv", index=False, encoding="utf-8-sig")

# closed-loop-only leaves with spend (not in Douyin TOP1500)
cl = d[d.track.notna()].groupby(["track","leaf","商品消费链路"])["s"].sum().unstack(fill_value=0).reset_index()
cl["直播日耗万"] = (cl.get("直播",0)/DAYS/1e4).round(2); cl["小店日耗万"] = (cl.get("小店",0)/DAYS/1e4).round(2)
dy_leaf_tokens = {t: set().union(*[toks(l) for l in dyg[dyg.track==t].leaf]) if (dyg.track==t).any() else set() for t in cl.track.unique()}
cl["抖音TOP1500命中"] = cl.apply(lambda r: bool(toks(r["leaf"]) & dy_leaf_tokens.get(r["track"], set())), axis=1)
cl_only = cl[(~cl["抖音TOP1500命中"]) & ((cl["直播日耗万"]>0)|(cl["小店日耗万"]>0))].sort_values(["track","直播日耗万"], ascending=[True,False])
cl_only.to_csv("/Users/congjiang/With/20260923/6fia/q4_closedloop_only_detail.csv", index=False, encoding="utf-8-sig")

tot = d.groupby("商品消费链路")["s"].sum()/DAYS/1e4
print("DAILY_TOTAL_WAN", tot.round(1).to_dict())
tt = d[d.track.notna()].groupby(["track","商品消费链路"])["s"].sum().unstack()/DAYS/1e4
print(tt.round(1))
print("\nSTATUS COUNTS"); print(cross.groupby(["赛道","直播状态"]).size().unstack(fill_value=0)); print(cross.groupby(["赛道","小店状态"]).size().unstack(fill_value=0))
for t, g in cross.groupby("赛道"):
    print("\n####", t)
    print(g[["节点","抖音细分类目","抖音SKU","抖音销售额指数","直播日耗万","小店日耗万","匹配闭环类目"]].to_string(index=False))
print("\n#### closed-loop only (not in TOP1500) top per track")
for t, g in cl_only.groupby("track"):
    print(t, g[["leaf","直播日耗万","小店日耗万"]].head(8).to_string(index=False))
