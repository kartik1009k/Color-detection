import cv2
import pandas as pd

# Load the image from the specified path
image_path = './walll.jpg'
image = cv2.imread(image_path)

# Initialize variables
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

while True:
    cv2.imshow("image", image)
    
    if clicked:
        # Convert to int explicitly before using
        b = int(b)
        g = int(g)
        r = int(r)
        
        # Draw a rectangle with the selected color and display color information
        cv2.rectangle(image, (20, 20), (750, 60), (b, g, r), -1)
        color_info = f"{find_color_name(r, g, b)} R={r} G={g} B={b}"
        cv2.putText(image, color_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Change text color for better visibility
        if r + g + b >= 600:
            cv2.putText(image, color_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when the space bar is pressed
    if cv2.waitKey(1) & 0xFF == 32:  # Space bar
        break

cv2.destroyAllWindows() 