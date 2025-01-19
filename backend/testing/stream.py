import cv2

phone_stream_url = "http://128.189.133.125:4747/video"
cap = cv2.VideoCapture(phone_stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the video frame
    cv2.imshow('Phone Camera Feed', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
