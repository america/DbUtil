#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from datetime import datetime


def writeLog(msg):
  scriptName = path.basename(__file__)
  dirName = path.dirname(__file__)
  logFile = dirName + "/" + scriptName + ".log"

  with open(logFile, 'a', encoding='utf-8') as fp:
    fmt = '%Y/%m/%d %H:%M:%S'
    fp.write(datetime.now().strftime(fmt) + " ")
    fp.write(msg + "\n")



