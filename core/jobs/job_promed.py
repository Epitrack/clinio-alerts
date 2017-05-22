# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core import Promed
import datetime
def start_promed():
    print("""
        Start PROMED SCRAP...
    """)
    promed = Promed()
    promed.scrap()
    # print("Start promed ",datetime.date)
    return