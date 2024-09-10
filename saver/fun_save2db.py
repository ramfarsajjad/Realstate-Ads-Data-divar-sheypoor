import json
import os
import csv
import time
import logging
import psycopg2
from psycopg2 import sql


def save2db(real_state):
    try:
        dir_main = os.path.dirname(os.path.abspath(__name__))

        dir_log = os.path.join(dir_main, 'logs')
        log_file = os.path.join(dir_log, 'save2db_log.log')
        logging.basicConfig(
            level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
        )

        logger = logging.getLogger(__name__)

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


        headers = [ "source","token","title","rent_sell","apartment_house","category","register_data",
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

        real_state = json.loads(real_state)
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
            logger.info('ADD TO DATABASE, SUCCESSFUL!')

        except:
            logger.error(f'{real_state["token"]} IS ALREADY EXISTS!')
            ar_conn.rollback()
            cur2.close()
            logger.exception(f'CAN NOT  ADD {real_state["token"]} TO DB!\nERORR:')

    
    except:
        logger.exception(f'CAN NOT  ADD {real_state["token"]} TO DB!\nERORR:')

