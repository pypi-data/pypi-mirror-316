class EventListener(object):
 
    def __init__(self):
        self.__eventhandlers = []
 
    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self
 
    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self
 
    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)
         
class Event(object):
     
    def __init__(self):
        self.handlers = {}

    def emit(self, event, data=None):
        self.handlers[event](data)
         
    def on(self, event, method):
        if event not in self.handlers:
            self.handlers[event] = EventListener()
        self.handlers[event] += method
         
    def off(self, event, reset=None, method=None):
        if reset:
            self.handlers[event] = EventListener()
        elif method and event in self.handlers:
            self.handlers[event] -= method
