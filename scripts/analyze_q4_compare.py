import pandas as pd
import re

csv_path = "/Users/congjiang/Downloads/通用分析数据集 (44).csv"
dy_path = "/Users/congjiang/Downloads/抖音蝉妈妈-日用百货 25 年Q4数据.xlsx"
out_path = "/Users/congjiang/With/20260923/6fia/q4_compare_detail.csv"

d = pd.read_csv(csv_path)
d["消耗数值"] = pd.to_numeric(d["消耗(元)"].replace({"~": "0", "": "0"}), errors="coerce").fillna(0)
d = d[d["商品消费链路"].isin(["直播", "小店"])].copy()
dy = pd.read_excel(dy_path)
dy_text = (dy["商品"].fillna("") + " " + dy["所属类目"].fillna("")).astype(str)

items = [
("全年基本盘", "艾灸贴", ["艾灸贴", "艾灸"]),
("全年基本盘", "足贴", ["足贴"]),
("全年基本盘", "蒸汽眼罩", ["蒸汽眼罩"]),
("全年基本盘", "护眼贴/眼贴", ["护眼贴", "眼贴"]),
("全年基本盘", "肚脐贴", ["肚脐贴"]),
("全年基本盘", "八髎贴", ["八髎贴", "八髎"]),
("全年基本盘", "三阴交贴", ["三阴交"]),
("全年基本盘", "乳贴", ["乳贴"]),
("全年基本盘", "鼻安合香", ["鼻安合香", "鼻贴"]),
("秋冬保暖", "暖宝宝/保暖贴", ["暖宝宝", "保暖贴", "暖贴"]),
("秋冬保暖", "暖手宝", ["暖手宝", "暖手"]),
("秋冬保暖", "自发热脚贴", ["自发热脚贴", "暖脚贴", "脚贴"]),
("秋冬保暖", "热敷艾灸贴", ["热敷艾灸贴", "热敷贴"]),
("秋冬保暖", "蒸汽热敷眼罩", ["蒸汽热敷眼罩", "蒸汽眼罩"]),
("肩颈腰膝", "护腰/腰贴", ["护腰", "腰贴", "腰椎贴"]),
("肩颈腰膝", "护膝/膝盖贴", ["护膝", "膝盖贴", "膝贴"]),
("肩颈腰膝", "肩颈贴/肩周贴", ["肩颈贴", "肩周贴", "肩贴"]),
("肩颈腰膝", "骨贴", ["骨贴"]),
("肩颈腰膝", "透骨贴/透骨膏", ["透骨贴", "透骨膏"]),
("肩颈腰膝", "老黑膏", ["老黑膏"]),
("肩颈腰膝", "关节喷剂", ["关节喷剂"]),
("肩颈腰膝", "防风贴", ["防风贴"]),
("年末焕新", "泡脚/足浴", ["泡脚", "足浴", "沐浴桶", "足浴桶"]),
("年末焕新", "修毛器", ["修毛器", "毛球修剪器", "鼻毛修剪器"]),
]

rows=[]
for node,item,kws in items:
    rx="|".join(map(re.escape,kws))
    dy_hit=dy_text.str.contains(rx,case=False,regex=True)
    for link in ["直播","小店"]:
        g=d[(d["商品消费链路"]==link)&d["类目"].astype(str).str.contains(rx,case=False,regex=True)]
        spend=g["消耗数值"].sum()
        rows.append({"节点池":node,"品类":item,"链路":link,"我方消耗元":round(spend,2),"我方匹配类目":"；".join(g.loc[g["消耗数值"]>0,"类目"].drop_duplicates().tolist()),"抖音Q4有跑":"是" if dy_hit.any() else "否","抖音匹配商品数":int(dy_hit.sum())})

r=pd.DataFrame(rows)
r["对比状态"]=r.apply(lambda x:"我方在跑" if x["我方消耗元"]>0 else ("抖音有跑·我方未跑" if x["抖音Q4有跑"]=="是" else "双方均未跑/机会池"),axis=1)
r.to_csv(out_path,index=False,encoding="utf-8-sig")
print(r.to_string(index=False))
print("\nSUMMARY")
print(r.groupby(["链路","对比状态"]).agg(品类数=("品类","size"),消耗元=("我方消耗元","sum")).to_string())
print("\nCSV_TOTAL")
print(d.groupby("商品消费链路")["消耗数值"].sum().to_string())
