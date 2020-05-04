import re
from regex_pattern import *
class Extractor:
    segment = {}
    segment['brand']        = '-'   
    segment['name']         = '-'   
    segment['model']        = '-'    
    segment['price']        = '-'   
    segment['grade']        = '-'   
    segment['year']         = '-'   
    segment['engine']       = '-'   
    segment['color']        = '-'   
    segment['body_type']    = '-'   
    segment['wheel_drive']  = '-'   
    segment['fuel']         = '-'   
    segment['mileage']      = '-'   
    segment['gear']         = '-'   
    segment['seater']       = '-'   
    segment['hand_drive']   = '-'  
    segment['region']       = '-'   
    segment['license']      = '-'   
    segment['phone']        = '-'

    @classmethod
    def extract(cls,post):
        post_list = post.split('\n')
        print(post_list)
        ph_list=[]
        for line in post_list:
            line = line.lower()
            line = str(line)
            cls.extract_segment(line=line,ph_list=ph_list)
            
        if len(ph_list) > 1:
            cls.segment['phone'] = ','.join(ph_list)
        else:
            cls.segment['phone'] = ''.join(ph_list)
        return cls.segment
    
    @classmethod
    def extract_segment(cls,line,ph_list):
        # print(line)
        if re.search(make_reg, str(line)) and cls.segment['brand'] == "-" :
            
            cls.segment['brand'] = re.search(make_reg, line).group()

        if cls.segment['name'] == '-':
            cls.get_name(line)

        if cls.segment['year'] == '-' and re.search(year_reg, str(line)):
            cls.get_year(line)

        if (cls.segment['grade'] == '-') and (re.search(grade_reg, str(line))):
           cls.get_grade(line)

        if cls.segment['color'] == '-' and re.search(color_reg, str(line)):
            cls.segment['color'] = re.search(color_reg, line).group()

        if (cls.segment['body_type'] == '-') and (re.search(body_reg,str(line))):
            cls.segment['body_type'] = re.search(body_reg, line).group()

        if (cls.segment['wheel_drive'] == '-') and (re.search(drive_reg,str(line))):
            cls.get_wheel_drive(line)  

        if cls.segment['fuel'] == '-' and re.search(fuel_reg,str(line)):
            cls.get_fuel(line)
            
        if cls.segment['engine'] == '-' and re.search(engine_reg, str(line)):
            cls.get_engine(line)

        if cls.segment['price'] == '-' and re.search(price_reg, str(line)):
            cls.get_price()

        if cls.segment['mileage'] == '-' and re.search(mileage_reg, str(line)):
            cls.get_mileage(line)

        if (cls.segment['region'] == '-') and (re.search(region_reg,str(line))):
            cls.get_region(line)

        if (cls.segment['gear'] == '-') and (re.search(drive_reg, str(line))):
            cls.get_gear(line)

        if (cls.segment['seater'] == '-') and (re.search(seater_reg, str(line))):
            cls.get_seater(line)
                
        if (cls.segment['hand_drive'] == '-') and (re.search(hand_reg,str(line))):
            cls.get_drive_position(line)
                
        if cls.segment['license'] == '-' and (re.search(license_reg,str(line))):
            cls.get_license(line)
            
        if re.search(ph_reg,str(line)):
            if re.search(ph_reg,line).group() not in ph_list:
                cls.get_phone(ph_list,line)
            else:
                pass

    
    @classmethod
    def get_name(cls,line):
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
                cls.segment['name'] = 'mark-2'
            else:
                cls.segment['name'] = model
        except:
            cls.segment['name'] = '-'
            
    @classmethod
    def get_year(cls,line):
        if re.search(r'[က-အ]', line) or line.startswith('ph') or line.startswith('09'):
            pass
        else:
            if re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line):
                cls.segment['year'] = re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line).group()
                
            elif re.search(r'model', line) and cls.segment['model'] == '-':
                model = line.replace('model','').strip()
                cls.segment['model'] = re.sub(r'\W+','',model).strip()
            else:
                cls.segment['model'] = '-'
    @classmethod
    def get_grade(cls,line):
        try:
            
            grade_ = re.sub('\W+',' ', line )  #remove special char
            grade_lst = grade_.split()
            grade_str = ''
            for g in grade_lst:
                if re.search('grade|\d+|model|[က-အ]|\/',g):
                    pass
                else:
                    grade_str += g
            cls.segment['grade'] = re.sub('\W+','',grade_str)
        except:
            cls.segment['grade'] = '-'
    @classmethod
    def get_wheel_drive(cls,line):
        try:
            drive_train = re.search(drive_reg, line).group()
            print(drive_train)
            cls.segment['wheel_drive'] = re.search(r'\d', drive_train).group() + ' wheel'
        except:
            cls.segment['wheel_drive'] = '-'

    @classmethod
    def get_fuel(cls,line):
        fuel_type = re.search(fuel_reg, line).group()
        if fuel_type == 'ဓာတ်ဆီ':
            cls.segment['fuel'] = 'petrol'
        elif fuel_type == 'ဒီဇယ်':
            cls.segment['fuel'] = 'diesel'
        else:
            cls.segment['fuel'] = fuel_type
            
    @classmethod
    def get_engine(cls,line):
        engine = re.search(engine_reg, line).group()
        displacement = float(re.search(r"\d+(\.\d+)?", engine).group())
        if displacement <100:
            displacement *=1000
        cls.segment['engine']= str(int(displacement)) + ' cc'
        
    @classmethod
    def get_price(cls,line):
        try:
            price = re.search(price_reg, line).group()
            check_comma = price.find(',')
            if check_comma !=-1:
                new_str = re.sub(",","",price)
                price = re.sub("သိန်း","",new_str)
                print(price)
                cls.segment['price'] = price
            else:
                price = re.search(r"\d+", line).group()
                if len(price) >2:
                    new_str = ''
                    for i in price:
                        if 4160 <= ord(i) <=4170:
                            new_str += str(ord(i)%10)
                        else:
                            new_str += i
                    cls.segment['price'] = new_str+' Lakhs'
                else:
                    cls.segment['price'] = '-'
        except:
            print("failed finding price")
            cls.segment['price'] = '-'
            
    @classmethod
    def get_mileage(cls,line):
        if re.search(r'\d+\,\d+', line):                                ## 140,000
            cls.segment['mileage'] = re.search(r'\d+\,\d+', line).group().replace(',','') + ' km'
        elif re.search(r'\d+ \+|\d+\+', line):                          ## 150000 + , 150,000+
            cls.segment['mileage'] = re.search(r'\d+ \+|\d+\+', line).group().strip('+').strip() + ' km'
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
                    cls.segment['mileage'] = new_str+' km'
                else:
                    cls.segment['mileage'] = '-'

            except:
                cls.segment['mileage'] = '-'
                
    @classmethod
    def get_region(cls,line):
        try:
            cls.segment['region'] = re.search(region_reg,line).group()
        except:
            cls.segment['region'] = '-'
            
    @classmethod
    def get_gear(cls,line):
        if ( line.find('auto') > 0 ):
            cls.segment['gear'] = 'auto'
        elif ( line.find('manual') > 0 ):
            cls.segment['gear'] = 'manual'
        else:
            cls.segment['gear'] = '-'
    @classmethod
    def get_seater(cls,line):
        try:
            cls.segment['seater'] = re.findall(r'\d',line)[0] + ' seats'
        except:
            cls.segment['seater'] = '-'
            
    @classmethod
    def get_drive_position(cls,line):
        drive_postion = re.search(hand_reg,line).group()
        if drive_postion == 'ဘယ်မောင်း' or drive_postion == "l.h.d" or drive_postion == "lhd":
            cls.segment['hand_drive'] = 'L.H.D'
        if drive_postion == 'ညာမောင်း' or drive_postion == "r.h.d" or drive_postion == "rhd":
            cls.segment['hand_drive'] = 'R.H.D'
            
    @classmethod
    def get_license(cls,line):
        result = re.search(license_reg,line).group()
        if re.search(r"license|licence|လိုင်စင်",result):
            cls.segment['license'] = "yes"
        else:
            cls.segment['license'] = result
          
    @staticmethod
    def get_phone(ph_list,line):
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
                
    
