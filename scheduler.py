import schedule
import time
from datetime import datetime
from threading import Thread

class Scheduler:
    def __init__(self):
        self.running = False
        self.scheduler_thread = None

    def run_scheduler(self):
        while self.running:
            schedule.run_pending()
            time.sleep(60)

    def schedule_task(self, task_func, schedule_type: str, schedule_time):
        """
        Schedule a task based on the specified schedule type and time
        """
        schedule.clear()
        
        if schedule_type == "Hourly":
            schedule.every(schedule_time).hours.do(task_func)
        
        elif schedule_type == "Daily":
            schedule.every().day.at(schedule_time.strftime("%H:%M")).do(task_func)
        
        elif schedule_type == "Weekly":
            day, time = schedule_time
            getattr(schedule.every(), day.lower()).at(
                time.strftime("%H:%M")).do(task_func)

        if not self.running:
            self.running = True
            self.scheduler_thread = Thread(target=self.run_scheduler)
            self.scheduler_thread.start()

    def stop(self):
        """
        Stop the scheduler
        """
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
