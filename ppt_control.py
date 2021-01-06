import redis
import threading
import queue
import keyboard
import ujson
'''
reference:
https://github.com/boppreh/keyboard
'''
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
                keyboard.press_and_release('n')
            elif msg == 'left':
                print("run Command: left")
                keyboard.press_and_release('p')
            elif msg == 'house': 
                print("run Command: house(home page)")   
                keyboard.press_and_release('Home')
            elif msg == 'down': 
                print("run Command: down(end page)")   
                keyboard.press_and_release('End') 
            elif msg == 'go': 
                print("run Command: go(full screen)")   
                keyboard.press_and_release('f5')  
            elif msg == 'off':
                print("run Command: off(ESC)")
                keyboard.press_and_release('Esc')  
            else:
                print("run Command: others")
        print("ppt_control finished")
        self.join()

def get_connect_info():
    file_path = "./ip_pwd.json"
    # open file
    f = open(file_path, 'r')
    content = ujson.loads(f.read())
    f.close()
    redis_ip = content["ip"]
    pwd = content["pwd"]
    #print("ip: %s" % redis_ip)
    #print("pwd: %s" % pwd)
    return redis_ip, pwd

def connect_to_redis():
    redis_ip, pwd = get_connect_info()
    r = redis.StrictRedis(host=redis_ip,password=pwd, port=8987,db=0)
    while r.ping() == False:
        print("connecting to redis server...")
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
    

