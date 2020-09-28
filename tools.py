# 工具类
import os
import shutil
from config import file_name_prefixs
class Tools:
    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            print(path + ' 目录已存在')
            return False

    def deldir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            print('目录不存在')
        else:
            shutil.rmtree(path)

    def getSuffix(self, file_name):
        spilt_array = file_name.split('.')
        if len(spilt_array) <= 1:
            exit('File name is too short!')
        else:
            return spilt_array[-1]

    def rename(self, path):
        files = os.listdir(path)
        for f in files:
            for prefix in file_name_prefixs:
                if f.find(prefix) != -1:
                    ff = f.replace(prefix, '')
                    ff_array = ff.split('.')
                    file_name =  ff_array[0] if len(ff_array[0]) != 0 else ff_array[1]
                    suffix = self.getSuffix(f)
                    new_name = file_name + '.' + suffix
                    is_exists = os.path.exists(new_name)
                    print(new_name)
                    try:
                        os.rename(path+f, path+new_name)
                    except Exception as e:
                        print(e)

                    break



if __name__ == '__main__':
    tool = Tools()
    tool.rename('D:/迅雷下载/佣兵的战争/video2/')


