from PIL import Image, ImageDraw, ImageFont

hand_width = 75
text = "z ogromną radością zapraszamy"
snumber = 4

space_width = font.getsize(snumber * " ")[0]
splitted = text.split(" ")
text_dspaces = ""

for i in splitted:
    if i != splitted[-1]:
        text_dspaces += i + snumber * " "
    else:
        text_dspaces += i

font = ImageFont.truetype("times.ttf", 12)
width = font.getsize(text_dspaces)[0]

total_width = 0
print("0")
for i in splitted:
    if i != splitted[-1]:
        print(total_width + round((font.getsize(i)[0] + space_width) * (hand_width / width), 1))
        total_width += round((font.getsize(i)[0] + space_width) * (hand_width / width), 1)
    else:
        print(total_width + round(font.getsize(i)[0] * (hand_width / width), 1))
        total_width += round(font.getsize(i)[0] * (hand_width / width), 1)
print(text)