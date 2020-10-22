import re
import sys,os
import pathlib
p = pathlib.Path('segmentation').resolve()
sys.path.append(str(p))
# sys.path.append('/home/mthk/Desktop/mmds-crawler/mmDS-FBCrawler-Selenium/segmentation')
from regex_pattern import *
import datetime


class Extractor:
    def __init__(self):
        self.segment = {}
        self.segment['brand'] = '-'
        self.segment['make'] = '-'
        self.segment['name'] = '-'
        self.segment['model'] = '-'
        self.segment['price'] = '-'
        self.segment['grade'] = '-'
        self.segment['year'] = '-'
        self.segment['engine'] = '-'
        self.segment['color'] = '-'
        self.segment['body_type'] = '-'
        self.segment['wheel_drive'] = '-'
        self.segment['fuel'] = '-'
        self.segment['mileage'] = '-'
        self.segment['gear'] = '-'
        self.segment['seater'] = '-'
        self.segment['hand_drive'] = '-'
        self.segment['region'] = '-'
        self.segment['licence_plate_no'] = '-'
        self.segment['phone1'] = '-'
        self.segment['phone2'] = '-'

    def extract(self, post):
        # if self.segment['brand'] =='-':
        #     print("Brand is not yet selected")

        post_list = post.split('\n')
        print(post_list)
        # print("post list for self.segmentation ----------> ")
        # print(post_list)

        ph_list = []
        for line in post_list:
            line = line.lower()
            line = str(line)
            self.extract_segment(line=line, ph_list=ph_list)

        if len(ph_list) >= 1:
            self.segment['phone1'] = ph_list[0]
            if len(ph_list) > 1:
                self.segment['phone2'] = ph_list[1]

        return self.segment

    def extract_segment(self, line, ph_list):
        # print(line)
        if re.search(make_reg, str(line)) and self.segment['brand'] == "-":

            self.segment['brand'] = re.search(make_reg, line).group()

        if re.search(make_reg, str(line)) and self.segment['make'] == "-":

            self.segment['make'] = re.search(make_reg, line).group()
            #

        if self.segment['name'] == '-' and re.search(models, str(line)):
            self.segment['name'] = re.search(models, str(line)).group()

        if self.segment['year'] == '-' and re.search(year_reg, str(line)):
            self.get_year(line)

        if (self.segment['grade'] == '-') and (re.search(grade_reg, str(line))):
            self.get_grade(line)

        if self.segment['color'] == '-' and re.search(color_reg, str(line)):
            self.segment['color'] = re.search(color_reg, line).group()

        if (self.segment['body_type'] == '-') and (re.search(body_reg, str(line))):
            self.segment['body_type'] = re.search(body_reg, line).group()

        if (self.segment['wheel_drive'] == '-') and (re.search(drive_reg, str(line))):
            self.get_wheel_drive(line)

        if self.segment['fuel'] == '-' and re.search(fuel_reg, str(line)):
            self.get_fuel(line)

        if self.segment['engine'] == '-' and re.search(engine_reg, str(line)):
            self.get_engine(line)

        if self.segment['price'] == '-' and re.search(price_reg, str(line)):
            # print("Price Detected")
            # print(line)
            self.get_price(line)

        if self.segment['mileage'] == '-' and re.search(mileage_reg, str(line)):
            self.get_mileage(line)

        if (self.segment['region'] == '-') and (re.search(region_reg, str(line))):
            self.get_region(line)

        if (self.segment['gear'] == '-') and (re.search(gear_reg, str(line))):
            self.get_gear(line)

        if (self.segment['seater'] == '-') and (re.search(seater_reg, str(line))):
            self.get_seater(line)

        if (self.segment['hand_drive'] == '-') and (re.search(hand_reg, str(line))):
            self.get_drive_position(line)

        if self.segment['licence_plate_no'] == '-' and (re.search(license_reg, str(line))):
            self.get_license(line)

        if re.search(ph_reg, str(line)):
            if re.search(ph_reg, line).group() not in ph_list:
                self.get_phone(ph_list, line)
            else:
                pass

        # def get_name(self,line):
        #     try:
        #         name = re.search(make_reg,line).group()
        #         models = line.split()
        #         try:
        #             num  = models.index(name)
        #             model=models[num+1]
        #         except:
        #             model = models[1]
        #         if re.search(except_reg, model):
        #             pass
        #         elif model == 'mark':
        #             self.segment['name'] = 'mark-2'

        #         else:
        #             self.segment['name'] = model

        #     except:
        #         self.segment['name'] = '-'

    def get_year(self, line):
        if line.startswith('ဖုန်း') or line.startswith('ph') or line.startswith('09'):
            pass
        else:
            if re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]', line):
                # self.segment['year'] = re.search(r'[1][9][9][0-9]|[2][0][0-9][0-9]',line).group()
                years = re.findall(r'[1][9][9][0-9]|[2][0][0-9][0-9]', line)
                current_yr = datetime.datetime.now().strftime("%Y")
                filterd_yrs = list(filter(lambda yr: yr <= current_yr, years))
                if filterd_yrs:
                    # Choose the first year
                    self.segment['year'] = filterd_yrs[0]
                else:
                    self.segment['year'] = '-'

            elif re.search(r'model', line) and self.segment['model'] == '-':
                model = line.replace('model', '').strip()
                self.segment['model'] = re.sub(r'\W+', '', model).strip()

            else:
                self.segment['model'] = '-'

    def get_grade(self, line):

        try:
            # line = re.sub(r"[()]","",line)
            position = line.find('grade')
            word_list = line.split()
            g_postions = []
            grades = []
            for w in word_list:
                # print(w)
                if re.search(r"[က-အ]|[-]|[/]|[()]|[:]", w) or len(w) > 3:
                    pass
                else:
                    grades.append(w)
                    g_postion = line.find(w)
                    g_postions.append(g_postion)

            if g_postions:
                ranges = []
                for val in g_postions:
                    pos = abs(position-val)
                    if val > position:
                        pos -= 4
                        ranges.append(pos)
                    else:
                        ranges.append(pos)
                # print(position)
                # print(g_postions)
                # print(ranges)
                grade = min(ranges)
                grade = ranges.index(grade)
                grade = grades[grade]
                print(grades)
                # print(ranges,position)
                print(grade)
                self.segment['grade'] = grade

            else:
                self.segment['grade'] = '-'
        except Exception as e:
            print(f"An error occur while trying to get grade : {str(e)}")
        # if start >= 8:
        #     grade_pattern = line[start-8:end+8]
        #     grade_list = grade_pattern.split()
        #     print(grade_list)
        #     grade_str = ''
        #     for g in grade_list:
        #         if re.search(r"[က-အ]|\-|[/]|grade",g) or len(g) > 3:
        #             pass
        #         else:
        #             grade_str +=g
        #     if len(grade_str) > 3:
        #         self.segment['grade'] = '-'
        #     else:
        #         self.segment['grade'] = grade_str

        # elif start < 3:
        #     grade_pattern = line[0:end+5]
        #     grade_list = grade_pattern.split()
        #     print(grade_list)
        #     grade_str = ''
        #     for g in grade_list:
        #         if re.search(r"[က-အ]|\-|[/]|grade",g) or len(g) > 3:
        #             pass
        #         else:
        #             grade_str +=g
        #     if len(grade_str) > 3:
        #         self.segment['grade'] = '-'
        #     else:
        #         self.segment['grade'] = grade_str

    # def get_grade(self,line):
    #     try:

    #         grade_ = re.sub(r'\s+',' ', line )  #remove special char
    #         grade_lst = grade_.split()
    #         print(grade_lst)
    #         grade = 0
    #         for g in grade_lst:
    #             if re.search("grade",g):
    #                 if re.search(r"[a-z]{3}\s*grade|[a-z]{2}\s*grade|[a-z]{1}\s*grade",g):
    #                     word = re.search(r"[a-z]{3}\s*grade|[a-z]{2}\s*grade|[a-z]{1}\s*grade",g).group()
    #                     grade = re.sub(r"grade","",word)

    #                 elif re.search(r"grade\s*[a-z]{3}|grade\s*[a-z]{2}|grade\s*[a-z]{1}",g):
    #                     word = re.search(r"grade\s*[a-z]{3}|grade\s*[a-z]{2}|grade\s*[a-z]{1}",g).group()
    #                     grade = re.sub(r"grade","",word)
    #                 else:
    #                     print("nth found")

    #             elif len(g) <=3 :
    #                 if re.search(r"[a-z]{3}|[a-z]{2}|[a-z]",g):
    #                     grade = re.search(r"[a-z]{3}|[a-z]{2}|[a-z]{1}",g).group()

    #             else:
    #                 pass

    #         # grade_str = re.sub('\W+','',grade)
    #         # if len(grade_str) <=3 :
    #         if grade != 0:
    #             self.segment['grade'] = grade
    #         else:
    #             self.segment['grade'] = '-'
    #     except:
    #         self.segment['grade'] = '-'

    def get_wheel_drive(self, line):
        try:
            drive_train = re.search(drive_reg, line).group()
            print(drive_train)
            self.segment['wheel_drive'] = re.search(
                r'\d', drive_train).group() + ' wheel'

        except:
            self.segment['wheel_drive'] = '-'

    def get_fuel(self, line):
        fuel_type = re.search(fuel_reg, line).group()
        if fuel_type == 'ဓာတ်ဆီ':
            self.segment['fuel'] = 'petrol'

        elif fuel_type == 'ဒီဇယ်':
            self.segment['fuel'] = 'diesel'

        else:
            self.segment['fuel'] = fuel_type

    def get_engine(self, line):
        engine = re.search(engine_reg, line).group()
        displacement = float(re.search(r"\d+(\.\d+)?", engine).group())
        if displacement < 100:
            displacement *= 1000
        self.segment['engine'] = str(int(displacement)) + ' cc'

    def get_price(self, line):
        try:
            mm_year_reg = r'[၁][၉][၀ဝ၁၂၃၄၅၆၇၈၉][၀ဝ၁၂၃၄၅၆၇၈၉]|[၂][၀ဝ][၀ဝ၁၂၃၄၅၆၇၈၉][၀ဝ၁၂၃၄၅၆၇၈၉]'
            line = re.sub(year_reg,'',line)
            line = re.sub(mm_year_reg,'',line)
            # print(line)
            price = re.search(price_reg, line).group()
            # print(price)
            # print(f"raw price ------------ > {price}")
            ### changing dollar to mm price ###
            if re.search(r"\$", price):
                price = re.sub(r",", "", price)
                dollar = re.search(r"\d+", price).group()
                # dollar price can be changed by the time
                mm_price = 1400 * int(dollar)
                price_lakhs = int(mm_price/100000)
                self.segment['price'] = str(price_lakhs) + "Lakhs"

            else:
                price = re.search(r"[၀ဝ၁၂၃၄၅၆၇၈၉]+|\d+", price).group()
                if len(price) > 1:
                    new_str = ''
                    for i in price:
                        if 4160 <= ord(i) <= 4170:
                            new_str += str(ord(i) % 10)
                        else:
                            new_str += i
                    
                    new_str = re.sub(r'[ဝ၀]','0',new_str) ### failed to change myanmar digits zero
                    self.segment['price'] = new_str+' Lakhs'

                else:
                    self.segment['price'] = '-'
        except Exception as e:
            # print(e)
            try:
                if re.search(r"သိိန်း|price|lakhs|lks|စျေး|သိန်း", price): 
                    # print(line)
                    digits = re.findall(r"[၀ဝ၁၂၃၄၅၆၇၈၉]+|\d+", line)
                    # print(digits)
                    if digits:
                        price = list(
                            filter(lambda digit: len(digit) <= 4, digits))
                        if price: ### continue operation if price is not empty otherwise pass to next iteration
                            price = price[0]
                            if len(price) < 2: ### we will pass if len price is too small
                                self.segment['price'] = '-' 
                            else:
                                new_str = ''
                                for i in price:
                                    if 4160 <= ord(i) <= 4170:
                                        new_str += str(ord(i) % 10)
                                    else:
                                        new_str += i
                                new_str = re.sub(r'[ဝ၀]','0',new_str)
                                self.segment['price'] = new_str + ' ' + 'Lakhs'
                        else:
                            self.segment['price'] = '-'
                    else:
                        self.segment['price'] = '-'
                else:
                    self.segment['price'] = '-'
            except:
                self.segment['price'] = '-'

    def get_mileage(self, line):
        if re.search(r'\d+\,\d+', line):  # 140,000
            self.segment['mileage'] = re.search(
                r'\d+\,\d+', line).group().replace(',', '') + ' km'

        elif re.search(r"(km|kilo|mileage|milage|ကိလို|ကီလို)\s*[-:/=]*\s*\d{5,6}|\d{5,6}\s*[-:/=]*\s*(km|kilo|mileage|milage|ကိလို|ကီလို)", line):
            mileage = re.search(r"(km|kilo|mileage|milage|ကိလို|ကီလို)\s*[-:/=]*\s*\d{5,6}|\d{5,6}\s*[-:/=]*\s*(km|kilo|mileage|milage|ကိလို|ကီလို)",line).group()
            self.segment['mileage'] = re.search(r'\d{5,6}',mileage).group()

        # elif re.search(r'\d+ \+|\d+\+', line):                          ## 150000 + , 150,000+
        #     self.segment['mileage'] = re.search(r'\d+ \+|\d+\+', line).group().strip('+').strip() + ' km'

        else:
            # print("Mileage not found !")
            try:
                # 1++++ , 3xxxxx, 4*****, 2 သိန်း
                array = re.search(
                    r'\d+\s*[+]+|\d+\s*[x]+|\d+\s*\*+|[(]*\d+[)]*\s*(သောင်း|သိန်း|သ်ိန်း)+', line).group() ### add '('and  ')' pattern
                # km = ''.join(array)
                km = re.sub("kilo", "", array)
                km = re.sub(" ", "", km)
                km = re.sub(r'[()]','',km) ### remove any '(' or ')'
                if km.find(',') >= 0:
                    mileage = km.replace(',', '')
                elif km.find('+') >= 0:
                    mileage = km.replace('+', '0')
                elif km.find('x') >= 0:
                    mileage = km.replace('x', '0')
                elif km.find('*') >= 0:
                    mileage = km.replace('*', '0')
                elif km.find('သောင်း') >= 0:
                    mileage = km.replace('သောင်း', '0000')
                elif km.find('သိန်း') >= 0:
                    mileage = km.replace('သိန်း', '00000')
                elif km.find("သ်ိန်း") >= 0:
                    mileage = km.replace('သ်ိန်း', '00000')
                else:
                    # print("nth found ")
                    mileage = km
                    # print(mileage)
                if len(mileage) < 7:
                    # print(mileage)
                    new_str = ''
                    for i in mileage:
                        if 4160 <= ord(i) <= 4170:
                            new_str += str(ord(i) % 10)
                        else:
                            new_str += i
                    self.segment['mileage'] = new_str+' km'

                else:
                    self.segment['mileage'] = '-'

            except Exception as e:
                self.segment['mileage'] = '-'

    def get_region(self, line):
        try:
            self.segment['region'] = re.search(region_reg, line).group()
        except:
            self.segment['region'] = '-'

    def get_gear(self, line):
        
        if (line.find('auto') > 0):
            self.segment['gear'] = 'auto'

        elif (line.find('manual') > 0):
            self.segment['gear'] = 'manual'

        else:
            print('gear not detected')
            self.segment['gear'] = '-'

    def get_seater(self, line):
        try:
            self.segment['seater'] = re.findall(r'\d', line)[0] + ' seats'

        except:
            self.segment['seater'] = '-'

    def get_drive_position(self, line):
        drive_postion = re.search(hand_reg, line).group()
        if drive_postion == 'ဘယ်မောင်း' or drive_postion == "l.h.d" or drive_postion == "lhd":
            self.segment['hand_drive'] = 'L.H.D'

        if drive_postion == 'ညာမောင်း' or drive_postion == "r.h.d" or drive_postion == "rhd":
            self.segment['hand_drive'] = 'R.H.D'

    def get_license(self, line):

        result = re.search(license_reg, line).group()
        if re.search(r"license|licence|လိုင်စင်", result):
            if re.search(r"\d[A-Za-z]|ygn|mdy|sgg|bgo|shn|npw|ayy|SHN|YGN|MDY|SGG|BGO", line):
                res = re.search(
                    r"\d[A-Za-z]|ygn|mdy|sgg|bgo|shn|npw|ayy|SHN|YGN|MDY|SGG|BGO", line).group()
                if re.search(r"\d[A-Za-z]", res):
                    res = res+"/****"
                    self.segment['licence_plate_no'] = res

                else:
                    self.segment['licence_plate_no'] = res

            else:
                self.segment['licence_plate_no'] = "-"
        else:
            self.segment['licence_plate_no'] = result.replace(" ", "")

    def get_phone(self, ph_list, line):
        phone_num = re.findall(ph_reg, line)
        for ph in phone_num:
            if re.search(mm_char, ph):
                ph_num = re.sub(" ", "", ph)
                ph_num = re.sub("-", "", ph_num)
                ph_num = re.sub("[.]", "", ph_num)
                x = u"{}".format(ph_num)
                ph_list.append(x)
            else:
                ph_num = re.sub(" ", "", ph)
                ph_num = re.sub("-", "", ph_num)
                ph_num = re.sub("[.]", "", ph_num)
                ph_num = re.sub("\+959", "09", ph_num)
                ph_list.append(ph_num)
