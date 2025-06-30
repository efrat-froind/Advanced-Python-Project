import random
from datetime import datetime
class Version:
    def __init__(self,message):
        self.hashCode = str(abs(hash(datetime.now())))
        self.date = datetime.now()
        self.routing = str("")
        self.message=message

