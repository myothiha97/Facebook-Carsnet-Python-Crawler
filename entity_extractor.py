import re
import pandas as pd
from converter import zg12uni51
import csv
import json
from regex_pattern import *

class Entity_extractor:
    
    @staticmethod
    def get_entity(post_text):
        post_list = post_text.split('\n')
        segment = {}
        segment['brand']        = '-'   ## honda,toyota
        segment['name']         = '-'   ## fit, corolla
        segment['model']        = '-'   ## 
        segment['price']        = '-'   ## 340 lakhs
        segment['grade']        = '-'   ## xs, full
        segment['year']         = '-'   ## 1999,2008
        segment['engine']       = '-'   ## 2000 cc,1300 cc
        segment['color']        = '-'   ## peral white, black
        segment['body_type']    = '-'   ## sedan,hatchback
        segment['wheel_drive']  = '-'   ## 2,4
        segment['fuel']         = '-'   ## petrol,diesel
        segment['mileage']      = '-'   ## 14000 km
        segment['gear']         = '-'   ## auto, manual
        segment['seater']       = '-'   ## 6-seater, 7-seater
        segment['hand_drive']   = '-'   ## RHD, LHD
        segment['region']       = '-'   ## mdy, ygn, bgo,
        segment['license']      = '-'   ## yes , no
        segment['phone']        = '-'
        ph_list=[]
        
        for line in post_list:
            line = line.lower()
            if True:
                if re.search(make_reg, line):
                    if segment['brand'] == "-":
                        segment['brand'] = re.search(make_reg, line).group()

                    if segment['name'] == '-':
                        try:
                            name = re.search(make_reg,line).group()
                            models = line.split()
                            try:
                                num  = models.index(name)
                                model=models[num+1]
                            except:
                                model = models[1]
                            if re.search(except_reg, model):
                                pass
                            elif model == 'mark':
                                segment['name'] = 'mark-2'
                            else:
                                segment['name'] = model
                        except:
                            segment['name'] = '-'

                if segment['year'] == '-' and re.search(year_reg, line):
                    if re.search(r'[က-အ]', line) or line.startswith('ph') or line.startswith('09'):
                        pass
                    else:
                        if re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line):
                            segment['year'] = re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line).group()
                            
                        elif re.search(r'model', line) and segment['model'] == '-':
                            model = line.replace('model','').strip()
                            segment['model'] = re.sub(r'\W+','',model).strip()
                        else:
                            segment['model'] = '-'

                if (segment['grade'] == '-') and (re.search(grade_reg, line)):
                    try:
                        grade_ = re.sub('\W+',' ', line )  #remove special char
                        grade_lst = grade_.split()
                        grade_str = ''
                        for g in grade_lst:
                            if re.search('grade|\d+|model|[က-အ]|\/',g):
                                pass
                            else:
                                grade_str += g
                        segment['grade'] = re.sub('\W+','',grade_str)
                    except:
                        segment['grade'] = '-'

                if segment['color'] == '-' and re.search(color_reg, line):
                    segment['color'] = re.search(color_reg, line).group()

                if (segment['body_type'] == '-') and (re.search(body_reg,line)):
                    segment['body_type'] = re.search(body_reg, line).group()

                if (segment['wheel_drive'] == '-') and (re.search(drive_reg,line)):
                    try:
                        drive_train = re.search(drive_reg, line).group()
                        print(drive_train)
                        segment['wheel_drive'] = re.search(r'\d', drive_train).group() + ' wheel'
                    except:
                        segment['wheel_drive'] = '-'    

                if segment['fuel'] == '-' and re.search(fuel_reg,line):
                    fuel_type = re.search(fuel_reg, line).group()
                    if fuel_type == 'ဓာတ်ဆီ':
                        segment['fuel'] = 'petrol'
                    elif fuel_type == 'ဒီဇယ်':
                        segment['fuel'] = 'diesel'
                    else:
                        segment['fuel'] = fuel_type

                if segment['engine'] == '-' and re.search(engine_reg, line):
                    engine = re.search(engine_reg, line).group()
                    displacement = float(re.search(r"\d+(\.\d+)?", engine).group())
                    if displacement <100:
                        displacement *=1000
                    segment['engine']= str(int(displacement)) + ' cc'

                if segment['price'] == '-' and re.search(price_reg, line):
                    try:
                        price = re.search(price_reg, line).group()
                        check_comma = price.find(',')
                        if check_comma !=-1:
                            new_str = re.sub(",","",price)
                            price = re.sub("သိန်း","",new_str)
                            print(price)
                            segment['price'] = price
                        else:
                            price = re.search(r"\d+", line).group()
                            if len(price) >2:
                                new_str = ''
                                for i in price:
                                    if 4160 <= ord(i) <=4170:
                                        new_str += str(ord(i)%10)
                                    else:
                                        new_str += i
                                segment['price'] = new_str+' Lakhs'
                            else:
                                segment['price'] = '-'
                    except:
                        print("failed finding price")
                        segment['price'] = '-'

                if segment['mileage'] == '-' and re.search(mileage_reg, line):
                    if re.search(r'\d+\,\d+', line):                                ## 140,000
                        segment['mileage'] = re.search(r'\d+\,\d+', line).group().replace(',','') + ' km'
                    elif re.search(r'\d+ \+|\d+\+', line):                          ## 150000 + , 150,000+
                        segment['mileage'] = re.search(r'\d+ \+|\d+\+', line).group().strip('+').strip() + ' km'
                    else:
                        try:
                            array = re.findall(r'\d+|\++|[x]+|\*+|သောင်း|သိန်း',line)  ## 1++++ , 3xxxxx, 4*****, 2 သိန်း
                            km = ''.join(array)
                            if km.find(',') >=0:
                                mileage = km.replace(',','')
                            elif km.find('+') >=0:
                                mileage = km.replace('+', '0')
                            elif km.find('x') >=0:
                                mileage = km.replace('x', '0')
                            elif km.find('*') >=0:
                                mileage = km.replace('*', '0')
                            elif km.find('သောင်း') >=0 :
                                mileage = km.replace('သောင်း', '0000')
                            elif km.find('သိန်း') >=0 :
                                mileage = km.replace('သိန်း','00000')
                            else:
                                mileage = km
                            if len(mileage)<7:
                                new_str = ''
                                for i in mileage:
                                    if 4160 <= ord(i) <=4170:
                                        new_str += str(ord(i)%10)
                                    else:
                                        new_str += i
                                segment['mileage'] = new_str+' km'
                            else:
                                segment['mileage'] = '-'

                        except:
                            segment['mileage'] = '-'

                if (segment['region'] == '-') and (re.search(region_reg,line)):
                    try:
                        segment['region'] = re.search(region_reg,line).group()
                    except:
                        segment['region'] = '-'


                if (segment['gear'] == '-') and (re.search(drive_reg, line)):
                    if ( line.find('auto') > 0 ):
                        segment['gear'] = 'auto'
                    elif ( line.find('manual') > 0 ):
                        segment['gear'] = 'manual'
                    else:
                        segment['gear'] = '-'

                if (segment['seater'] == '-') and (re.search(seater_reg, line)):
                    try:
                        segment['seater'] = re.findall(r'\d',line)[0] + ' seats'
                    except:
                        segment['seater'] = '-'
                        
                if (segment['hand_drive'] == '-') and (re.search(hand_reg,line)):
                    drive_postion = re.search(hand_reg,line).group()
                    
                    if drive_postion == 'ဘယ်မောင်း' or drive_postion == "l.h.d" or drive_postion == "lhd":
                        segment['hand_drive'] = 'L.H.D'
                    if drive_postion == 'ညာမောင်း' or drive_postion == "r.h.d" or drive_postion == "rhd":
                        segment['hand_drive'] = 'R.H.D'
                        
                if segment['license'] == '-' and (re.search(license_reg,line)):
                    result = re.search(license_reg,line).group()
                    if re.search(r"license|licence|လိုင်စင်",result):
                        segment['license'] = "yes"
                    else:
                        segment['license'] = result
                    
                if re.search(ph_reg,line):
                    if re.search(ph_reg,line).group() not in ph_list:
                        phone_num = re.findall(ph_reg,line)
                        for ph in phone_num:
                            if re.search(mm_char,ph):
                                ph_num = re.sub(" ","",ph)
                                ph_num = re.sub("-","",ph_num)
                                ph_num = re.sub("[.]","",ph_num)
                                x = u"{}".format(ph_num)
                                ph_list.append(x)
                            else:
                                ph_num = re.sub(" ","",ph)
                                ph_num = re.sub("-","",ph_num)
                                ph_num = re.sub("[.]","",ph_num)
                                ph_num = re.sub("\+959","09",ph_num)
                                ph_list.append(ph_num)
                        
                    else:
                        continue
        if len(ph_list) > 1:
            segment['phone'] = ','.join(ph_list)
        else:
            segment['phone'] = ''.join(ph_list)
        return segment 
    
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
        zawgyi = Entity_extractor.isZawGyi(sentence)
        if zawgyi:
            zawgyi_list = re.findall(zawgyiReg,post)
            uni_list= [Entity_extractor.toUnicode(uni_code) for uni_code in zawgyi_list ]
            for i in range(len(uni_list)):
                standard = re.sub(zawgyi_list[i],uni_list[i],post)
            check_re = re.findall(zawgyiReg,standard)
            if check_re:
                standard = Entity_extractor.toUnicode(standard)
                print(standard)
            else:
                print(standard) 
        else:
            print("This is unicode")
            standard = sentence
            print(standard) 
        entity_list = Entity_extractor.get_entity(standard)
        # return entity_list    ### Uncomment this line and comment the below two line if u want to use it in crawler!!! 
        json_data = json.dumps(entity_list,indent=4)
        print(json_data) ### The phone number will be shown in unicode character when convert to json data !!
        
if __name__ =="__main__":
    extractor = Entity_extractor()
    str1="""Honda Fit
$160
Honda fit gE6
အျဖဴေရာင္Fတန္း
2009 model
ေစ်းတန္တန္ေလးနဲေရာင္းေပးမယ္
အတိုက္အခိုက္ကင္းအာမာခံတယ္
နိနက္ကင္း
၁၆၀သိန္း
၀၉၂၅၀၂၀၁၂၂၆"""
    Entity_extractor.retrieve_entity(str1)
    