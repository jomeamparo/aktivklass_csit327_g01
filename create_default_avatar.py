from PIL import Image, ImageDraw, ImageFont
import os

def create_default_avatar():
    # Create a directory for media if it doesn't exist
    os.makedirs('media', exist_ok=True)
    os.makedirs('media/student_profiles', exist_ok=True)
    
    # Create a 300x300 blue background image
    img = Image.new('RGB', (300, 300), color=(73, 109, 137))
    
    # Draw a simple avatar placeholder
    d = ImageDraw.Draw(img)
    
    # Draw a circle for the head
    d.ellipse((100, 70, 200, 170), fill=(240, 240, 240))
    
    # Draw a larger ellipse for the body
    d.ellipse((75, 200, 225, 350), fill=(240, 240, 240))
    
    # Save the image
    img.save('media/default_avatar.jpg')
    print("Default avatar created at media/default_avatar.jpg")

if __name__ == "__main__":
    create_default_avatar() 