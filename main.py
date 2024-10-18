import cv2

def nothing(x):
    pass

def update_thresholds(value):
    global lowerThreshold, upperThreshold
    overallThreshold = max(0, min(255, value))
    
    buffer = 0
    lowerThreshold = max(0, overallThreshold - buffer)
    upperThreshold = min(255, overallThreshold + buffer)

    cv2.setTrackbarPos("lowerThreshold", "Controls", lowerThreshold)
    cv2.setTrackbarPos("upperThreshold", "Controls", upperThreshold)

cv2.namedWindow("Controls")

cv2.createTrackbar("lowerThreshold", "Controls", 0, 255, nothing)
cv2.createTrackbar("upperThreshold", "Controls", 0, 255, nothing)
cv2.createTrackbar("overallThreshold", "Controls", 0, 255, update_thresholds)

cap = cv2.VideoCapture(0)


def Sobel(image):
    ksize = 3

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=ksize)
    gY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=ksize)

    gX = cv2.convertScaleAbs(gX)
    gY = cv2.convertScaleAbs(gY)

    combined = cv2.addWeighted(gX, 0.5, gY, 0.5, 0)

    return gX, gY, combined


while True:
    ret, frame = cap.read()

    if not ret:
        break

    lowerThreshold = cv2.getTrackbarPos("lowerThreshold", "Controls")
    upperThreshold = cv2.getTrackbarPos("upperThreshold", "Controls")

    canny = cv2.Canny(frame, lowerThreshold, upperThreshold)
    
    gX, gY, combined = Sobel(frame)

    cv2.imshow("Camera", frame)
    cv2.imshow("Canny", canny)

    # uncomment these to see sobel work on horizontal and vertical axis
    # cv2.imshow("Sobel gX", gX)
    # cv2.imshow("Sobel gY", gY)

    cv2.imshow("Sobel", combined)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
