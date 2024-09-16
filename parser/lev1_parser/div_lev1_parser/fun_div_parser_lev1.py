import requests
import json
import csv
import codecs
import os
from div_decode import decode_unicode
from div_secfind import dicfdr
from div_cleaning_section import section_cleaner
from div_cleaning_section import section_basic_clean
from div_cleaning_section import listdata_basic_clean
from div_record_date import rec_date
import time
import logging
from setup_log import setup_logger

    



# URL API
def div_parser1(token):

    dir_main = os.path.dirname(os.path.abspath(__name__))
    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'div_parser_lev1.log')

    if 'logger_div_pars1' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_div_pars1')
    else:
        logger = setup_logger(log_file, 'logger_div_pars1')

    
    try:
        
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
            data['sc_time'] = time.time()

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
            
            return data


            

        else:
            print(f'Error fetching data: {response.status_code}')
            return None
            
    except:
        logger.exception(f'CAN NOT  PARSE {token} DIV DATA!\nERORR:')
        return None


