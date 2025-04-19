import torch
from torchvision import models, transforms
from PIL import Image, ImageDraw, ImageFont
#import matplotlib.pyplot as plt
import json

def detect_objects(image_path, target_classes, threshold=0.4):
    
    # COCO 类别标签 (从 1 到 91，0 是背景)
    COCO_CLASSES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
        'traffic light', 'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
        'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'handbag', 'tie',
        'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
        'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
        'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'couch','chair',
        'potted plant', 'bed', 'N/A', 'N/A','dining table',  'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
        'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    ]
    
    '''
    # 为每个类别指定一个固定的颜色（可以更改为你喜欢的颜色）
    COLORS = [
        (255, 0, 0),  # 红色
        (0, 255, 0),  # 绿色
        (0, 0, 255),  # 蓝色
        (255, 255, 0),  # 黄色
        (0, 255, 255),  # 青色
        (255, 0, 255),  # 品红
        (192, 192, 192),  # 灰色
        (128, 0, 0),  # 深红
        (0, 128, 0),  # 深绿
        (255, 165, 0),  # 橙色
        # 为了覆盖91个类别，重复颜色列表直到有足够的颜色
    ] * 10  # 扩展颜色列表以适应91个类别
    '''

    # 加载图像
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    print(f"Image width: {width}, Image height: {height}")

    # 转换为 tensor
    image_tensor = transforms.ToTensor()(image).unsqueeze(0)

    # 加载预训练模型
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    # 进行推理
    with torch.no_grad():
        prediction = model(image_tensor)

    # 获取检测结果
    boxes = prediction[0]['boxes']
    labels = prediction[0]['labels']
    scores = prediction[0]['scores']

    # 过滤得分较低的框
    mask = scores > threshold
    boxes = boxes[mask]
    labels = labels[mask]
    scores = scores[mask]

    # 初始化绘图工具
    #draw = ImageDraw.Draw(image)

    # 初始化目标类别索引
    target_class_indices = [COCO_CLASSES.index(cls) for cls in target_classes]

    # 初始化目标类别边界框列表
    target_boxes = {cls: [] for cls in target_classes}

    # 遍历检测结果
    for box, label, score in zip(boxes, labels, scores):
        if label.item() not in target_class_indices:
            continue

        # 获取框的坐标 (xmin, ymin, xmax, ymax)
        xmin, ymin, xmax, ymax = box

        # 根据类别分配固定的颜色
        #color = COLORS[label.item() % len(COCO_CLASSES)]  # 使用类别ID选择颜色

        # 绘制矩形框
        #draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=3)

        # 获取标签名称
        label_name = COCO_CLASSES[label.item()]  # 将标签转换为名称
        label_text = f"{label_name}: {score:.2f}"  # 标签名和得分

        '''
        # 使用更大的字体绘制标签
        try:
            font = ImageFont.truetype("arial.ttf", size=30)  # 设置字体和大小
        except IOError:
            font = ImageFont.load_default()  # 如果无法加载字体，使用默认字体

        # 绘制标签
        draw.text((xmin, ymin), label_text, font=font, fill=color)
        '''

        # 如果是目标类别，将其边界框添加到列表中
        if label_name in target_classes:
            target_boxes[label_name].append([xmin.item(), ymin.item(), xmax.item(), ymax.item()])

    return image, target_boxes

#'''
# 示例用法
image_path = r"input\D18.jpg"
target_classes = ['person','chair']#'dining table','chair',
detected_image, detected_boxes = detect_objects(image_path, target_classes)

chairs_boxes = detected_boxes['chair']

# 读取现有的 data.json 文件
json_file = "D18data.json"
try:
    with open(json_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    # 如果文件不存在，初始化一个空的字典
    data = {}

# 将新的 chairs_boxes 数据添加到字典中
data["D18_chairs_boxes"] = chairs_boxes

with open("D18data.json", "w") as f:
    json.dump(data, f, indent=2)

print("D18data.json")
#'''

'''
# 显示图像
plt.figure(figsize=(10, 10))
plt.imshow(detected_image)
plt.axis('off')  # 关闭坐标轴
plt.show()

# 保存图像
output_path = "output\detected_output.jpg"
detected_image.save(output_path)

'''