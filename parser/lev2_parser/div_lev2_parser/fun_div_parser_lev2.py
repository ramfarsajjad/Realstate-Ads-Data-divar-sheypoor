import os
import json
from plus_cleaning_section import p_clean_sec
import time
import logging

dir_main = os.path.dirname(os.path.abspath(__name__))

dir_log = os.path.join(dir_main, 'logs')
log_file = os.path.join(dir_log, 'div_parser_lev2_log.log')
logging.basicConfig(
    level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
)

logger = logging.getLogger(__name__)


# چاپ نام فایل‌ها
def div_parser2(data):
    
    try:
        data = json.loads(data)
        token = data["details"]["token"]
        p_clean_sec(data)
        
        directory = os.path.join(dir_main, 'archieved_files/lev2_parsed_ads/div_lev2_parsed_ads')    
        careful_cleaned_file_name = os.path.join(directory, f'cc_{token}')

        with open(careful_cleaned_file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


        logger.info('DIV SUPER! cleanup carefully')

        return data

    except:
        logger.exception(f'DIV {token} CAN NOT CAREFULLY CLEANUP!\nERORR:')

        return None
    
