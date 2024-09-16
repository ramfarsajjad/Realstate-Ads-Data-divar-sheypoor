import os
import json
from plus_cleaning_section import p_clean_sec
import time
import logging
from setup_log import setup_logger


# چاپ نام فایل‌ها
def div_parser2(data):
    
    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'div_parser_lev2.log')

    if 'logger_div_pars2' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_div_pars2')
    else:
        logger = setup_logger(log_file, 'logger_div_pars2')

    try:
        data = json.loads(data)
        token = data["details"]["token"]
        p_clean_sec(data)
        
        directory = os.path.join(dir_main, 'archieved_files/lev2_parsed_ads/div_lev2_parsed_ads')    
        careful_cleaned_file_name = os.path.join(directory, f'cc_{token}.json')

        with open(careful_cleaned_file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


        logger.info('DIV SUPER! cleanup carefully')

        return data

    except:
        logger.exception(f'DIV {token} CAN NOT CAREFULLY CLEANUP!\nERORR:')

        return None
    
