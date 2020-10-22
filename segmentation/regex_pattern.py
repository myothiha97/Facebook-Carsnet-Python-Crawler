import re
zawgyiReg = '\u1031\u103b|^\u1031|^\u103b|[\u1022-\u1030\u1032-\u1039\u103b-\u103d\u1040-\u104f]\u103b|\u1039$|\u103d\u103c|\u103b\u103c|[\u1000-\u1021]\u1039[\u101a\u101b\u101d\u101f\u1022-\u102a\u1031\u1037-\u1039\u103b\u1040-\u104f]|\u102e[\u102d\u103e\u1032]|\u1032[\u102d\u102e]|[\u1090-\u1099][\u102b-\u1030\u1032\u1037\u103c-\u103e]|[\u1000-\u102a]\u103a[\u102c-\u102e\u1032-\u1036]|[\u1023-\u1030\u1032-\u1039\u1040-\u104f]\u1031|[\u107e-\u1084][\u1001\u1003\u1005-\u100f\u1012-\u1014\u1016-\u1018\u101f]|\u1025\u1039|[\u1081\u1083]\u108f|\u108f[\u1060-\u108d]|[\u102d-\u1030\u1032\u1036\u1037]\u1039|\u102c\u1039|\u101b\u103c|[^\u1040-\u1049]\u1040\u102d|\u1031?\u1040[\u102b\u105a\u102e-\u1030\u1032\u1036-\u1038]|\u1031?\u1047[\u102c-\u1030\u1032\u1036-\u1038]|[\u102f\u1030\u1032]\u1094|\u1039[\u107E-\u1084]'
# zawgyiReg2 =  '\u102c\u1039', '\u103a\u102c', \s.'(\u103b|\u1031|[\u107e-\u1084])[\u1000-\u1021]','^(\u103b|\u1031|[\u107e-\u1084])[\u1000-\u1021]', '[\u1000-\u1021]\u1039[^\u1000-\u1021]', '\u1025\u1039' ,'\u1039\u1038' ,'[\u102b-\u1030\u1031\u103a\u1038](\u103b|[\u107e-\u1084])[\u1000-\u1021]' ,'\u1036\u102f','[\u1000-\u1021]\u1039\u1031' , '\u1064','\u1039' . self::WHITESPACE, '\u102c\u1031','[\u102b-\u1030\u103a\u1038]\u1031[\u1000-\u1021]', '\u1031\u1031', '\u102f\u102d', '\u1039$'
mm_char = "\u1040|\u1041|\u1042|\u1043|\u1044|\u1045|\u1046|\u1047|\u1048|\u1049"
make_reg = r'acura|audi|bentley|bmw|buick|cadillac|chevrolet|chrysler|citeron|dodge|daihatsu|fiat|ford|gmc|honda|hyundai|infiniti|jaguar|jeep|kia|land rover|lexus|lincoln|maserati|mazada|mazda|mercedes|mini|mitsubishi|mitsubshi|nissan|peugeot|range rover|renault|subaru|suzuki|tesla|toyota|vauxhall|volkswagen|volvo|hillix|isuzu|ferrari|mercedes-benz'
# except_reg    = r'\W+|luxury|sedan|hatchback|hybrid|coupe|suv|convertible|minivan|wagon|pickup|truck|mingalar|myanmar|brand|[က-အ]+'
# model_reg = r'model'
grade_reg = r'grade'
year_reg = r'[1][9][9][0-9]|[2][0][0-9][0-9]|model|year'
engine_reg = r'\d{4} cc|\d{4}. cc|\d{4}cc|\d{4}.cc|[1-4]\.[0-9] cc|[1-4]\.[0-9]. cc|[1-4]\.[0-9]cc|1-4]\.[0-9].cc|\b[1-4]\.[0-9]\b|\d\.\d CC'
color_reg = r'pearl white|black|dark grey|white|silver|gray|blue'
body_reg = r'sedan|hatchback|hybrid|coupe|suv|convertible|minivan|wagon|pickup|truck'
# drive_reg     = r'4x4|\dw|\dwd|\d wd|\d wheel||\dwheel|\dweel|\d weel|\dWD|\d WD|\d[.]*\s*wd'
drive_reg = r"4x4|\d\s*w\s*d|\d\s*W\s*D|\d\s*wheel|\d[.]*\s*w\s*d|\d\s*weel|\d\s*w|\d\s*W"
fuel_reg = r'diesel|petrol|ဓာတ်ဆီ|ဒီဇယ်'
mileage_reg = r'km|kilo|mileage|milage|ကိလို|ကီလို'
gear_reg = r'auto|manual|gear'
region_reg = r'ygn|mdy|shn|sgg|bgo|npw|ayy|rke|kyn|chn'
seater_reg = r'seater|seaters|seating'
hand_reg = r'ဘယ်မောင်း|ညာမောင်း|l.h.d|r.h.d|lhd|rhd'
# license_reg   = r'number|license|licence|လိုင်စင်|ygn|mdy|sgg|bgo|'
license_reg = r"\d\s*[a-z]\s*\-\s*\d{4}|\d\s*[a-z]\s*[/]\s*\d{4}|\d\s*[a-z]\s*[/]\s*\d{4}|\d\s*[a-z]\s*[-/ ]\s*(ygn|mdy|shn|sgg|bgo|npw|ayy|rke|kyn|chn)|\d\s*[A-Za-z]\s*[-/ ]*\s*\([A-Za-z]+\)|\d\s*[A-Za-z]\s*[-/ ]\s*[*.+x]+|license|licence|လိုင်စင်"
price_reg = r'သိိန်း\s*[၀ဝ၁၂၃၄၅၆၇၈၉]+|[၀ဝ၁၂၃၄၅၆၇၈၉]+\s*သိိန်း|\$\s*\d+\,\d+|\d+\s*သိိန်း|သိိန်း\s*\d+|\d+\s*lakhs|lakhs\s*\d+|စျေး\s*\=*\s*\d+|စျေး\s*\=*\s*[၀ဝ၁၂၃၄၅၆၇၈၉]+|စျေး\s*\-*\s*\d+|စျေး\s*\-*\s*[၀ဝ၁၂၃၄၅၆၇၈၉]+|\d+\s*lhks|lhks\s*\d+|ဈေးနူန်း\s*\=*\s*[၀ဝ၁၂၃၄၅၆၇၈၉]+|ဈေးနူန်း\s*\=*\s*\d+|ဈေးနူန်း\s*\-*\s*[၀ဝ၁၂၃၄၅၆၇၈၉]+|ဈေးနူန်း\s*\-*\s*\d+|စျေးနှုန်း\s*[-= ]*\s*\d+|\d+\s*lks|lks\s*\d+|သိိန်း|price|lakhs|lks|စျေး|သိန်း'
ph_reg = r"09-\d{9}|09\s*\d{9}|၀၉[၀-၉]{9}|၀၉-[၀-၉]{9}|09-\d{7}|09\s*\d{7}|၀၉[၀-၉]{7}|၀၉-[၀-၉]{7}|09\s*\d{3}\s*\d{3}\s*\d{3}|\+959\s*\d{9}|\+959\s*\d{7}|09[.]*\d{9}|09[.]*\d{7}|09\s*\d{4}\s*\d{3}\s*\d{2}|09\s*\d{3}\s*\d{4}|\+959\s*-\s*\d{9}|\+959\s*-\s*\d{7}|09\d{2}\s*\d{3}\s*\d{4}"

raw_car_models = '''markII,mark2,alphard,
Landcrusier,wish,caldina,succeed,
fielder,brevis,ractis,kluger,
vitz,harrier,rav4,rush,noah,celsior,
axio,hilux,corolla,crown,fortuner,insight,crv,fit,odyssey,civic,ciaz,swift,ertiga,solio,x4.x6,730,i3,750i,x5,320i,
530i,demio,bt-50,biante,titan,
axela,rx-8,starex,sonata,grandeur,tucson,
grandstarex,starex,grand,accent,
sportage,rio,optima,carnival,sorento,picanto,carens,k3,bentayaga,q8,a4,a3,q7,a1,a7,srx,escalade,explorer,f150,everest,ranger,
focus,edge,transit,forester,xe,e-pace,lx570,rx350,gs200t,rx300,
nx300,ls460,gs350,nx200t,
levante,e300,s550,c180,e200,a200,
b180,slk350,e320,gl350,gl450,
c300,glc250,b170,glc300,e250,
rvr,pajero,mirage,colt,delica,
outlander,fuso,asx,eclipse,
x-trail,sunny,qashqai,wingroad,juke,elgrand,cedric,advan,van,
navara,rogue,model3,modelx,xc90,xc60,v40,bighorn,elf,d-max,dmax,wizard,trooper'''
raw_models = re.sub(r'\n', '', raw_car_models)
# print(raw_models)
models = re.sub(r'[,]', '|', raw_models)
models = models.strip()

# print(models)
if __name__ == "__main__":
    ''' Testing '''
    test_string = """အရောင်း အလဲထပ် ပြပါ
iR.V & Fair Lady ထဲက ပြပါ
အလိုက်ပေးလဲမယ် Caldina Gt4 2002 2.0 Turbo Modify စက်ရုပ် လေး Wheel Tex မှာ ဒီရုပ်ပေါက်တယ်နော်
၁၈ဝ သိန်း

. . . . . . . . . . . . . . . . . . . . .
Wish 2003 XS Grade အမှန်
M တန်း နံပါတ်နဲ့တင် ကြွေလို့ရတယ် Pearl White ကားအလွန်သန့် 1.8 Cc
၂ဝ၉ သိိန်း
ဖုန်း 09450029089"""
    
    # if re.search(models, test_string.lower()):
    #     print(re.search(models, test_string.lower()).group())
    #     print("is working")

    if re.search(price_reg,test_string):
        print('pattern found')
        print(re.search(price_reg,test_string).group())
    
