import cv2
from ultralytics import YOLO

# Set the video file path directly
VIDEO_PATH = "../yolov8/20250118_123057.mp4"  # 🔹 Change this to your actual video file

# Load the YOLO model
model = YOLO('yolov8n.pt')

# Open the video file
cap = cv2.VideoCapture(VIDEO_PATH)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference with stream=True
    results = model(frame, stream=True)

    # Filter results to only show people (class 0 in COCO dataset)
    for result in results:
        for detection in result.boxes:
            if detection.cls == 0:  # Class 0 is 'person' in COCO dataset
                bbox = detection.xyxy[0].cpu().numpy().astype(int)
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()