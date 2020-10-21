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
    str1 = """
မဂၤလာပါ ၿမိဳ႕နယ္ေပါင္းစုံမွ အလုပ္အပ္ထားေသာလူႀကီးမင္းမ်ားထံဒုတိယအႀကိမ္ အားလုံးပို႔ေဆာင္ေပးလိုက္ပါပီ  သက္ဆိုင္ရာကားဂိတ္ အျမန္ေခ်ာ႐ုံးမ်ားမွာထုတ္ယူလုိ႔ရပါပီ အိမ္မွာေနရင္းလဲ အလုပ္တာဝန္ေတြက ႐ွိေသးေတာ့ တာဝန္ထမ္းေဆာင္လ်က္ပါ မဂၤလာပါ လူႀကီးမင္းတိ ု႔ ေျဖ ဆို ရန္ ခက္ ခဲ ေသာ ယာဥ္ေမာင္း လိုင္ စင္ အမ်ိဴ းမ်ိဴ း တို႔အတြက္ တိက်မွန္ကန္ ျမန္ဆန္ေအာင္ေဆာင္ရြက္ေပးတာ  ေအာင္ျမင့္မိုရ္
ေငြေၾကး ကိတ္စလိမ္လည္ျခင္းမ႐ွိတာ ေအာင္ျမင့္မိုရ္
Customer စိတ္တိုင္းက် ဦးစားေပးေဆာင္ရြက္တာ ေအာင္ျမင့္မိုရ္
ေစ်းႏုန္းမွန္ကန္တိက်တာ ေအာင္ျမင့္မိုရ္ ဘာပဲလိုလို ေအာင္ျမင့္မိုရ္ ကိုသာ ဟဲလိုလိုက္ပါ 09677873443 အက်ိဴ းေဆာင္မ်ားလဲဆက္သြယ္ႏိုင္ပါသည္  မွတ္ခ်က္ ( အတုအပျပဳလုပ္ေဆာင္ရြက္ျခင္းမ႐ွိပါ သျဖင့္ စရံေငြေပးသြင္းမွသာအလုပ္လက္ခံေဆာင္ရြက္ေပးပါသည္ ) မိတ္ေဟာင္းမိတ္သစ္အေပါင္း သြားလမ္းသာလုိ႔လာလမ္းေျဖာင့္ျဖဴ းပါေစဗ်ား"""

    Entity_extractor.retrieve_entity(str1)
