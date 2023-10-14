import HumanDetector
import numpy
import schedule
import time
from datetime import datetime

def run():
    print("객체 감지 시작")
    detected_list = HumanDetector.detect()
    
    # 감지 후 인식된 객체 수 리스트의 평균을 구하고 반올림
    m = round(numpy.mean(detected_list)) 
    # 현재 시간 구하기
    time_today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    print(f'{time_today} 감지 결과:{m}명')
    
    #log 폴더에 txt파일로 저장
    file= open("log/detected_log.txt","w+",encoding="utf-8")
    file.write(f"{time_today} 감지 결과:{m}명")
    file.close()

#평일 아침 08:30분에 객체 감지 시작
schedule.every().monday.at("08:30").do(run)
schedule.every().tuesday.at("08:30").do(run)
schedule.every().wednesday.at("08:30").do(run)
schedule.every().thursday.at("08:30").do(run)
schedule.every().friday.at("08:30").do(run)

#테스트용 코드 - 1분마다 run 실행
#schedule.every(1).minute.do(run)

#스케줄 시작
while True:
    print("스케줄 동작중...")
    schedule.run_pending()
    time.sleep(10)
