import re
import pandas as pd
from converter import zg12uni51
import csv
import json
zawgyiReg = '\u1031\u103b|^\u1031|^\u103b|[\u1022-\u1030\u1032-\u1039\u103b-\u103d\u1040-\u104f]\u103b|\u1039$|\u103d\u103c|\u103b\u103c|[\u1000-\u1021]\u1039[\u101a\u101b\u101d\u101f\u1022-\u102a\u1031\u1037-\u1039\u103b\u1040-\u104f]|\u102e[\u102d\u103e\u1032]|\u1032[\u102d\u102e]|[\u1090-\u1099][\u102b-\u1030\u1032\u1037\u103c-\u103e]|[\u1000-\u102a]\u103a[\u102c-\u102e\u1032-\u1036]|[\u1023-\u1030\u1032-\u1039\u1040-\u104f]\u1031|[\u107e-\u1084][\u1001\u1003\u1005-\u100f\u1012-\u1014\u1016-\u1018\u101f]|\u1025\u1039|[\u1081\u1083]\u108f|\u108f[\u1060-\u108d]|[\u102d-\u1030\u1032\u1036\u1037]\u1039|\u102c\u1039|\u101b\u103c|[^\u1040-\u1049]\u1040\u102d|\u1031?\u1040[\u102b\u105a\u102e-\u1030\u1032\u1036-\u1038]|\u1031?\u1047[\u102c-\u1030\u1032\u1036-\u1038]|[\u102f\u1030\u1032]\u1094|\u1039[\u107E-\u1084]'
# zawgyiReg2 =  '\u102c\u1039', '\u103a\u102c', \s.'(\u103b|\u1031|[\u107e-\u1084])[\u1000-\u1021]','^(\u103b|\u1031|[\u107e-\u1084])[\u1000-\u1021]', '[\u1000-\u1021]\u1039[^\u1000-\u1021]', '\u1025\u1039' ,'\u1039\u1038' ,'[\u102b-\u1030\u1031\u103a\u1038](\u103b|[\u107e-\u1084])[\u1000-\u1021]' ,'\u1036\u102f','[\u1000-\u1021]\u1039\u1031' , '\u1064','\u1039' . self::WHITESPACE, '\u102c\u1031','[\u102b-\u1030\u103a\u1038]\u1031[\u1000-\u1021]', '\u1031\u1031', '\u102f\u102d', '\u1039$'
mm_char = "\u1040|\u1041|\u1042|\u1043|\u1044|\u1045|\u1046|\u1047|\u1048|\u1049"
make_reg      = r'acura|audi|bentley|bmw|buick|cadillac|chevrolet|chrysler|citeron|dodge|daihatsu|fiat|ford|gmc|honda|hyundai|infiniti|jaguar|jeep|kia|land rover|lexus|lincoln|maserati|mazada|mercedes|mini|mitsubishi|mitsubshi|nissan|peugeot|range rover|renault|subaru|suzuki|tesla|toyota|vauxhall|volkswagen|volvo|hillix|isuzu'
except_reg    = r'\W+|luxury|sedan|hatchback|hybrid|coupe|suv|convertible|minivan|wagon|pickup|truck|mingalar|myanmar|brand|[က-အ]+'
model_reg     = r'model'
grade_reg     = r'grade'
year_reg      = r'[1][9][9][0-9]|[2][0][0-9][0-9]|model|year'
engine_reg    = r'\d{4} cc|\d{4}. cc|\d{4}cc|\d{4}.cc|[1-4]\.[0-9] cc|[1-4]\.[0-9]. cc|[1-4]\.[0-9]cc|1-4]\.[0-9].cc|\b[1-4]\.[0-9]\b|\d\.\d CC'
color_reg     = r'pearl white|black|dark grey|white|silver|gray|blue' 
body_reg      = r'sedan|hatchback|hybrid|coupe|suv|convertible|minivan|wagon|pickup|truck'
# drive_reg     = r'4x4|\dw|\dwd|\d wd|\d wheel||\dwheel|\dweel|\d weel|\dWD|\d WD|\d[.]*\s*wd'
drive_reg     = r"4x4|\d\s*wd|\d\s*WD|\d\s*wheel|\d[.]*\s*wd|\d\s*weel|\d\s*w|\d\s*W"
fuel_reg      = r'diesel|petrol|ဓာတ်ဆီ|ဒီဇယ်'
mileage_reg   = r'km|kilo|mileage|milage|ကိလို|ကီလို'
gear_reg      = r'auto|manual|gear'
region_reg    = r'ygn|mdy|shn|sgg|bgo|shn|npw|ayy'
seater_reg    = r'seater|seaters|seating'
hand_reg      = r'ဘယ်မောင်း|ညာမောင်း|l.h.d|r.h.d|lhd|rhd'
# license_reg   = r'number|license|licence|လိုင်စင်|ygn|mdy|sgg|bgo|'
license_reg   = r"\d[A-Z]-\d{4}|\d[a-z]-\d{4}|\d[A-Z]\([A-Z]+\)|\d[A-Z][-/ ][*]+|license|licence|လိုင်စင်|ygn|mdy|sgg|bgo|SHN"
price_reg     = r'price|သိန်း|သိန်း [၀-၉]+|[၀-၉]+ သိန်း|\$\d\d\,\d\d\d|\d+သိန်း|\d+\s*lakhs|lakhs\s*\d+'
ph_reg        = r"09-\d{9}|09\s*\d{9}|၀၉[၀-၉]{9}|၀၉-[၀-၉]{9}|09-\d{7}|09\s*\d{7}|၀၉[၀-၉]{7}|၀၉-[၀-၉]{7}|09\s*\d{3}\s*\d{3}\s*\d{3}|\+959\s*\d{9}|\+959\s*\d{7}|09[.]*\d{9}|09[.]*\d{7}|09\s*\d{4}\s*\d{3}\s*\d{2}|09\s*\d{3}\s*\d{4}"    
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
        if (len(line) > 10000000):
            continue
        else:
            if re.search(make_reg, line):
                if segment['brand'] == "-":
                    segment['brand'] = re.search(make_reg, line).group()

                if segment['name'] == '-':
                    try:
                        name = re.search(make_reg,line).group()
                        # print(name)
                        models = line.split()
                        # print(models)
                        try:
                            num  = models.index(name)
                            # print(num)
                            model=models[num+1]
                            # print(model)
                        except:
                            model = models[1]
                        if re.search(except_reg, model):
                            # print("model found in except")
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
                    print("try finding price")
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
                    # print(phone_num)
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
                    # if re.search(r"[+]959",ph_num) !=None:
                    #     # pt = re.search(r"[+]959",ph_num).group()
                    #     ph_num = re.sub("/+959","09",ph_num)
                    #     ph_list.append(ph_num)
                    # else:
                    #     ph_list.append(ph_num)
                else:
                    continue
    if len(ph_list) > 1:
        # print(ph_list)
        segment['phone'] = ','.join(ph_list)
    else:
        segment['phone'] = ''.join(ph_list)
    return segment              

def isZawGyi(text):
    if (re.search(zawgyiReg,text) != None):
        return True
    return False

def toUnicode(text):
    return (zg12uni51(input_text = text))
       
def retrieve_entity(post):
    sentence = (str(post)+'\n\n')
    zawgyi = isZawGyi(sentence)
    if zawgyi:
        zawgyi_list = re.findall(zawgyiReg,post)
        uni_list= []
        for i in zawgyi_list:
            uni_code = toUnicode(i)
            uni_list.append(uni_code)
        print("There are zawgyi fonts in text : ",zawgyi_list)
        print("unicode string : ",uni_list)
        for i in range(len(uni_list)):
            standard = re.sub(zawgyi_list[i],uni_list[i],post)
        check_re = re.findall(zawgyiReg,standard)
        if check_re:
            print("Zawgyi fonts still exist in text")
            print("Converted the whole text to unicode")
            standard = toUnicode(standard)
            print(standard)
        else:
            print("Succeed replacing zawgyi fonts with unicodes")
            print(standard) 
    else:
        print("This is unicode")
        standard = sentence
        print(standard) 
    entity_list = get_entity(standard)
    # return entity_list    ### Uncomment this line and comment the below two line if u want to use it in crawler!!! 
    json_data = json.dumps(entity_list,indent=4)
    print(json_data) ### The phone number will be shown in unicode character when convert to json data !!
if __name__=="__main__":
    
    str1 = """Nissan caravan GL - 2007 (လူစီး အမှန်)
$185
Myanmar
ပစ်ကပ် - စလွန်း - DV
အလဲထပ်ရတယ် နော်

- Nissan Caravan ( အိမ်ရှည် )

Model - 2007 , GL ဂရိတ်
- လူစီးလိုင်စင် လိုင်စင်ဝေး
- ဓာတ်ဆီ 2.4 Auto 2WD
- ဆွဲကပ် မော်တာ 2ချပ်ပါ
- ဘေးဆလိုက်တံခါး ဆွဲကပ် မော်တာ
- နောက်ဖုန်း စွဲကပ် မော်တာ
- auto ခြေနင်း on /off
- Original နောက်အဲယာကွန်း
- နောက် 13 ခုံဆင်ထားတယ်
- နောက် စလိုက် မှန် 3ချပ်
- လက်တင်စီးရုံပဲ, လုပ်ချက်မရှိ
- ကညန ယဉ်စစ်ပီးသာပါ

စျေး - 185 သိန်း (ပါးပါးရှော့)
ဖုန်း - 09 - 254006630
"""
    retrieve_entity(str1)   
