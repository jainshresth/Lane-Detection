import cv2
import numpy as np


def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    height, width = edges.shape
    roi_vertices = [
        (width * 0.1, height),
        (width * 0.4, height * 0.6),
        (width * 0.6, height * 0.6),
        (width * 0.9, height)
    ]
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [np.array(roi_vertices, np.int32)], 255)

    masked_edges = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=50)

    line_image = np.zeros_like(frame)
    if lines is not None:
        filtered_lines = filter_lines(lines)
        draw_lines(line_image, filtered_lines)
        road_width = calculate_road_width(filtered_lines, height)
    else:
        road_width = 0

    result = cv2.addWeighted(frame, 0.8, line_image, 1, 0)

    return result, road_width


def filter_lines(lines):
    filtered_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1 + 1e-6)  # Add a small value to avoid division by zero
            if 0.5 < abs(slope) < 2:  # Filter lines based on slope
                filtered_lines.append(line)
    return filtered_lines


def draw_lines(image, lines, color=(0, 0, 255), thickness=2):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)


def calculate_road_width(lines, height):
    bottom_y = height - 1
    lane_lines = [line for line in lines if line[0][1] > bottom_y // 2 and line[0][3] > bottom_y // 2]
    if len(lane_lines) < 2:
        return 0
    x_coordinates = [x for line in lane_lines for x, y in [(line[0][0], line[0][1]), (line[0][2], line[0][3])] if
                     y > bottom_y * 0.8]
    road_width = max(x_coordinates) - min(x_coordinates) if x_coordinates else 0
    return road_width


video_path = 'project_video.mp4'
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    processed_frame, road_width = process_frame(frame)

    cv2.putText(processed_frame, f'Road Width: {road_width} px', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
