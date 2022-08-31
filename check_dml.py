import os
import sys
import re

class CheckDml:
    """
    @author:siuloong
    @date :2022-08-16
    检查DML语句是否执行。
    运行方法python check_dml.py 总的日志文件路径  需要执行的脚本路径
    无第三方库
    存在的问题：
        1、输入错误的参数异常没处理 --已处理
        2、路径下的文件如果是ANSI编码的处理不了，会报错，需要手动先改为utf8编码
    """
    def run(self):
        message = ("""参数错误，请输入正确得路径。
        格式为python check_dml [$路径一] [$路径二]
        $路径一  为总的日志文件路径
        $路径二  为需要执行的脚本路径""")
        # if sys.argv[3]:
        #     print(sys.argv[3] + '参数错误，只能支持两个参数\n'+message)

        if os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]):
            open('.//all.txt', 'w').close()
            self.open_file(sys.argv[1])
            self.open_file(sys.argv[2])
        else:
            print(message)

    def open_file(self, fpaths):
        """打开文件，将sql追加到列表"""
        self.list_file_dirs = self._dir_or_file(fpaths)
        self.new_file1 = open('.//all.txt', 'a+', encoding='utf-8')
        for list_file_dir in self.list_file_dirs:
            self.fo = self._foemat_txt(list_file_dir)
            if fpaths==sys.argv[1]:
                self.new_file1.write("--------" + list_file_dir + "--------\n")
                self.new_file1.write(str(self.fo))
            elif fpaths == sys.argv[2]:
                self._check_in(self.fo,list_file_dir)
            else:
                print('err')
        self.new_file1.close()

    def  _dir_or_file(self,fpath):
        """判断参数是文件还是路径，路径的话遍历路径经将文件路径记录到列表"""
        self.file_paths = []
        for dirpath, dirnames, filenames in os.walk(fpath):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                self.file_paths.append(file_path)
        return self.file_paths

    def _foemat_txt(self,list_file_dir):
        try:
            self.fot = open(list_file_dir, 'r', encoding='utf8').read()
        except:
            print('\n文件格式错误:'+list_file_dir+'需要将文件另存为文件编码为utf-8的编码文件。')
        self.fot = self.fot.strip()  # 删除前后空格
        self.fot = self.fot.lower()  # 所有字母转为小写
        self.fot = re.sub('\s{2,}', " ", self.fot)  # 删除2个及以上的空格
        self.fot = self.fot.replace("\n", "")
        self.fot = self.fot.replace("\r", "")
        self.fot = self.fot.replace(";", ";\n")
        self.fot = self.fot.replace("insert into", "\ninsert into")
        self.fot = self.fot.replace("update ", "\nupdate ")
        self.fot = self.fot.replace("delete ", "\ndelete ")
        self.fot = re.sub("#\S+", " ", self.fot)  # 删除注释
        self.fot = re.sub("--\S+", " ", self.fot)  # 删除注释
        self.fot = re.sub("/\*\S+", " ", self.fot)  # 删除注释
        self.fot = self.fot.strip()  # 删除前后空格
        self.fot = self.fot.strip('\t')
        files = '.\\aaa.txt'
        open(files, 'w', encoding='utf-8').write(self.fot)
        list = []
        for line in open(files, 'r', encoding='utf-8'):
            if re.match('^insert|update|delete', line):
                list.append(line)
        return list

    def _check_in(self,list_fos,efilename):
        """对比sql是否在结果中"""
        # self.oalllogs = open('.//all.txt', 'r', encoding='utf-8')
        # self.alllogs = self.oalllogs.read()
        try:
            self.oalllogs = open('.//all.txt', 'r', encoding='utf-8')
            self.alllogs = self.oalllogs.read()
        except:
            print('\n文件格式错误:'+efilename+'需要将文件另存为文件编码为utf-8的编码文件。')

        # print(self.alllogs)
        for list_fo in list_fos:
            list_fo = list_fo.replace("\n", "")
            list_fo = list_fo.strip()
            result = list_fo in self.alllogs
            if result:
                pass
            else:
                print('\n'+efilename+'未执行语句：\n'+list_fo)
                print(11)

        self.oalllogs.close()

if __name__ == '__main__':
    cdml = CheckDml()
    cdml.run()
