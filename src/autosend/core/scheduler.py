import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job
from apscheduler.triggers.base import BaseTrigger
from datetime import datetime
import logging

class AdvancedSchedular():
    def __init__(self):
        self._sheduler = QtScheduler()
        self._started = False

    def shedular_start(self):
        if not self._started:
            self._sheduler.start()
            self._started = True
    
    def shutdown(self, wait: bool=True):
        if self._started:
            self._sheduler.shutdown(wait=wait)
            self._started = False
    
    def add_job(self, job: Job):
        self._scheduler.add_job(job.func, job.trigger, job.args, job.kwargs, job.id, job.name)
 
    def get_job(self, job_id: str) -> Job:
        return self._scheduler.get_job(job_id)
    
    def get_jobs(self) -> list[Job]:
        return self._scheduler.get_jobs()
    
    def remove_job(self, job_id: str):
        job = self.get_job(job_id)
        if job:
            self._scheduler.remove_job(job_id)
    
    def pause_job(self, job_id: str):
        job = self.get_job(job_id)
        if job:
            job.pause()
    
    def resume_job(self, job_id: str):
        job = self.get_job(job_id)
        if job:
            job.resume()
    
    def export_jobs(self):
        self._sheduler.export_jobs(r"src\autosend\core\tasks.json")

    def import_jobs(self):
        self._sheduler.import_jobs(r"src\autosend\core\tasks.json")
    