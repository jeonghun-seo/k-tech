import time
import cv2
from ultralytics import YOLO
import supervision as sv

def detect():
    model = YOLO('yolov8n.pt')

    capture_duration = 15
    start_time = time.time()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    count = []
    
    while True:
        
        ret, frame = cap.read()
        if not ret:
            print('Cam Error')
            break
        class_names = []  # 빈 리스트 생성
        result = model(frame,classes=[0,1])[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[detections.class_id==0]
        count.append(len(detections))
        print(len(detections))
        labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _ in detections
            ]
    
        for label in labels:
            class_name = label.split()[0]  # 클래스 이름 추출
            class_names.append(class_name)  # 클래스 이름을 class_names 리스트에 추가
        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels)

        cv2.imshow('yolov8', frame)
    
        stop = int(time.time() - start_time)
        if stop > capture_duration:
            break
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return count