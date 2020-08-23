
class Meta():
    def __init__(self):
        self.queue=[]

    def push(self, input):
        #input type is json{ time, label, name}
        self.queue.append(input)

    def pop(self):
        while not self.queue:
            continue
        return self.queue.pop(0)