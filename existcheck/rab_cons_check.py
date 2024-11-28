import pika
from fun_div_existck import exist_check
import json

def div_callback(ch, method, properties, body):
    print(f"Received scraped data: {body.decode()}")
    exist_check(body.decode(), 'div') 
    
    # تأییدیه پیام
    ch.basic_ack(delivery_tag=method.delivery_tag)

def syp_callback(ch, method, properties, body):
    print(f"Received scraped data: {body.decode()}")
    exist_check(body.decode(), 'syp') 
    
    # تأییدیه پیام
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_checking():
    credentials = pika.PlainCredentials('sjd_rabbitmq', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='div_expired_check')
    channel.queue_declare(queue='syp_expired_check')

    channel.basic_consume(queue='div_expired_check', on_message_callback=div_callback)
    channel.basic_consume(queue='syp_expired_check', on_message_callback=syp_callback)

    print('Waiting for tokens...')
    channel.start_consuming()

if __name__ == "__main__":
    start_checking()
