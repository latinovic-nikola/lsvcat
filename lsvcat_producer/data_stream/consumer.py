from confluent_kafka import Consumer
from utils.config import config

def init_consumer():
    global c
    
    bootstrap_server = config('KAFKA', 'bootstrap_servers')
    broker_topic = config('KAFKA','default_topic')
    c = Consumer({
        'bootstrap.servers': bootstrap_server,
        'group.id': 'g1',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([broker_topic])


def start_listening():
    try:
        while True:
            msg = c.poll(100)
            if msg is None:
                continue
            if msg.error():
                print('Error reading message')
            print(msg.value().decode('utf-8'))
    except KeyboardInterrupt:
        print('Interrupted by the user.')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    init_consumer()
    start_listening()