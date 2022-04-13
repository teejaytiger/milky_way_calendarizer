## Milky Way Calendarizer

Turns the milky way photography guide at [Capture The Atlas](https://capturetheatlas.com) into an ICS calendar! Here's how it does it:

1. Converts the PDF into an image using `pdf2image` and an installation of `Poppler`, which must be installed and linked in `conv2img.py` (shortcut is to unpack poppler to mirror `C:\Program Files (x86)\poppler\Library\bin` where it's already expected)
2. Crop the output `image0.png` with `cv2` to size and do some light preprocessing before OCR
3. OCR with `pytesseract` and an installation of `Tesseract`. Again, modify the installation path in `img2ics.py` or mirror `C:\Program Files\Tesseract-OCR\tesseract.exe` to shortcut. 
4. String manipulation magic and ics using `icalendar`

## Installation
This was a personal proj with no virtualenv, so I don't have a requirements file. run:

`python -m pip install pdf2image pytesseract opencv-python icalendar`

### Windows 
Install Tesseract on Windows from [This github Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Install Poppler on Windows using [This build](https://github.com/oschwartz10612/poppler-windows/releases/tag/v22.01.0-0)

### Linux
```
sudo apt update
sudo apt install poppler-utils tesseract-ocr
```

## Running
Modify `location` on line 9 of `img2ics.py` to reflect the location of your closest darksite. You can find areas on [Dark Site Finder](http://darksitefinder.com/maps/world.html) and compare to Google Maps (or Apple Maps or Bing if something is wrong with you) to find a location URL to replace with. Otherwise, you'll be coming to Ice House 2 Observation Point in California.
> Note: You also don't have to put a URL in. You can put pretty much anything you want, like "backyard" or geo-coordinates if you're a try-hard.


Modify `imagepath = "36deg_MW.pdf"` on line 2 of `conv2img.py` to reflect the path of the PDF reflecting the chart covering your latitude from [Capture The Atlas](https://capturetheatlas.com) and execute:

```
python conv2img.py
python img2ics.py
```

There should be three created files:

* `cropped.png` (a cropped image used to improve OCR accuracy)
* `image0.png` (the image generated after converting the PDF)
* A file with the `.ics` extension. This is the file that can be imported into your calendar!

> Note: I left my latitude in just so you can see an example. You can delete it