import queue
class IterableQueue(queue.Queue):
    def __init__(self):
        super().__init__()

    def __iter__(self):
        while True:
            try:
                yield self.get_nowait()
            except:
                break
        return

    def __next__(self):
        try:
            item = self.get_nowait()
            return item
        except:
            return
