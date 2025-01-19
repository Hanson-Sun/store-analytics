from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from pymongo import MongoClient
from datetime import datetime
import threading
from yolo import AIVisionDetector

app = Flask(__name__)
CORS(app)

## MONGO DB SCAFFOLDING
MONGO_URI = "mongodb+srv://nicholaschang0930:1aCcoFMQxHdYCxoG@cluster0.f9jls.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
client = MongoClient(MONGO_URI)
db = client["store_analytics"]
analytics_collection = db["analytics"]

# TODO

FRAME = None

class VideoStream:
    def __init__(self, url):
        self._is_playing = False
        self._thread = None
        self._url = url
        self._cap = cv2.VideoCapture(url)
        self._lock = threading.Lock()
        self._current_frame = None
        self._detector = AIVisionDetector()
        self._data = None
    
    def get_frame(self):
        global FRAME
        with self._lock:
            if not self._cap.isOpened():
                print("Error: VideoCapture is not opened.")
                return None
            ret, frame = self._cap.read()
            self._current_frame = frame
            FRAME = frame
            if not ret:
                print("Error: Could not get frame!!")
                return None
            return frame
        
    def process_frame(self, frame):
        data = self._detector.detect(frame)
        detections = self._detector.track(frame, data[0])

        frame_data, centroids, timestamp = self._detector.process_data((detections, data[1]))

        return frame_data, centroids, timestamp
    
    def _play_video(self):
        while self._is_playing:
            frame = self.get_frame()
            if frame is None:
                break
            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self._is_playing = False
                break

    def play_video(self):
        if not self._is_playing:
            self._is_playing = True
            self._thread = threading.Thread(target=self._play_video)
            self._thread.daemon = True
            self._thread.start()
    
    def stop_video(self):
        self._is_playing = False
        if self._thread is not None:
            self._thread.join()

    def set_url(self, url):
        self._url = url
        self._cap = cv2.VideoCapture(url)

        print(f"URL SET TO {url}")

    def release(self):
        self._cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.stop_video()
        self.release()

@app.route('/set_camera_url', methods=['POST'])
def set_camera_url():
    global video
    data = request.json
    if not data:
        return jsonify({"status": "error", "result": "No data received."})
    url = data.get("url")
    if not url:
        return jsonify({"status": "error", "result": "No URL provided."})
    video.set_url(url)
    return jsonify({"status": "success", "result": "Camera URL updated."})


@app.route('/get_camera_url', methods=['GET'])
def get_camera_url():
    return jsonify({"result": video._url})

def generate_video():
    while True:
        frame = FRAME
        if frame is None:
            print("frame not found")
            continue

        frame_data, centroids, timestamp = video.process_frame(frame)
        frame = video._detector.draw_boxes(frame, frame_data)

        # if len(centroids) > 0 and datetime.now().second % 1 == 0:
        #     insert_data(frame_data, centroids, timestamp)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_heatmap():
    global heatmap_accumulator
    # while True:
    #     # okay actually do something here

@app.route('/heatmap_feed')
def heatmap_feed():
    return Response(generate_heatmap(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        return jsonify({"status": "success", "result": data})
    elif request.method == 'GET':
        return jsonify({"result": "Send some data using POST!"})

# API route to store data from MongoDB
@app.route('/api/store_data', methods=['POST'])
def store_data():
    data = request.json
    result = analytics_collection.insert_one(data)
    return jsonify({"status": "success", "result": f"Coordinate stored in the database {result}"})

def insert_data(frame_data, centroids, timestamp):
    data_list = []
    for centroid, data in zip(centroids, frame_data):
        data_list.append({
            "timestamp": timestamp,
            "coordinates": centroid,
            "box": data['box'],
            "id": data['id']
        })
    
    result = analytics_collection.insert_many(data_list)
    return result

# API route to retrieve data from MongoDB
@app.route('/api/get_data', methods=['GET'])
def get_data():
    data = analytics_collection.find({})
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "Not found"}), 404

if __name__ == '__main__':
    video = VideoStream("http://10.43.245.35:4747/video")
    video.play_video()

    app.run(debug=False)

