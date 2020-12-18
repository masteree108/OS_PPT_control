import json
import redis

def connect_to_redis():
    redis_ip = 'x.x.x.x'
    r = redis.StrictRedis(host=redis_ip,password="2u04sl3", port=8987,db=0)
    print("start")
    while r.ping()==False:
        print("connecting to redis server...");
    print("connected to redis server!!")
    return r


def subscribe(r):
    sub = r.pubsub()
    sub.subscribe('PPT_COMMAND')

    try:
        for i in sub.listen():
            if i.get('data') == b'right':
                print("Receives Command: right")
            elif i.get('data') == b'left':
                print("Receives Command: left")
    except:
        print("something causes error")

if __name__ == '__main__':
    print("start")
    r = connect_to_redis()
    subscribe(r)


