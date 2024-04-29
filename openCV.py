
## camera test

from picamera2 import Picamera2, Preview
import time
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.DRM)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")

## openCV demo - no awareness

import cv2

stream = cv2.VideoCapture(0)

if not stream.isOpened():
    print("Error: Cannot open camera")
    exit()

while(True):
    ret, frame = stream.read()
    if not ret:
        print("Error: Cannot read frame")
        break

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
