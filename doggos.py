# Authored by Richard Harrah, Richard Harrah, and Richard Harrah
# Download the images used from here: http://www.pcs.cnu.edu/~richard.harrah/doggos.tar
# Extract the contents into the images directory.
# NOTE: It takes a loooooooooooooooooooooooong time to read all of the doggos. You may want to use a
#       subset of the doggos.

from PIL import Image
import itertools, os, signal, sys, time


# Create SIGINT handler
def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Create a spinner for the CLI
spinner = itertools.cycle(['|', '/', '-', '\\'])


def spin(text=''):
    output = '{0}{1}'.format(text, spinner.next())
    sys.stdout.write(output)  # write the next character
    sys.stdout.flush()  # flush stdout buffer (actual character display)
    time.sleep(0.1)
    sys.stdout.write('\b' * len(output))  # erase the last written char


breeds_colors = dict()

images_dir = '{0}/doggos'.format(os.getcwd())
print 'Loading all breeds from images directory!'
# Loop through all subdirectories in the images directory
for image_dir in os.listdir(images_dir):
    image_dir_path = os.path.join(images_dir, image_dir)
    if os.path.isdir(image_dir_path) is not True:
        continue
    # Determine the breed of the doggo
    breed = image_dir[image_dir.find('-') + 1:]
    # Set the images for the breed to an empty set
    breeds_colors[breed] = set()
    # Loop through all images of doggos in the image subdirectory
    for doggo_image in os.listdir(image_dir_path):
        spin('Loading and processing doggos... ')
        doggo_image_path = os.path.join(image_dir_path, doggo_image)
        if os.path.isfile(doggo_image_path) is not True:
            continue
        # Load the doggo image
        doggo = Image.open(doggo_image_path)
        # Setup total values for doggo image
        doggo_total_pixel = doggo.width * doggo.height
        doggo_total_r = 0
        doggo_total_g = 0
        doggo_total_b = 0
        # Iterate through the doggo picture and add pixel RGB to total values for doggo
        for x in range(0, doggo.width):
            for y in range(0, doggo.height):
                doggo_pixel = doggo.getpixel((x, y))
                doggo_total_r += doggo_pixel[0]
                doggo_total_g += doggo_pixel[1]
                doggo_total_b += doggo_pixel[2]
        # Come up with the average for the doggo
        doggo_average_r = int(doggo_total_r / doggo_total_pixel)
        doggo_average_g = int(doggo_total_g / doggo_total_pixel)
        doggo_average_b = int(doggo_total_b / doggo_total_pixel)
        breeds_colors[breed].add((doggo_average_r, doggo_average_g, doggo_average_b))

breeds_average_colors = dict()
print 'Processing average colors of breeds!'
for (breed, colors) in breeds_colors.viewitems():
    breed_total_r = 0
    breed_total_g = 0
    breed_total_b = 0
    for (r, g, b) in colors:
        breed_total_r += r
        breed_total_g += g
        breed_total_b += b
    breed_average_r = breed_total_r / len(colors)
    breed_average_g = breed_total_g / len(colors)
    breed_average_b = breed_total_b / len(colors)
    breeds_average_colors[breed] = (breed_average_r, breed_average_g, breed_average_b)

longest_breed_name = 0
for breed in breeds_colors.viewkeys():
    breed_len = len(breed)
    if breed_len > longest_breed_name:
        longest_breed_name = breed_len

color_length = 15
print 'Average colors calculated!'
print '=' * (2 + max(longest_breed_name, 5) + 3 + color_length + 2)
print '| {0} | {1} |'.format('Breed'.center(longest_breed_name, ' '), 'Color'.center(color_length, ' '))
print '=' * (2 + max(longest_breed_name, 5) + 3 + color_length + 2)
for breed in sorted(breeds_average_colors.viewkeys()):
    colors = breeds_average_colors[breed]
    human_readable_breed = breed.replace('_', ' ').replace('-', '_').title()
    human_readable_color = '({0}, {1}, {2})'.format(colors[0], colors[1], colors[2])
    print '| {0} | {1} |'.format(human_readable_breed.center(longest_breed_name, ' '),
                                 human_readable_color.center(color_length, ' '))
print '=' * (2 + max(longest_breed_name, 5) + 3 + color_length + 2)