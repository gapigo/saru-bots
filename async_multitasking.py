from queue import Queue
# https://stackoverflow.com/questions/34469060/python-native-coroutines-and-send

# ------------------------------------------------------------
#                       === Tasks ===
# ------------------------------------------------------------
class Task:
    taskid = 0
    def __init__(self,target):
        Task.taskid += 1
        self.tid = Task.taskid   # Task ID
        self.target = target        # Target coroutine
        self.sendval = None          # Value to send

    # Run a task until it hits the next yield statement
    def run(self):
        return self.target.send(self.sendval)


# ------------------------------------------------------------
#                      === Scheduler ===
# ------------------------------------------------------------
class Scheduler:
    def __init__(self):
        self.ready = Queue()   
        self.taskmap = {}        

    def new(self,target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def exit(self,task):
        print("Task %d terminated" % task.tid)
        del self.taskmap[task.tid]

    def schedule(self,task):
        self.ready.put(task)

    def mainloop(self):
         while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result,SystemCall):
                    result.task  = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


# ------------------------------------------------------------
#                   === System Calls ===
# ------------------------------------------------------------
class SystemCall:
    def handle(self):
        pass

    def __await__(self):
        return (yield self)


# Return a task's ID number
class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


class YieldControl(SystemCall):
    def handle(self):
        self.task.sendval = None   # setting sendval is optional
        self.sched.schedule(self.task)


# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
if __name__ == '__main__':
    async def foo():
        mytid = await GetTid()
        for i in range(3):
            print("I'm foo", mytid)
            await YieldControl()


    async def bar():
        mytid = await GetTid()
        for i in range(5):
            print("I'm bar", mytid)
            await YieldControl()

    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()