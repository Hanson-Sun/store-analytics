from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import threading
from yolo import AIVisionDetector
from scipy.spatial import KDTree

app = Flask(__name__)
CORS(app)

## MONGO DB SCAFFOLDING
# MONGO_URI = "mongodb+srv://nicholaschang0930:1aCcoFMQxHdYCxoG@cluster0.f9jls.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
MONGO_URI = "mongodb+srv://user:user@nwhacks2025.5wysc.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks2025"
client = MongoClient(MONGO_URI)
db = client["store-analytics"]
analytics_collection = db["test1"]

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
            # cv2.imshow('Camera Feed', frame)
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

        if len(centroids) > 0 and datetime.now().second % 1 == 0:
            insert_data(frame_data, centroids, timestamp)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    for centroid, data in zip(centroids, frame_data):
        box = [int(coord) for coord in data['box']]
        obj_id = int(data['id'])
        centroid = [float(coord) for coord in centroid]

        data_list.append({
            "time": utc_time,
            "obj_id": obj_id,
            "coordinates": centroid,
            "box": box
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

@app.route('/api/get_dimensions', methods=['GET'])
def get_dimensions():
    # get dimensions of the video feed
    if FRAME is None:
        return jsonify({"height": 480, "width": 640})
    height, width, _ = FRAME.shape
    return jsonify({"height": height, "width": width})

@app.route('/api/get_heatmap_data', methods=['GET'])
def get_heatmap_data():
    # Get the start and end times specified by the user
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    # Convert the start and end times to datetime objects
    if start_time_str and float(start_time_str) >= 0:
        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=timezone.utc)
    else:
        start_time = datetime.min.replace(tzinfo=timezone.utc)  # Default to the earliest possible time

    if end_time_str and float(end_time_str) >= 0:
        end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=timezone.utc)
    else:
        end_time = datetime.now(timezone.utc)  # Default to the latest possible time

    # Retrieve all data from the database within the specified time range
    data = analytics_collection.find({
        "time": {
            "$gte": start_time,
            "$lte": end_time
        }
    })

    coordinates = [entry['coordinates'] for entry in data]
    if not coordinates:
        return jsonify([]) 

    tree = KDTree(coordinates)

    radius = float(request.args.get('radius', 10))

    heatmap_data = []
    max_intensity = 0
    for coord in coordinates:
        indices = tree.query_ball_point(coord, radius)
        intensity = len(indices)
        max_intensity = max(max_intensity, intensity)
        heatmap_data.append({
            "x": coord[0],
            "y": coord[1],
            "intensity": intensity
        })

    for point in heatmap_data:
        point['intensity'] = (point['intensity'] / max_intensity) * 100

    return jsonify(heatmap_data)

@app.route('/api/count_unique_objects', methods=['GET'])
def count_unique_objects():
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    # Convert the start and end times to datetime objects
    if start_time_str and float(start_time_str) >= 0:
        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=timezone.utc)
    else:
        start_time = datetime.min.replace(tzinfo=timezone.utc)  # Default to the earliest possible time

    if end_time_str and float(end_time_str) >= 0:
        end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=timezone.utc)
    else:
        end_time = datetime.now(timezone.utc)  # Default to the latest possible time

    data = analytics_collection.find({
        "time": {
            "$gte": start_time,
            "$lte": end_time
        }
    })

    unique_obj_ids = set(entry['obj_id'] for entry in data)

    return jsonify({"result": len(unique_obj_ids)})

@app.route('/api/get_object_paths', methods=['GET'])
def get_object_paths():
    # Get the start and end times specified by the user
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    # Convert the start and end times to datetime objects
    if start_time_str and float(start_time_str) >= 0:
        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=timezone.utc)
    else:
        start_time = datetime.min.replace(tzinfo=timezone.utc)  # Default to the earliest possible time

    if end_time_str and float(end_time_str) >= 0:
        end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=timezone.utc)
    else:
        end_time = datetime.now(timezone.utc)  # Default to the latest possible time

    # Retrieve all data from the database within the specified time frame
    data = analytics_collection.find({
        "time": {
            "$gte": start_time,
            "$lte": end_time
        }
    })

    # Group data by obj_id and sort by time
    object_paths = {}
    for entry in data:
        obj_id = entry['obj_id']
        if obj_id not in object_paths:
            object_paths[obj_id] = []
        object_paths[obj_id].append({
            "time": entry['time'],
            "coordinates": entry['coordinates']
        })

    # Sort the paths by time for each object
    for obj_id in object_paths:
        object_paths[obj_id].sort(key=lambda x: x['time'])

    return jsonify(object_paths)

@app.route('/api/unique_objects_per_hour', methods=['GET'])
def unique_objects_per_hour():
    # Get the number of days specified by the user
    days = int(request.args.get('days', 1))  # Default to 1 day if not specified

    # Calculate the start and end times
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    # Retrieve all data from the database within the specified time frame
    data = analytics_collection.find({
        "time": {
            "$gte": start_time,
            "$lte": end_time
        }
    })

    hourly_counts = defaultdict(set)
    for entry in data:
        hour = entry['time'].hour
        obj_id = entry['obj_id']
        hourly_counts[hour].add(obj_id)

    hourly_counts = {hour: len(obj_ids) for hour, obj_ids in hourly_counts.items()}
    return jsonify(hourly_counts)


if __name__ == '__main__':
    video = VideoStream("http://10.43.245.35:4747/video")
    video.play_video()

    app.run(port = 8000, debug=False)

