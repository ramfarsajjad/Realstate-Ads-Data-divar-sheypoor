import requests
import json
import csv
import codecs
import os
from syp_safe_clean import data_cleaner
from syp_safe_clean import image_cleaner
from syp_safe_clean import prop_cleaner
from syp_safe_clean import categ_cleaner
import time
import logging
from setup_log import setup_logger


    # URL API
def syp_parser2(data):

    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'syp_parser_lev2.log')

    if 'logger_syp_pars2' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_syp_pars2')
    else:
        logger = setup_logger(log_file, 'logger_syp_pars2')


    try:
        data = json.loads(data)
        token = data["main"]["id"]
        data_cleaner(data)
        data['main']['location'] = data['schema']['mainEntity'].pop('geo')
        data.pop('schema')
        image_cleaner(data)
        prop_cleaner(data)
        categ_cleaner(data)
        data['main']['location'].pop('@type')
        data['main']['location'].pop('address')


        directory = os.path.join(dir_main, 'archieved_files/lev2_parsed_ads/syp_lev2_parsed_ads')
        careful_cleaned_file_name = os.path.join(directory, f'cc_{token}.json')

        with open(careful_cleaned_file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        logger.info('SHEYP SUPER! cleanup carefully')

        return data

    except:
        logger.exception(f'SHEYP {token} CAN NOT CAREFULLY CLEANUP!\nERORR:')

        return None