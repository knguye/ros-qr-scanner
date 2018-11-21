from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type = str, default ="barcode.csv",
    help = "path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize video stream, let camera sensor warm up
print ("[INFO] Starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0) # warmup camera

# open the output CSV file for writing and initialize the set of
# barcodes found so far
csv = open(args["output"], "w")
found = set()

# loop over frames from video stream
while True:
    # grab the frame from the stream and resize it to max. 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width = 400)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

# loop through the detected barcodes
    for barcode in barcodes:
        # extract the bounding location of the barcode,
        # and draw the bounding box surrounding the barcode
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # to draw the barcode data, we convert the data from bytes -> string
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw barcode data and type on the image itself
        # EDIT THIS FOR ROS & QT IMPLEMENTATION
        text = "<{}>: {}".format(barcodeType, barcodeData)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)

        if barcodeData not in found:
            csv.write("{}, {}\n".format(datetime.datetime.now(),
                barcodeData))
            csv.flush()
            found.add(barcodeData)

    # show output frame
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        break

# close the output CSV file, do some cleanup
print ("[INFO] cleaning up..")
csv.close()
cv2.destroyAllWindows()
vs.stop()


