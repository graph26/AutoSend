import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job
from apscheduler.triggers.base import BaseTrigger
import json
from datetime import datetime

class AdvancedSchedular():
    def __init__(self):
        self._sheduler = AsyncIOScheduler()
        self._started = False

    async def start(self):
        if not self._started:
            self._sheduler.start()
            self._started = True
    
    async def shutdown(self, wait: bool=True):
        if self._started:
            self._sheduler.shutdown(wait=wait)
            self._started = False
    
    def add_job(self, job: Job):
        self._scheduler.add_job(job.func, job.trigger, job.args, job.kwargs, job.id, job.name,
                                job.misfire_grace_time, job.coalesce, job.max_instances, job.next_run_time, executor=job.executor)
 
    def get_job(self, job_id: str):
        return self._scheduler.get_job(job_id)
    
    def get_jobs(self):
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
    
    