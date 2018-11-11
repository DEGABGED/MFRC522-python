from Queue import Queue
import threading
import json

import requests

class RequestQueue:
    Size = 300

    def __init__(self):
        self.queue = Queue(self.Size)
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def get_queue(self):
        return self.queue

    def dump(self):
        while not self.queue.empty():
            obj = self.queue.get()
            print obj

    def send(self, payload):
        # Send the json
        try
            res = requests.post(self.url, payload)
            return true
        except requests.ConnectionError
            return false

    def run(self):
        while(True):
            # Check the queue for jobs
            if self.queue.empty():
                continue

            job = json.dumps(self.queue.get())
            while(not self.send(job))

            # Finished
            self.queue.task_done()

