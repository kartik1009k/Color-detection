import cv2
import pandas as pd

# Load the image from the specified path
image_path = './pallete.png'  # Update this path as needed
image = cv2.imread(image_path)

# Initialize variables to hold color values and click state
clicked = False
b = g = r = x = y = 0

# Load color data from a CSV file
color_labels = ["color", "color_name", "hex", "R", "G", "B"]
colors = pd.read_csv('colors.csv', names=color_labels, header=None)

# Function to find the closest color name based on RGB values
def find_color_name(r, g, b):
    min_dist = float('inf')
    color_name = ""
    for i in range(len(colors)):
        # Calculate distance in RGB space
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
        # Ensure RGB values are integers
        b, g, r = image[y, x].astype(int)  

# Create a window and set the mouse callback function
cv2.namedWindow('image')
cv2.setMouseCallback('image', get_color)

while True:
    # Display the image
    cv2.imshow("image", image)
    
    if clicked:
        # Convert to integers explicitly
        b = int(b)
        g = int(g)
        r = int(r)
        
        # Draw a rectangle with the selected color
        cv2.rectangle(image, (20, 20), (750, 60), (b, g, r), -1)
        color_info = f"{find_color_name(r, g, b)} R={r} G={g} B={b}"
        cv2.putText(image, color_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Adjust text color for visibility against the background
        if r + g + b >= 600:
            cv2.putText(image, color_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False  # Reset click state

    # Exit the loop when the space bar is pressed
    if cv2.waitKey(1) & 0xFF == 32:  # Space bar
        break

# Clean up and close all OpenCV windows
cv2.destroyAllWindows()
