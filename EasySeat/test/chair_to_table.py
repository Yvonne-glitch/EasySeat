import torch
from sklearn.cluster import KMeans
import numpy as np
import json
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# 从 JSON 文件中加载 chairs_boxes
with open("chairs_boxes.json", "r") as f:
    chairs_boxes = json.load(f)

print("加载的 chairs_boxes:", chairs_boxes)

# 将检测框转换为中心点坐标
def get_center(box):
    xmin, ymin, xmax, ymax = box
    return [(xmin + xmax) / 2, (ymin + ymax) / 2]

chair_centers = np.array([get_center(box) for box in chairs_boxes])

# 使用 KMeans 聚类将椅子分为若干组（每组 4 把椅子）
n_clusters = len(chairs_boxes) // 4  # 假设每套桌椅有 4 把椅子
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(chair_centers)

# 获取每组的椅子
groups = {}
for i, label in enumerate(kmeans.labels_):
    if label not in groups:
        groups[label] = []
    groups[label].append(chairs_boxes[i])

# 加载图片
image_path = "input.jpg"
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# 遍历每组，推断桌子的位置
for label, chairs_in_group in groups.items():
    
    '''
    if len(chairs_in_group) != 4:
        continue  # 如果不是 4 把椅子，跳过
    '''
    '''
    if len(chairs_in_group) > 4:
        # 如果椅子数量超过 4 把，拆分为多个组
        for i in range(0, len(chairs_in_group), 4):
            group = chairs_in_group[i:i+4]
            xmin_list = [box[0] for box in group]
            ymin_list = [box[1] for box in group]
            xmax_list = [box[2] for box in group]
            ymax_list = [box[3] for box in group]

            table_xmin = min(xmin_list)
            table_ymin = min(ymin_list)
            table_xmax = max(xmax_list)
            table_ymax = max(ymax_list)

            table_box = [table_xmin, table_ymin, table_xmax, table_ymax]

            # 打印结果
            print(f"桌椅组 {label + 1}-{i//4 + 1}:")
            print(f"桌子边界框: {table_box}")
            for j, chair_box in enumerate(group):
                print(f"椅子 {j + 1} 边界框: {chair_box}")
            
            draw.rectangle(table_box, outline="blue", width=3)
    '''

    # 提取四把椅子的坐标
    xmin_list = [box[0] for box in chairs_in_group]  # 所有椅子的 xmin
    ymin_list = [box[1] for box in chairs_in_group]  # 所有椅子的 ymin
    xmax_list = [box[2] for box in chairs_in_group]  # 所有椅子的 xmax
    ymax_list = [box[3] for box in chairs_in_group]  # 所有椅子的 ymax

    # 计算四把椅子的最大范围
    table_xmin = min(xmin_list)  # 四把椅子的最小 x 坐标
    table_ymin = min(ymin_list)  # 四把椅子的最小 y 坐标
    table_xmax = max(xmax_list)  # 四把椅子的最大 x 坐标
    table_ymax = max(ymax_list)  # 四把椅子的最大 y 坐标

    # 桌子的边界框
    table_box = [table_xmin, table_ymin, table_xmax, table_ymax]

    # 打印结果
    print(f"桌椅组 {label + 1}:")
    print(f"桌子边界框: {table_box}")
    for i, chair_box in enumerate(chairs_in_group):
        print(f"椅子 {i + 1} 边界框: {chair_box}")

    # 绘制桌子的红色边界框
    # 绘制桌子的红色边界框
    draw.rectangle(table_box, outline="red", width=3)

    # 在红色框上标注桌子组编号
    # 选择一个合适的字体和大小
    font = ImageFont.truetype("arial.ttf", 20)  # 你可以根据需要调整字体和大小
    text = f"桌子组 {label + 1}"

    # 计算文本的位置，放在框的左上角
    text_x = table_xmin
    text_y = table_ymin - font.getsize(text)[1] - 5  # 留一点空间

    # 如果文本超出图像范围，调整位置
    if text_y < 0:
        text_y = table_ymin + 5  # 放在框的内部

    # 在图像上绘制文本
    draw.text((text_x, text_y), text, font=font, fill="red")

# 显示图片
plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis('off')  # 关闭坐标轴
plt.show()

# 保存标注后的图片
output_path = "output.jpg"
image.save(output_path)
print(f"标注后的图片已保存为 {output_path}")