import json
import os
import csv
from div_decnum_pass import decnum
from div_listdata_pass import listd_p
import time
import logging
import psycopg2
from psycopg2 import sql
from setup_log import setup_logger





def div_parser3(data):

    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'div_parser_lev3.log')

    if 'logger_div_pars3' in logging.Logger.manager.loggerDict:
        logger = logging.getLogger('logger_div_pars3')
    else:
        logger = setup_logger(log_file, 'logger_div_pars3')

    try:



        data = json.loads(data)
        real_state = {
            "source" : 'divar',
            "token" : data["details"]["token"],
            "sc_time" : data['sc_time'],
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
            "tamin_hot_water" : '',
            "expired_date" : ''
        }


        if not real_state["apartment_house"] == None:
            word = real_state["apartment_house"].split('-')
            if word[0] == 'villa' or word[0] == 'house':
                real_state["apartment_house"] = 'house'
            elif word[0] == 'apartment':
                real_state["apartment_house"] = 'apartment'
        
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

        if not real_state["rent_sell"] == None:
            # word = real_state["rent_sell"].split('-')
            if real_state["rent_sell"] == 'residential-rent':
                real_state["rent_sell"] = 'rent'
            elif real_state["rent_sell"] == 'residential-sell':
                real_state["rent_sell"] = 'sell'


        logger.info('JSON IS READY!')
        
        return real_state

    except:
        logger.exception(f'CAN NOT  PREPARE {real_state["token"]}!\nERORR:')
        
        return None
