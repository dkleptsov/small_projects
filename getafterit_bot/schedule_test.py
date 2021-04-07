import schedule
import time

def notify():
    print("Hello!")

schedule.every(1).to(3).seconds.do(notify)