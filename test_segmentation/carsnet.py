import re
import pandas as pd
from converter import zg12uni51
import csv
import json

# from segmentation.regex_pattern import *
# from segmentation.extract_info import Extractor

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
    str1 = """မြို့တွင်းသာမကခရီးဝေးအသုံးပြုလိုသောမိတ်ဆွေညီအကိုမောင်နှမများအတွက်{CRV-RD.1} အလွန်ကောင်းမွန်သောကားလေးတစီးကိုပိုင်ရှင်ကိုယ်တိုင်ရောင်းချပေးချင်ပါတယ်
PleaseAdmin ကားလေးတစီးရောင်းချခွင့်ပြုပါ
Name HONDA CRV-{RD-1}
Model -1998 (seatbelt)
Colour White
Reg No-4D1567(YGN)
( လူအမည်ပေါက်)
စပါယ်ယာဘီးနောက်ချိတ်
Grade RD -1 (4-W/D)
EnginePower 2000cc(2.0)
Trans 4W/D-Auto
{ ကီလို ၂၀ ကျော်လျှင်2W/Dဖြင့်autoပြောင်းပေးပါသည်
Kilo (1)သိန်းကျော်
Licemce Exp (-31-7-2021)
Original Alloy & 4Goodtires
TV -DVD&Backcam
Original Guard
ရှေ့ဖေါက်လင့်မီး
နောက်စကွိုင်လာ
ဘီးနောက်ဂျိတ်
နာက်မှန် ၅ ချပ်မဲ
Original ရေကာ သဲကာ ခြေနင်းအစုံ
ရှေ့လက်တင်{၂ } ဖက်
နောက်လက်တင်
ရှေ့စာကြည့်မီး
လက်ကိုင်ကွင်း ၄ ကွင်း
အင်ဂျင်အောက်ပိုင်းသံချေးဆားပွင့်မရှိ
အင်ဂျင်အောက်ပိုင်းအထူးကောင်းမွန်
Aircom အေးဆိမ့်
အတွင်းခန်းအလွန်သန့်
အတွင်းခန်းအနာအဆာ အပေါက်အပြဲ
အစွန်းအထင်းလုံးဝမရှိ
100%အတိုက်အခိုက်ကင်း
ပြုပြင်စရာလုံးဝမလိုသောကားလေးကို
Price ္
157(သိန်း)
စိတ်ဝင်စားမေးမြန်းလိုလျှင်
Phone 09 5064640
09 775064640
ယာဉ်မှနကန်မှု့စိတ်ကြိုက်စစ်ဆေးနိုင်
On line တွင်အမြဲမရှိပါသဖြင့်ဖုန်းဖြင့်သာဆက်သွယ်ပေးပါ"""

    Entity_extractor.retrieve_entity(str1)
