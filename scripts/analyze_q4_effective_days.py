import pandas as pd, numpy as np, re, json

TH = 2000  # 有效消耗日阈值：元/天
csv_path = "/Users/congjiang/Downloads/通用分析数据集 (45).csv"
map_path = "/Users/congjiang/Downloads/拆商品类目划分赛道明细.xlsx"
out_dir = "/Users/congjiang/With/20260923/6fia/"

d = pd.read_csv(csv_path, usecols=["类目", "时间", "商品消费链路", "消耗(元)"])
d = d[d["时间"].notna() & d["商品消费链路"].isin(["直播", "小店"])].copy()
d["s"] = pd.to_numeric(d["消耗(元)"].replace({"~": "0"}), errors="coerce").fillna(0)
d["dt"] = pd.to_datetime(d["时间"], format="%Y/%m/%d")

m = pd.read_excel(map_path, sheet_name="最新表").iloc[:8].copy(); m["赛道"] = m["赛道"].ffill()
lk = {}
for _, r in m.iterrows():
    if r["子赛道"] == "其他": continue
    for c in str(r["商品统一类目v2"]).splitlines():
        if c.strip(): lk[c.strip()] = r["子赛道"]
d["track"] = d["类目"].map(lk)
from track_rules import is_chem
chem_mask = (d.track == "清洁工具") & d["类目"].map(is_chem)
print("chem excluded from 清洁工具: wan", round(d[chem_mask].s.sum() / 1e4, 1), d[chem_mask].groupby("商品消费链路").s.sum().div(1e4).round(1).to_dict())
d.loc[chem_mask, "track"] = None
from track_rules import apply_overrides
d["track"] = [apply_overrides(t, c) if isinstance(t, str) else t for t, c in zip(d.track, d["类目"])]
d["track"] = d["track"].where(d["track"].notna(), None)
d["leaf"] = d["类目"].str.split("-").str[-1]

# 日历校验
print("date range", d.dt.min().date(), d.dt.max().date(), d.dt.nunique())
print("total yuan", round(d.s.sum()), d.groupby("商品消费链路").s.sum().round().to_dict())

# 节点定义（不重叠）
nodes = [("①换季启动", "2025-10-01", "2025-10-20"), ("②双11", "2025-10-21", "2025-11-11"),
         ("③立冬小雪", "2025-11-12", "2025-11-30"), ("④双12冬至", "2025-12-01", "2025-12-22"), ("⑤年末", "2025-12-23", "2025-12-31")]
def node_of(dt):
    for n, a, b in nodes:
        if pd.Timestamp(a) <= dt <= pd.Timestamp(b): return n
    return "?"
d["node"] = d.dt.map(node_of)

# 大盘按天
daily = d.groupby(["商品消费链路", "dt"]).s.sum().unstack(0).fillna(0)
daily_track = d[d.track.notna()].groupby(["商品消费链路", "track", "dt"]).s.sum()

# 类目 × 链路 有效日统计
def stats(g):
    g = g.sort_values("dt")
    eff = g[g.s >= TH]
    if len(eff) == 0:
        return pd.Series(dict(总消耗=g.s.sum(), 有消耗天数=int((g.s > 0).sum()), 有效天数=0, 在跑日耗=0.0, 首日=None, 末日=None, 跨度=0, 峰值日耗=g.s.max(), 峰值日=g.loc[g.s.idxmax(), "dt"] if g.s.max() > 0 else None, 节点分布=""))
    span = (eff.dt.max() - eff.dt.min()).days + 1
    nd = eff.groupby("node").s.sum(); nd = (nd / nd.sum() * 100).round(0).astype(int)
    return pd.Series(dict(总消耗=g.s.sum(), 有消耗天数=int((g.s > 0).sum()), 有效天数=len(eff), 在跑日耗=eff.s.mean(), 首日=eff.dt.min(), 末日=eff.dt.max(), 跨度=span,
                          峰值日耗=g.s.max(), 峰值日=g.loc[g.s.idxmax(), "dt"], 节点分布="/".join(f"{k}{v}%" for k, v in nd.items() if v > 0)))

sub = d[d.track.notna()]
st = sub.groupby(["track", "类目", "leaf", "商品消费链路"]).apply(stats).reset_index()
st = st[st.有效天数 > 0].copy()
st["在跑日耗万"] = (st.在跑日耗 / 1e4).round(2)
st["总消耗万"] = (st.总消耗 / 1e4).round(1)
st["峰值日耗万"] = (st.峰值日耗 / 1e4).round(2)
st["连续性"] = (st.有效天数 / st.跨度).round(2)
st["首日"] = st.首日.dt.strftime("%m.%d"); st["末日"] = st.末日.dt.strftime("%m.%d"); st["峰值日"] = st.峰值日.dt.strftime("%m.%d")
st = st.sort_values(["商品消费链路", "track", "在跑日耗万"], ascending=[True, True, False])
st[["商品消费链路", "track", "类目", "leaf", "有效天数", "跨度", "连续性", "在跑日耗万", "峰值日耗万", "峰值日", "首日", "末日", "总消耗万", "节点分布"]].to_csv(out_dir + "q4_category_effective_days.csv", index=False, encoding="utf-8-sig")

# 赛道级：有效日定义为赛道当日消耗≥TH
def tstats(g):
    eff = g[g.s >= TH]
    return pd.Series(dict(有效天数=len(eff), 在跑日耗万=round(eff.s.mean() / 1e4, 1), 总消耗万=round(g.s.sum() / 1e4, 1), 峰值日耗万=round(g.s.max() / 1e4, 1), 峰值日=g.loc[g.s.idxmax(), "dt"].strftime("%m.%d"),
                          首日=eff.dt.min().strftime("%m.%d") if len(eff) else "", 末日=eff.dt.max().strftime("%m.%d") if len(eff) else ""))
tr = daily_track.reset_index().groupby(["商品消费链路", "track"]).apply(tstats).reset_index().sort_values(["商品消费链路", "在跑日耗万"], ascending=[True, False])
print(tr.to_string(index=False))

# 赛道 × 节点 日耗（节点内日均）
tn = sub.groupby(["商品消费链路", "track", "node"]).s.sum().reset_index()
ndays = {n: (pd.Timestamp(b) - pd.Timestamp(a)).days + 1 for n, a, b in nodes}
tn["日耗万"] = tn.apply(lambda r: r.s / ndays[r.node] / 1e4, axis=1).round(1)
tn_p = tn.pivot_table(index=["商品消费链路", "track"], columns="node", values="日耗万", fill_value=0).reset_index()
print(tn_p.to_string(index=False))

# 大盘节点日耗
tot_n = d.groupby(["商品消费链路", "node"]).s.sum().reset_index()
tot_n["日耗万"] = tot_n.apply(lambda r: r.s / ndays[r.node] / 1e4, axis=1).round(1)
print(tot_n.pivot(index="商品消费链路", columns="node", values="日耗万"))

# 被剔除的类目（有消耗但无一天≥2k）
allst = sub.groupby(["track", "类目", "商品消费链路"]).s.agg(["sum", lambda x: (x > 0).sum()]).reset_index()
allst.columns = ["track", "类目", "链路", "总消耗", "有消耗天数"]
kept = set(zip(st.类目, st.商品消费链路))
allst["保留"] = [(c, l) in kept for c, l in zip(allst.类目, allst.链路)]
drop = allst[(~allst.保留) & (allst.总消耗 > 0)]
print("dropped categories:", len(drop), "spend wan", round(drop.总消耗.sum() / 1e4, 1), "kept", len(kept), "kept spend wan", round(st.总消耗.sum() / 1e4, 1))

# 输出 JSON 供 HTML 使用
js = {}
for (l, t), g in st.groupby(["商品消费链路", "track"]):
    js.setdefault(l, {})[t] = [dict(leaf=r.leaf, days=int(r.有效天数), span=int(r.跨度), daily=float(r.在跑日耗万), peak=float(r.峰值日耗万), peakd=r.峰值日, a=r.首日, b=r.末日, tot=float(r.总消耗万), nd=r.节点分布) for r in g.itertuples()]
json.dump(dict(items=js, track=tr.to_dict(orient="records"), track_node=tn_p.to_dict(orient="records"),
               daily={l: {k.strftime("%m.%d"): round(v / 1e4, 1) for k, v in daily[l].items()} for l in daily.columns},
               track_daily={f"{l}|{t}": {k.strftime("%m.%d"): round(v / 1e4, 2) for k, v in g.droplevel([0, 1]).items()} for (l, t), g in daily_track.groupby(level=[0, 1])}),
          open(out_dir + "q4_effective_days.json", "w", encoding="utf-8"), ensure_ascii=False)
print("\nTOP per link/track")
for (l, t), g in st.groupby(["商品消费链路", "track"]):
    print(f"\n## {l} / {t}")
    print(g[["leaf", "有效天数", "跨度", "在跑日耗万", "峰值日耗万", "峰值日", "首日", "末日", "节点分布"]].head(12).to_string(index=False))
