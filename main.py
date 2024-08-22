# Executes HUD, runs basic object detection and will have data from ./pathPlanning.py
import cv2
import streamlit as st
from ultralytics import YOLO
import pathPlanning
import trajectoryControl

yolo = YOLO("yolov10s.pt")

st.title("Drone Feed HUD")  # Title for Streamlit HUD
source = cv2.VideoCapture(1, cv2.CAP_DSHOW) #captureDevice = camera
frame_placeholder = st.empty()  # placeholder for camera feed

#! Run path planner
st.write("Running path planner...")
Wn, Wf = pathPlanning.main()
st.write("Waypoints generated: ", Wn, Wf)

#! Run trajectory control

#! Show live updated data (hopefully?) - probably use multithreading and get values from trajectory control to display in Streamlit HUD
# Lowest priority

#! Run object detection and display camera feed
while cv2.waitKey(1) != 27:  # Escape
    has_frame, frame = source.read()

    if not has_frame:
        st.error("Failed to capture video frame")
        break
    results = yolo.track(frame, stream=True)

    # process each video frame
    for result in results:
        all_classes = result.names

        for box in result.boxes:
            #! Display bounding boxes
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
    # Convert the frame from BGR to RGB format (OpenCV uses BGR by default)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame in Streamlit
    frame_placeholder.image(frame, channels="RGB")


source.release()
cv2.destroyAllWindows()
