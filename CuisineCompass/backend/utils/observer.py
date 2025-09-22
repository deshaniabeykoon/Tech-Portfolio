class Observer:
    def update(self, event_data):
        pass

class Logger(Observer):
    def update(self, event_data):
        print(f"[LOG] User did: {event_data}")

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, event_data):
        for observer in self._observers:
            observer.update(event_data)
