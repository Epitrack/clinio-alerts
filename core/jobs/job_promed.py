# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core import Promed
import datetime

def start_promed():
    print("\nStart PROMED SCRAP...\n")
    promed = Promed()
    promed.scrap()
    return