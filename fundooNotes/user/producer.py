import json
import pika


class RabbitServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    def sign_up_message(self, *args):
        """
        args:queue,token,user_data
        """
        channel = self.connection.channel()
        channel.queue_declare(queue=args[0])
        channel.basic_publish(exchange='',
                              routing_key=args[0],
                              body=json.dumps({'user': args[2], 'token': args[1]}))
        print(f" [x] Sent {args[1]}'")

    def __del__(self):
        self.connection.close()
