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
        print(standard,"\n")
        print("----------------------------")
        extractor = Extractor()
        entity_list = extractor.extract(str(standard))
        print(entity_list)
        return entity_list
       
        
if __name__ =="__main__":
    extractor = Entity_extractor()
    str1="""အရောင်း/ အလဲ
ကားအသန့်လေးကို (၁၂၇ သိန်း) ဖြင့်တန်တန်လေး
လေးရောင်းမည် မြန်မြန်လေးဝယ်ထားနော်
ကားကောင်းစျေးတန်ဆိုတော့မြန်တယ်နော်
ကားကတော့ရှယ်လေးဗျာ org kilo 50000 ကျော်
အကြမ်း/အ​ချောလား မြို့တွင်း/​ဟိုင်းဝေး
ဆီ(10000)ဖိုးနဲ့နေပြည်တော်အသွားပြန်ရတယ်ဗျာ
လူကြီးလူငယ်မရွေး ပါကင်အတွက်စိတ်ပူစရာမလို
စတိုင်ကျကျလေးစီးဗျာ
🚗SUZUKI SWIFT 🇯🇵
🚘2008
🚘SMART KEY/ digital aircon
🚗4X2 ဒိုက်ခွက်နီကယ်
🚘ဓါတ်ဆီ engine (1300 CC )
🚗air con ရှယ် (စောင်ခြုံဂရိတ်)
🚘အော်ရီဂျင်နယ် TV&back AUDIO
အသံထွက်ရှယ်မိုက်သည်
🚘အတွင်းသန့် ထိုင်ခုံအပြောင်း
🚘အဲကွန်းအေးစိမ့်
🚗အင်ဂျင်ရှယ်
🚘အောက်ပိုင်း အသံ လုံးဝ မရှိ
🚗တာယာ ၄ လုံးအသစ်
🚘YGN-3E
🚗ရှေ့ HDမီးသီး fong lamp မီး
🚘အလွိုင်းဂွေထည့်ထားသည် တာယာဆိုက်ကြီး
☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️
လိုင်စင်တော့ဝင်ရမည်
အတိုက်ခိုက်ရှင်း အရိုးဆစ်ရှယ်လှသည်
မှန်ချိုးမှန်ခေါက်မှန်ချိန်မီးချိန် မီးအလှဆင်ထားသည် Airbag(2)လုံး လုပ်ချက်မရှိပါ
လည်သာကူရှင်စွပ်ထည့်ထားသည် အင်ဂျင်ရှယ်
ဂွေဆိုက်ကြီးထည့်ထားတော့အောက်ပိုင်း
လွတ်သည် လက်တင်စီးယုံဘဲ
ထည့်စရာကတော့ဆီပါဘဲ
💵 ၁၂၇ သိန်း (အပြောကောင်းလျှင်နည်းနည်းလျော့ပေးမည်)
📱 095091405
Wai Yan"""
    Entity_extractor.retrieve_entity(str1)
    
  