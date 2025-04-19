import xml.etree.ElementTree as ET
import json
from PIL import Image, ImageDraw, ImageFont

def parse_xml_and_sort_tables(xml_file):
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 初始化一个列表来存储桌子的边界框
    table_boxes = []

    # 遍历所有的 <object> 标签
    for obj in root.findall('object'):
        # 提取类别名称
        name = obj.find('name').text
        if name == 'a_set':  # 确保是桌子对象
            # 提取边界框坐标
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # 将坐标添加到列表中
            table_boxes.append([xmin, ymin, xmax, ymax])

    # 按照从左到右、从下到上的顺序对桌子进行排序
    # 先按 xmin 排序（从左到右），如果 xmin 相同，则按 ymax 排序（从下到上）
    table_boxes.sort(key=lambda box: (box[0], -box[3]))

    return table_boxes

# 输入 XML 文件路径
xml_file = 'input\D18.xml'

# 解析并排序桌子
tables_boxes = parse_xml_and_sort_tables(xml_file)

# 打印结果
for i, table_box in enumerate(tables_boxes):
    print(f"桌子 {i + 1}: {table_box}")

# 读取现有的 D5data.json 文件
json_file = "D18data.json"
try:
    with open(json_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    # 如果文件不存在，初始化一个空的字典
    data = {}

# 将新的 tables_boxes 数据添加到字典中
data["D18_tables_boxes"] = tables_boxes

# 将更新后的数据保存回 data.json 文件
with open(json_file, "w") as f:
    json.dump(data, f, indent=2)

# 加载图像
image_path = 'input\D18.jpg'  # 替换为你的图像路径
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# 设置字体（如果没有指定字体文件，可以使用默认字体）
# 设置字体大小
font_size = 50  # 调整字体大小
font = ImageFont.truetype("arial.ttf", font_size)  # 使用 Arial 字体，大小为 30

# 在图像上绘制桌子编号
for i, table_box in enumerate(tables_boxes):
    xmin, ymin, xmax, ymax = table_box
    center_x = (xmin + xmax) // 2
    center_y = (ymin + ymax) // 2
    draw.text((center_x, center_y), str(i + 1), fill="red", font=font)

# 保存绘制后的图像
output_image_path = 'output\output_D18_numtables.jpg'  # 替换为你的输出图像路径
image.save(output_image_path)

print(f"已将带有编号的图像保存到 {output_image_path}")


