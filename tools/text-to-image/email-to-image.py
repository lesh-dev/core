#!/usr/bin/python

# simple email image generator.
# (c) 2012 vdm <vdm-photo@ya.ru>
# (c) 2012 fizlesh.ru

import Image, ImageFont, ImageDraw, sys, os, re

def GetParam(paramName):
	fullName = "--" + paramName
	if fullName in sys.argv:
		pos = sys.argv.index(fullName) + 1
		if pos > len(sys.argv):
			raise RuntimeError("Parameter value for '" + fullName + "' was not specified. ")
		return sys.argv[pos]
	return None
	
def ProcessColor(color):
	if len(color) == 6:
		check = re.sub("[A-Fa-f0-9]", "", color)
		if check != "":
			raise RuntimeError("Incorrect color specification. Use #RRGGBB or RRGGBB notation. ")
		return "#" + color
	elif len(color) == 7:
		check = re.sub("[A-Fa-f0-9]", "", color[1:])
		if check != "" or color[0] != "#":
			raise RuntimeError("Incorrect color specification. Use #RRGGBB or RRGGBB notation. ")		
		return color
	else: 
		raise RuntimeError("Color has incorrect format. Use #RRGGBB or RRGGBB notation. ")
	
	
if len(sys.argv) < 2:
	print "Syntax:   email-to-image.py <email> [ --back #RGB-back-color ] [ --text #RGB-text-color ] [ --size font-size ] [ --border border-width ] " 
	print "Example:  email-to-image.py dmvn@mccme.ru --back 9EC78B --text 000000 --size 12 --border 2"
	print "Default colors are white (FFFFFF) for background and black (000000) for text."
	print "Default font size is 12, border width is 2. " 
	sys.exit(1)

border = 2

try:
	border = int(GetParam("border") or "2")
except:
	raise RuntimeError("Cannot understand 'border' parameter (number expected)")

fontSize = 12

try:
	fontSize = int(GetParam("size") or "12");
except:
	raise RuntimeError("Cannot understand 'size' parameter (number expected)")

backColorStr = GetParam("back") or "FFFFFF";
textColorStr = GetParam("text") or "000000";
	
email = sys.argv[1]

backColor = ProcessColor(backColorStr)
textColor = ProcessColor(textColorStr)

image = Image.new("RGB", (1000, 400), backColor)
draw = ImageDraw.Draw(image)

textFont = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", fontSize)
textWidth, textHeight = draw.textsize(email, font = textFont)
draw.text((border, border), email, font = textFont, fill = textColor)

cropBox = (0,0, textWidth+2*border, textHeight + 2*border)
image = image.crop(cropBox)

fileName = email.replace("@", "-at-") + ".png"
image.save(fileName)

print "Output written to", fileName



