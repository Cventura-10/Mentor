""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""nimport os
from PIL import Image

# Define the path to the static images directory
static_images_path = '/Users/carlosventura/Mentor/educacion-singular-platform/app/static/images/'

# Ensure the directory exists
os.makedirs(static_images_path, exist_ok=True)

# Create a new image (you can customize the size and color as needed)
image_size = (800, 200)  # Example size: 800x200 pixels
image_color = (73, 109, 137)  # Example color: a shade of blue-gray

# Create a new image with the specified size and color
new_image = Image.new('RGB', image_size, image_color)

# Define the path for the new image
image_path = os.path.join(static_images_path, 'header-bg.jpg')

# Save the image to the specified path
new_image.save(image_path)

print(f'Image created and saved at {image_path}')
