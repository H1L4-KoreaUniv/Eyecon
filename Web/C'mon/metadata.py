
class Meta():
    def __init__(self):
        self.queue=[]
        self.student_info=[]
        self.warning=0

    def push(self, input):
        #input type is json{ time, label, name}
        self.queue.append(input)

    def pop(self):
        while not self.queue:
            continue
        return self.queue.pop(0)

    # {'time':'0813012','value':1},{'time':'0813013','value':0},{'time':'0813014','value':1}
    #                            ,{'time':'0813015','value':1}