import json
import os
import csv
from syp_secfind import dicfdr
from syp_decnum_pass import decnum
import time
import logging

dir_main = os.path.dirname(os.path.abspath(__name__))

dir_log = os.path.join(dir_main, 'logs')
log_file = os.path.join(dir_log, 'syp_saver_log.log')
logging.basicConfig(
    level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
)

logger = logging.getLogger(__name__)




while True:
    
    dbfname = os.path.join(dir_main, 'agahi_sheyp.csv')
    if os.path.isfile(dbfname):
        print(f"{dbfname} exists.")
    else:
        print(f"{dbfname} does not exist. created a new one")

        

    headers = ["token","title","rent/sell","apartment/house","category","register_data",
            "description","province", "city","district","price","credit","rent",
            "business-type","image","build_date","room","meterage",
            "location","elevator","parking", "storage",
            "unitpf","tabaghe", "sanad","jahat","vaziat", "balkon",
            "wc", "jenskaff", "cooler", "heater", "tamin_hot_water"]
        
    real_state =  dict.fromkeys(headers)

    with open(dbfname, mode='w' , encoding='utf-8' , newline='') as file:
        writer = csv.DictWriter(file, fieldnames=real_state.keys())            
        writer.writeheader()



    directory = os.path.join(dir_main, 'archieved_files/lev2_parsed_ads/syp_lev2_parsed_ads')

    # لیست تمام فایل‌ها و پوشه‌ها در مسیر مشخص‌شده
    all_files_and_dirs = os.listdir(directory)
    # فیلتر کردن فایل‌ها (حذف پوشه‌ها)
    all_files = [f for f in all_files_and_dirs if os.path.isfile(os.path.join(directory, f))]


    for cc_file in all_files:
        try:                
            
            cleaned_file_name = os.path.join(directory, f'{cc_file}')
            # cleaned_file_name = os.path.join(directory, 'cc_gZdqjt6v.json')
        
            # خواندن فایل JSON
            with open(cleaned_file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            real_state = {
                "token" : data["main"]["id"],
                "title" : data["seo"]["title"],
                "rent/sell" :'',
                "apartment/house" : '',
                "category" : '',
                "register_data" : '',
                "description" : data["seo"]["description"],
                "province" : data['main']['category'][decnum(data['main']['category'], 'region')]['region'],
                "city" : data['main']['category'][decnum(data['main']['category'], 'city')]['city'],
                "district" : '',
                "price" : '',
                "credit": '',
                "rent" : '',
                "business-type" : '',
                "image" : data['main']['IMAGE'],
                "build_date" :'' ,
                "room" : '' ,
                "meterage" : '' ,
                "location" : data['main']['location'],
                "elevator" : '',
                "parking" : '',
                "storage" : '',
                "unitpf" : '',
                "tabaghe" : '',
                "sanad" : '',
                "jahat" : '',
                "vaziat": '',
                "balkon" : '',
                "wc" : '',
                "jenskaff" : '',
                "cooler" : '',
                "heater" : '',
                "tamin_hot_water" : ''

                
            }
            
            if not decnum(data['main']['category'], 'category_2') == None:
                real_state['category'] = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2']
                word = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2'].split()
                if word[-1] == 'ویلا':
                    real_state["apartment/house"] = 'house'
                elif word[-1] == 'آپارتمان':
                    real_state["apartment/house"] = 'apartment'
                else:
                    real_state['apartment/house'] = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2']
                if word[0] == 'رهن':
                    real_state["rent/sell"] = 'rent'
                elif word[0] == 'خرید':
                    real_state["rent/sell"] = 'sell'
                else:
                    real_state["rent/sell"] = data['main']['category'][decnum(data['main']['category'], 'category_2')]['category_2']

            if not decnum(data['main']['category'], 'neighbourhood') == None:
                real_state["district"] = data['main']['category'][decnum(data['main']['category'], 'neighbourhood')]['neighbourhood']   

            if real_state['rent/sell'] == 'sell':
                real_state['price'] = data['main']['price'][0]['amount']
            elif real_state['rent/sell'] == 'rent':
                if not decnum(data['main']['property'], 'رهن') == None:
                    word = data['main']['property'][decnum(data['main']['property'], 'رهن')]['رهن'].split()
                    real_state['credit'] = word[0]
                if not decnum(data['main']['property'], 'اجاره') == None:
                    word = data['main']['property'][decnum(data['main']['property'], 'اجاره')]['اجاره'].split()
                    real_state['rent'] = word[0]

            if not decnum(data['main']['property'], 'سن بنا') == None:
                    word = data['main']['property'][decnum(data['main']['property'], 'سن بنا')]['سن بنا'].split()            
                    if word[0] == 'نوساز':
                        word[0] = 0
                    elif word[0] == 'بیشتر':
                        word[0] = 33
                    b_date = 1403 - int(word[0])
                    real_state['build_date'] = b_date

            if not decnum(data['main']['property'], 'تعداد اتاق') == None:
                real_state['room'] = int(data['main']['property'][decnum(data['main']['property'], 'تعداد اتاق')]['تعداد اتاق'])

            if not decnum(data['main']['property'], 'متراژ') == None:
                real_state['meterage'] = data['main']['property'][decnum(data['main']['property'], 'متراژ')]['متراژ']

            if not decnum(data['main']['property'], 'آسانسور') == None:
                real_state['elevator'] = data['main']['property'][decnum(data['main']['property'], 'آسانسور')]['آسانسور']

            if not decnum(data['main']['property'], 'پارکینگ') == None:
                real_state['parking'] = data['main']['property'][decnum(data['main']['property'], 'پارکینگ')]['پارکینگ']    

            if not decnum(data['main']['property'], 'انباری') == None:
                real_state['storage'] = data['main']['property'][decnum(data['main']['property'], 'انباری')]['انباری']



        # نوشتن فایل CSV
            with open(dbfname, mode='a' , encoding='utf-8' , newline='') as file: 
                writer = csv.DictWriter(file, fieldnames=real_state.keys())
                writer.writerow(real_state)

            logger.info('ADD TO SHEYP CSV, SUCCESSFUL!')


        except:
            logger.exception(f'CAN NOT  ADD {real_state["token"]} TO SHEYP CSV!\nERORR:')

    time.sleep(90)
