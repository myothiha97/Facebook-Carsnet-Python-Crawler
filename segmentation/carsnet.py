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
        return (zg12uni51(input_text=text))

    @classmethod
    def retrieve_entity(cls, post):
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


if __name__ == "__main__":
    extractor = Entity_extractor()
    str1 = """■ Honda ☆ Insight ☆
* Sale Price
▪︎
[ 147 သိန်း ]
* model - 2009
* Grade - G
* licence - exp ( 30-05-2021)
* အတွင်းအပြင် အလွန်သန့်
* အတိုက်ခိုက်ရှင်း,
* engine, အောက်ပိုင်းကောင်း,
* AC အေး ,Tyres 4လုံးအသစ်,
* အိမ်စီး ကား ကောင်းလေးရောင်းချင်ပါတယ်
*
09967607261,
* 09 254446465"""

    Entity_extractor.retrieve_entity(str1)
