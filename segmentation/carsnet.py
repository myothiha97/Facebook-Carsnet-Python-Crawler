import re
import pandas as pd
from converter import zg12uni51
import csv
import json
from segmentation.regex_pattern import *
from segmentation.extract_info import Extractor
# from extract_info import Extractor
from myanmartools import ZawgyiDetector
import time
# from regex_pattern import *
# from extract_info import Extractor
# from myanmartools import ZawgyiDetector

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
        # print("-------------------This is segementation--------------------")
        # print(entity_list)
        # time.sleep(60)
        return entity_list
       
        
if __name__ =="__main__":
    extractor = Entity_extractor()
    str1="""#Mitsubishi RVR ထဲ က ကားကောင်းကားသန့်လေးကိုမှရှာနေသောသူများအတွက်
#model 2010
#paddle shift
#G grade push start
#very good condition
#kilo 60000 ကျော်
#engine power 1800 CC ကို Eco mode ပါ၍ဆီစားသက်သာသည်။
#price 290lakhs Nego
#စိတ်တိုင်းကျစစ်ဆေးနိုင်ပါသည်။ကားကောင်းကြောင်း 100% အာမခံသည်။
#ph no 09 790 135 661
#လိုင်စင်လေးလည်းဝေးတယ်နော်
Myo Win Thant"""
    Entity_extractor.retrieve_entity(str1)
    
  