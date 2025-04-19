import json

# 假设从 JSON 文件中导入 table_boxes 和 chair_boxes
def load_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data['D18_tables_boxes'], data['D18_chairs_boxes']

# 计算椅子的中心点坐标
def get_center(box):
    return (box[0] + box[2]) / 2, (box[1] + box[3]) / 2

# 判断点是否在矩形范围内
def is_point_in_box(point, box):
    x, y = point
    xmin, ymin, xmax, ymax = box
    return xmin <= x <= xmax and ymin <= y <= ymax

# 主函数
def assign_chairs_to_tables(table_boxes, chair_boxes):
    # 初始化 a_set，每个桌子对应一个列表，存储椅子的标号
    a_set = [[] for _ in range(len(table_boxes))]

    # 遍历每把椅子
    for chair_id, chair_box in enumerate(chair_boxes):
        chair_center = get_center(chair_box)
        
        # 遍历每张桌子
        for table_id, table_box in enumerate(table_boxes):
            # 判断椅子中心是否在桌子范围内
            if is_point_in_box(chair_center, table_box):
                a_set[table_id].append(chair_id)
                break  # 一旦找到合适的桌子，就跳出循环

    # 将每个桌子的椅子列表填充到长度为 10，不足部分用 -1 填充
    for table_id in range(len(a_set)):
        a_set[table_id] += [-1] * (10 - len(a_set[table_id]))

    return a_set

# 示例：从 JSON 文件加载数据
json_file = 'D18data.json'  # 假设数据存储在 data.json 文件中
tables_boxes, chairs_boxes = load_data_from_json(json_file)

# 分配椅子到桌子
a_set = assign_chairs_to_tables(tables_boxes, chairs_boxes)

with open(json_file, "r") as f:
    data = json.load(f)

data["D18_a_set"] = a_set

with open(json_file, "w") as f:
    json.dump(data, f, indent=2)

# 打印结果
for table_id, chairs in enumerate(a_set):
    print(f"桌子 {table_id + 1} 的椅子编号: {chairs}")