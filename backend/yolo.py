import cv2
from ultralytics import YOLO

class AIVisionDetector:
    model = YOLO('yolov8n.pt')

    def __init__(self):
        self._data = []
        pass

    def detect(self, frame) -> list:
        results = self.model(frame, stream=True)
        frame_data = []
        for result in results:
            for detection in result.boxes:
                if detection.cls == 0:
                    bbox = detection.xyxy[0].cpu().numpy().astype(int)
                    frame_data.append(bbox)

        self._data.append(frame_data)
        return frame_data
    
    def draw_boxes(self, frame, boxes) -> None:
        for box in boxes:
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        return frame
