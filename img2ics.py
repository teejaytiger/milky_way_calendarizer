import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import dateutil.parser
import uuid

location = "https://www.google.com/maps/place/Ice+House+Observation+Point+2/@38.7968588,-120.412539,17.01z/data=!4m5!3m4!1s0x809a3b46babfc661:0xbd9b207741fda9ab!8m2!3d38.7968579!4d-120.4103521"

class CEvent:

    def __init__(self, row, type="mw"):
        self.date = row[0]
        self.illumination = row[1]
        self.moonrise = row[2]
        self.moonset = row[3]
        self.sunset = row[4]
        self.sunrise = row[5]
        self.mwstart = row[6]
        self.mwend = row[7]
        self.mwhours = row[8]
        self.gcstart = row[9]
        self.gcend = row[10]
        self.gchours = row[11]
        self.elevation = row[12]
        if type=="gc": self.event = self.makecal(type = "gc")
        if type=="mw": self.event = self.makecal(type = "mw")

    def makecal(self, type="gc"):
        event = Event()
        if type=="gc": summary = 'Galactic Center Viewing!'
        if type=="mw": summary = 'Milky Way Viewing!'
        
        # use milky way start and end times to create event
        mwstart = dateutil.parser.parse("{} {}".format(self.date, self.mwstart))
        delta = self.mwhours.split(":")
        gcdelta = int(self.gchours.split(":")[0])
        if (gcdelta>=3): summary="Photograph the Milky Way!"
        delta = timedelta(hours=int(delta[0]), minutes=int(delta[1]))
        #mwend = dateutil.parser.parse("{} {}".format(self.date, self.mwend))
        mwend = mwstart + delta

        # start building the event object
        event.add('summary', summary)
        event['uid'] = uuid.uuid4()
        event.add('dtstart', mwstart)
        event.add('dtend', mwend)
        event.add('dtstamp', datetime.now())
        event.add('geo', "38.796846, -120.410442")
        event.add('location', location)
        if type=="gc": description = "Galactic Center from {} to {} at {}".format(self.gcstart,self.gcend,self.elevation)
        if type=="mw": description = "No Galactic center Viewing"
        event.add('description', "{} <br/> Moonset:{} <br/>Moonrise:{} <br/>Sunset:{} <br/>Sunrise:{} <br/>Illumination:{}".format(
            description,
            self.moonset,
            self.moonrise,
            self.sunset,
            self.sunrise,
            self.illumination
        ))
        return event

img = cv2.imread('image0.png')
custom_config = r'--oem 3 --psm 6'

img = img[:, 336:5962]
cv2.imwrite("cropped.png", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, 0)

t = pytesseract.image_to_string(mask, config=custom_config)

# get the title
l = t.split("\n")
title = l[0]

# Start the ics
cal = Calendar()
cal.add('prodid', '-//@teejaytiger//{}//'.format(title))
cal.add('version', '2.0')

for row in l:    
    i=row.split()
    try: 
        dateutil.parser.parse(i[0])
        for item in i[2:5]:
            if ":" not in item: i.remove(item)
        if not "-" in i[10]:
            formatted = i[:12]
            formatted.append(("".join(i[12:])))
            v = CEvent(formatted)
            cal.add_component(v.event)
        else:
            # milky way not visible
            pass
    #ParserError doesn't catch for some reason idk idc
    except Exception as e:
        continue 

f = open("{}.ics".format(title), 'wb')
f.write(cal.to_ical())
f.close()
