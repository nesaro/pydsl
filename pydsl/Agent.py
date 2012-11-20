class Agent:
    def __init__(self, exchange, name, subscriptionlist = []):
        """Subscription is the exchange key to connect to aside the name"""
        self.exchange = exchange

    def start(self):
        raise NotImplementedError

class AgentNetwork:
    #generates the network from a list
    def __init__(self, initlist, outputsubscription):
        """initlist allows agent declaration,
        outputsubscription tells the key to connect to for outputs"""
        #declare exchange
        for x,y,z in initlist:
            Agent(exchange, x, y, z)
        #call subprocess per agent

    def send_input(self, content):
        """Sends an input to the network"""
        pass

    def collect_output(self, timeout=10):
        """Collects output if it exists"""
        pass
