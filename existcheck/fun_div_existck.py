import requests
import json
import os
import time
import logging
from setup_log import setup_logger
import psycopg2
import datetime
    


def exist_check(token, src):
    
    dir_main = os.path.dirname(os.path.abspath(__name__))
    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'exist_check.log')

    if 'exist_ck' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('exist_ck')
    else:
        logger = setup_logger(log_file, 'exist_ck')


    try:
        if src == 'div':
            address = 'https://api.divar.ir/v8/posts-v2/web/'
            url = f"{address}{token}"
            response = requests.get(url)

        elif src == 'syp':
            address = 'https://www.sheypoor.com/api/v10.0.0/listings/'
            url = f"{address}{token}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)


        # بررسی وضعیت پاسخ
        if response.status_code == 404:
            current_date = datetime.date.today()
            exp_date = f"{current_date.day}-{current_date.month}-{current_date.year}"

            conn = psycopg2.connect(
                    host="localhost",
                    database="ads_realstate",
                    user= "sjd_admin",
                    password="1234"
                )

            cur = conn.cursor()
            if src == 'div':
                cur.execute("""UPDATE div_table
                            SET expired_date = %s
                            WHERE token = %s;""", (exp_date, token))
            elif src == 'syp':
                cur.execute("""UPDATE syp_table
                            SET expired_date = %s
                            WHERE token = %s;""", (exp_date, token))
                
            conn.commit()
            cur.close()
            conn.close()

            logger.info('expired date insert successfully')
    except:
        logger.exception('CAN NOT  INESERT EXPIRED DATE!\nERORR:')
