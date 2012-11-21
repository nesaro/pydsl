import pika
import sys
import json
import threading
import time

credentials = pika.PlainCredentials('root', '1234')

class Agent(threading.Thread):
    def __init__(self, exchange, name, actiondictionary):
        """Subscription is the exchange key to connect to aside the name"""
        threading.Thread.__init__(self)
        self.daemon = True
        self.exchange = exchange
        if name == "output":
            raise Exception("output is a protected name")
        self.name = name 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( host='localhost', credentials=credentials))
        self.channeloutput = self.connection.channel()
        self.channelinput = self.connection.channel()
        result = self.channelinput.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.actiondictionary = actiondictionary
        routing_key = "std." + self.name
        self.channelinput.queue_bind(exchange=self.exchange,
                           queue=self.queue_name,
                           routing_key=routing_key)
        

    def __del__(self):
        self.connection.close()
        
    def emit_message(self, destination, message):
        if destination == 'output':
            routing_key='out.*'
        else:
            routing_key =  'std.' + destination
        obj = {'message':message, 'destination':destination, 'source':self.name}
        self.channeloutput.basic_publish(exchange=self.exchange, routing_key=routing_key, body=json.dumps(obj))

    def onmessage(self, ch, method, properties, body):
        obj = json.loads(body)
        #default signature for function : (parentobj, messagedictionary)
        #special inputs: input
        #special output: output
        return self.actiondictionary[obj['source']](self, obj)

    def run(self):
        self.channelinput.basic_consume(self.onmessage,
                              queue=self.queue_name,
                              no_ack=False)
        self.channelinput.start_consuming()

class AgentNetwork:
    #generates the network from a list
    def __init__(self, exchange, initlist):
        """initlist allows agent declaration,
        outputsubscription tells the key to connect to for outputs"""
        self.exchange = exchange
        self.connection = connection = pika.BlockingConnection(pika.ConnectionParameters( host='localhost', credentials=credentials))
        self.channelinput = self.connection.channel()
        self.channelinput.exchange_declare(exchange=self.exchange, type='topic')
        result = self.channelinput.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channeloutput = self.connection.channel()
        #declare exchange
        self.agentlist = []
        for (name,dic) in initlist:
            self.agentlist.append(Agent(self.exchange, name, dic))
        #call subprocess per agent
        routing_key = 'out.*'
        self.channelinput.queue_bind(exchange=self.exchange,
                           queue=self.queue_name,
                           routing_key=routing_key)

    def __del__(self):
        self.connection.close()
        
    def send_input(self, message):
        """Sends an input to the network"""
        obj = {'message':message, 'destination':'*', 'source':'input'}
        for x in self.agentlist:
            routing_key='std.'+x.name
            self.channeloutput.basic_publish(exchange=self.exchange, routing_key=routing_key, body=json.dumps(obj))


    def call(self,message):
        slept = 0
        for element in self.agentlist:
            element.start()
        self.send_input(message)
        time.sleep(0.5)
        while slept < 9:
            method_frame, header_frame, body = self.channelinput.basic_get(queue = self.queue_name)
            if method_frame:
                self.channelinput.basic_ack(delivery_tag=method_frame.delivery_tag)
                return json.loads(body)
            time.sleep(0.5)
            slept += 0.5
        return None

