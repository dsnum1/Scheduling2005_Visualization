#### This is a project that was aimed to build a visualization of all algorithms
#### used in CE2005. I hope this code allows you to visualize different scenarios
#### and conduct your own test cases and scenarios.

import matplotlib.pyplot as plt




class Process:
    def __init__(self,cpuburstlen, arrivaltime, processname):
        self.name=processname
        self.cpuburstlen=cpuburstlen
        self.arrivaltime=arrivaltime
        self.remaining_time = cpuburstlen

    def decrementRemainingTime(self):
        self.remaining_time-=1
    


class ProcessorInstance:
    
    def __init__(self):
        self.process_list = []
        self.current_time_tick = 0
        self.current_process = None
    def addProcess(self, process): self.process_list.append(process)
    def removeProcess(self): self.process_list.remove(self.current_process)
    def getProcessList(self): return self.process_list
    def incrementTime(self):    self.current_time_tick+=1
    def getTime(self): return self.current_time_tick
    def setCurrentProcess(self, process): self.current_process = process # else print("Already Process running")
    def getCurrentProcess(self): return self.current_process
    def decrementProcessTime(self): self.current_process.decrementRemainingTime()

    
class Algorithm:
        '''
        Algorithm class defines the parent class for the algorithms
        '''
        def __init__(self):
            self.name=""
            self.description=""
        def showDescription(self):print("NAME : "+self.name) if(self.name!="") else print("!!!ERROR : NAME NOT SET")
        def setName(self, name): self.name = name
        def getName(self): return self.name
        def setDescription(self, desc):self.description = desc
        def getDescription(self): return self.description

class FirstComeFirstServe(Algorithm):
        ### Look at the processes at every time step
        ### Check which process arrived first
        ### Execute the process
        ### Remove the process from the queue
        def finalAlgorithm(self, process_list, current_process):
            min_atime_process = process_list[0]
            for process in process_list:
                if(process.arrivaltime < min_atime_process.arrivaltime):
                    min_atime_process = process
            return min_atime_process
        

class ShortestJobFirst(Algorithm):
        ### Check which function in the processor List has the smallest burst length and remove it
        def performAlgorithm(self, process_list, current_process):
            min_rtime_process = process_list[0]
            for process in process_list:
                if(process.remaining_time < min_rtime_process.remaining_time):
                    min_rtime_process = process
            return min_rtime_process
        pass

class ShortestJobFirstNonPremptive(ShortestJobFirst):
        ### Remove process in the process List when the current process is completed
        def __init__(self):
            super().__init__()
            self.type = "n"
        def finalAlgorithm(self, process_list, current_process):
                x = super().performAlgorithm(process_list)
                if(current_process == None):
                    return x
                if(current_process.remaining_time ==0):
                    return x
                else:
                    return current_process

class ShortestRemainingTimeFirst(ShortestJobFirst):
        ### Remove process from the process list and replace it with the shortest remaining type
        def __init__(self):
            super().__init__()
            self.name = "SJFS"
        def finalAlgorithm(self, process_list, current_process):
                
                x = super().performAlgorithm(process_list, current_process)
                return x
        pass

class RoundRobin(Algorithm):
        def __init__(self):
            super().__init__()
            self.name = "Round Robin"
            self.quanta = 1
            self.counter = 0
            self.index =0
        ### Run all processes for a defined time stamp
        def finalAlgorithm(self, process_list, current_process):
            #print(self.index, [x.name for x in process_list])
            if(len(process_list)==1):
                return process_list[0]
            if(self.counter>=self.quanta):
                self.counter=0
                self.index = (self.index+1)%len(process_list)
            #print(self.index, len(process_list))
            p = process_list[self.index]
            self.counter+=1
            return p
        pass

    
p1 = Process(20, 0, "p1")
p2 = Process(20, 0, "p2")
p3 = Process(20, 0, "p3")

compiled_processes = [p1,p2,p3]
y = ProcessorInstance()

algo = RoundRobin()

gantt_list = {}
gantt_list[p1.name] = []
gantt_list[p2.name] = []
gantt_list[p3.name] = []

for tick in range(0, 20):
    ### add processes to the process list only when they are active
    for j in compiled_processes:
        if(j.arrivaltime == tick):
            y.addProcess(j)

    
    ### if no current process running, we can easily just assign the process
    if(y.getCurrentProcess()!= None):
        y.decrementProcessTime()
        #if current process has completed then it needs to be removed.
        if(y.getCurrentProcess().remaining_time == 0):
            y.removeProcess()
            y.setCurrentProcess(None)

    if(len(y.getProcessList())==0):
        continue       

    ### perform algorithm to get the nextprocess
    requested_process = algo.finalAlgorithm(y.getProcessList(), y.getCurrentProcess())
    #if algorithm type == premptive or current process has 0 remaining time
    if(y.getCurrentProcess()== None):
        y.setCurrentProcess(requested_process)
    elif(algo.name =="SJFS" or "Round Robin" ):
        y.setCurrentProcess(requested_process)

    x = gantt_list[requested_process.name]
    x.append((tick, 1))
    gantt_list[requested_process.name] = x
    

    # Debugging output.
    print(tick,y.getCurrentProcess().name)

print(gantt_list)

# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt
 
# Declaring a figure "gnt"
fig, gnt = plt.subplots()
 
# Setting Y-axis limits
gnt.set_ylim(0, 30)
 
# Setting X-axis limits
gnt.set_xlim(0, 20)
 
# Setting labels for x-axis and y-axis
gnt.set_xlabel('seconds since start')
gnt.set_ylabel('Processor')
 
# Setting ticks on y-axis
gnt.set_yticks([10, 20, 30])
# Labelling tickes of y-axis
gnt.set_yticklabels(['p1', 'p2', 'p3'])
 
# Setting graph attribute
gnt.grid(True)
 
# Declaring a bar in schedule
gnt.broken_barh(gantt_list["p1"],(0,10), facecolors =('tab:orange'))
gnt.broken_barh(gantt_list["p2"],(10,10), facecolors =('tab:red'))
gnt.broken_barh(gantt_list["p3"],(20,10), facecolors =('tab:blue'))

 
# Declaring multiple bars in at same level and same width
#gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
                       #  facecolors ='tab:blue')
 
#gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
                          #        facecolors =('tab:red'))

fig.show()
 
