import re
import pandas as pd
from converter import zg12uni51
import csv
import json

from segmentation.regex_pattern import *
from segmentation.extract_info import Extractor

# from regex_pattern import *
# from extract_info import Extractor

from myanmartools import ZawgyiDetector
import time


class Entity_extractor:
    @staticmethod            
    def isZawGyi(text):
        detector = ZawgyiDetector()
        score = detector.get_zawgyi_probability(text)
        if score >= 0.9:
            return True
        return False
    
    @staticmethod
    def toUnicode(text):
        return (zg12uni51(input_text = text))    
    @classmethod
    def retrieve_entity(cls,post):
        # print(post)
        sentence = (str(post)+'\n\n')
        zawgyi = cls.isZawGyi(sentence)
        if zawgyi:
            # print("This is zawgyi")
            standard = cls.toUnicode(post)
            # print(standard)
            # time.sleep(60)
        else:
            # print("This is unicode!")
            standard = post
            # print(standard)
            # time.sleep(60)
        # print(standard,"\n")
        # print("----------------------------")
        extractor = Extractor()
        entity_list = extractor.extract(str(standard))
        print("-------------------This is segementation--------------------")
        print(entity_list)
        # time.sleep(60)
        return entity_list
       
        
if __name__ =="__main__":
    extractor = Entity_extractor()
    str1="""HONDA FIT GP1,2011
$205
205 သိန်း
Light Green colour,2011 model
အော်ဆေး95 % ,Japan or TV or bc
DVD CD SD USB HDD AM/FM AUX
 kilo 8 သိန်းကျော် 1300 CC
လိုင်စင်အသစ်,တာယာအသစ်
အင်ဂျင် အောက်ပိုင်း ရှယ်ကောင်း
3L-9+++(YGN),2022/4လပိုင်း
IMA Bettery စိတ်ကြိုက်စစ်ပါ
အလုံ တွင်ကားကြည့်နိုင်ပါသည်
09-766644851
09-448236117"""

    Entity_extractor.retrieve_entity(str1)
    
  