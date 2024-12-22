# 1. Installing OpenCV Library
# Command:
# pip install opencv-python

# 2. Loading and Playing a Video
import cv2
video = cv2.VideoCapture("example.mp4")
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    cv2.imshow("Video Playback", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# 3. Converting Video Frames to Grayscale
import cv2
video = cv2.VideoCapture("example.mp4")
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale Video", gray_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# 4. Applying Edge Detection (Canny Algorithm)
import cv2
video = cv2.VideoCapture("example.mp4")
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    edges = cv2.Canny(frame, 100, 200)
    cv2.imshow("Edge Detection", edges)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# 5. Overlaying Text on Video Frames
import cv2
video = cv2.VideoCapture("example.mp4")
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    cv2.putText(frame, "Hello, Video!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Video with Text", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# 6. Saving Video Output
import cv2
video = cv2.VideoCapture("example.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (int(video.get(3)), int(video.get(4))))
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    out.write(frame)
    cv2.imshow("Saving Video", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
out.release()
cv2.destroyAllWindows()

# 7. Extracting Frames from a Video
import cv2
video = cv2.VideoCapture("example.mp4")
frame_count = 0
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    if frame_count % 30 == 0:
        cv2.imwrite(f"frame_{frame_count}.jpg", frame)
    frame_count += 1
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# 8. Combining Videos
import cv2
video1 = cv2.VideoCapture("video1.mp4")
video2 = cv2.VideoCapture("video2.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('combined.avi', fourcc, 30.0, (int(video1.get(3)), int(video1.get(4))))
while video1.isOpened() and video2.isOpened():
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    if not ret1 or not ret2:
        break
    out.write(frame1)
    out.write(frame2)
video1.release()
video2.release()
out.release()
cv2.destroyAllWindows()

# 9. Adding Filters to Video Frames
import cv2
video = cv2.VideoCapture("example.mp4")
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)
    cv2.imshow("Blurred Video", blurred_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# 10. Full Example: Advanced Video Processing
import cv2
video = cv2.VideoCapture("example.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('processed_output.avi', fourcc, 30.0, (int(video.get(3)), int(video.get(4))))
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_frame, 100, 200)
    out.write(edges)
    cv2.imshow("Processed Video", edges)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
out.release()
cv2.destroyAllWindows()
