from queue import Queue, Empty
from threading import *
from datetime import datetime
class EventManager:
    def __init__(self):
        self.__enentQueue = Queue()
        self.__active = False
        self.__thread = Thread(target=self.__run)  # 将Start方法作为多线程处理，以此同时处理多个事件
        self.__handlers = {}  # 存放事件字典，一对多，一个事件可以有多个处理方法
        pass
    def __run(self):
        '''
        开启
        :return:
        '''
        while self.__active == True:  #
            try:
                event = self.__enentQueue.get(block=True, timeout=1)  # 从事件队列中获取事件，阻塞一秒
                self.__event_process(event)  # 调用事件处理方法
            except Empty:
                pass
            pass
        pass
    def start(self):
        self.__active = True
        self.__thread.start()  # 启动线程

        pass
    def stop(self):
        self.__active = False
        self.__thread.join()
    def __event_process(self, event):
        if event.type_ in self.__handlers:
            for handler in self.__handlers[event.type_]:
                handler(event)
        pass
    def register(self, type_, handler):
        try:
            handler_list = self.__handlers[type_]
        except KeyError:
            self.__handlers[type_] = []
            handler_list = self.__handlers[type_]
        if handler not in handler_list:
            handler_list.append(handler)
    def unregister(self, type_, handler):
        try:
            handler_list = self.__handlers[type_]
            if handler in handler_list:
                handler_list.remove(handler)
            if not handler_list:
                del handler_list[type_]
        except KeyError:
            pass
    def put(self, event):
        self.__enentQueue.put(event)
        pass

class Event:
    def __init__(self, type_):
        self.type_ = type_
        self.dict = {}

Event_ARTICLE = "推送文章"
Event_GET = "征集文章"
# 事件源
class PublicPush:  # 公众号
    def __init__(self, EventManager):
        self.__EventManager = EventManager
    def push_article(self):
        event = Event(Event_ARTICLE)  # 创立事件
        event.dict['article'] = '如何优雅的写代码'
        self.__EventManager.put(event)

    def get_article(self):
        event = Event(Event_GET)
        event.dict['article'] = '仰望星空，脚踏实地'
        self.__EventManager.put(event)

# 监听者
class Listener:  # 读者
    def __init__(self, username):
        self.__username = username
    def Read(self, event):
        if event.type_ == Event_ARTICLE:
            print(self.__username, "收到文章：", event.dict['article'])

class Writer:  # 作者
    def __init__(self, username):
        self.__username = username
    def Write(self, event):
        if event.type_ == Event_GET:
            print(self.__username, "看到正文信息：", event.dict['article'], "，正在苦思冥想")
if __name__ == "__main__":
    lister1 = Listener("jack")
    lister2 = Listener("Mike")
    writer1 = Writer("Tom")
    writer2 = Writer("Jerry")

    eventManager = EventManager()
    eventManager.register(Event_ARTICLE, lister1.Read)  # 推送文章给读者1读
    eventManager.register(Event_ARTICLE, lister2.Read)

    eventManager.register(Event_GET, writer1.Write)  # 征文
    eventManager.register(Event_GET, writer2.Write)

    eventManager.start()
    public = PublicPush(eventManager)
    timer = Timer(2, public.push_article)
    timer2 = Timer(4, public.get_article)
    timer.start()
    timer2.start()
    timer.join()
    timer2.join()
    eventManager.stop()


