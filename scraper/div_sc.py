import requests
import json
from pprint import pprint
import csv
import os
import time
import logging
from datetime import datetime, timezone, timedelta

dir_main = os.path.dirname(os.path.abspath(__name__))

dir_log = os.path.join(dir_main, 'logs')
log_file = os.path.join(dir_log, 'div_sc_log.log')
logging.basicConfig(
    level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
)

logger = logging.getLogger(__name__)

# URL API
page_num = 0
count_day = 0
count_hours = 2
now = datetime.now(timezone.utc)
cur_date = now - timedelta(hours = count_hours)
formatted_date = cur_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

while True:
    try:
        page_num += 1
        if page_num > 3:
            count_hours += 1
            page_num = 1
            if count_hours > 24:
                now = now - timedelta(days = 1)
                count_hours = 0
                count_day += 1
            cur_date = now - timedelta(hours= count_hours)
            formatted_date = cur_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            
        if count_day > 30:
            break

        url = 'https://api.divar.ir/v8/postlist/w/search'

            

        
        print(f'page = {page_num}\n date = {formatted_date}')

        payload = {"city_ids":["1767"],"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData",
                                                          "last_post_date":formatted_date,
                                                          "page":page_num,"layer_page":page_num,
                                                          "search_uid":"b9d21a49-88e0-4937-9e29-01bc4635b658"},
                                                          "search_data":{"form_data":{"data":{"category":{"str":{"value":"real-estate"}}}},"server_payload":{"@type":"type.googleapis.com/widgets.SearchData.ServerPayload","additional_form_data":{"data":{"sort":{"str":{"value":"sort_date"}}}}}}}

        # ارسال درخواست GET به URL مشخص شده
        response = requests.post(url, json= payload)

        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            # تبدیل داده‌های دریافتی به فرمت JSON
            data = response.json()
            # چاپ داده‌ها
            # pprint(data)/home/sjd/Desktop/Realstate-Ads-Data-divar-sheypoor-/sc_ads/
            api_dir = os.path.join(dir_main, "archieved_files/api_firstpage/div_api_firstpage")
            all_api_files_and_dirs = os.listdir(api_dir)
            all_api_files = [f for f in all_api_files_and_dirs if os.path.isfile(os.path.join(api_dir, f))]
            api_name = os.path.join(api_dir, f"apidiv{len(all_api_files)}.json")
            try:
                with open(api_name, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(e)


            dir_tokfile = os.path.join(dir_main, 'scraper')
            myfile = os.path.join(dir_tokfile, "div_tokbase.json")
            if os.path.isfile(myfile):
                print(f"{myfile} exists.")
                with open(myfile, 'r') as file:
                    tokcell = json.load(file)
                    bdata = set(tokcell)
            else:
                print(f"{myfile} is not exists. created a new one")
                bdata = set()


            newtok = set(data["action_log"]["server_side_info"]["info"]["tokens"])
            bdata.update(newtok)

            setdata_list = list(bdata)

            # f = open('a1.json', "a+")
            # f.write(json.dumps(data))
            # f.close()

            f = open(myfile , "w")
            f.write(json.dumps(setdata_list))
            f.close()


            logger.info('div tokens downloaded successfully')
            if data['pagination']['has_next_page'] == False:
                break
            
        else:
            print(f'Error fetching data: {response.status_code}')

        
        

    except:
        logger.exception('CAN NOT  DOWNLOAD DIV TOKENS!\nERORR:')

    time.sleep(0.1)
