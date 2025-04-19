import os
import json
import argparse
from PIL import Image
from InitChairFasterRCNN import detect_objects
from CountTablePeople import load_data_from_json, match_people_to_chairs
from video_timer_backend import get_frames_at_current_time, start_timers, get_video_duration
import random


# 设置根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURE_DIR = os.path.join(ROOT_DIR, "picture")
INPUT_DIR = os.path.join(ROOT_DIR, "input")
OUTPUT_IMAGE_PATH = os.path.join(os.path.dirname(ROOT_DIR), "server", "assets", "output.png")
TABLE_REDDOT_JSON = os.path.join(ROOT_DIR, "table_reddot.json")

def gen_map(time_ms=None):
    numbers = [1, 5, 15, 18]
    num = [None] * 20
    num[1] = 0
    num[5] = 1
    num[15] = 2
    num[18] = 3

    # 加载背景图片
    bg_image_path = os.path.join(PICTURE_DIR, "bg.png")
    try:
        bg_image = Image.open(bg_image_path).copy()
    except FileNotFoundError:
        print(f"Error: 背景图像未找到：{bg_image_path}")
        return

    # 加载红点位置数据
    try:
        with open(TABLE_REDDOT_JSON, "r") as f:
            table_reddot = json.load(f)
            uncover_table = table_reddot.get("uncover_table", [])
            table_reddot = table_reddot.get("tables", [])
    except FileNotFoundError:
            uncover_table = []
            table_reddot = []
        
    
    occupy_por = [0,0,0,0,0]

    # 如果提供了时间参数，从视频中获取帧
    if time_ms is not None:
        frames = get_frames_at_current_time(time_ms)
        for n, frame in zip(numbers, frames):
            if frame is not None:
                # 将OpenCV图像转换为PIL图像
                frame = Image.fromarray(frame)
                # 保存帧到临时文件
                temp_image_path = os.path.join(INPUT_DIR, f"D{n}_people.jpg")
                frame.save(temp_image_path)
                print(f"已保存视频帧到: {temp_image_path}")

    for n in numbers:
        # 加载桌椅数据
        json_file = os.path.join(ROOT_DIR, f'D{n}data.json')
        table_boxes, chair_boxes, a_set = load_data_from_json(json_file, n)

        # 识别人物
        
        image_path = os.path.join(INPUT_DIR, f"D{n}_people.jpg")
        target_classes = ['person']
        detected_image, detected_boxes = detect_objects(image_path, target_classes)

        people_boxes = detected_boxes['person']
        chair_occupied, table_people_count = match_people_to_chairs(table_boxes, chair_boxes, a_set, people_boxes)
        
        for i, count in enumerate(table_people_count):

            occupy_por[count] += 1

            if count == 0:
                continue

            try:
                x = table_reddot[num[n]][i + 1][0]
                y = table_reddot[num[n]][i + 1][1]
                print(f"x:{x}, y:{y}")

                # 加载人数图标
                count_image_path = os.path.join(PICTURE_DIR, f"{count}.png")
                try:
                    image = Image.open(count_image_path)

                    # 缩小
                    new_size = (image.width // 5, image.height // 5)
                    image = image.resize(new_size, Image.Resampling.LANCZOS)

                    # 计算粘贴位置
                    paste_x = x - image.width // 2
                    paste_y = y - image.height // 2

                    # 粘贴
                    bg_image.paste(image, (paste_x, paste_y), image)

                except FileNotFoundError:
                    print(f"Warning: {count_image_path} not found!")
                    continue

            except IndexError:
                print(f"Warning: No coordinates for table {i + 1} in classroom D{n}")
                continue

    values = [0, 1, 2, 3, 4]     # 对应的值

    for i in range(len(uncover_table)):
        x = uncover_table[i][0]
        y = uncover_table[i][1]
        print(f"x:{x},y:{y}")
        count = random.choices(values, weights=occupy_por, k=1)[0]
        #print(f"count:{count}")

        # 加载对应的图片
        count_image_path = os.path.join(PICTURE_DIR, f"{count}.png")
        image = Image.open(count_image_path)

        # 缩小图片
        # 例如，将图片缩小到原来的一半
        new_size = (image.width // 5 , image.height// 5 )
        image = image.resize(new_size, Image.Resampling.LANCZOS)

        image_center_x = image.width // 2
        image_center_y = image.height // 2
        
        #print(f"image_center_x:{image_center_x},image_center_y:{image_center_y}")

        # 计算粘贴的起始坐标
        paste_x = x - image_center_x
        paste_y = y - image_center_y
        

        # 如果图片有透明通道，使用 image 作为 mask
        bg_image.paste(image, (paste_x, paste_y), image) 
    
    

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
    
    # 保存图片
    try:
        bg_image.save(OUTPUT_IMAGE_PATH)
        print(f"Image successfully saved to {OUTPUT_IMAGE_PATH}")
    except Exception as e:
        print(f"Error saving image: {e}")

    return bg_image

# 生成并显示地图
if __name__ == "__main__":
    print("test main!!!!")
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='生成座位分布图')
    parser.add_argument('--no-window', action='store_true', help='不显示窗口')
    parser.add_argument('--time', type=int, help='视频时间戳（毫秒）')
    args = parser.parse_args()

    # 生成地图
    result_image = gen_map(args.time)
    
    # 只有在不是 --no-window 模式下才显示图像
    if result_image and not args.no_window:
        result_image.show()
