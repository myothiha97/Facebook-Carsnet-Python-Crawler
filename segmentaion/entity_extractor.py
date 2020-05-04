import re
import pandas as pd
from converter import zg12uni51
import csv
import json
from regex_pattern import *
from extract_info import Extractor
class Entity_extractor:
    @staticmethod            
    def isZawGyi(text):
        if (re.search(zawgyiReg,text) != None):
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
            zawgyi_list = re.findall(zawgyiReg,post)
            uni_list= [cls.toUnicode(uni_code) for uni_code in zawgyi_list ]
            for i in range(len(uni_list)):
                standard = re.sub(zawgyi_list[i],uni_list[i],post)
            check_re = re.findall(zawgyiReg,standard)
            if check_re:
                standard = cls.toUnicode(standard)
        else:
            standard = sentence
            print(standard)
        print(standard)
        entity_list = Extractor.extract(str(standard))
        # return entity_list    ### Uncomment this line and comment the below two line if u want to use it in crawler!!! 
        json_data = json.dumps(entity_list,indent=4)
        print(json_data)
        
    
        
if __name__ =="__main__":
    extractor = Entity_extractor()
    str1="""Honda Fit
$160
Honda fit gE6
အျဖဴေရာင္Fတန္း
2009 model
095102482
09420219475
095102482
ေစ်းတန္တန္ေလးနဲေရာင္းေပးမယ္
အတိုက္အခိုက္ကင္းအာမာခံတယ္
နိနက္ကင္း
၁၆၀သိန္း
၀၉၂၅၀၂၀၁၂၂၆"""
    Entity_extractor.retrieve_entity(str1)
    