from crontab import CronTab

def start_job():
    cron = CronTab(user=True)
    cron.remove_all()
    # Create the updated job
    job = cron.new(command="/usr/local/bin/python3 /project/clear_cache.py >> /var/log/cron.log 2>&1")
    job.minutes.every(59)

    cron.write()


