from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

# Initialize YOLOv8 and DeepSORT
model = YOLO("yolov8n.pt")  # Load YOLOv8 model
tracker = DeepSort(max_age=30, n_init=3)

video_path = "../yolov8/20250118_123057.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read frame.")
        break

    # YOLOv8 inference
    results = model(frame)
    detections = []
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        conf = float(result.conf[0])
        class_id = int(result.cls[0])
        detections.append([x1, y1, x2, y2, conf, class_id])

    print("Detections:", detections)

    # Draw detections directly for debugging
    for det in detections:
        x1, y1, x2, y2, conf, class_id = det
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

