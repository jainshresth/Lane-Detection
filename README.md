# LaneDetection-RoadWidthEstimation

A real-time lane detection and road width estimation tool using OpenCV and Python.

## Features
- Converts frames to grayscale and applies Gaussian blur for noise reduction.
- Detects edges using the Canny edge detection algorithm.
- Defines a region of interest (ROI) to focus on the lane lines.
- Uses Hough Transform to detect line segments in the ROI.
- Filters out irrelevant lines based on their slope.
- Draws detected lane lines on the original frame.
- Estimates the road width in pixels.

## Requirements
- Python 3.x
- OpenCV 4.x
- NumPy

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/LaneDetection-RoadWidthEstimation.git
    ```
2. Navigate to the project directory:
    ```sh
    cd LaneDetection-RoadWidthEstimation
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Place your video file in the project directory.
2. Update the `video_path` variable in the script to point to your video file.
3. Run the script:
    ```sh
    python main.py
    ```
4. Press `q` to exit the video playback.

## Code Explanation
- **process_frame(frame):** Processes each frame to detect lane lines and calculate the road width.
- **filter_lines(lines):** Filters out lines that don't match the expected slope for lane lines.
- **draw_lines(image, lines):** Draws the detected lane lines on the image.
- **calculate_road_width(lines, height):** Calculates the width of the road based on detected lane lines.


