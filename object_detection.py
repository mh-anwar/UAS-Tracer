# Object Detection from UAS Camera Feed
import cv2
import platform


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
    # Adjust camera settings
    # Increase brightness and contrast
    # cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.7)  # Adjust and test with values between 0 and 1
    # cap.set(cv2.CAP_PROP_CONTRAST, 0.7)    # Adjust and test with values between 0 and 1
    # Remove exposure adjustment to use the default
    # cap.set(cv2.CAP_PROP_EXPOSURE, -6)     # Commented out to use default exposure
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


def initialize_tracker(
    tracker_type="CSRT",
):
    # Initialize and return tracker based on chosen tracking type
    # this function never asks for the tracker type, but leaving KCF and MOSSE options in case of future use
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


def track_object(cap, tracker, bounding_box):
    # Initialize tracker with frame and bounding box
    tracker.init(get_frame(cap), bounding_box)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        ok, bounding_box = tracker.update(frame)

        if ok:
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

        cv2.imshow("Object Tracking", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
        elif key == ord("q"):  # 'q' key pressed
            return False  # Signal to reselect object
    return True  # Signal to continue tracking


def main():
    # Camera setup
    cap = setup_camera()

    while True:
        # Capture initial frame for object selection
        frame = get_frame(cap)

        # Allow user to select ROI
        bounding_box = select_roi(frame)

        # Initialize tracker
        tracker = initialize_tracker()

        # Track the object until 'q' is pressed
        continue_tracking = track_object(cap, tracker, bounding_box)
        if not continue_tracking:
            print("Reselecting object...")

        # Exit loop when ESC is pressed
        if continue_tracking:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
