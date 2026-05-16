#!/usr/bin/python
import csv
from collections import defaultdict
from pyecharts.charts import Scatter3D, Timeline
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import time

# ---------- 1. 读取数据，按 t 分组 ----------
groups = defaultdict(list)
with open('strinova_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)               # 若有表头则跳过；若首行为数据请注释或删除此行
    for row in reader:
        if len(row) != 4:
            continue
        try:
            a = float(row[0])
            b = float(row[1])
            c = float(row[2])
        except ValueError:
            continue
        t = row[3]
        groups[t].append((b, c, a))   # 顺序：x=b, y=c, z=a

# ---------- 2. 计算整体范围，用于自动缩小空白 ----------
all_b = [p[0] for pts in groups.values() for p in pts]
all_c = [p[1] for pts in groups.values() for p in pts]
all_a = [p[2] for pts in groups.values() for p in pts]

if not all_b:
    raise ValueError("CSV 文件中没有有效数据，请检查。")

# ---------- 3. 为不同分组准备颜色列表 ----------
colors = [
    "#c23531", "#2f4554", "#61a0a8", "#d48265", "#91c7ae",
    "#749f83", "#ca8622", "#bda29a", "#6e7074", "#546570",
    "#c4ccd3"
]
# 可按需扩充或调整

# ---------- 4. 创建 3D 散点图 ----------
scatter3d = Scatter3D(init_opts=opts.InitOpts(width="100vw", height="100vh", theme=ThemeType.WHITE))
scatter3d.set_global_opts(
    title_opts=opts.TitleOpts(title=f"Strinova Data Statistics (Updated at {time.time()})"),
    legend_opts=opts.LegendOpts(pos_top="5%", type_="scroll"),
)

# 逐个添加分组系列
for idx, (t_name, points) in enumerate(groups.items()):
    color = colors[idx % len(colors)]
    scatter3d.add(
        series_name=t_name,
        data=[list(p) for p in points],   # [[b, c, a], ...]
        xaxis3d_opts=opts.Axis3DOpts(
            name="Output",
            type_="value",
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            name="Tactical",
            type_="value",
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name="Rank",
            type_="value",
        ),
        grid3d_opts=opts.Grid3DOpts(width=100,depth=100,height=100,is_show=True),
        # 自定义该系列点的样式
        itemstyle_opts=opts.ItemStyleOpts(color=color),
    )

# ---------- 5. 输出 HTML ----------
scatter3d.render("index.html")
print("File ready: index.html")
