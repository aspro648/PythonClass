# Use Python Image Library (PIL) to crop and annotate an image.

import Image, ImageDraw, ImageFont
import os, sys


base_dir = os.getcwd()
target_file = 'sim3109.png'
target_path = os.path.join(base_dir, target_file)
fontSize = 12
font = ImageFont.truetype('arial.ttf', fontSize)

# Identify regions of interest
crop_pos = (764, 326)  #(x, y) of upper right corner
crop_size = (501, 433)      #(length, width)
crop_box = (crop_pos[0], crop_pos[1], crop_pos[0] + crop_size[0],
            crop_pos[1] + crop_size[1])

title_pos = (25, 274)
title_size = (400, 47)
boxTitle = (title_pos[0], title_pos[1],
            title_pos[0] + title_size[0], title_pos[1] + title_size[1])

time_pos = (687, 772)
time_size = (68, 19)
boxTime = (time_pos[0], time_pos[1],
           time_pos[0] + time_size[0], time_pos[1] + time_size[1])


# Get image, crop it
im = Image.open(target_path)
new_im = im.crop(crop_box)

# Get title and paste
title = im.copy()
title = title.crop(boxTitle)
title_x_pos = new_im.size[0] / 2 - title.size[0] / 2
title_y_pos = 10
new_im.paste(title, (title_x_pos, title_y_pos))

# Get time step and paste
time = im.copy()
time = time.crop(boxTime)
draw = ImageDraw.Draw(time)
draw.text((7, 4), '@       us', fill='black', font=font)
time_x_pos = new_im.size[0] / 2 - time.size[0] / 2
time_y_pos = title_y_pos + title.size[1] + 10
new_im.paste(time, (time_x_pos, time_y_pos))

# Add watermark of sim number
newName = target_file.split('.')[0]
draw = ImageDraw.Draw(new_im)
textSize = draw.textsize(newName, font=font)
name_x_pos = new_im.size[0] - textSize[0] - 20
name_y_pos = new_im.size[1] - textSize[1] - 5
draw.text((name_x_pos, name_y_pos), newName, fill='darkgrey', font=font)

# Save file
print target_file, '->', newName + '_breakoff.png'
new_im.save(newName + '_breakoff.png')



