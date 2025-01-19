import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import time
import random

class AIVisionDetector:
    model = YOLO('yolov8n.pt')
    tracker = DeepSort(max_age=5)

    def __init__(self):
        self.colors = {}
        self.THRESHOLD = 0.7

    def detect(self, frame) -> tuple:
        timestamp = time.time()
        frame_data = []
        detections = self.model(frame)[0] 

        for data in detections.boxes.data.tolist():
            confidence = data[4] 

            if confidence < self.THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            class_id = int(data[5])
            bbox = [xmin, ymin, xmax - xmin, ymax - ymin]
            frame_data.append([bbox, confidence, class_id])

        return (frame_data, timestamp)

    def track(self, frame, boxes) -> list:
        detections = []
        tracks = self.tracker.update_tracks(boxes, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            ltrb = track.to_tlbr().astype(int)
            x1, y1, x2, y2 = ltrb
            detections.append({"box": [x1, y1, x2, y2], 'id': track_id})

        return detections

    def process_data(self, frame_data) -> tuple:
        centroids = []
        for data in frame_data[0]:
            box = data['box']
            x1, y1, x2, y2 = box
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            centroids.append((cx, cy))

        return (frame_data[0], centroids, frame_data[1])
    
    def get_color(self, track_id):
        if track_id not in self.colors:
            self.colors[track_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return self.colors[track_id]

    def draw_boxes(self, frame, boxes) -> None:
        for box in boxes:
            color = self.get_color(box['id'])
            cv2.rectangle(frame, (box['box'][0], box['box'][1]), (box['box'][2], box['box'][3]), color, 2)
            cv2.putText(frame, str(box['id']), (box['box'][0], box['box'][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        return frame
