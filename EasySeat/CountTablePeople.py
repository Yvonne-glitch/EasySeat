import os
import json
import torch
from torchvision import models, transforms
from PIL import Image, ImageDraw, ImageFont
from InitChairFasterRCNN import detect_objects

# 获取当前文件所在目录作为根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 跨平台拼接路径
def get_path(*args):
    return os.path.join(ROOT_DIR, *args)

# 加载 JSON 数据
def load_data_from_json(json_file, n):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data[f'D{n}_tables_boxes'], data[f'D{n}_chairs_boxes'], data[f'D{n}_a_set']

# 判断人中心点是否在椅子范围
def is_point_in_chair_box(point, chair_box):
    x, y = point
    xmin, ymin, xmax, ymax = chair_box
    return xmin <= x <= xmax and ymin <= y <= ymax

# 判断人的脚是否在桌子范围
def is_point_in_table_box(person_box, table_box):
    x = (person_box[0] + person_box[2]) / 2
    xmin, ymin, xmax, ymax = table_box
    return xmin <= x <= xmax and ymin <= person_box[1] <= ymax

# 主匹配函数
def match_people_to_chairs(table_boxes, chair_boxes, a_set, people_boxes):
    # 初始化椅子占用数组和桌子内人数数组
    rows = len(chair_boxes)
    cols = 10
    chair_occupied = [[False for _ in range(cols)] for _ in range(rows)]

    table_people_count = [0] * len(table_boxes)

    # 遍历每个人
    for person_id, person_box in enumerate(people_boxes):
        person_center = [(person_box[0] + person_box[2]) / 2, (person_box[1] + person_box[3]) / 2]

        # 遍历每张桌子
        for table_id, table_box in enumerate(table_boxes):
            # 如果桌子内人数已经到4
            if table_people_count[table_id] == 4:
                break
            # 判断人的中心是否在桌子范围内
            if is_point_in_table_box(person_box, table_box):
                # 遍历桌子内的每把椅子
                for chair_id in a_set[table_id]:
                    # 如果这套桌椅没椅子就结束
                    if chair_id == -1:
                        break
                    chair_box = chair_boxes[chair_id]
                    # 判断人的中心是否在椅子范围内
                    if is_point_in_chair_box(person_center, chair_box) and not chair_occupied[chair_id]:
                        # 标记椅子为已占用
                        chair_occupied[table_id][chair_id] = True
                        # 记录桌子内的人数
                        break  # 一旦找到合适的椅子，就跳出循环
                table_people_count[table_id] += 1
                break

    return chair_occupied, table_people_count
'''
# 处理单个编号
def diff_file_people(n):
    json_file = os.path.join(ROOT_DIR, f'D{n}data.json')
    image_path = os.path.join(ROOT_DIR, 'input', f'D{n}_people.jpg')

    table_boxes, chair_boxes, a_set = load_data_from_json(json_file, n)
    target_classes = ['person']

    detected_image, detected_boxes = detect_objects(image_path, target_classes)
    people_boxes = detected_boxes['person']

    chair_occupied, table_people_count = match_people_to_chairs(table_boxes, chair_boxes, a_set, people_boxes)
'''
# 程序入口
if __name__ == "__main__":
    numbers = [1, 5, 15, 18]
    for number in numbers:
        diff_file_people(number)
