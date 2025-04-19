import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import os
import json

# XML 文件路径
xml_file = 'input\\reddotbg.xml'  # 替换为你的 XML 文件路径

# 解析 XML 文件
tree = ET.parse(xml_file)
root = tree.getroot()

# 提取红点的中心坐标
red_dot_centers = []
for obj in root.findall('object'):
    name = obj.find('name').text
    if name == 'reddot':
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        
        # 计算中心坐标
        center_x = (xmin + xmax) // 2
        center_y = (ymin + ymax) // 2
        
        # 假设监控编号和桌子编号
        d_id = 0  # 监控编号
        id = 0    # 桌子编号
        
        # 将数据添加到列表中
        red_dot_centers.append([center_x, center_y, d_id, id])

# 按 center_x 排序（从左到右），如果 center_x 相同，则按 center_y 排序（从下到上）
red_dot_centers.sort(key=lambda dot: (dot[0], -dot[1]))
# 输出结果
for i, data in enumerate(red_dot_centers):
    print(f"Red Dot {i + 1}: x={data[0]}, y={data[1]}, d_id={data[2]}, id={data[3]}")

red_dot_centers[25-1][0] = 234
index = 0
temp = red_dot_centers[index][0]
while index < len(red_dot_centers):
    if red_dot_centers[index][0]<= temp + 5 :
        red_dot_centers[index][0] = temp
    else : temp = red_dot_centers[index][0]
    index += 1

red_dot_centers.sort(key=lambda dot: (-dot[1], dot[0]))
red_dot_centers[44-1][1] = 545
index = 0
temp = red_dot_centers[index][1]
while index < len(red_dot_centers):
    if red_dot_centers[index][1]>= temp - 5 :
        red_dot_centers[index][1] = temp
    else : temp = red_dot_centers[index][1]
    index += 1
    
# 按 center_x 排序（从左到右），如果 center_x 相同，则按 center_y 排序（从下到上）
red_dot_centers.sort(key=lambda dot: (dot[0], -dot[1]))

json_file = 'reddot.json' 

with open(json_file, "w") as f:
    json.dump(red_dot_centers, f, indent=2)

# 输出结果
for i, data in enumerate(red_dot_centers):
    print(f"Red Dot {i + 1}: x={data[0]}, y={data[1]}, d_id={data[2]}, id={data[3]}")

# 加载图像
image_path = 'picture\\bg.png'  # 替换为你的图像路径
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# 设置字体大小
font = ImageFont.load_default() # 使用 Arial 字体，大小为 30

# 在图像上绘制红点编号
for i, data in enumerate(red_dot_centers):
    center_x, center_y, _, _ = data
    draw.text((center_x, center_y), str(i + 1), fill="green", font=font, anchor="mm")

# 保存绘制后的图像
output_image_path = 'output\\output_reddotbg.png'  # 替换为你的输出图像路径
os.makedirs(os.path.dirname(output_image_path), exist_ok=True)  # 确保输出目录存在
image.save(output_image_path)

print(f"已将带有编号的图像保存到 {output_image_path}")




'''
# 读取图片
image_path = r"picture\bg.png"  # 替换为你的图片路径
image = cv2.imread(image_path)

# 定义红点的颜色范围（BGR格式）
lower_red = np.array([32, 69, 233])
upper_red = np.array([32, 69, 233])

# 创建掩码，提取红点区域
mask = cv2.inRange(image, lower_red, upper_red)

# 使用形态学操作去除噪声
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# 查找轮廓
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 提取红点的中心坐标
red_points = []
for contour in contours:
    # 计算轮廓的中心
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        red_points.append((cX, cY))

# 输出红点的中心坐标
for point in red_points:
    print(point)

# 可选：在原图上绘制红点中心
for point in red_points:
    cv2.circle(image, point, 5, (0, 255, 0), -1)  # 用绿色标记红点中心

# 保存或显示结果
cv2.imwrite("output\redTogreen_image.jpg", image)  # 保存结果图片
cv2.imshow("Red Points", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''