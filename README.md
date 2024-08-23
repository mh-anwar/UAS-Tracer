# Visual Target Detection Influenced Trajectory Generation
Implemented using path planning algorithm from [A path planning algorithm for a crop monitoring fixed-wing unmanned aerial system](https://link.springer.com/article/10.1007/s11432-023-4087-4) that develops a path in a field to find an object, which is detected using a drone camera feed that is processed with OpenCV and YOLOV10. Once the object is detected a trajectory towards it is generated. The recommended path, along with current drone statistics and live camera feed are displayed in a HUD. 


## Run Instructions
- [Create an Anaconda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
  - ```conda create -n target_tracking```
  - ```conda activate target_tracking```
- Run ```pip install -r requirements.txt```
- Start the "ground control" with ```streamlit run main.py```

### Individual Script Testing
- Run ```python3 path_planning.py``` to generate Waypoints given the input vector map
- Run ```python3 object_detection.py``` to detect objects given a camera feed - requires Waypoints as input
- Run ```python3 trajectory_generation.py``` to generate heading commands and a waypoint