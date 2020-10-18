from queue import Queue, Empty
from threading import *
# 第三方模块
from PyQt5.QtCore import QTimer
# 自己开发的模块
from eventType import *

class EventManager:
    def __init__(self):
        self.__enentQueue = Queue()
        self.__active = False
        self.__thread = Thread(target=self.__run)  # 将Start方法作为多线程处理，以此同时处理多个事件

        # 计时器
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__onTimer)  # 结束时调用函数__onTimer
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
    def __event_process(self, event):
        if event.type_ in self.__handlers:
            for handler in self.__handlers[event.type_]:
                handler(event)
        pass
    def __onTimer(self):
        """向事件队列中存入计时器事件"""
        event = Event(EVENT_TIMER)
        self.put(event)
    def start(self):
        self.__active = True
        self.__thread.start()  # 启动线程
        self.__timer.start(1000)
        pass
    def stop(self):
        self.__active = False
        self.__thread.join()

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
    def __init__(self, type_=None):
        self.type_ = type_
        self.dict = {}

def test():
    """测试函数"""
    import sys
    from datetime import datetime
    from PyQt5.QtCore import QCoreApplication

    def simletest(event):
        print(u'处理每秒触发的计时器事件：%s' % str(datetime.now()))
    app = QCoreApplication(sys.argv)
    ee = EventManager()
    ee.register(EVENT_TIMER, simletest)
    ee.start()
    app.exec_()
if __name__ == "__main__":
    test()
    pass

