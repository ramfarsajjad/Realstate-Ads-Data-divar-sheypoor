import requests
import json
import csv
import codecs
import os
from syp_safe_clean import data_cleaner
import time
import logging
from setup_log import setup_logger

    

def syp_parser1(token):

    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'syp_parser_lev1.log')

    if 'logger_syp_pars1' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_syp_pars1')
    else:
        logger = setup_logger(log_file, 'logger_syp_pars1')

    try:     
        address = 'https://www.sheypoor.com/api/v10.0.0/listings/'
        url = f"{address}{token}"
        # url = 'https://www.sheypoor.com/api/v10.0.0/listings/441454780'

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            
            data = response.json()
            
            jdata = json.dumps(data, ensure_ascii=False)


            check_directory = os.path.join(dir_main, 'archieved_files/scraped_ads/syp_scraped_ads')
            check_file_name = os.path.join(check_directory, f'check_{token}.json')

            f = open(check_file_name, "w", encoding='utf-8')
            f.write(jdata)
            f.close()
            

            with open(check_file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
            

            data['schema'] = json.loads(data['meta']['seo']['schema'].pop(0))
            data.pop('jsonapi')
            data.pop('links')
            data['meta']['seo'].pop('meta')
            data['meta']['seo'].pop('links')
            data['meta']['seo'].pop('schema')
            data['seo'] = data['meta'].pop('seo')
            data.pop('meta')
            data['main'] = data.pop('data')
            data['sc_time'] = time.time()
            # data_cleaner(data)



            directory = os.path.join(dir_main, 'archieved_files/lev1_parsed_ads/syp_lev1_parsed_ads')
            cleaned_file_name = os.path.join(directory, f'{token}.json')

            with open(cleaned_file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            logger.info('clean up sheyp')

            return data

        else:
            print(f'Error fetching data: {response.status_code}')
            return None
                        

    except:
        logger.exception(f'CAN NOT  PARSE {token} SHEYP DATA!\nERORR:')
        return None

