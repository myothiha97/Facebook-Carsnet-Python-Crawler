import re
import pandas as pd
from converter import zg12uni51
import csv
import json
import sys,os
import pathlib
p = pathlib.Path('segmentation').resolve()
sys.path.append(str(p))
# sys.path.append(os.path.abspath(os.path.join('..','extract_info')))

from regex_pattern import *
from extract_info import Extractor

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
            print("This is zawgyi")
            standard = cls.toUnicode(post)
            # print(standard)
            # time.sleep(60)
        else:
            print("This is unicode!")
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
    str1 = """#မဂၤလာပါ
#ယခုလိုအခ်ိန္မ်ိဳးမွက်န္းမာေရးအထူးဂ႐ုစ္ိုက္ၾကပါရွင္
#လူႀကီးမင္းမ်ားကိုလုပ္ငန္းသံုး_စက္ရံုဖယ္ရီသံုး(၁တန္)(၁တန္ခြဲ)ကားေလးမ်ားႏွင့္မိတ္ဆက္ပါရေစရွင္
Hyundai Porter-2(1တန္)(၁၀ေပ)
Model .. ၂၀၁၅/ ၂၀၁၆ / ၂၀၁၇
Gear Type .. Manual /Auto (7 speed)
Engin Power .. 2500 Cc
လိုင္စင္ .. BGo( လူမည္ေပါက္)

၂၀၁၆ = ၁၆၀ သိန္း (။ ။)
၂၀၁၇ = ၁၆၅ သိန္း (။ ။)
အရစ္က် သိန္း-၇၀ / သိန္း-၈၀ / သိန္း ၉ဝ စသြင္းၿပီး
က်န္ေငြကို ၂ ႏွစ္ အထိ အရစ္က်ဝယ္ယူႏိုင္ပါၿပီ
တစ္လကို ၅သိန္းဝန္းက်င္သြင္းရပီး Model အျမင့္နဲ႔ ေကာင္းေကာင္းကားသန္႔ေလးမ်ားကို ေရာင္းခ်ေပးေနပါသည္။
#အရစ္က်ဝယ္ယူပါကေစ်းႏႈန္းအနည္းငယ္အေျပာင္းလဲရွိပါတယ္
ဘဏ္ႏွင့္မခ်ိတ္ဆက္ဘဲ..ကုမၸဏီတိုက္႐ိုက္အေရာင္းပါ
#ပိုင္ဆိုင္မႈစာရြက္စာတန္းေပးစရာမလိုပါ_ျပစရာမလိုပါ"""

    Entity_extractor.retrieve_entity(str1)
