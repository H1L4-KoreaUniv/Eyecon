
class Meta():
    def __init__(self):
        self.queue=[]
        self.student_info=[]
        self.warning=0
        self.cnt=1
        self.sum=0
        self.minute_sum=0
        self.minute_cnt=1

    def push(self, input):
        # input type is json{ time, value}
        self.queue.append(input)

    def pop(self):
        while not self.queue:
            continue
        return self.queue.pop(0)
