# 1. Installing Pillow Library
# Command:
# pip install Pillow

# 2. Loading and Creating Images
from PIL import Image

# Load an image
image = Image.open("example.jpg")
image.show()

# Create a new image
new_image = Image.new("RGB", (500, 500), (255, 255, 255))
new_image.show()

# 3. Viewing Basic Image Properties
print(f"Format: {image.format}")
print(f"Size: {image.size}")
print(f"Mode: {image.mode}")

# 4. Resizing Images
resized_image = image.resize((300, 300))
resized_image.show()

image.thumbnail((300, 300))
image.show()

# 5. Rotating and Flipping Images
rotated_image = image.rotate(45)
rotated_image.show()

flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
flipped_image.show()

rotated_image_expand = image.rotate(45, expand=True)
rotated_image_expand.save("rotated_image_auto_expand.png")
rotated_image_expand.show()

# 6. Cropping Images
cropped_image = image.crop((100, 100, 400, 400))
cropped_image.show()

# 7. Drawing Shapes on Images
from PIL import ImageDraw

draw = ImageDraw.Draw(image)
draw.rectangle([50, 50, 200, 200], outline="black", fill="blue")
draw.ellipse([250, 50, 400, 200], outline="black", fill="green")
draw.line([50, 300, 400, 350], fill="red", width=5)
image.show()

# 8. Adding Text to Images
from PIL import ImageFont

font = ImageFont.truetype("arial.ttf", 36)
draw.text((50, 400), "Hello, Pillow!", font=font, fill="black")
image.show()

# 9. Applying Filters to Images
from PIL import ImageFilter

blurred_image = image.filter(ImageFilter.BLUR)
blurred_image.show()

sharpened_image = image.filter(ImageFilter.SHARPEN)
sharpened_image.show()

contour_image = image.filter(ImageFilter.CONTOUR)
contour_image.show()

# 10. Color Transformations
gray_image = image.convert("L")
gray_image.show()

rgb_image = gray_image.convert("RGB")
rgb_image.show()

# 11. Combining Images
image1 = Image.open("image1.jpg")
image2 = Image.open("image2.png")
image2 = image2.resize(image1.size)
image1.paste(image2, (50, 50))
image1.show()

# 12. Saving Images
image.save("output_image.png")
image.save("output_image.jpg", "JPEG")

# 13. Image Transparency
transparent_image = Image.new("RGBA", (500, 500), (255, 255, 255, 0))
draw = ImageDraw.Draw(transparent_image)
draw.rectangle([50, 50, 200, 200], fill=(255, 0, 0, 128))
transparent_image.save("transparent_image.png")
transparent_image.show()

# 14. Image Blending
image1 = Image.open("image1.jpg")
image2 = Image.open("image2.png")
image2 = image2.resize(image1.size)
blended_image = Image.blend(image1, image2, alpha=0.5)
blended_image.show()

# 15. Comprehensive Image Processing
image = Image.open("example.jpg")
image.thumbnail((400, 400))
rotated_image = image.rotate(45, expand=True)
draw = ImageDraw.Draw(rotated_image)
draw.rectangle([50, 50, 200, 200], outline="black", fill="blue")
draw.ellipse([250, 50, 400, 200], outline="black", fill="green")
font = ImageFont.truetype("arial.ttf", 36)
draw.text((50, 250), "Hello, World!", font=font, fill="black")
filtered_image = rotated_image.filter(ImageFilter.SHARPEN)
filtered_image.save("final_output.png")
filtered_image.show()

# 16. Creating Basic Animations (GIF)
from PIL import ImageDraw

def create_frame(ball_position):
    frame = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(frame)
    draw.ellipse([ball_position, 150, ball_position + 50, 200], fill="blue")
    return frame

frames = [create_frame(x) for x in range(0, 350, 10)]
frames[0].save("bouncing_ball.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)

# 17. Animation of Multiple Shapes
def create_frame_with_shapes(frame_num):
    frame = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(frame)
    circle_position = 50 + frame_num * 5
    draw.ellipse([circle_position, 150, circle_position + 50, 200], fill="blue")
    draw.rectangle([150, 150, 200, 200], fill="green")
    return frame

frames = [create_frame_with_shapes(frame_num) for frame_num in range(20)]
frames[0].save("moving_circle_rotating_rect.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
