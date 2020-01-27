import re
import pandas as pd
from converter import zg12uni51

# data = pd.read_csv('carsnet-large.csv')
# post = data[['post']]

zawgyiReg = '\u1031\u103b|^\u1031|^\u103b|[\u1022-\u1030\u1032-\u1039\u103b-\u103d\u1040-\u104f]\u103b|\u1039$|\u103d\u103c|\u103b\u103c|[\u1000-\u1021]\u1039[\u101a\u101b\u101d\u101f\u1022-\u102a\u1031\u1037-\u1039\u103b\u1040-\u104f]|\u102e[\u102d\u103e\u1032]|\u1032[\u102d\u102e]|[\u1090-\u1099][\u102b-\u1030\u1032\u1037\u103c-\u103e]|[\u1000-\u102a]\u103a[\u102c-\u102e\u1032-\u1036]|[\u1023-\u1030\u1032-\u1039\u1040-\u104f]\u1031|[\u107e-\u1084][\u1001\u1003\u1005-\u100f\u1012-\u1014\u1016-\u1018\u101f]|\u1025\u1039|[\u1081\u1083]\u108f|\u108f[\u1060-\u108d]|[\u102d-\u1030\u1032\u1036\u1037]\u1039|\u102c\u1039|\u101b\u103c|[^\u1040-\u1049]\u1040\u102d|\u1031?\u1040[\u102b\u105a\u102e-\u1030\u1032\u1036-\u1038]|\u1031?\u1047[\u102c-\u1030\u1032\u1036-\u1038]|[\u102f\u1030\u1032]\u1094|\u1039[\u107E-\u1084]'

make_reg = r'acura|audi|bentley|bmw|buick|cadillac|chevrolet|chrysler|citeron|dodge|fiat|ford|gmc|honda|hyundai|infiniti|jaguar|jeep|kia|land rover|lexus|lincoln|maserati|mazda|mercedes|mini|mitsubishi|nissan|peugeot|range rover|renault|subaru|suzuki|tesla|toyota|vauxhall|volkswagen|volvo'
model_reg = r'majesty|alphard|wish|kluger|fit|succeed|hiace|swift|colt plus|rav4|rav 4|pajero|crv|ratis|surf|prado|caldina|belta|rav_4|mark|demio|ad van|corolla|march|probox|harrier|rx 450h|celica|vitz|insight|royal saloon|colt|crown'
fuel_reg = r'diesel|petrol|ဓာတ်ဆီ|ဒီဇယ်'
year_reg = r'1996|1997|1998|1999|2000|2001|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019'
price_reg = r'price|သိန်း'
engine_reg = '\d{4} cc|\d{4}. cc|\d{4}cc|\d{4}.cc|[1-4]\.[0-9] cc|[1-4]\.[0-9]. cc|[1-4]\.[0-9]cc|1-4]\.[0-9].cc'
mileage_reg = r'km|kilo|mileage|ကိလို|ကီလို'
color_reg = r'white|silver|gray|pearl white|black' 
plate_reg = r'[a-z][a-z]\/|[1-9][a-z]\/'

def get_entity(post_text):
    post_list = post_text.split('\n')
    #print(post_list)
    segment = {}
    segment['make'] = '-'
    segment['year'] = '-'
    segment['fuel'] = '-'
    segment['model'] = '-'
    segment['price'] = '-'
    segment['color'] = '-'
    segment['engine'] = '-'
    segment['mileage'] = '-'
    segment['license-initial'] = '-'
    
    for line in post_list:
        ### All Make(Brand)
        line = line.lower()
        #print(line)
        
        if re.search(make_reg, line):
            segment['make'] = re.search(make_reg, line).group()
            
            if segment['model'] == '-':
                try:
                    model = line.split()[1]
                    if re.search(except_reg, model):
                        pass
                    elif model == 'mark':
                        segment['model'] = 'mark-2'
                    else:
                        segment['model'] = model
                except:
                    segment['model'] = '-'
    
        if segment['year'] == '-':
            if re.search(year_reg, line):
                segment['year'] = re.search(year_reg, line).group()
                
        if segment['color'] == '-':
            if re.search(color_reg, line):
                segment['color'] = re.search(color_reg, line).group()
        ### All Fuel
        ### All Fuel
        if segment['fuel'] == '-':
            if re.search(fuel_reg,line):
                fuel_type = re.search(fuel_reg, line).group()
                if fuel_type == 'ဓာတ်ဆီ':
                    segment['fuel'] = 'petrol'
                elif fuel_type == 'ဒီဇယ်':
                    segment['fuel'] = 'diesel'
                else:
                    segment['fuel'] = fuel_type
            
            
        ### All displacement
        if segment['engine'] == '-':
            if re.search(engine_reg, line):
                engine = re.search(engine_reg, line).group()
                displacement = float(re.search(r"\d+(\.\d+)?", engine).group())
                if displacement <100:
                    displacement *=1000
                segment['engine']= str(int(displacement)) + ' cc'
            
        if segment['price'] == '-':
            if line.find('price') >=0 or line.find('သိန်း') >=0 :
                try:
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
                    segment['price'] = '-'
                    
        if segment['mileage'] == '-':
                if re.search(mileage_reg, line):
                    try:
                        array = re.findall(r'\d+|\++|[x]+|\*+|သောင်း|သိန်း',line)
                        km = ''.join(array)
                        if km.find('+') >=0:
                            milage = km.replace('+', '0')
                        elif km.find('x') >=0:
                            milage = km.replace('x', '0')
                        elif km.find('*') >=0:
                            milage = km.replace('*', '0')
                        elif km.find('သောင်း') >=0 :
                            milage = km.replace('သောင်း', '0000')
                        elif km.find('သိန်း') >=0 :
                            milage = km.replace('သိန်း','00000')
                        else:
                            milage = km
                        if len(milage)<7:
                            new_str = ''
                            for i in milage:
                                if 4160 <= ord(i) <=4170:
                                    new_str += str(ord(i)%10)
                                else:
                                    new_str += i
                            segment['mileage'] = new_str+' km'
                        else:
                            segment['mileage'] = '-'
                        
                    except:
                        segment['mileage'] = '-'
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
        standard = toUnicode(sentence)
    else:
        standard = sentence
    entity_list = get_entity(standard)
    return entity_list