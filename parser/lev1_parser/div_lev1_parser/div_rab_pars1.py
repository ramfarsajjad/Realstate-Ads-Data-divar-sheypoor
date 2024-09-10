import pika
from fun_div_parser_lev1 import div_parser1
import json


def callback(ch, method, properties, body):
    print(f"Received scraped data: {body.decode()}")
    parsed_data = div_parser1(body.decode())
    
    if not parsed_data:  # اگر parsed_data خالی یا None باشد
        print("Parsed data is null or empty. Removing token from queue.")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # تأییدیه پیام برای حذف آن از صف
        return
    
    send_parsed_data_to_queue(parsed_data)
    # تأییدیه پیام
    ch.basic_ack(delivery_tag=method.delivery_tag)

def send_parsed_data_to_queue(data):
    credentials = pika.PlainCredentials('sjd_rabbitmq', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='div_queue_parsed_data')
    jdata = json.dumps(data, ensure_ascii=False)
    channel.basic_publish(exchange='', routing_key='div_queue_parsed_data', body=jdata)
    print(f"Sent parsed data: {data}")

    connection.close()

def start_parsing():
    credentials = pika.PlainCredentials('sjd_rabbitmq', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='div_token')

    channel.basic_consume(queue='div_token', on_message_callback=callback)

    print('Waiting for scraped data to parse...')
    channel.start_consuming()

if __name__ == "__main__":
    start_parsing()
