import time
import cv2
from ultralytics import YOLO
import supervision as sv

def detect():
    model = YOLO('yolov8n.pt') # yolo 모델 불러오기
    
    cap = cv2.VideoCapture(0) # 캡쳐 디바이스 선택
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 캡쳐할 화면의 가로 크기 설정
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)# 캡쳐할 화면의 세로 크기 설정
    
    capture_duration = 15 # 객체 감지가 실행될 시간
    start_time = time.time() 
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    count = [] # frame 마다 인식된 객체의 수를 저장할 리스트 초기화
    
    while True:
        # 캡쳐 디바이스에서 정보 읽기
        ret, frame = cap.read()
        # 디바이스에서 영상을 가져올 수 없는 경우 에러 출력후 종료 
        if not ret: 
            print('Cam Error')
            break
        
        # class 이름을 저장할 리스트 초기화
        class_names = []  
        
        # 디바이스에서 캡쳐한 frame을 yolo 모델이 감지하도록 넣어줌
        result = model(frame,classes=[0,1])[0]
        
        #모델이 객체를 감지한 정보를 가져와서 현재 감지된 객체의 갯수를 세고, 리스트에 저장
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[detections.class_id==0]
        count.append(len(detections)) 
        print(len(detections)) #현재 인식된 객체 수 출력
        
        # box에 정보를 표시하기 위해 model engine으로부터 현재 인식중인 class 데이터 가져오기 
        labels = [ 
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _ in detections
            ]
        
        # 사용자에게 현재 감지된 객체를 시각화 하기 위해 사용
        for label in labels:
            class_name = label.split()[0]  # 클래스 이름 추출
            class_names.append(class_name)  # 클래스 이름을 class_names 리스트에 추가
            
        frame = box_annotator.annotate( # 인식된 객체 box를 frame에 합성
            scene=frame,
            detections=detections,
            labels=labels)

        cv2.imshow('K-Tech', frame) # 화면에 결과 출력
    
        stop = int(time.time() - start_time) # 시작 시간으로부터 지난 시간 저장
        if stop > capture_duration or cv2.waitKey(1) == ord('q'): #캡쳐 시간이 다 되었거나 q키를 누를경우 종료
            break
    
    # 카메라 초기화 
    cap.release()
    cv2.destroyAllWindows()
    return count #감지된 객체 수 리스트 반환