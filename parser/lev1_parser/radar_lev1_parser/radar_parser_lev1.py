import requests
import json
import csv
import codecs
import os
import time
import logging

dir_main = os.path.dirname(os.path.abspath(__name__))

dir_log = os.path.join(dir_main, 'logs')
log_file = os.path.join(dir_log, 'div_parser_lev1_log.log')
logging.basicConfig(
    level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
)

logger = logging.getLogger(__name__)

while True:

    tok_dir_file = os.path.join(dir_main, 'scraper')
    TokFile = os.path.join(tok_dir_file, 'div_tokbase.json')
    with open(TokFile, 'r') as file:
        tokcell = json.load(file)

    # URL API
    for token in tokcell:

        try:
            exist_tok_directory = os.path.join(dir_main, 'archieved_files/scraped_ads/div_scraped_ads')
            exist_tok = os.path.join(exist_tok_directory, f'check_{token}.json')
            if os.path.isfile(exist_tok):
                continue

            token.split(',')
            address = 'https://api.divar.ir/v8/posts-v2/web/'

            url = f"{address}{token}"
            # url = 'https://api.divar.ir/v8/posts-v2/web/gZ3WGNlB'

            response = requests.get(url)

            # بررسی وضعیت پاسخ
            if response.status_code == 200:
                
                data = response.json()
                
                jdata = json.dumps(data, ensure_ascii=False)


                check_directory = os.path.join(dir_main, 'archieved_files/scraped_ads/div_scraped_ads')
                check_file_name = os.path.join(check_directory, f'check_{token}.json')

                f = open(check_file_name, "w", encoding='utf-8')
                f.write(jdata)
                f.close()
                

                with open(check_file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                

                data.pop('share', None)
                data.pop('contact', None)
                spamkey_webengg = ['brand_model', 'status', 'gender', 'originality', 'cat_1', 'cat_2', 'cat_3']
                for key in spamkey_webengg:
                    data['webengage'].pop(key, None)

                data['category'] = data.pop('analytics', None)

                spamkey_seo = ['android_package_name', 'android_app_url']
                for key in spamkey_seo:
                    data['seo'].pop(key, None)

                data['category'] = data.pop('category', None)
                data['details'] = data.pop('webengage', None)

                section_basic_clean(data['sections'])
                listdata_basic_clean(data['sections'])
                rec_date(data['seo'])


                section_cleaner(data['sections'], 'MAP')
                section_cleaner(data['sections'], 'BUSINESS_SECTION')
                section_cleaner(data['sections'], 'IMAGE')


                directory = os.path.join(dir_main, 'archieved_files/lev1_parsed_ads/div_lev1_parsed_ads')
                cleaned_file_name = os.path.join(directory, f'{token}.json')

                with open(cleaned_file_name, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                # with open('testclean.json', 'w', encoding='utf_8') as file:
                #     json.dump(newdata, file, ensure_ascii=False, indent=4)
                #     file.write('\n')
                    

                logger.info('clean up div')


                

            else:
                print(f'Error fetching data: {response.status_code}')
                
        except:
            logger.exception(f'CAN NOT  PARSE {token} DIV DATA!\nERORR:')

    time.sleep(60)

