import pika
import requests
import json
import os
import subprocess
import time
import psycopg2

def download_token(base):

    token = []
    conn = psycopg2.connect(
                host="localhost",
                database="ads_realstate",
                user= "sjd_admin",
                password="1234"
            )

    cur = conn.cursor()

    if base == "div":
        cur.execute("SELECT token, expired_date FROM div_table;")

    elif base == "syp":
        cur.execute("SELECT token, expired_date FROM syp_table;")
    
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for row in rows:
        token.append(row[0])

    if token:
        return token
    else:
        return None
    


def send_token(data, src):
    credentials = pika.PlainCredentials('sjd_rabbitmq', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # channel.queue_delete(queue='div_expired_check')
    # channel.queue_delete(queue='syp_expired_check')
    
    channel.queue_declare(queue='div_expired_check')
    channel.queue_declare(queue='syp_expired_check')


    if src == "div":
        for item in data:
            channel.basic_publish(exchange='',
                                routing_key='div_expired_check',
                                body=item)
    elif src == "syp":
        for item in data:
            channel.basic_publish(exchange='',
                                routing_key='syp_expired_check',
                                body=item)
    connection.close()

if __name__ == "__main__":
    while(True):
        div_token = download_token("div")
        syp_token = download_token("syp")
        if div_token:
            send_token(div_token, "div")
        if syp_token:
            send_token(syp_token, "syp")

        print('waiting for next check...')
        time.sleep(1800)