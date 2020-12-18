import schedule
import time
from app1.models import User

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)