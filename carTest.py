import cv2

vidPath = r'C:\Users\coanh\Desktop\Desktop\Work\Computer Vision\carv2.mp4'
cascadePath = r'C:\Users\coanh\Desktop\Desktop\Work\Computer Vision\cars.xml'

cap = cv2.VideoCapture(vidPath)
carCascade = cv2.CascadeClassifier(cascadePath)

SCREEN_Y = 360
LineY = 150
SCREEN_X = 500
startX = 350
font = cv2.FONT_HERSHEY_SIMPLEX
detectLine = 50



def countCar(carsCounter, y, whileCounter):
    count = carsCounter

    if whileCounter == 0:
        if y <= detectLine:
            cv2.line(crop, (0, detectLine), (SCREEN_X, detectLine), (0, 0, 255), 2)
            count += 1
            return count
    else:
        if y <= detectLine + 2 and y >= detectLine - 2:
            cv2.line(frames, (startX, convertCord(detectLine)), (SCREEN_X, convertCord(detectLine)), (0, 0, 255), 2)
            count += 1
            return count
    return count




def convertCord(y):
    return y + LineY - 20


# def stopDetect(center):
#
#     x, y = center
#
#     if y > SCREEN_Y:
#         drawCenter(center)
#
#     else:

# def drawContour(contours):
#     for contour in contours:
#         moment = cv2.moments(contour)
#         if moment["m00"] != 0:t(mo
# #             cX = inment["m10"] / moment["m00"])
#             cY = int(moment["m01"] / moment["m00"])
#
#             cv2.drawContours(frames, [contour], -1, (255, 0, 255), 2)
#             cv2.circle(frames, (cX, cY), 3, (255, 255, 0), 2)
#
#         return contours



carsCounter = 0

sub = cv2.createBackgroundSubtractorMOG2()
sub.setDetectShadows(detectShadows=False)

whileCounter = 0

while True:

    hasFrame, frames = cap.read()

    if not hasFrame:
        print("video ended...")
        break

    crop = frames[LineY - 20:SCREEN_Y, 0:SCREEN_X].copy()

    blurG = cv2.GaussianBlur(crop, (17, 15), 0)

    blur = cv2.blur(crop, (20, 20), 0)

    gray = cv2.cvtColor(blurG, cv2.COLOR_BGR2GRAY)

    blurGray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    cars = carCascade.detectMultiScale(gray, 1.09, 2)

    cv2.line(frames, (startX, convertCord(detectLine)), (SCREEN_X, convertCord(detectLine)), (125, 20, 122), 2)
    cv2.line(crop, (0, detectLine), (SCREEN_X, detectLine), (125, 20, 122), 2)
    cv2.putText(frames, "Number of Cars "+str(carsCounter), (SCREEN_X - 500, 50), font, 1, (255, 0, 255), 2)

    carLength = len(cars)

    if whileCounter == 0:
        for (x, y, w, h) in cars:
            center = (x + w//2, convertCord(y) + h//2)
            centerY = int(y + h//2)

            cv2.circle(crop, (x + w // 2, y + h // 2), 1, (0, 0, 255), 2)
            cv2.circle(frames, center, 1, (0, 0, 255), 2)
            carsCounter = countCar(carsCounter, y, whileCounter)

    elif whileCounter > 0:

        if prevCarLength - carLength != 0:
            for (x, y, w, h) in cars:
                center = (x + w // 2, convertCord(y) + h // 2)
                centerY = int(y + h // 2)

                cv2.circle(crop, (x + w // 2, y + h // 2), 1, (0, 0, 255), 2)
                cv2.circle(frames, center, 1, (0, 0, 255), 2)
                carsCounter = countCar(carsCounter, y, whileCounter)


    cv2.imshow("Car Counter", frames)


    if cv2.waitKey(33) == 27:
        break

    prevCarLength = carLength

    whileCounter += 1



cv2.destroyAllWindows()
