import threading

class Publisher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, subscriber, topic):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)

    def publish(self, message, topic):
        if topic in self.subscribers:
            for subscriber in self.subscribers[topic]:
                subscriber.event.set()
                subscriber.message = message

class Subscriber:
    def __init__(self, name):
        self.name = name
        self.event = threading.Event()
        self.message = None

    def receive(self):
        self.event.wait()
        print(f"{self.name}" +"received message:" 
              f"{self.message}")
        self.event.clear()


publisher = Publisher()

subscriber_1 = Subscriber("Subscriber 1")
subscriber_2 = Subscriber("Subscriber 2")
subscriber_3 = Subscriber("Subscriber 3")
subsrciber_4 = Subscriber("Subscriber 4")

publisher.subscribe(subscriber_1, "sports")
publisher.subscribe(subscriber_2, "entertainment")
publisher.subscribe(subscriber_3, "sports")
publisher.subscribe(subsrciber_4, "sports")

publisher.publish("Soccer match result", "sports")
subscriber_1.receive()
subsrciber_4.receive()
