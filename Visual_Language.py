from PIL import Image


# Function to change the color of solid black images in an image to a new color
def change_image_color(image, new_color):
    image = image.convert("RGBA")  # Ensure image is in RGBA mode for alpha transparency
    data = image.getdata()  # Get image data

    # Modify image data to change black or near-black pixels to the new color
    new_data = [
        new_color + (item[3],) if item[0] <= 30 and item[1] <= 30 and item[2] <= 30 else item
        for item in data
    ]

    image.putdata(new_data)  # Update image with modified data
    return image


# Function to rotate an image by a given angle
def rotate_image(image, angle):
    return image.rotate(angle, expand=1)  # Rotate and expand to fit the whole rotated image


# Define the mapping for each group to their corresponding image file
image_mapping = {
    "nd": "Symbols/ND.png",
    "wh": "Symbols/WH.png",
    "nt": "Symbols/NT.png",
    "gh": "Symbols/GH.png",
    "qu": "Symbols/QU.png",
    # Add remaining letter mappings
    "b": "Symbols/B.png",
    "c": "Symbols/C.png",
    "d": "Symbols/D.png",
    "f": "Symbols/F.png",
    "g": "Symbols/G.png",
    "h": "Symbols/H.png",
    "j": "Symbols/J.png",
    "k": "Symbols/K.png",
    "l": "Symbols/L.png",
    "m": "Symbols/M.png",
    "n": "Symbols/N.png",
    "p": "Symbols/P.png",
    "r": "Symbols/R.png",
    "s": "Symbols/S.png",
    "t": "Symbols/T.png",
    "v": "Symbols/V.png",
    "w": "Symbols/W.png",
    "x": "Symbols/X.png",
    "y": "Symbols/Y.png",
    "z": "Symbols/Z.png",
    # Add digraph mappings
    "ch": "Symbols/CH.png",
    "sh": "Symbols/SH.png",
    "th": "Symbols/TH.png",
    "ng": "Symbols/NG.png",
    # Add vowel mappings
    "a": "Symbols/A.png",
    "e": "Symbols/E.png",
    "i": "Symbols/I.png",
    "o": "Symbols/O.png",
    "u": "Symbols/U.png"
}


# Function to calculate the positions of images on the canvas based on the word length and canvas size
def calculate_positions(word_length, canvas_size, direction):
    positions = []
    img_size = 50  # Fixed size for each symbol/image

    # Define the central area on the canvas to place images
    central_area_start = ((canvas_size[0] - 800) // 2, (canvas_size[1] - 800) // 2)
    central_area_end = (central_area_start[0] + 800, central_area_start[1] + 800)

    # Determine positions based on the specified direction
    if direction == 'diagonal_lr':  # Diagonal from top left to bottom right
        start_pos, end_pos = central_area_start, central_area_end
    elif direction == 'diagonal_rl':  # Diagonal from top right to bottom left
        start_pos, end_pos = (central_area_end[0], central_area_start[1]), (central_area_start[0], central_area_end[1])
    elif direction == 'middle_up':  # Vertical from middle bottom to middle top
        mid_x = central_area_start[0] + 400
        start_pos, end_pos = (mid_x, central_area_end[1]), (mid_x, central_area_start[1])

    # Calculate and store each position
    for i in range(word_length):
        proportion = i / max(1, word_length - 1)
        pos_x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * proportion) - img_size // 2
        pos_y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * proportion) - img_size // 2
        positions.append((pos_x, pos_y))

    return positions


# Updated function to place images in order and distribute them evenly across three lines
def place_images_for_word(base_image, word, canvas_size):
    images_to_place = []  # List to hold paths of images corresponding to each character/digraph in the word

    # Determine images to place based on the characters/digraphs in the word
    i = 0
    while i < len(word):
        if i < len(word) - 1 and word[i:i + 2] in image_mapping:  # Check for digraphs
            images_to_place.append(image_mapping[word[i:i + 2]])
            i += 2
        elif word[i] in image_mapping:  # Check for single characters
            images_to_place.append(image_mapping[word[i]])
            i += 1
        else:
            print(f"Warning: No image mapping found for '{word[i]}'")
            i += 1

    # Strategy for distributing images across three lines/directions
    num_lines = 3
    images_per_line = len(images_to_place) // num_lines
    remainder = len(images_to_place) % num_lines

    # Define the start and end points for each of the three lines
    points = [
        ((100, 100), (900, 900)),  # Top left to bottom right
        ((900, 100), (100, 900)),  # Top right to bottom left
        ((500, 900), (500, 100))  # Middle bottom to middle top
    ]

    directions = ['diagonal_lr', 'diagonal_rl', 'middle_up']  # Directions for the lines
    colors = ['#FF0000', '#FF9A00', '#FFE808']  # Color codes for different directions

    # Iterating over each line to place images
    image_idx = 0  # Index to track the current image to be placed

    # This middle variable will serve the purpose of stopping overlap in the middle
    middle = 100
    for line_idx, (start_point, end_point) in enumerate(points):
        # Determine number of images on the current line, considering the remainder
        num_images_this_line = images_per_line + (1 if line_idx < remainder else 0)

        # Calculate positions for the current line
        positions = calculate_positions(num_images_this_line, canvas_size, directions[line_idx])

        # Place each image at its calculated position
        for position in positions:
            if image_idx < len(images_to_place):
                image_path = images_to_place[image_idx]  # Get image path
                image = Image.open(image_path)  # Open image
                color_rgb = hex_to_rgb(colors[line_idx])  # Get RGB color for current direction
                colored_image = change_image_color(image, color_rgb)  # Color the image

                # If image is at the centre point
                if position == (475, 475):
                    # Move it to the left of the last potentially overlapping image
                    position = (middle, 500)
                    middle += 375

                base_image.paste(colored_image, position, colored_image)  # Paste colored image onto base image
                image_idx += 1
            else:
                break  # Break if no more images to place

    return base_image  # Return the base image with all symbols placed


# Function to convert hex color code to an RGB tuple
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Remove '#' if present
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))  # Convert to RGB tuple
