import cv2
from ultralytics import YOLO

# load yolov8 - attempt interchanging w/other models
yolo = YOLO("yolov10s.pt")

# start video capture
videoCap = cv2.VideoCapture(0)

# calibration of camera may be needed

while True:
    # read each frame
    ret, frame = videoCap.read()
    if not ret:
        continue
    results = yolo.track(frame, stream=True)

    # process each video frame
    for result in results:
        all_classes = result.names

        for box in result.boxes:
            if box.conf[0] > 0.5:  # display if confidence of object is >50%
                # get coordinates and map to integers
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # get class of object
                cls = int(box.cls[0])

                # retreive object name
                object_name = all_classes[cls]

                # draw the bounding box                 color is blue
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # display object name + confidence
                cv2.putText(
                    frame,
                    f"{object_name} {box.conf[0]:.2f}",
                    (x1, y1),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (255, 0, 0),
                    2,
                )
    # show image, if e is pressed then Exit
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break

# end video capture + destroy frame window
videoCap.release()
cv2.destroyAllWindows()
