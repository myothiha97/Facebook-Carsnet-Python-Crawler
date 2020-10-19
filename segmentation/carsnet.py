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
    str1="""Toyota Mark X 2022 2019
2004 Model
Kilo-160000
Metallic Black Color
2500 CC (Octane)
Auto Gear, 2WD
Push Start , Smart Key
First Owner, Car at good condition
1H- 9**2
Yangon Licence
သိန်း: ၁၃၃  (ညှိနှိုင်း)
ရန်ကုန်မြို့ ရန်ကင်း တွင်ကားကြည့်နိုင်ပါသည်
09-766644851
09-88423611"""

    Entity_extractor.retrieve_entity(str1)
    
  