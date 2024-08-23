# Executes HUD, runs basic object detection and will have data from ./pathPlanning.py
import streamlit as st
import cv2
import path_planning
import object_detection
import trajectory_control
import pandas as pd
import platform
import numpy as np


def setup_camera(camera_index=0, resWidth=1280, resHeight=720):
    # Initialize camera
    if platform.system() == "Windows":
        cap = cv2.VideoCapture(
            camera_index, cv2.CAP_DSHOW
        )  # flag for Windows DirectShow
    else:
        cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Unable to read camera feed")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resWidth)  # Set resolution width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resHeight)  # Set resolution height

    return cap


def get_frame(cap):
    # Capture frame from camera
    ret, frame = cap.read()
    if not ret:
        print("Cannot read frame")
        cap.release()
        cv2.destroyAllWindows()
        exit()
    return frame


def select_roi(frame):
    # Select the bounding box
    bounding_box = cv2.selectROI("Tracking", frame, False)
    cv2.destroyWindow("Tracking")
    return bounding_box


def initialize_tracker(tracker_type="CSRT"):
    # Initialize and return tracker based on chosen tracking type
    trackers = {
        "CSRT": cv2.TrackerCSRT_create,
        "KCF": cv2.TrackerKCF_create,
        "MOSSE": cv2.legacy.TrackerMOSSE_create,
    }

    if tracker_type not in trackers:
        print(f"Invalid tracker type '{tracker_type}'. Using default CSRT tracker.")
        tracker_type = "CSRT"

    tracker = trackers[tracker_type]()
    return tracker


def track_object(
    cap,
    tracker,
    bounding_box,
    frame_placeholder,
):
    # Define display height including space for text
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    display_height = frame_height + 100

    # Initialize tracker with frame and bounding box
    tracker.init(get_frame(cap), bounding_box)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        success, bounding_box = tracker.update(frame)

        if success:
            (x, y, w, h) = [int(v) for v in bounding_box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.putText(
                frame,
                "Tracking failure detected",
                (100, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 255),
                2,
            )

        # Create a blank image with additional space for text
        display_image = np.zeros((display_height, frame_width, 3), dtype=np.uint8)
        display_image[:frame_height, :frame_width] = frame

        # Display the result
        cv2.imshow("Object Tracking", display_image)
        frame_placeholder.image(display_image, channels="BGR")

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
        elif key == ord("q"):  # 'q' key pressed
            return False  # Signal to reselect object
    return True  # Signal to continue tracking


def main():

    #! Base HUD Setup
    st.title("UAS Tracer")
    current_status = st.empty()
    frame_placeholder = st.empty()  # placeholder for camera feed

    current_status.text("Starting up camera feed...")
    cap = object_detection.setup_camera()

    #! Run path planner
    current_status.text("Running path planner...")
    Wn, Wf = path_planning.main()

    df_1 = pd.DataFrame(Wn.T, columns=["X", "Y"])
    df_2 = pd.DataFrame(Wf.T, columns=["X", "Y"])

    st.title("Generated Waypoints")

    st.write("Wn:")
    st.table(df_1)

    st.write("Wf:")
    st.table(df_2)

    #! Run trajectory control
    current_status.text("Running trajectory control...")
    trajectory_control.main(Wn)
    # ? NEED TO ADD TABLE FOR TRAJECTORY CONTROL DATA

    #! Run object detection
    while True:
        # Capture initial frame for object selection
        frame = get_frame(cap)

        current_status.text("Selecting object...")
        # Allow user to select ROI
        bounding_box = select_roi(frame)

        # Initialize tracker
        tracker = initialize_tracker()

        current_status.text("Running object detection...")
        # Track the object until 'q' is pressed
        continue_tracking = track_object(cap, tracker, bounding_box, frame_placeholder)
        if not continue_tracking:
            print("Reselecting object...")

        # Exit loop when ESC is pressed
        if continue_tracking:
            break

    cap.release()
    cv2.destroyAllWindows()


main()
"""
Idea: use one camera feed in main.py
- Run path planner
- Run trajectory control - feed Wn from main.py to trajectory control
- Run object detection with the same camera feed
- Display data from path planner and trajectory control in HUD
- Display object detection results in it's own CV2 window (no streaming to streamlit)
- Potentially annotate streamlit cam feed with data from path planner and trajectory control
"""
