import argparse
from pyzbar import pyzbar
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
    help="path to input image")
args = vars(ap.parse_args())

# loading input image
image = cv2.imread(args["image"])

# finding barcodes in the image and decoding all of them
barcodes = pyzbar.decode(image)

# loop through the detected barcodes
for barcode in barcodes:
    # extract the bounding location of the barcode,
    # and draw the bounding box surrounding the barcode
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # to draw the barcode data, we convert the data from bytes -> string
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # draw barcode data and type on the image itself
    # EDIT THIS FOR ROS & QT IMPLEMENTATION
    text = "<{}>, {}".format(barcodeType, barcodeData)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 0, 255), 2)
    
    print ("[INFO] type: {} barcode: {}".format(barcodeType, barcodeData))

cv2.imshow("Image", image)
cv2.waitKey(0)