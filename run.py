'''
Created on Jul 3, 2015

@author: Adam
'''

import pika
import msgpack

from ib import structures
from matplotlib import pyplot
from multiprocessing import queues

class IBDataManager:
    def __init__(self):
        print 'Initializing IBDataManager'
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue='contractDetails')
        self._channel.queue_declare(queue='requests')
        self._channel.queue_declare(queue='tickPrice')
        
        self._channel.basic_consume(self._on_response, queue='contractDetails', no_ack=True)
        self._channel.basic_consume(self._on_response, queue='tickPrice', no_ack=True)
        
        self._responses = queues.Queue()
        
        self._req_id = 0
        
        self._requests = {}
        
        self._market_data = {}
        
        self._dirty = False
        
    def start(self):
        print 'starting IBDataManager'
        while True:
            self._connection.process_data_events()
            while not self._responses.empty():
                response = self._responses.get()
                method_to_call = getattr(self, response['method'])
                print 'calling ' + response['method']
                method_to_call(response['data'])
    
            if self._dirty:
                self.run_all()
    
    def run_all(self):
        x_call_bids = [x for x in self._market_data if self._market_data[x][0] != None]
        y_call_bids = [self._market_data[x][0] for x in x_call_bids]
        
        x_call_asks = [x for x in self._market_data if self._market_data[x][1] != None]
        y_call_asks = [self._market_data[x][1] for x in x_call_asks]
        
        x_put_bids = [x for x in self._market_data if self._market_data[x][2] != None]
        y_put_bids = [self._market_data[x][2] for x in x_put_bids]
        
        x_put_asks = [x for x in self._market_data if self._market_data[x][3] != None]
        y_put_asks = [self._market_data[x][3] for x in x_put_asks]
        
        pyplot.plot(x_call_bids, y_call_bids, '+', x_call_asks, y_call_asks, ',', x_put_bids, y_put_bids, '.', x_put_asks, y_put_asks, '1')
        pyplot.show()
        self._dirty = False
        
    def publish_request(self, request_type, data):
        packer = msgpack.Packer(autoreset=False)
        req_id = self._get_reqId()
        request = {'request_type': request_type,
                   'data'        : data}
        packer.pack(request_type)
        packer.pack(req_id)
        packer.pack(data)
        self._channel.basic_publish(exchange='', routing_key='requests', body=packer.bytes())
        self._requests[req_id] = request
        
    def contractDetails(self, data):
        unpacker = msgpack.Unpacker()
        unpacker.feed(data)
        contract_details = structures.ContractDetails()
        contract_details.populate_from_buffer(unpacker)
        self._market_data[contract_details.summary.strike] = [None, None, None, None]
        self.publish_request('reqMktData', contract_details.summary())
        
    def tickPrice(self, data):
        unpacker = msgpack.Unpacker()
        unpacker.feed(data)
        req_id = unpacker.next()
        field = unpacker.next()
        price = unpacker.next()
        contract = structures.Contract(*self._requests[req_id]['data'])
        if field == 1:
            if contract.right[0] == 'C':
                self._market_data[contract.strike][0] = price
            else:  
                self._market_data[contract.strike][2] = price
            self._dirty = True
        elif field == 2:
            if contract.right[0] == 'C':
                self._market_data[contract.strike][1] = price
            else:
                self._market_data[contract.strike][3] = price
            self._dirty = True
        
    def _get_reqId(self):
        self._req_id += 1
        return self._req_id
        
    def __del__(self):
        self._connection.close()
        
    def _on_response(self, ch, method, properties, body):
        self._responses.put({'method': method.routing_key, 'data': body})
        
if __name__ == '__main__':
    manager = IBDataManager()
    contract = structures.Contract(symbol='ES',secType='FOP',expiry='201509',exchange='GLOBEX')
    
    manager.publish_request('reqContractDetails', contract())
    
    manager.start()