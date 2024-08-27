import json
import os
import csv
from div_decnum_pass import decnum
from div_listdata_pass import listd_p
import time
import logging
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user= "sjd_admin",
    password="1234"
)

conn.autocommit = True

cur = conn.cursor()

cur.execute("select 1 from pg_database where datname = 'ads_realstate';")

database_exists = cur.fetchone()
if not database_exists:
    cur.execute("create database ads_realstate")
conn.autocommit = False
cur.close()
conn.close()

ar_conn= psycopg2.connect(
    host="localhost",
    database="ads_realstate",
    user= "sjd_admin",
    password="1234"
)
cur1 = ar_conn.cursor()


headers = ["token","title","rent_sell","apartment_house","category","register_data",
           "description","province", "city","district","price","credit","rent",
           "business_type","image","build_date","room","meterage",
           "location","elevator","parking", "storage",
           "unitpf","tabaghe", "sanad","jahat","vaziat", "balkon",
           "wc", "jenskaff", "cooler", "heater", "tamin_hot_water"]

cur1.execute("""SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_name = 'rs_table'
); """)

table_exists = cur1.fetchone()[0]
if not table_exists:
    cur1.execute("create table rs_table(id serial)")
    for item in headers:
        cur1.execute(f"""alter table rs_table
                     add {item} text;
                     """)
        ar_conn.commit()

    cur1.execute("""alter table rs_table
             add primary key(token);
             """)
ar_conn.commit()
cur1.close()

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

    real_state =  dict.fromkeys(headers)

    directory = os.path.join(dir_main, 'archieved_files/lev2_parsed_ads/div_lev2_parsed_ads')

    # لیست تمام فایل‌ها و پوشه‌ها در مسیر مشخص‌شده
    all_files_and_dirs = os.listdir(directory)

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
                "rent_sell" : data["category"]["cat2"],
                "apartment_house" : data["category"]["cat3"],
                "category" : data["details"]["category"],
                "register_data" : data["seo"]["register_date"],
                "description" : data["seo"]["description"],
                "province" : '',
                "city" : data["details"]["city"],
                "district" : data["details"]["district"],
                "price" : data["details"]["price"],
                "credit": data["details"]["credit"],
                "rent" : data["details"]["rent"],
                "business_type" : data["details"]["business_type"],
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
                # url_txt = ',\n'.join(real_state["image"])
                real_state["image"] = str(real_state["image"])


            if not decnum(data, 'MAP') == None:
                if "type" in data['sections'][decnum(data, 'MAP')]["MAP"]:
                    real_state['location'] = data['sections'][decnum(data, 'MAP')]["MAP"]["fuzzy_data"]["point"]
                else:
                    real_state['location'] = data['sections'][decnum(data, 'MAP')]["MAP"]["exact_data"]["point"]
                # map_txt = ',\n'.join(f"{key}: {value}" for key, value in real_state["location"].items())
                real_state["location"] = str(real_state["location"])

            if not decnum(data, 'LIST_DATA') == None:
                real_state.update(listd_p(data['sections'][decnum(data, 'LIST_DATA')]['LIST_DATA'], real_state))



            columns = real_state.keys()
            values = [real_state[column] for column in columns]

            insert_query = sql.SQL("INSERT INTO rs_table ({}) VALUES ({})").format(
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )
            cur2 = ar_conn.cursor()

            try:
                cur2.execute(insert_query, values)
                ar_conn.commit()
                cur2.close()

            except:
                logger.error(f'DIV {real_state["token"]} IS ALREADY EXISTS!')
                ar_conn.rollback()
                cur2.close()

                continue


            logger.info('ADD TO DIV ‌DATABASE, SUCCESSFUL!')

        except:
            logger.exception(f'CAN NOT  ADD {real_state["token"]} TO DIV CSV!\nERORR:')


    time.sleep(90)