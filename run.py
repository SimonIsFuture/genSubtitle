import os 
import time
from config import cur_dir, video_path, sound_dir, temp_pic_dir, subtile_dir, rec_file, allowed_video_suffix, rec_fail_file
from main import Processor

def check_movie(movie_name):
    movie_names = []

    with open(rec_file, 'r', encoding='utf-8') as f:
        movie_names = f.readlines()
        f.close()

    for name in movie_names:
        if movie_name == name.strip('\n'):
            return False    
    return True

def get_movie_list():
    res = []
    files = os.listdir(video_path)
    # 获取后缀
    for f in files:
        suffix = f.split('.')[-1]
        if (suffix.lower() in allowed_video_suffix) and check_movie(f):
            res.append(f)
    return res

def after_process(movie_name):
    # 处理完成后的操作
    # Step1 写入已经处理过的文件
    with open(rec_file, 'a', encoding='utf-8') as f:
        f.write(movie_name+'\n')
        f.close()
    os.remove(video_path + movie_name)
    print('Process {} end!'.format(movie_name))

def fail_to_process(movie_name):
    # 操作失败的电影名称
    with open(rec_fail_file, 'a', encoding='utf-8') as f:
        f.write(movie_name + '\n')
        f.close()
    
if __name__ == '__main__':
    while True:
        movies = get_movie_list()
        # 如果没有可以处理的电影
        if len(movies) == 0:
            print('No movie to process, the program will sleep for 30 min...')
            time.sleep(60 * 30) # 过30分钟再看..
            continue

        # 如果有电影可以处理
        for m in movies:
            try:
                p = Processor()
                p.start_to_process(m)
                after_process(m)
            except Exception as e:
                print(e)
               
