from PIL import Image, ImageDraw

FLAGS = [
    ["#000000", "#A3A3A3", "#FFFFFF", "#800080"],  # asexual
    ["#5BCEFA", "#F5A9B8", "#FFFFFF", "#F5A9B8", "#5BCEFA"],  # trans
]

im = Image.new("RGB", (2000, 2000), (255, 255, 255))
draw = ImageDraw.Draw(im)
bar_x_width = int(im.size[0] / len(FLAGS))
current_x_pos = 0

for flag in FLAGS:
    bar_y_width = int(im.size[1] / len(flag))
    current_y_pos = 0

    for colour in flag:
        draw.rectangle(
            (
                current_x_pos,
                current_y_pos,
                current_x_pos + bar_x_width + 1,
                current_y_pos + bar_y_width + 1,
            ),
            fill=colour,
        )
        current_y_pos += bar_y_width

    current_x_pos += bar_x_width

im.save("flagBlock.png")
