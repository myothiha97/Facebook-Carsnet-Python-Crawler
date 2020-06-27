import re
# from regex_pattern import *
from segmentation.regex_pattern import *

class Extractor:
    def __init__(self):
        self.segment = {}
        self.segment['brand']        = '-'
        self.segment['make']         = '-'  
        self.segment['name']         = '-'
        self.segment['model']        = '-'    
        self.segment['price']        = '-'   
        self.segment['grade']        = '-'   
        self.segment['year']         = '-'   
        self.segment['engine']       = '-'   
        self.segment['color']        = '-'   
        self.segment['body_type']    = '-'   
        self.segment['wheel_drive']  = '-'   
        self.segment['fuel']         = '-'   
        self.segment['mileage']      = '-'   
        self.segment['gear']         = '-'   
        self.segment['seater']       = '-'   
        self.segment['hand_drive']   = '-'  
        self.segment['region']       = '-'   
        self.segment['license']      = '-'   
        self.segment['phone']        = '-'
    def extract(self,post):
        # if self.segment['brand'] =='-':
        #     print("Brand is not yet selected")
        
            post_list = post.split('\n')
            print(post_list)
            # print("post list for self.segmentation ----------> ")
            # print(post_list)
            
            ph_list=[]
            for line in post_list:
                line = line.lower()
                line = str(line)
                self.extract_segment(line=line,ph_list=ph_list)
                
            if len(ph_list) > 1:
                self.segment['phone'] = ','.join(ph_list)
            else:
                self.segment['phone'] = ''.join(ph_list)
            return self.segment
        
    def extract_segment(self,line,ph_list):
        # print(line)
        if re.search(make_reg, str(line)) and self.segment['brand'] == "-" :
            
            self.segment['brand'] = re.search(make_reg, line).group()

        if re.search(make_reg, str(line)) and self.segment['make'] == "-" :
            
            self.segment['make'] = re.search(make_reg, line).group()

        if self.segment['name'] == '-':
            self.get_name(line)

        if self.segment['year'] == '-' and re.search(year_reg, str(line)):
            self.get_year(line)

        if (self.segment['grade'] == '-') and (re.search(grade_reg, str(line))):
           self.get_grade(line)

        if self.segment['color'] == '-' and re.search(color_reg, str(line)):
            self.segment['color'] = re.search(color_reg, line).group()

        if (self.segment['body_type'] == '-') and (re.search(body_reg,str(line))):
            self.segment['body_type'] = re.search(body_reg, line).group()

        if (self.segment['wheel_drive'] == '-') and (re.search(drive_reg,str(line))):
            self.get_wheel_drive(line)  

        if self.segment['fuel'] == '-' and re.search(fuel_reg,str(line)):
            self.get_fuel(line)
            
        if self.segment['engine'] == '-' and re.search(engine_reg, str(line)):
            self.get_engine(line)

        if self.segment['price'] == '-' and re.search(price_reg, str(line)):
            self.get_price(line)

        if self.segment['mileage'] == '-' and re.search(mileage_reg, str(line)):
            self.get_mileage(line)

        if (self.segment['region'] == '-') and (re.search(region_reg,str(line))):
            self.get_region(line)

        if (self.segment['gear'] == '-') and (re.search(drive_reg, str(line))):
            self.get_gear(line)

        if (self.segment['seater'] == '-') and (re.search(seater_reg, str(line))):
            self.get_seater(line)
                
        if (self.segment['hand_drive'] == '-') and (re.search(hand_reg,str(line))):
            self.get_drive_position(line)
                
        if self.segment['license'] == '-' and (re.search(license_reg,str(line))):
            self.get_license(line)
            
        if re.search(ph_reg,str(line)):
            if re.search(ph_reg,line).group() not in ph_list:
                self.get_phone(ph_list,line)
            else:
                pass

    
    def get_name(self,line):
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
                self.segment['name'] = 'mark-2'
            else:
                self.segment['name'] = model
        except:
            self.segment['name'] = '-'
    
    
    
    def get_year(self,line):
        if re.search(r'[က-အ]', line) or line.startswith('ph') or line.startswith('09'):
            pass
        else:
            if re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line):
                self.segment['year'] = re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line).group()
                
            elif re.search(r'model', line) and self.segment['model'] == '-':
                model = line.replace('model','').strip()
                self.segment['model'] = re.sub(r'\W+','',model).strip()
            else:
                self.segment['model'] = '-'
    
    def get_grade(self,line):
        try:
            grade_ = re.sub('\W+',' ', line )  #remove special char
            grade_lst = grade_.split()
            grade_str = ''
            for g in grade_lst:
                if re.search('grade|\d+|model|[က-အ]|\/',g):
                    pass
                else:
                    grade_str += g
            self.segment['grade'] = re.sub('\W+','',grade_str)
        except:
            self.segment['grade'] = '-'
    
    def get_wheel_drive(self,line):
        try:
            drive_train = re.search(drive_reg, line).group()
            print(drive_train)
            self.segment['wheel_drive'] = re.search(r'\d', drive_train).group() + ' wheel'
        except:
            self.segment['wheel_drive'] = '-'

    
    def get_fuel(self,line):
        fuel_type = re.search(fuel_reg, line).group()
        if fuel_type == 'ဓာတ်ဆီ':
            self.segment['fuel'] = 'petrol'
        elif fuel_type == 'ဒီဇယ်':
            self.segment['fuel'] = 'diesel'
        else:
            self.segment['fuel'] = fuel_type
            
    
    def get_engine(self,line):
        engine = re.search(engine_reg, line).group()
        displacement = float(re.search(r"\d+(\.\d+)?", engine).group())
        if displacement <100:
            displacement *=1000
        self.segment['engine']= str(int(displacement)) + ' cc'
        
    
    def get_price(self,line):
        try:
            price = re.search(price_reg, line).group()
            ### changing dollar to mm price ###
            # print(f"raw price ------------ > {price}")
            if re.search(r"\$",price):
                price = re.sub(r",","",price)
                dollar = re.search(r"\d+",price).group()
                mm_price = 1400 * int(dollar) ### dollar price can be changed by the time 
                price_lakhs = int(mm_price/100000)
                self.segment['price'] = str(price_lakhs) + "Lakhs"
            else:
                price = re.search(r"\d+", price).group()
                
                if len(price) > 1:
                    new_str = ''
                    for i in price:
                        if 4160 <= ord(i) <=4170:
                            new_str += str(ord(i)%10)
                        else:
                            new_str += i
                    self.segment['price'] = new_str+' Lakhs'
                else:
                    self.segment['price'] = '-'
        except:
            print("failed finding price")
            self.segment['price'] = '-'
            
    
    def get_mileage(self,line):
        if re.search(r'\d+\,\d+', line):                                ## 140,000
            self.segment['mileage'] = re.search(r'\d+\,\d+', line).group().replace(',','') + ' km'
        elif re.search(r'\d+ \+|\d+\+', line):                          ## 150000 + , 150,000+
            self.segment['mileage'] = re.search(r'\d+ \+|\d+\+', line).group().strip('+').strip() + ' km'
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
                    self.segment['mileage'] = new_str+' km'
                else:
                    self.segment['mileage'] = '-'

            except:
                self.segment['mileage'] = '-'
                
    
    def get_region(self,line):
        try:
            self.segment['region'] = re.search(region_reg,line).group()
        except:
            self.segment['region'] = '-'
            
    
    def get_gear(self,line):
        if ( line.find('auto') > 0 ):
            self.segment['gear'] = 'auto'
        elif ( line.find('manual') > 0 ):
            self.segment['gear'] = 'manual'
        else:
            self.segment['gear'] = '-'
    
    def get_seater(self,line):
        try:
            self.segment['seater'] = re.findall(r'\d',line)[0] + ' seats'
        except:
            self.segment['seater'] = '-'
            
    
    def get_drive_position(self,line):
        drive_postion = re.search(hand_reg,line).group()
        if drive_postion == 'ဘယ်မောင်း' or drive_postion == "l.h.d" or drive_postion == "lhd":
            self.segment['hand_drive'] = 'L.H.D'
        if drive_postion == 'ညာမောင်း' or drive_postion == "r.h.d" or drive_postion == "rhd":
            self.segment['hand_drive'] = 'R.H.D'
            
    
    def get_license(self,line):
        
        result = re.search(license_reg,line).group()
        if re.search(r"license|licence|လိုင်စင်",result):
            if re.search(r"\d[A-Za-z]|ygn|mdy|sgg|bgo|shn|npw|ayy|SHN|YGN|MDY|SGG|BGO",line):
                res = re.search(r"\d[A-Za-z]|ygn|mdy|sgg|bgo|shn|npw|ayy|SHN|YGN|MDY|SGG|BGO",line).group()
                if re.search(r"\d[A-Za-z]",res):
                    res = res+"/****"
                    self.segment['license'] = res
                else:
                    self.segment['license'] = res
            else:
                self.segment['license'] = "-"
        else:
            self.segment['license'] = result
          
    
    def get_phone(self,ph_list,line):
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
                
    
