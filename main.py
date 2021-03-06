from queue import Queue, PriorityQueue
import threading

class Process :

    def __init__(self, id, arrival_time, burst_time, io_time):
        self._id = id
        self._arrival_time = arrival_time
        self._burst_time = burst_time
        self._io_time = io_time
        self._remaining_time = burst_time
        self._start_time = -1

    @property
    def arrival_time(self):
        return self._arrival_time

    @property
    def burst_time(self):
        return self._burst_time

    def setStartTime(self, time):
        self._start_time = time

    def setEndTime(self, time):
        self._end_time = time

    def setRemainingTime(self, time):
        self._remaining_time = time

    def getBurstTime(self):
        return self._burst_time

    def getArrivalTime(self):
        return self._arrival_time

    def getTurnaroundTime(self):
        return self._end_time - self._arrival_time

    def getWaittingTime(self):
        return self.getTurnaroundTime() - self._burst_time

    def getResponseTime(self):
        return self._start_time - self._arrival_time

    def getStartTime(self):
        return self._start_time

    def getRemainingTime(self):
        return self._remaining_time

    def run(self, time, sec):
        self._remaining_time -= sec
        if(self._start_time == -1):
            self._start_time = time
        if(self._remaining_time == 0):
            self._end_time = time + sec

    def isFinished(self):
        return self._remaining_time == 0

    def getID(self):
        return self._id

    def getIOTime(self):
        return id

    def __str__(self):
        return 'id:{} arrival_time:{} burst_time:{} io_time:{}'.format(self.id, self.arrival_time, self.burst_time, self.io_time)

class CPU: 
    
    def __init__(self, all_process):
        self.all_proccess = []
        self.ready_queue = Queue(maxsize = len (all_process)) 
        self.waiting_queue = Queue(maxsize = len(all_process))
        # self.active_list = []
        for p in all_process:
            self.all_proccess.append(Process(p.getID(), p.getArrivalTime(), p.getBurstTime(), p.getIOTime()))

    def FCFS(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        

        tmp = self.all_proccess[:]
        tmp.sort(key = lambda c: c.arrival_time, reverse = False)
        for process in tmp:
            self.ready_queue.put(process)
        while not self.ready_queue.empty() or not self.waiting_queue.empty():
            p = self.ready_queue.get()
            if (p.getArrivalTime() > self.time):
                self.time = p.getArrivalTime()
            p.setStartTime(self.time)
            self.time += p.getBurstTime()
            p.setEndTime(self.time)
            p.setRemainingTime(0)
            self.total_burst_time += p.getBurstTime()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time
        
        #print all CPU variables
        print ("FCFS:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)

    def SJF(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        sorted_on_arrival_time = self.all_proccess[:]
        sorted_on_arrival_time.sort(key = lambda c: c.arrival_time, reverse = False)
        
        sorted_on_burst_time = []

        while (len(sorted_on_arrival_time) != 0 or len(sorted_on_burst_time) != 0):
            tmp = sorted_on_arrival_time[:]
            for p in tmp:
                if (p.getArrivalTime() <= self.time):
                    sorted_on_burst_time.append(p)
                    sorted_on_arrival_time.remove(p)
                if (p.getArrivalTime() > self.time):
                    next_arrival_time = p.getArrivalTime()
                    break

            sorted_on_burst_time.sort(key = lambda c: c.burst_time, reverse = True)
            
            if (len(sorted_on_burst_time) == 0):
                self.time = next_arrival_time
                continue
            else:
                p = sorted_on_burst_time.pop()
                p.setStartTime(self.time)
                self.time += p.getBurstTime()
                p.setEndTime(self.time)
                p.setRemainingTime(0)
                self.total_burst_time += p.getBurstTime()

        #printAllProcess()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time

        #print all CPU variables
        print ("SJF:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)

    def RR(self):
        sorted_on_arrival_time = Queue(maxsize=len(self.all_proccess))
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0
        

        sorted_on_arrival_time = self.all_proccess[:]
        sorted_on_arrival_time.sort(key = lambda c: c.arrival_time, reverse= False)
        
        
        while (not self.ready_queue.empty() or len(sorted_on_arrival_time)!=0):
            
            if (self.ready_queue.empty()):
                p = sorted_on_arrival_time[0]
                self.time = p.getArrivalTime()
                self.ready_queue.put(p)
                sorted_on_arrival_time.remove(p)
            
                    
                    
            p = self.ready_queue.get()
                
            if (p.getStartTime() == -1):
                p.setStartTime(self.time)
            if (p.getRemainingTime() > 5):
                self.time = self.time + 5
                self.total_burst_time = self.total_burst_time + 5
                p.setRemainingTime(p.getRemainingTime() - 5)
            else:
                self.time += p.getRemainingTime()
                self.total_burst_time += p.getRemainingTime()
                p.setRemainingTime(0)
                p.setEndTime(self.time)
     
            tmp = sorted_on_arrival_time[:]
            for process in tmp:
                if (process.arrival_time<=self.time):
                    self.ready_queue.put(process)
                    sorted_on_arrival_time.remove(process)
            if(not p.isFinished()):
                self.ready_queue.put(p)

        #printAllProcess()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time

        #print all CPU variables
        print ("RR:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)

    def SRT(self):
        #ititial time and burst_time 
        self.time = 0
        self.total_burst_time = 0

        sorted_on_arrival_time = self.all_proccess[:]
        sorted_on_arrival_time.sort(key = lambda c: c.arrival_time, reverse= False)
        
        sorted_on_burst_time = []

        while (len(sorted_on_arrival_time) != 0 or len(sorted_on_burst_time) != 0):
            tmp = sorted_on_arrival_time[:]
            for p in tmp:
                if (p.getArrivalTime() <= self.time):
                    sorted_on_burst_time.append(p)
                    sorted_on_arrival_time.remove(p)
                if (p.getArrivalTime() > self.time):
                    next_arrival_time = p.getArrivalTime()
                    break
            
            sorted_on_burst_time.sort(key = lambda c: c.burst_time, reverse= True)

            if (len(sorted_on_burst_time) == 0):
                self.time = next_arrival_time
                continue
                
            else:
                p = sorted_on_burst_time.pop()
                if (p.getStartTime() == -1):
                    p.setStartTime(self.time)
                self.time += 1
                p.setRemainingTime(p.getRemainingTime() - 1)
                if (p.isFinished()):
                    p.setEndTime(self.time)
                else:
                    sorted_on_burst_time.append(p)
                self.total_burst_time += 1
                

        #printAllProcess()

        # evaluate the CPU variables AWT, ATT, ART, Throughput, Utilization
        self.average_waiting_time = sum([x.getWaittingTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_turnaround_time = sum([x.getTurnaroundTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.average_response_time = sum([x.getResponseTime() for x in self.all_proccess]) / len(self.all_proccess)
        self.throughput = len(self.all_proccess)/ self.time
        self.cpu_utilization =  self.total_burst_time/self.time

        #print all CPU variables
        print ("SRT:")
        print ("Avg. W.T.: ", self.average_waiting_time)
        print ("Avg. T.T.: ", self.average_turnaround_time)
        print ("Avg. R.T: ", self.average_response_time)
        print ("Throughput: ", self.throughput)
        print ("CPU Utilization: ", self.cpu_utilization)

def printAllProcess() :
    # print all process attributes
    for process in self.all_proccess:
        print (process)
        print (process.start_time)
        print (process.end_time)
        print ("ResponseTime: " , process.getResponseTime())
        print ("WatingTime: " , process.getWaittingTime())
        print ("TurnAroundTime: " , process.getTurnaroundTime())
        print ("==========================")

process = []
number_of_process = int(input(""))
for i in range(number_of_process):
    str = input()
    str_list = str.split(" ") 
    process.append(Process(i+1,int (str_list[0]), int(str_list[1]), int(str_list[2])))

cpu1 = CPU(process)
cpu2 = CPU(process)
cpu3 = CPU(process)
cpu4 = CPU(process)

FCFS = threading.Thread(cpu1.FCFS())
SJF = threading.Thread(cpu2.SJF())
RR = threading.Thread(cpu3.RR())
SRT = threading.Thread(cpu4.SRT())

FCFS.start()
SJF.start()
RR.start()
SRT.start()
