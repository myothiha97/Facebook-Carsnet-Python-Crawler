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
    str1 = """09950454604
ေစ်း-229 သိန္းပါးပါးေလ်ွာ့မယ္
Toyota SUCCEED (NCP58) TXG PACKAGE( ေလးလံုးေလးေပါက္)
Model-2011 February (2) လပိုင္း
2011 model ျဖစ္ေသာေႀကာင့္ ဒိုင္ခြက္အျဖဴ ,ေနာက္မီးျဖဴ ျဖစ္သြားျပီ
Colour-White (058) ကုတ္အမွန္
Engine-1500CC......2Wheel
Grade-TXG package (ေလးလံုးေလးေပါက္) grade 4.5 cancellation ပါတယ္
္ပါဝါေလးေပါက္ ေခါင္းမွီးေလးလံုး ဘတ္မွန္အႀကီး မွန္ခ်ိဳးမွန္ေခါက္ မွန္ငါးခ်က္မဲ လက္ကိုင္းကြင္းေလးကြင္း မွန္ခ်ိန္း မီးခ်ိန္း အကုန္ပါတယ္
Kilo-66000 စြန္းစြန္း
နံပါတ္အလြန္ျမင့္တယ္ MANDALAY LICENSE (1N-####) လူအမည္ေပါက္
ေတာက္ေလ်ွာက္အနက္ ,နံပါတ္အလြန္လွ
MDY license ကို BGO/MON ႀကိုက္ရာတယ္လိုင္စင္ေျပာင္းနိုင္သည္
လိုင္စင္သက္တမ္းကုန္ဆံုးရက္ (31.3.2021)
တလတ္ကိုင္
ဘရိတ္မီးေနာက္တုတ္ပါတယ္
Toyota Japan key romote အမွန္ပါတယ္
TV and original back camera
TV တြင္ CD .DVD USB.SD CARD .AUX.BLUETOOTH အကုန္ဖတ္ပါတယ္
Air corn အလြန္ရွယ္ေအး တေတာ္ေအးတယ္
ေဘာင္အမွတ္-NCP58-0080425
Engine oil နွင့္ Autoဆီအသစ္လွဲထားတယ္
bettery အသစ္
အင္ဂ်င္ရွယ္ ေအာက္ပိုင္းအသံတစ္သံမရွိ
ကားအလြန္ေကာင္းအတိုက္ခိုက္လံုးဝမရွိ ကားအသစ္တိုင္းရွိ,ဂ်ပန္ခ်တဲ့အတိုင္းကားကအသစ္တိုင္းရွိတယ္,ေတာက္ေလ်ွာက္အနက္ လည္သာတစ္စီးလံုးခင္းသာတယ္
ထိုင္ခံုအစြပ္လည္းထည့္ထားတယ္
ကားတစ္စီးလံုးသံျပား ေဖ်ာင္ေဖ်ာင္ဘဲ
original ေဆးပတ္လည္,ေအာ္ေဆး 100%
Alloy အသစ္နီးပါးရွိတယ္
တာယာေလးလံုးအသစ္ခ်ြတ္ခ်ြတ္,Tyre power 100%
ကားအသစ္တိုင္းရွိ ဂ်ပန္အနံ့ေတညင္မေပ်ာက္ေသးဘူး
ကားဆိုမွကားကားေႀကာင့္အေရာင္းဝယ္ပ်တ္စရာမရွိ
ကားကတစ္ျပားဖိုးမွထည့္စရာမလိုဘူလက္တင္စီးရံုးဘဲ
ကားေႀကာင့္လံုးဝမပ်က္ေစရဘူး
ပိုင္ရွင္ကိုယ္တိုင္ေရာင္းမည္
ေစ်း--229သိန္းပါးပါးေလ်ွာ့မည္
ရန္ကုန္ျမိဳ့တြင္ကားႀကည့္ရမယ္
ဆက္သြယ္ရန္ဖံုး 09950454604
09798237745
09950622613"""

    Entity_extractor.retrieve_entity(str1)
