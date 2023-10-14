import HumanDetector
import numpy
import schedule
import time
from datetime import datetime

def run():
    print("객체 감지 시작")
    detected_list = HumanDetector.detect()
    m = round(numpy.mean(detected_list))
    time_today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    print(f'{time_today} 감지 결과:{m}명')
    
    file= open("log/detected_log.txt","w+",encoding="utf-8")
    file.write(f"{time_today} 감지 결과:{m}명")
    file.close()

schedule.every(1).minute.do(run)

while True:
    print("스케줄 동작중...")
    schedule.run_pending()
    time.sleep(10)
