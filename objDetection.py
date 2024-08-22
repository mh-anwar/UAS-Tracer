#obj detection for UAS

import cv2
# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to read camera feed")
    exit()
# Adjust camera settings
# Further increase brightness and contrast
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.7)  # Adjust and test with values between 0 and 1
cap.set(cv2.CAP_PROP_CONTRAST, 0.7)    # Adjust and test with values between 0 and 1
# Remove exposure adjustment to use the default
# cap.set(cv2.CAP_PROP_EXPOSURE, -6)     # Commented out to use default exposure
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set resolution width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set resolution height
# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Cannot read first frame")
    cap.release()
    cv2.destroyAllWindows()
    exit()
# Select the bounding box
bbox = cv2.selectROI("Tracking", frame, False)
cv2.destroyWindow("Tracking")
# Initialize the tracker with the first frame and bounding box
tracker_type = 'CSRT'  # Choose tracker: 'CSRT', 'KCF', 'MOSSE'
if tracker_type == 'CSRT':
    tracker = cv2.TrackerCSRT_create()
elif tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
elif tracker_type == 'MOSSE':
    tracker = cv2.TrackerMOSSE_create()
else:
    print("Invalid tracker type")
    cap.release()
    cv2.destroyAllWindows()
    exit()
ok = tracker.init(frame, bbox)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    # Update tracker
    ok, bbox = tracker.update(frame)
    # Draw bounding box
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    # Display result
    cv2.imshow("Tracking", frame)
    # Exit if ESC pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()