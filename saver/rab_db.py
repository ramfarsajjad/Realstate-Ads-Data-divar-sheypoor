import pika
from fun_save2db import save2db
import json

def callback(ch, method, properties, body):
    print(f"Received scraped data: {body.decode()}")
    save2db(body.decode()) 
    
    # تأییدیه پیام
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_saving():
    credentials = pika.PlainCredentials('sjd_rabbitmq', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='div_prepared_data')
    channel.queue_declare(queue='syp_prepared_data')

    channel.basic_consume(queue='div_prepared_data', on_message_callback=callback)
    channel.basic_consume(queue='syp_prepared_data', on_message_callback=callback)

    print('Waiting for scraped data to parse...')
    channel.start_consuming()

if __name__ == "__main__":
    start_saving()
