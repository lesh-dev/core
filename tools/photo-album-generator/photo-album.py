import os

num = 0

print open("header.html").read()

for fileName in os.listdir("."):
#	print fileName
	if ".jpg" not in fileName:
#		print "not jpeg"
		continue
	descFile = fileName.replace(".jpg", ".txt")
	desc = ""
	try:
		df = open(descFile)
		desc = df.read().strip()
	except IOError:
		pass
	imgClass = "album-left"
	if num == 1:
		imgClass = "album-right"
		
	print '<img class="' + imgClass + '" src="/flpic/' + fileName + '" alt="' + fileName + '"></img>'
	print '<p class="' + imgClass + '">'
	if num == 0:
		print '<img class="album-arrow-left" src="/flpic/misc/arrow-left-small.png" alt="arrow left" title="' + fileName + '"></img>'	
	if num == 1:
		print '<img class="album-arrow-right" src="/flpic/misc/arrow-right-small.png" alt="arrow right" title="' + fileName + '"></img>'	

	print desc 
	print '</p>'
	print ''
	if True or num == 1:
		print '<div style="clear:both;"></div>'
		print ''

	num = (num + 1) % 2

print "</div>"