import cv2
import numpy as np
from augraphy import *
import random

def half_paper_method(image, file_name=None, save=False, random_seed=80):
    # Set random seed for reproducibility
    random.seed(random_seed)
    np.random.seed(random_seed)

    # Randomly choose the direction to apply the effect
    choices = ["left", "right"]
    direction = random.choice(choices)

    # Get image dimensions
    height, width = image.shape[:2]

    # Choose a random vertical split position
    split_position = random.randint(0, width)

    # Create a mask based on the random split position and direction
    mask = np.zeros((height, width), dtype=np.uint8)
    if direction == "right":
        mask[:, :split_position] = 255  # Apply effect to the left of split_position
    else:
        mask[:, split_position:] = 255  # Apply effect to the right of split_position

    # Extract the section of the image to augment
    if direction == "right":
        section = image[:, :split_position]
    else:
        section = image[:, split_position:]

    # Create BadPhotocopy augmentation
    bad_photocopy = BadPhotoCopy(
        noise_type=1,
        noise_side=direction,
        noise_iteration=(1,1),
        noise_value=(10,50),
        noise_size=(1,1),
        noise_sparsity=(0.5,0.5),
        edge_effect=0,
    )

    # Apply augmentation to the extracted section
    augmented_section = bad_photocopy(section)

    # Place the augmented section back into the original image
    final_image = image.copy()
    if direction == "right":
        final_image[:, :split_position] = augmented_section
    else:
        final_image[:, split_position:] = augmented_section

    return final_image

if __name__ == "__main__":
    # Load the image
    image = cv2.imread("./img_src/clean_15726443_06.png")

    # Apply the half_paper function
    final_image = half_paper_method(image)

    # Display the result
    cv2.imshow('Result', final_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()