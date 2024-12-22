# Lab 1: Loading and Displaying an Image with Pillow
from PIL import Image

# Load the image
image = Image.open("example.jpg")

# Display the image
image.show()

# Save the image in a new format
image.save("new_image.png")

# Lab 2: Image Manipulation (Resize, Crop, Grayscale)
from PIL import Image, ImageEnhance

# Load the image
image = Image.open("example.jpg")

# Resize the image
resized_image = image.resize((300, 300))
resized_image.show()

# Crop the image
cropped_image = image.crop((100, 100, 400, 400))
cropped_image.show()

# Convert to grayscale
grayscale_image = image.convert("L")
grayscale_image.show()

# Adjust brightness
enhancer = ImageEnhance.Brightness(image)
bright_image = enhancer.enhance(1.5)  # 1.5 times brighter
bright_image.show()

# Lab 3: Drawing Shapes and Text on an Image
from PIL import Image, ImageDraw, ImageFont

# Load the image
image = Image.open("example.jpg")
draw = ImageDraw.Draw(image)

# Draw a rectangle
draw.rectangle((50, 50, 200, 200), outline="red", width=5)

# Draw text
font = ImageFont.load_default()
draw.text((50, 250), "Hello, World!", font=font, fill="white")

# Show the image
image.show()

# Save the image
image.save("edited_image.jpg")

# Lab 4: Playing Audio with Pygame
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load and play the audio
pygame.mixer.music.load("example.mp3")
pygame.mixer.music.play()

# Keep the script running to allow audio to play
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# Lab 5: Video Processing with OpenCV
import cv2

# Open video file
video = cv2.VideoCapture("example.mp4")

# Loop through each frame
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Apply grayscale filter
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the frame
    cv2.imshow("Video", gray_frame)

    # Press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release video and close windows
video.release()
cv2.destroyAllWindows()

# Lab 6: Creating a Multimedia Slideshow with Audio
import cv2
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Play on loop

# List of image files for the slideshow
image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]

# Display each image for 2 seconds
for image_file in image_files:
    image = cv2.imread(image_file)
    cv2.imshow("Slideshow", image)
    cv2.waitKey(2000)  # Wait for 2 seconds

# Stop the music and release resources
pygame.mixer.music.stop()
cv2.destroyAllWindows()

# Lab 7: Simple GUI for Image Manipulation with Tkinter
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    image.thumbnail((300, 300))
    img_display = ImageTk.PhotoImage(image)
    label.config(image=img_display)
    label.image = img_display  # Keep a reference to avoid garbage collection

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Create a label to display the image
label = tk.Label(root)
label.pack()

# Create an open button
button = tk.Button(root, text="Open Image", command=open_image)
button.pack()

# Start the Tkinter event loop
root.mainloop()

# Lab 8: Final Project Example (Image Editor)
from PIL import Image, ImageFilter

# Load an image
image = Image.open("example.jpg")

# Apply some filters
blurred_image = image.filter(ImageFilter.BLUR)
contour_image = image.filter(ImageFilter.CONTOUR)

# Show results
blurred_image.show()
contour_image.show()

# Save results
blurred_image.save("blurred_example.jpg")
contour_image.save("contour_example.jpg")

# Lab 9: Face Detection with OpenCV
import cv2

# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the video file or camera
video = cv2.VideoCapture(0)  # Use 0 for webcam, or 'example.mp4' for video file

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the frame
    cv2.imshow("Face Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release video and close windows
video.release()
cv2.destroyAllWindows()
