import pika
import requests
import json
import os
import subprocess
import time
from fun_div_sc import div_sc
from fun_syp_sc import syp_sc

def scrape_data(base):

    dir_main = os.path.dirname(os.path.abspath(__name__))
    TokDir = os.path.join(dir_main, 'scraper')

    if base == "div":
        div_sc()
        TokFile = os.path.join(TokDir,'div_tokbase.json')
        with open(TokFile, 'r') as file:
            tokcell = json.load(file)
        tokcell = set(tokcell)
        newtok = list(tokcell.difference(div_BufTok))
        div_BufTok.update(tokcell)

    elif base == "syp":
        syp_sc()
        TokFile = os.path.join(TokDir,'syp_tokbase.json')
        with open(TokFile, 'r') as file:
            tokcell = json.load(file)
        tokcell = set(tokcell)
        newtok = list(tokcell.difference(syp_BufTok))
        syp_BufTok.update(tokcell)

    if newtok:
        return newtok
    else:
        return None
    


def send_scraped_data(data, src):
    credentials = pika.PlainCredentials('sjd_rabbitmq', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # channel.queue_delete(queue='div_token')
    # channel.queue_delete(queue='syp_token')
    
    channel.queue_declare(queue='div_token')
    channel.queue_declare(queue='syp_token')


    if src == "div":
        for item in data:
            channel.basic_publish(exchange='',
                                routing_key='div_token',
                                body=item)
    elif src == "syp":
        for item in data:
            channel.basic_publish(exchange='',
                                routing_key='syp_token',
                                body=item)
    connection.close()

if __name__ == "__main__":

    dir_main = os.path.dirname(os.path.abspath(__name__))
    TokDir = os.path.join(dir_main, 'scraper')
    
    TokFile = os.path.join(TokDir,'div_tokbase.json')
    with open(TokFile, 'r') as file:
        div_BufTok = json.load(file)
    div_BufTok = set(div_BufTok)

    TokFile = os.path.join(TokDir,'syp_tokbase.json')
    with open(TokFile, 'r') as file:
        syp_BufTok = json.load(file)
    syp_BufTok = set(syp_BufTok)

    # div_BufTok = set()
    # syp_BufTok = set()
    
    while(True):
        div_data = scrape_data("div")
        syp_data = scrape_data("syp")
        if div_data:
            send_scraped_data(div_data, "div")
        if syp_data:
            send_scraped_data(syp_data, "syp")

        time.sleep(5)