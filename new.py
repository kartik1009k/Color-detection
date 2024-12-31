import cv2
import pandas as pd
import os

# Load the image from the specified path
image_path = './ak.jpg'  # Update this path as needed
if not os.path.exists(image_path):
    print(f"Image file not found: {image_path}")
    exit()

image = cv2.imread(image_path)

# Initialize variables
clicked = False
b = g = r = x = y = 0

# Load color data from a CSV file
csv_path = 'colors.csv'  # Make sure the file is in the correct directory
if not os.path.exists(csv_path):
    print(f"CSV file not found: {csv_path}")
    exit()

color_labels = ["color", "color_name", "hex", "R", "G", "B"]
colors = pd.read_csv(csv_path, names=color_labels, header=None)

# Function to find the closest color name based on RGB values
def find_color_name(r, g, b):
    min_dist = float('inf')
    color_name = ""
    for i in range(len(colors)):
        dist = abs(r - colors.iloc[i]["R"]) + abs(g - colors.iloc[i]["G"]) + abs(b - colors.iloc[i]["B"])
        if dist < min_dist:
            min_dist = dist
            color_name = colors.iloc[i]["color_name"]
    return color_name

# Mouse callback function to get color on double-click
def get_color(event, x_pos, y_pos, flags, param):
    global b, g, r, x, y, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        x, y = x_pos, y_pos
        b, g, r = image[y, x].astype(int)  # Ensure values are integers

# Create a window and set the mouse callback function
cv2.namedWindow('image')
cv2.setMouseCallback('image', get_color)

# Resize image if it's too large for the screen
max_width = 800
if image.shape[1] > max_width:
    aspect_ratio = image.shape[0] / image.shape[1]
    image = cv2.resize(image, (max_width, int(max_width * aspect_ratio)))

# Function to split text into multiple lines if it's too long for the image width
def split_text_into_lines(text, max_width, font_scale, thickness):
    words = text.split(" ")
    lines = []
    current_line = ""
    
    for word in words:
        temp_line = current_line + " " + word if current_line else word
        (text_width, _), _ = cv2.getTextSize(temp_line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        if text_width <= max_width:
            current_line = temp_line
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

while True:
    cv2.imshow("image", image)
    
    if clicked:
        # Convert to int explicitly before using
        b = int(b)
        g = int(g)
        r = int(r)
        
        # Prepare text content
        color_info = f"{find_color_name(r, g, b)} R={r} G={g} B={b}"

        # Define text settings
        font_scale = 1
        thickness = 2
        padding = 10

        # Get the lines of text that will fit the image width
        max_text_width = image.shape[1] - 20  # Leave some space on the sides
        lines = split_text_into_lines(color_info, max_text_width, font_scale, thickness)
        
        # Get the total height of the text (number of lines)
        text_height = cv2.getTextSize("Test", cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0][1]
        total_text_height = (text_height + padding) * len(lines)

        # Ensure the rectangle and text fit within the top of the image
        top_rect_height = total_text_height + padding
        if top_rect_height > image.shape[0]:
            top_rect_height = image.shape[0]  # Limit rectangle height if image is small

        # Draw a rectangle at the top
        cv2.rectangle(image, (0, 0), (image.shape[1], top_rect_height), (b, g, r), -1)

        # Display each line of color information text within the rectangle
        for i, line in enumerate(lines):
            y_position = (i + 1) * (text_height + padding) - padding // 2
            cv2.putText(image, line, (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

        clicked = False

    # Break the loop when the space bar is pressed
    if cv2.waitKey(1) & 0xFF == 32:  # Space bar
        break

cv2.destroyAllWindows()
 