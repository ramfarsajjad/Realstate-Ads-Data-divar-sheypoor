import json
import os
import csv

from div_decnum_pass import decnum
from div_listdata_pass import listd_p
import time
import logging

dir_main = os.path.dirname(os.path.abspath(__name__))

dir_log = os.path.join(dir_main, 'logs')
log_file = os.path.join(dir_log, 'div_saver_log.log')
logging.basicConfig(
    level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
)

logger = logging.getLogger(__name__)




while True:

    dbfname = os.path.join(dir_main, 'agahi_div.csv')
    if os.path.isfile(dbfname):
        print(f"{dbfname} exists.")
    else:
        print(f"{dbfname} does not exist. created a new one")

    

    headers = ["token","title","rent/sell","apartment/house","category","register_data",
           "description","city","district","price","credit","rent",
           "business-type","image","build_date","room","meterage",
           "location","elevator","parking", "storage",
           "unitpf","tabaghe", "sanad","jahat","vaziat", "balkon",
           "wc", "jenskaff", "cooler", "heater", "tamin_hot_water"]
    
    real_state =  dict.fromkeys(headers)


    with open(dbfname, mode='w' , encoding='utf-8' , newline='') as file:
        writer = csv.DictWriter(file, fieldnames=real_state.keys())            
        writer.writeheader()



    directory = os.path.join(dir_main, 'archieved_files/lev2_parsed_ads/div_lev2_parsed_ads')

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
                "token" : data["details"]["token"],
                "title" : data["seo"]["web_info"]["title"],
                "rent/sell" : data["category"]["cat2"],
                "apartment/house" : data["category"]["cat3"],
                "category" : data["details"]["category"],
                "register_data" : data["seo"]["register_date"],
                "description" : data["seo"]["description"],
                "city" : data["details"]["city"],
                "district" : data["details"]["district"],
                "price" : data["details"]["price"],
                "credit": data["details"]["credit"],
                "rent" : data["details"]["rent"],
                "business-type" : data["details"]["business_type"],
                "image" : '',
                "build_date" :'' ,
                "room" : '' ,
                "meterage" : '' ,
                "location" : '',
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
            
            if not decnum(data, 'IMAGE') == None:
                real_state["image"] = data['sections'][decnum(data, 'IMAGE')]["IMAGE"]

            if not decnum(data, 'MAP') == None:
                if "type" in data['sections'][decnum(data, 'MAP')]["MAP"]:
                    real_state['location'] = data['sections'][decnum(data, 'MAP')]["MAP"]["fuzzy_data"]["point"]
                else:
                    real_state['location'] = data['sections'][decnum(data, 'MAP')]["MAP"]["exact_data"]["point"]

            if not decnum(data, 'LIST_DATA') == None:
                real_state.update(listd_p(data['sections'][decnum(data, 'LIST_DATA')]['LIST_DATA'], real_state))



        # نوشتن فایل CSV
            with open(dbfname, mode='a' , encoding='utf-8' , newline='') as file: 
                writer = csv.DictWriter(file, fieldnames=real_state.keys())
                writer.writerow(real_state)

            logger.info('ADD TO DIV CSV, SUCCESSFUL!')

        except:
            logger.exception(f'CAN NOT  ADD {real_state["token"]} TO DIV CSV!\nERORR:')


    time.sleep(90)