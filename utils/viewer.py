import os
import cv2
import sys

sys.path.append('.')


def load_images_from_folder(folder_path):
    images = []
    filenames = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])
    for filename in filenames:
        img = cv2.imread(os.path.join(folder_path, filename))
        if img is not None:
            images.append(img)
    return images


def open_viewer(folder_path):
    images = load_images_from_folder(folder_path)

    cv2.namedWindow("Frames Viewer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frames Viewer", 600, 800)
    current_index = 0

    while True:
        cv2.imshow("Frames Viewer", images[current_index])

        key = cv2.waitKey(0) & 0xFF

        # Handle key presses
        if key == ord('q'):
            # Quit the viewer
            break
        elif key == ord('p'):
            # Move to the next image
            current_index = (current_index + 1) % len(images)
        elif key == ord('o'):
            # Move to the previous image
            current_index = (current_index - 1) % len(images)

    cv2.destroyAllWindows()
