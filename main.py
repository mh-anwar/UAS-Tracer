# Executes HUD, runs basic object detection and will have data from ./pathPlanning.py
import path_planning
import object_detection
import trajectory_control


#! Run path planner
Wn, Wf = path_planning.main()

#! Run trajectory control

#! Show live updated data (hopefully?) - probably use multithreading and get values from trajectory control to display in Streamlit HUD
# Lowest priority

#! Run object detection and display camera feed
object_detection.main(Wn)


"""
Idea: use one camera feed in main.py
- Run path planner
- Run trajectory control - feed Wn from main.py to trajectory control
- Run object detection with the same camera feed
- Display data from path planner and trajectory control in HUD
- Display object detection results in it's own CV2 window (no streaming to streamlit)
- Potentially annotate streamlit cam feed with data from path planner and trajectory control

"""
