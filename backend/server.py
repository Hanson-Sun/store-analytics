from flask import Flask, Response, jsonify, request
import cv2
import numpy as np
from pymongo import MongoClient
from datetime import datetime
import threading

app = Flask(__name__)

## MONGO DB SCAFFOLDING
MONGO_URI = "mongodb://localhost:27017/" 
client = MongoClient(MONGO_URI)
db = client["store_analytics"]
analytics_collection = db["analytics"]

# TODO
class AIVisionDetector:
    self.video_stream = None
    self.detector = None


class VideoVisualizer:
    def __init__(self):
        self.video_stream = None



class VideoStream:
    def __init__(self, url):
        self._is_playing = False
        self._thread = None
        self._url = url
        self._cap = cv2.VideoCapture(url)
    
    def get_frame(self):
        ret, frame = self._cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return None
        return frame
    
    def _play_video(self):
            while self._is_playing:
                frame = self.get_frame()
                if frame is None:
                    break
                cv2.imshow('Camera Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_video()
                    break
            self.release()

    def play_video(self):
        if not self._is_playing:
            self._is_playing = True
            self._thread = threading.Thread(target=self._play_video)
            self._thread.start()
    
    def stop_video(self):
        self._is_playing = False
        if self._thread is not None:
            self._thread.join()

    def set_url(self, url):
        self._url = url
        self._cap = cv2.VideoCapture(url)

    def release(self):
        self._cap.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.release()


video = VideoStream("http://128.189.133.125:4747/video")

def generate_video():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('frame', frame)
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def generate_heatmap():
    global heatmap_accumulator
    # while True:
    #     # okay actually do something here

@app.route('/set_camera_url', methods=['POST'])
def set_camera_url():
    global VIDEO_STREAM_URL
    global cap
    data = request.json
    VIDEO_STREAM_URL = data['camera_url']
    cap = cv2.VideoCapture(VIDEO_STREAM_URL)
    return jsonify({"status": "success", "result": "Camera URL updated."})

@app.route('/get_camera_url', methods=['GET'])
def get_camera_url():
    return jsonify({"result": VIDEO_STREAM_URL})

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

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

@app.route('/api/store_data', methods=['POST'])
def store_data():
    # replace with actual implemtation
    # try:
    #     data = request.json
    #     if not data:
    #         return jsonify({"status": "error", "message": "No data received."})

    #     data['timestamp'] = datetime.utcnow().isoformat()

    #     analytics_collection.insert_one(data)

    #     return jsonify({"status": "success", "message": "Data stored in the database."})
    # except Exception as e:
    #     return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "success", "result": "Data stored in the database."})

# API route to retrieve data from MongoDB
@app.route('/api/get_data', methods=['GET'])
def get_data():
    # replace with actual implementation
    # try:
    #     # Fetch all documents from the collection
    #     data = list(analytics_collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id field from the output
    #     return jsonify(data)
    # except Exception as e:
    #     return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "success", "result": "Data retrieved from the database."})

if __name__ == '__main__':
    app.run(debug=True)
