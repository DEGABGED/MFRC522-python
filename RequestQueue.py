from Queue import Queue

class RequestQueue:
    Size = 300

    def __init__(self):
        self.queue = Queue(self.Size)

    def get_queue(self):
        return self.queue

    def dump(self):
        while not self.queue.empty():
            obj = self.queue.get()
            print obj
