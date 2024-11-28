import json
import os
import csv
import time
import logging
import psycopg2
from psycopg2 import sql
from setup_log import setup_logger

def save2db(real_state):
    try:
        dir_main = os.path.dirname(os.path.abspath(__name__))

        dir_log = os.path.join(dir_main, 'logs')
        log_file = os.path.join(dir_log, 'save2db.log')
        
        if 'logger_save2db' in logging.Logger.manager.loggerDict:
            logger = logging.getLogger('logger_save2db')
        else:
            logger = setup_logger(log_file, 'logger_save2db')

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

        headers = [ "source","token","sc_time", "title","rent_sell","apartment_house","category","register_data",
                    "description","province", "city","district","price","credit","rent",
                    "business_type","image","build_date","room","meterage",
                    "location","elevator","parking", "storage",
                    "unitpf","tabaghe", "sanad","jahat","vaziat", "balkon",
                    "wc", "jenskaff", "cooler", "heater", "tamin_hot_water", "expired_date"]

        real_state = json.loads(real_state)
        columns = real_state.keys()
        values = [real_state[column] for column in columns]

        if real_state['source'] == 'divar':
            cur1 = ar_conn.cursor()            
            cur1.execute("""SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'div_table'
            ); """)

            table_exists = cur1.fetchone()[0]
            if not table_exists:
                cur1.execute("create table div_table(id serial)")
                for item in headers:
                    cur1.execute(f"""alter table div_table
                                add {item} text;
                                """)
                    ar_conn.commit()

                cur1.execute("""alter table div_table
                        add primary key(token);
                        """)
                
            ar_conn.commit()
            insert_query = sql.SQL("INSERT INTO div_table ({}) VALUES ({})").format(
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )
            cur1.close()


        elif real_state['source'] == 'sheypoor':
            cur1 = ar_conn.cursor()
            cur1.execute("""SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'syp_table'
            ); """)

            table_exists = cur1.fetchone()[0]
            if not table_exists:
                cur1.execute("create table syp_table(id serial)")
                for item in headers:
                    cur1.execute(f"""alter table syp_table
                                add {item} text;
                                """)
                    ar_conn.commit()

                cur1.execute("""alter table syp_table
                        add primary key(token);
                        """)
            ar_conn.commit()
            insert_query = sql.SQL("INSERT INTO syp_table ({}) VALUES ({})").format(
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )
            cur1.close()
            
        
        try:
            cur1 = ar_conn.cursor()
            cur1.execute(insert_query, values)
            ar_conn.commit()
            cur1.close()
            logger.info('ADD TO DATABASE, SUCCESSFUL!')

        except:
            logger.error(f'{real_state["token"]} IS ALREADY EXISTS!')
            ar_conn.rollback()
            cur1.close()
            logger.exception(f'CAN NOT  ADD {real_state["token"]} TO DB!\nERORR:')

        ar_conn.close

    
    except:
        logger.exception(f'CAN NOT  ADD {real_state["token"]} TO DB!\nERORR:')

