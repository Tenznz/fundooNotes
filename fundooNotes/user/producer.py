import json

import pika


def send_token(token,email):
    # connection to rabbitmq server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # check for queue in consumer exist
    channel.queue_declare(queue='user_token')

    #
    channel.basic_publish(exchange='',
                          routing_key='user_token',
                          body=json.dumps({'email':email,'token':token}))
    print(f" [x] Sent {token}'")

    connection.close()
