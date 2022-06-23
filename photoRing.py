from PIL import Image, ImageDraw
import argparse

parser = argparse.ArgumentParser(
    description="Add an overlay to an image with a circular cutout"
)
parser.add_argument("input", metavar="INPUT", type=str, help="base image")
parser.add_argument("overlay", metavar="OVERLAY", type=str, help="overlay image")
parser.add_argument(
    "--width",
    dest="width",
    default=7,
    type=int,
    help="border ring width in percent of radius",
)

args = parser.parse_args()

base_image = Image.open(args.input)
overlay_image = Image.open(args.overlay)

# Aspect ratio and size checks
base_aspect_ratio = base_image.size[0] / base_image.size[1]
overlay_aspect_ratio = overlay_image.size[0] / overlay_image.size[1]

if base_aspect_ratio != overlay_aspect_ratio:
    print(
        f"Warning: best results are obtained when both images have the same aspect ratio.\n{base_aspect_ratio=}, {overlay_aspect_ratio=}"
    )

if (
    base_image.size[0] > overlay_image.size[0]
    or base_image.size[1] > overlay_image.size[1]
):
    print(
        f"Warning: scaling up overlay image. Best results are obtained when the overlay image is larger than or the same size as the base image.\n{base_image.size=}, {overlay_image.size=}"
    )

# Resize images to be the same size, distorting the overlay if needs be.
overlay_image = overlay_image.resize(base_image.size)

# Determine square box for the circle cutout to be from
x_ring_width = int((base_image.size[0] / 2) * (args.width / 100))
y_ring_width = int((base_image.size[1] / 2) * (args.width / 100))

mask_box = (
    x_ring_width,
    y_ring_width,
    base_image.size[0] - x_ring_width,
    base_image.size[1] - y_ring_width,
)

# Create mask
mask = Image.new("L", base_image.size, 0)
ImageDraw.Draw(mask).ellipse(mask_box, fill=255)

# Put base_image on top of overlay_image with respect to mask
output_image = Image.composite(base_image, overlay_image, mask)

# Save to disk
split_input_name = args.input.split(".")
output_image_name = ".".join(split_input_name[0:-1] + ["rings", split_input_name[-1]])
output_image.save(output_image_name)

print(f"Saved as {output_image_name}")
