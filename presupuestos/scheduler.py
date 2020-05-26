import schedule
import time

def hola():
    print("Hola")

schedule.every(2).seconds.do(hola)

while 1:
    schedule.run_pending()
    time.sleep(1)