#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax
import os
import re

properties_new = "E:\\pyproject\\opsDev\\jdbc\\jdbc.properties_new"
fpaths = f'E:\\pyproject\\opsDev\\jdbc'
comdir = f'\\common\\jdbc.properties'

class MovieHandler(xml.sax.ContentHandler):

    def __init__(self,list_file_dir,nods):
        self.nei_name = ""
        self.value =""
        self.list_file_dir = list_file_dir
        self.nods = nods

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        self.CurrentAttributes = attributes
        if tag == "bean":
            if attributes.getLength() > 1:
                parent = attributes.getNames()
                if parent[1] =="parent":
                    # print("\n##############################")
                    pass
        if tag == "property":
            lurl = attributes.getNames()
            self.nei_name = attributes.getValue(lurl[0])
            if self.nei_name == "url":
                self.value = attributes["value"]
            elif self.nei_name == "username":
                self.value = attributes["value"]
            else:
                self.nei_name = None

    # 元素结束调用
    def endElement(self, tag):
        if self.CurrentData == "property":
            if self.nei_name:
                self.matchObj = re.match(r'\${.*}', self.value)
                if self.matchObj:
                    self.fot = self.matchObj.group().strip()  # 删除前后空格
                    self.fot = self.fot.replace("${", "")
                    self.fot = self.fot.replace("}", "=")
                    self.fjdb = fpaths+self.nods+comdir
                    # print("\n$$$$$$$$$$$$$$",self.fjdb,"$$$$$",fpaths,self.nods,comdir)
                    with open(properties_new, encoding='utf-8') as f:
                        for line in f.readlines():
                            if self.fot in line:
                                self.value = re.sub(self.fot,"",line)
                                self.value = self.value.replace("\n", "")
                                self.value = self.value.replace("\r", "")
                # print(self.nei_name, "\t", self.value, end="\t")
                if self.nei_name == 'url':
                    print("\n",self.nods,"\t",self.list_file_dir,"\t", self.value, end='\t')
                else:
                    print(self.value, end='\t')
                self.vmmatchObj = re.match(r'^jdbc:mysql:.*\?', self.value)
                self.vomatchObj = re.match(r'^jdbc:oracle:.*', self.value)
                self.datebese = ""
                if self.vmmatchObj:
                    self.valuemy = re.split("/", self.vmmatchObj.group())
                    self.datebese = self.valuemy[-1].replace("?","")
                    print(self.datebese, end='\t')

                elif self.vomatchObj:
                    self.vomatchObj = re.findall(r'SERVICE_NAME.*\)', self.vomatchObj.group())
                    self.valueor = self.vomatchObj[0]
                    self.lvalueor = re.split('\)', self.valueor)
                    self.datebese = (self.lvalueor[0]).replace("SERVICE_NAME=","")
                    self.datebese = self.datebese.replace("SERVICE_NAME =", "")
                    print( self.datebese, end='\t')
        self.CurrentData = ""

class Durl():
    def __init__(self):
        list_file_dirs = self._dir_or_file(fpaths)
        print("nods\tserversname\turl\tdatabase\tusername", end="")
        for list_file_dir in list_file_dirs:
            self.list_file_dir = list_file_dir
            self.service = re.split("\\\\",self.list_file_dir)
            self.servicename2 = self.service[-2]
            self.nods = self.service[-3]
            # print("\n********************************serversname : ",self.servicename2,"********************************")
            # 创建一个 XMLReader
            parser = xml.sax.make_parser()
            # turn off namepsaces
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            # 重写 ContextHandler
            Handler = MovieHandler(self.servicename2,self.nods)
            parser.setContentHandler(Handler)
            parser.parse(self.list_file_dir)

    def  _dir_or_file(self,fpath):
        """判断参数是文件还是路径，路径的话遍历路径经将文件路径记录到列表"""
        self.file_paths = []
        for dirpath, dirnames, filenames in os.walk(fpath):
            for filename in filenames:
                if filename =="datasource.xml":
                    file_path = os.path.join(dirpath, filename)
                    self.file_paths.append(file_path)
        return self.file_paths

if (__name__ == "__main__"):
    DDurl = Durl()