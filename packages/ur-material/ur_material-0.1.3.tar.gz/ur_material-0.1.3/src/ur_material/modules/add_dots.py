import cv2
import numpy as np
import random

def add_random_speckles(image, file_name=None, save=False, random_seed=42):
    """
    Adds random black speckles of irregular shapes to an image.
    
    Parameters:
    - image: numpy array (image loaded with cv2.imread())
    - num_points: int (number of black speckles to add)
    
    Returns:
    - Modified image with black speckles.
    """
    random.seed(random_seed)

    num_points = random.randint(10,15)

    output = image.copy()

    # Get image dimensions
    height, width = image.shape[:2]

    for _ in range(num_points):
        # Generate random center coordinates for the speckle
        center_x = random.randint(0, width - 1)
        center_y = random.randint(0, height - 1)

        # Generate random vertices for irregular shapes
        vertices = []
        num_vertices = random.randint(3, 6)  # Polygon with 3-6 vertices
        for _ in range(num_vertices):
            angle = random.uniform(0, 2 * np.pi)
            radius = random.randint(1, 2)        # change dots size here
            vertex_x = int(center_x + radius * np.cos(angle))
            vertex_y = int(center_y + radius * np.sin(angle))
            vertices.append([vertex_x, vertex_y])

        # Convert vertices into a numpy array suitable for cv2.polylines
        pts = np.array(vertices, np.int32)
        pts = pts.reshape((-1, 1, 2))

        # Draw the irregular polygon
        cv2.fillPoly(output, [pts], (0, 0, 0))
        
    if output.ndim == 3:
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    
    return output

if __name__=="__main__":
    # Usage example:
    # Load an image (Ensure the path is correct)
    image_path = '../img_src/1022104527_01df78fd-245d-4301-9e5b-19690d0206a9.png'
    image = cv2.imread(image_path)

    # Add random speckles
    modified_image = add_random_speckles(image, num_points=50)

    # Display the modified image
    cv2.imshow('Image with Random Speckles', modified_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optionally, save the modified image
    # cv2.imwrite('modified_image_with_irregular_speckles.jpg', modified_image)