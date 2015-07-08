'''
Created on Jul 3, 2015

@author: Adam
'''

import pika
import msgpack

from ib import request_structures
        
def callback(ch, method, properties, body):
    data = msgpack.unpack(body)
    print ' [x] Received ' + body
    
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='tickPrice')
    
    channel.basic_consume(callback,
                      queue='tickPrice',
                      no_ack=True)
    
    channel.queue_declare(queue='requests')

    packer = msgpack.Packer(autoreset=False)
    
    packer.pack('reqMktData')
    packer.pack(1)
    contract = request_structures.Contract(symbol='ES',secType='FUT',expiry='201509',exchange='GLOBEX')
    packer.pack(contract())
    
    channel.basic_publish(exchange='',
                          routing_key='requests',
                          body=packer.bytes())
    print ' [x] Sent Contract'

    while True:
        connection.process_data_events()
    
    connection.close()