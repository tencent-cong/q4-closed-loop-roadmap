# Q4 闭环链路 Road Map

抖音 Q4 TOP1500 / 10 月榜 与 腾讯闭环（直播 / 小店）去年 Q4 按天消耗的节点 × 赛道对比。

## 页面（下载后用浏览器直接打开）
- `q4-closed-loop-compare-lite.html`：单页机会地图：增量机会品在前、存量品在后，每格 ≤ 7 个，不含消耗数据
- `q4-closed-loop-compare-v2.html`：赛道 × 节点 对比表，存量品 / 增量机会品同格展示，可切换直播 / 小店
- `q4-closed-loop-effective-days.html`：类目有效跑量周期看板（有效天数、在跑日耗、时间轴）
- `q4-closed-loop-roadmap.html`：早期 Road Map 总览

## 数据（data/）
- `q4_compare_items_effective.csv`：逐品对比明细（链路 × 节点 × 状态 × 在跑日耗 × 有效天数）
- `q4_category_effective_days.csv`：闭环类目有效日统计
- `q4_track_cross_detail.csv` / `q4_closedloop_only_detail.csv`：赛道交叉与闭环独有明细
- `*.json`：页面渲染用数据

## 口径
- 赛道分类参考情报台「创意和卖点分析」8 赛道
- 清洁工具 = 物理清洁 + 洗浴工具（泡脚桶 / 沐浴桶 / 搓澡），化学清洁（清洁剂 / 除味 / 驱虫 / 洗衣类）剔除；手霜 / 足霜等个护类目删除；保鲜袋 / 保鲜膜归收纳用品
- 有效日：类目单日消耗 ≥ 2000 元；在跑日耗 = 有效日均值
- 节点：①寒露霜降换季(10.01-10.20) ②双11(10.21-11.11) ③立冬小雪(11.12-11.30) ④双12大雪冬至(12.01-12.22) ⑤春节大扫除·年货(12.23-)
- 页面行序：家居家纺、厨具置顶，其余按链路日耗倒序

## 复现（scripts/）
原始数据集不在仓库内。依次运行 `analyze_q4_effective_days.py` → `analyze_compare_effective.py` → `build_*.py`，口径规则见 `track_rules.py`。
