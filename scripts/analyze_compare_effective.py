import pandas as pd, numpy as np, re, json

TH = 2000
csv_path = "/Users/congjiang/Downloads/通用分析数据集 (45).csv"
map_path = "/Users/congjiang/Downloads/拆商品类目划分赛道明细.xlsx"
out = "/Users/congjiang/With/20260923/6fia/"

# 1. 上一版对比表的品清单（含节点、抖音Q4命中、10月榜指数）
s = open(out + "q4-closed-loop-compare.html", encoding="utf-8").read()
m = re.search(r"const D=(\[.*?\]);", s, re.S)
D = json.loads(m.group(1))
items = pd.DataFrame(D, columns=["track", "name", "node", "live_old", "shop_old", "dy_q4", "dy_oct"])
print("items", len(items), items.track.value_counts().to_dict())

# 2. by 天闭环数据
d = pd.read_csv(csv_path, usecols=["类目", "时间", "商品消费链路", "消耗(元)"])
d = d[d["时间"].notna() & d["商品消费链路"].isin(["直播", "小店"])].copy()
d["s"] = pd.to_numeric(d["消耗(元)"].replace({"~": "0"}), errors="coerce").fillna(0)
d["dt"] = pd.to_datetime(d["时间"], format="%Y/%m/%d")
mp = pd.read_excel(map_path, sheet_name="最新表").iloc[:8].copy(); mp["赛道"] = mp["赛道"].ffill()
lk = {}
for _, r in mp.iterrows():
    if r["子赛道"] == "其他": continue
    for c in str(r["商品统一类目v2"]).splitlines():
        if c.strip(): lk[c.strip()] = r["子赛道"]
d["track"] = d["类目"].map(lk)
from track_rules import is_chem, CHEM_ITEMS
d.loc[(d.track == "清洁工具") & d["类目"].map(is_chem), "track"] = None
items = items[~items.name.isin(CHEM_ITEMS)].copy()
from track_rules import apply_overrides, ITEM_TRACK_OVERRIDE, DROP_ITEMS
d["track"] = [apply_overrides(t, c) if isinstance(t, str) else t for t, c in zip(d.track, d["类目"])]
items = items[~items.name.isin(DROP_ITEMS)].copy()
items["track"] = [ITEM_TRACK_OVERRIDE.get(n, t) for n, t in zip(items.name, items.track)]
print("items after chem removal", len(items))
d["leaf"] = d["类目"].str.split("-").str[-1]
d = d[d.track.notna()]

def toks(x):
    x = re.sub(r"[（(].*?[)）]", "", str(x))
    o = set()
    for p in re.split(r"[/、 ]", x):
        p = p.strip()
        if len(p) >= 2 and p != "其他": o.add(p)
    return o

leaf_by_track = {t: g.leaf.drop_duplicates().tolist() for t, g in d.groupby("track")}
def match_leaves(track, name):
    t = toks(name); key = name.replace("粘毛", "黏毛"); t |= toks(key)
    exact, loose = [], []
    for l in leaf_by_track.get(track, []):
        lt = toks(l)
        if l == name or l == key or (lt & t): exact.append(l)
        elif any(k in l for k in t) or any(k in name for k in lt): loose.append(l)
    return exact, loose

# 第一遍：精确归属；第二遍：宽松匹配不抢占其他品已精确命中的类目
exact_map, loose_map, claimed = {}, {}, {}
for r in items.itertuples():
    e, lo = match_leaves(r.track, r.name); exact_map[(r.track, r.name)] = e; loose_map[(r.track, r.name)] = lo
    for l in e: claimed.setdefault((r.track, l), set()).add(r.name)
def final_leaves(track, name):
    e = exact_map[(track, name)]
    lo = [l for l in loose_map[(track, name)] if (track, l) not in claimed]
    return e + lo

nodes = [("①", "2025-10-01", "2025-10-20"), ("②", "2025-10-21", "2025-11-11"), ("③", "2025-11-12", "2025-11-30"), ("④", "2025-12-01", "2025-12-22"), ("⑤", "2025-12-23", "2025-12-31")]
def node_of(dt):
    for n, a, b in nodes:
        if pd.Timestamp(a) <= dt <= pd.Timestamp(b): return n
d["nd"] = d.dt.map(node_of)

def eff(sub):
    if len(sub) == 0: return dict(days=0, daily=0.0, a="", b="", peak=0.0, nd="")
    g = sub.groupby("dt").s.sum()
    e = g[g >= TH]
    if len(e) == 0: return dict(days=0, daily=0.0, a="", b="", peak=round(g.max() / 1e4, 2), nd="")
    ndd = sub[sub.dt.isin(e.index)].groupby("nd").s.sum(); ndd = (ndd / ndd.sum() * 100).round(0).astype(int)
    return dict(days=int(len(e)), daily=round(e.mean() / 1e4, 2), a=e.index.min().strftime("%m.%d"), b=e.index.max().strftime("%m.%d"), peak=round(g.max() / 1e4, 2), nd="/".join(f"{k}{v}%" for k, v in ndd.items() if v > 0))

rows = []
for r in items.itertuples():
    ls = final_leaves(r.track, r.name)
    sub = d[(d.track == r.track) & (d.leaf.isin(ls))]
    live = eff(sub[sub["商品消费链路"] == "直播"]); shop = eff(sub[sub["商品消费链路"] == "小店"])
    rows.append(dict(track=r.track, name=r.name, node=int(r.node), dy_q4=int(r.dy_q4), dy_oct=float(r.dy_oct), matched="；".join(ls[:4]), n_leaf=len(ls),
                     live_days=live["days"], live_daily=live["daily"], live_a=live["a"], live_b=live["b"], live_peak=live["peak"], live_nd=live["nd"],
                     shop_days=shop["days"], shop_daily=shop["daily"], shop_a=shop["a"], shop_b=shop["b"], shop_peak=shop["peak"], shop_nd=shop["nd"],
                     live_old=r.live_old, shop_old=r.shop_old))
R = pd.DataFrame(rows)
# 口径一致性检查：上一版有消耗但按天匹配不到的
chk = R[((R.live_old > 0) & (R.live_days == 0)) | ((R.shop_old > 0) & (R.shop_days == 0))]
print("old>0 but no effective day:", len(chk)); print(chk[["track", "name", "live_old", "live_days", "live_peak", "shop_old", "shop_days", "shop_peak", "matched"]].to_string(index=False))
print("new>0 but old==0:", len(R[((R.live_old == 0) & (R.live_days > 0)) | ((R.shop_old == 0) & (R.shop_days > 0))]))

def status(link, r):
    days = r[f"{link}_days"]; other = "shop" if link == "live" else "live"; dy = (r.dy_q4 == 1) or (r.dy_oct > 0)
    if days > 0: return "存量·抖音也在跑" if dy else "存量·闭环独有"
    if r.dy_q4 == 0 and r.dy_oct > 0 and r.live_days == 0 and r.shop_days == 0: return "增量·10月榜新增"
    if r[f"{other}_days"] > 0: return "增量·另一链路已跑"
    return "增量·抖音在投闭环未投"
R["live_status"] = R.apply(lambda r: status("live", r), axis=1); R["shop_status"] = R.apply(lambda r: status("shop", r), axis=1)
R = R.sort_values(["track", "node", "live_daily"], ascending=[True, True, False])
R.to_csv(out + "q4_compare_items_effective.csv", index=False, encoding="utf-8-sig")
print(R.groupby(["track", "live_status"]).size().unstack(fill_value=0)); print(R.groupby(["track", "shop_status"]).size().unstack(fill_value=0))
json.dump(R.to_dict(orient="records"), open(out + "q4_compare_items.json", "w", encoding="utf-8"), ensure_ascii=False)
