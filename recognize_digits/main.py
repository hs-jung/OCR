# import the necessary package
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1) : 0,
    (0, 0, 1, 0, 0, 1, 0) : 1,
    (1, 0, 1, 1, 1, 0, 1) : 2,
    (1, 0, 1, 1, 0, 1, 1) : 3,
    (0, 1, 1, 1, 0, 1, 0) : 4,
    (1, 1, 0, 1, 0, 1, 1) : 5,
    (1, 1, 0, 1, 1, 1, 1) : 6,
    (1, 0, 1, 0, 0, 1, 0) : 7,
    (1, 1, 1, 1, 1, 1, 1) : 8,
    (1, 1, 1, 1, 0, 1, 1) : 9,
}

image = cv2.imread("../assets/test1.jpeg")

image = imutils.resize(image, height=500)
gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

# 엣지맵
# cv2.imshow('image', edged)
# cv2.waitKey()
# cv2.destroyAllWindows()

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
disPlayCnt = None

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4 :
        disPlayCnt = approx
        break

warped = four_point_transform(gray, disPlayCnt.reshape(4, 2))
output = four_point_transform(image, disPlayCnt.reshape(4, 2))

# ouput
# cv2.imshow('image', output)
# cv2.waitKey()
# cv2.destroyAllWindows()

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# cv2.imshow('image', output)
# cv2.waitKey()
# cv2.destroyAllWindows()

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []

# cv2.imshow('image', output)
# cv2.waitKey()
# cv2.destroyAllWindows()

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)

    if w >= 15 and ( h >= 30 and h <= 40):
        digitCnts.append(c)

digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

digits = []

cv2.imshow('image', output)
cv2.waitKey()
cv2.destroyAllWindows()

for c in digitCnts:
    (x, y, w, h) = cv2.boundingRect(c)
    roi = thresh[y:y + h, x:x + w]
    (roiH, roiW) = roi.shape
    (dW, dH) = (int (roiW * 0.25), int(roiH * 0.15))
    dHC = int(roiH * 0.05)

    segments = [
        ((0, 0), (w, dH)),
        ((0, 0), (dW, h // 2)),
        ((w - dW, 0), (w, h // 2)),
        ((0, (h // 2) - dHC) , (w, (h // 2) + dHC)),
        ((0, h // 2), (dW, h)),
        ((w - dW, h // 2), (w, h)),
        ((0, h - dH), (w,h))
    ]
    on = [0] * len(segments)

    for ( i, ((xA, yA), (xB, yB))) in enumerate(segments):
        segROI = roi[yA:yB, xA:xB]
        total = cv2.countNonZero(segROI)
        area = (xB - xA) * (yB - yA)

        if total / float(area) > 0.5:
            on[i] = 1

    digit = DIGITS_LOOKUP[tuple(on)]
    digits.append(digit)
    cv2.rectangle(output, (x,y), (x + w, y + h), (0,255, 0), 1)
    cv2.putText(output, str(digit), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

    print(u"{}{}.{} \u00b0C".format(*digits))
    cv2.imshow("Input", image)
    cv2.imshow("Output", output)
    cv2.waitKey(0)
