from tools import Tools
from moviepy.editor import *
import os
import cv2
from cnocr import CnOcr
import datetime
import hashlib
import logging
from config import cur_dir, video_path, sound_dir, temp_pic_dir, subtile_dir
logging.basicConfig(level=logging.NOTSET)


class soundExtracter:
    def __init__(self, file_name):
        self.file_path = video_path + file_name
        # 内部的file name是不带后缀的
        f_suffix = file_name.split('.')[-1]
        self.file_name = file_name.replace('.'+f_suffix, '')
        self.sound_file_path = sound_dir
        # 创建那个目录
        tools = Tools()
        tools.mkdir(self.sound_file_path)

    def _load_video(self):
        self.video = VideoFileClip(self.file_path)

    def _extract_video(self):
        audio = self.video.audio
        audio.write_audiofile(self.sound_file_path + self.file_name + '.mp3')

    def extract_audio(self):
        self._load_video()
        self._extract_video()


class moviePicExtractor:
    def __init__(self, file_name):
        self.file_path = video_path + file_name
        # 内部的file name是不带后缀的
        f_suffix = file_name.split('.')[-1]
        self.file_name = file_name.replace('.' + f_suffix, '')

        self.temp_save_path = hashlib.md5(self.file_name.encode(encoding='UTF-8')).hexdigest()
    def _video_split(self, video_path, save_path):
        '''
        @param video_path:视频路径
        @param save_path:保存切分后帧的路径
        '''
        vc = cv2.VideoCapture(video_path)
        # 一帧一帧的分割 需要几帧写几
        c = 0
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False
        while rval:
            rval, frame = vc.read()
            # 每秒提取2帧图片
            if c % 10 == 0:
                _shape = frame.shape
                height = _shape[0]
                width = _shape[1]
                frame = frame[2 * height // 3: height, 0: width]
                cv2.imwrite(save_path + "/" + str('%06d' % c) + '.jpg', frame)
                cv2.waitKey(1)
            c = c + 1

    def cut(self):
        video_path = self.file_path
        # 测试文件夹是否存在
        save_path = temp_pic_dir + self.temp_save_path
        tool = Tools()
        tool.mkdir(save_path)
        self._video_split(video_path, save_path)

    # 获取现在保存图片的字幕进行识别
    def getPicDirPath(self):
        return temp_pic_dir + self.temp_save_path

    def del_dir(self):
        save_path = temp_pic_dir + self.temp_save_path
        tool = Tools()
        tool.deldir(save_path)


class textRecongiser:
    ocr = CnOcr()

    def __init__(self, file_name, temp_save_path):
        f_suffix = file_name.split('.')[-1]
        self.file_name = file_name.replace('.' + f_suffix, '')

        self.temp_pic_dir = temp_save_path
        self.output_text_dir = subtile_dir

    def gen_subtitle(self):
        total_content = []
        files = os.listdir(self.temp_pic_dir)
        for f in files:
            t = self.ocr.ocr(self.temp_pic_dir + '/' + f)
            for tt in t:
                line = ''.join(tt) + '\n'
                total_content.append( line )

        # write into file
        with open(self.output_text_dir + self.file_name + '.txt', 'w', encoding='utf8') as f:
            f.write(self._processContent(total_content))
            f.close()

    def  _processContent(self, content_array):
        final_content = ''
        t_content_array = []
        for c in content_array:
            if c not in t_content_array:
                t_content_array.append(c)

        # print(t_content_array)
        for t in t_content_array:
            final_content += t
        return final_content.strip('\n')


class Processor:
    def start_to_process(self, movie_name):
        starttime = datetime.datetime.now()
        logging.warning('Start to extract audio from movie {}'.format(movie_name))
        se = soundExtracter(file_name=movie_name)
        se.extract_audio()

        logging.warning('Start to extract pictures from movie {}'.format(movie_name))
        mpe = moviePicExtractor(file_name=movie_name)
        mpe.cut()

        logging.warning('Start to recongise pictures from movie {}'.format(movie_name))
        tr = textRecongiser(file_name=movie_name, temp_save_path=mpe.getPicDirPath())
        tr.gen_subtitle()

        mpe.del_dir()
        
        endtime = datetime.datetime.now()
        print((endtime - starttime).seconds)