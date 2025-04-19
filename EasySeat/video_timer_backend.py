import cv2
import time
import threading
import os

# 视频文件路径列表
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(ROOT_DIR, "video")
video_paths = [
    os.path.join(VIDEO_DIR, "D01.mp4"),
    os.path.join(VIDEO_DIR, "D05.mp4"),
    os.path.join(VIDEO_DIR, "D15.mp4"),
    os.path.join(VIDEO_DIR, "D18.mp4")
]

# 四个计时器
timers = [0] * 4
# 四个视频的时长（秒）
video_durations = [0] * 4

# 读取视频时长
def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    return duration

# 启动计时器
def start_timers():
    for i, path in enumerate(video_paths):
        video_durations[i] = get_video_duration(path)
        def timer_function(index):
            while True:
                time.sleep(1)
                timers[index] = (timers[index] + 1) % video_durations[index]
        threading.Thread(target=timer_function, args=(i,)).start()

# 获取指定时间对应的视频帧
def get_frames_at_current_time(time_ms=None):
    frames = []
    for i, path in enumerate(video_paths):
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # 如果提供了时间参数，使用它；否则使用计时器的当前时间
        if time_ms is not None:
            # 将毫秒转换为秒，并取模视频长度
            time_sec = (time_ms / 1000) % video_durations[i]
            frame_index = int(time_sec * fps)
        else:
            frame_index = int(timers[i] * fps)
            
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if ret:
            # 将BGR转换为RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        else:
            frames.append(None)
        cap.release()
    return frames

if __name__ == "__main__":
    # 启动计时器
    start_timers()

    # 测试获取指定时间的帧
    test_time_ms = 60000  # 1分钟
    frames = get_frames_at_current_time(test_time_ms)
    print(f"获取到 {len([f for f in frames if f is not None])} 个视频帧")
    