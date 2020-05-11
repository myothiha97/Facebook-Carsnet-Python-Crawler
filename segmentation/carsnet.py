import re
import pandas as pd
from converter import zg12uni51
import csv
import json
# from regex_pattern import *
from segmentation.regex_pattern import *
from segmentation.extract_info import Extractor
# from extract_info import Extractor
from myanmartools import ZawgyiDetector

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
        sentence = (str(post)+'\n\n')
        zawgyi = cls.isZawGyi(sentence)
        if zawgyi:
            standard = cls.toUnicode(post)
        else:
            standard = sentence
        entity_list = Extractor.extract(str(standard))
        return entity_list  
       
        
    
        
if __name__ =="__main__":
    extractor = Entity_extractor()
    str1="""5-5-2020 အဂၤါ ညေန ( 4:30 ) အတြက္
(စာကို ဆံုတိုင္ေအာင္္ ဖက္ပါ)
မန္ဘာေၾကး မရွိ ဂဏန္းေရာင္းမစားဘူး
ေငြႀကိဳ လႊဲစရာ မလိုဘူးမိတ္ေဆြ
အတြက္ အထူး (ကလယ္နာဆိုဒ္) ေအာတစ္ကြက္
( 1 )ကြက္ထဲ အပိုင္ ထုိးရမယ္ (100%%)အာမခံတယ္
(2)ကြက္ ( 3 )ဆုိမထုိးန႔ဲ အာမခံနဲ႔ေပးမွာေနာ္
အပိုမေျပာဘူးယံုၾကည္ရင္ေတာ hi ထား
ဆရာအတြက္ေတာ့ ပိုထိုးေပးပါ။ ပိုထိုးေပးနိုင္မွ လာယူ
ေပါက္ေပး စနစ္ျဖင့္သာ ကူညီးမယ္
ဆႏၵရွိမွ လာေတာင္း
ok မျပန္ႏိူင္ရင္ လာမေတာင္းပါနဲ႔
ေပါက္သီး အမွန္ 100% အာမခံတယ္
( 09 250320473)- ဖုန္​းကို ႐ိုး႐ိုး ဖုန္းမက္ေဆ့ကေန
ျမင္ျမင္ျခင္း hi ထားပါ အခု hi ထား
5...ရက္ ညေန အပိုင္ေပါက္ေစရမယ္။
မေပါက္ ထိုးရင္းပါျပန္ေရာ္ လိုက္မယ္"""
    Entity_extractor.retrieve_entity(str1)
    