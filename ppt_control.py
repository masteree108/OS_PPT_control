import redis
import threading
import queue

class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        print("ppt_control init ok")

    def run(self):
        msg = ""
        while(msg != 'end'):
            #print("msg: %s" % msg)
            msg = str(self.queue.get())
            if msg == 'right':
                print("run Command: right")
            elif msg == 'left':
                print("run Command: left")
            else:
                print("run Command: others")
        print("ppt_control finished")
        self.join()

def connect_to_redis():
    redis_ip = 'x.x.x.x'
    r = redis.StrictRedis(host=redis_ip,password="2u04sl3", port=8987,db=0)
    while r.ping() == False:
        print("connecting to redis server...");
    print("connected to redis server!!")
    return r


def subscribe(r, ppt_control, data_queue):
    sub = r.pubsub()
    sub.subscribe('PPT_COMMAND')
    get_data = ""
    try:
        for mes in sub.listen():
            responses = mes.get('data')
            # below if can aviod first data = 1(it means subscribe sucessfully) into inside of if
            if isinstance(responses, bytes):
                get_data = responses.decode('utf-8')
                data_queue.put(get_data)
                print("Receives Command decode: %s" % get_data)
    except:
        get_data = "end"
        ppt_control.join()
        print("something causes error")

if __name__ == '__main__':
    r = connect_to_redis()
    data_queue = queue.Queue()
    ppt_control = Worker(data_queue)
    ppt_control.start()
    subscribe(r, ppt_control, data_queue)
    

