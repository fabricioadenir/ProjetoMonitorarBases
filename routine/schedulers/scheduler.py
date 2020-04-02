from apscheduler.schedulers.background import BackgroundScheduler
from routine.schedulers.monitoring import run_monitoring

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_monitoring, 'interval', minutes=1)
    scheduler.start()
