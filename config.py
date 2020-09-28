import os
# config lines
cur_dir = os.getcwd().replace('\\', '/')
# 存放视频的路径
video_path ='D:/迅雷下载/佣兵的战争/video2/'
# 存放音频的路径
sound_dir = 'E:/电影文件/audio_09.28/'
# 存放临时图像的路径
temp_pic_dir = ''
# 存放字幕的路径
subtile_dir = cur_dir + '/subtitle/'
# 已经处理过的电影文件存放的目录
rec_file = cur_dir + '/rec_file.txt'
# 操作失败的电影记录文件
rec_fail_file = cur_dir + '/rec_fail_file.txt'
# 合法的视频后缀类型
allowed_video_suffix = [
    'mkv', 'mp4', 'avi', 'rmvb'
]
# 包含的文件名前缀
file_name_prefixs = [
 '[[阳光电影www.ygdy8.com]', '[电影天堂www.dy2018.net]', '[阳光电影www.ygdy8.com]','[电影天堂-www.dy2018.net]',
    '[无极电影-www.wujidy.com]', '[小调网-www.xiaodiao.com]', '[阳光电影www.ygdy8.com].'
]