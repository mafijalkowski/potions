import time


class Notification:
    def __init__(self, message: str, lifetime_seconds: float = 1.5):
        self.message = message
        self.lifetime_seconds = lifetime_seconds
        self.created = time.time()

    def still_alive(self):
        return time.time() <= self.created + self.lifetime_seconds
