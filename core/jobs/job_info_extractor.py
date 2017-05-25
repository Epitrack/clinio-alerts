# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core import InfoExtractor
import datetime

def start_extractor(link,date,text_):
    print("\nRun extractor : ",date['data'])
    i = InfoExtractor(link,date,text=text_)
    i.run()
    i.print_soft()
    i.persist()
    return