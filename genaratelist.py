#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

#!@Time   : 2018/4/16 下午2:25
#!@Author : xudongxu
#!@File   : genaratelist.py
import os.path
import glob
import argparse

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='imagelist file path')
    args = parser.parse_args()
    path = args.dir
    output = open('imagelist.txt', 'w')
    output.truncate()
    for file in glob.glob(path+'/*.JPG'):
        name=os.path.basename(file).split('.')[0]
        output.write(name+'\n')
    output.close()