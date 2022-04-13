from pdf2image import convert_from_path
imagepath = "45deg_MW.pdf"

images = convert_from_path(imagepath, 500, poppler_path=r'C:\Program Files (x86)\poppler\Library\bin')
for i, image in enumerate(images):
    fname = 'image'+str(i)+'.png'
    image.save(fname, "PNG")   