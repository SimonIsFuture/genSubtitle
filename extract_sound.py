import os
from main import soundExtracter
from config import video_path


if __name__ == '__main__':
    files = os.listdir(video_path)
    for f in files:
        print('开始处理' + f)
        try:
            se = soundExtracter(f)
            se.extract_audio()
        except Exception as e:
            print(e)