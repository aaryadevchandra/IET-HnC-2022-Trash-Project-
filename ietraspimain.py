import cv2
import serial
import requests
import datetime, time

# need to make sure we're using usb camera instead of CSI cameras which is the default raspi cameras
# cv2 functions only work on usb cameras
cap = cv2.VideoCapture(0)

def getUnixMillis():
    millisecond = datetime.datetime.now()
    timestamp = time.mktime(millisecond.timetuple()) * 1000
    return timestamp

# list containing jsons with each json object having lat lng and timestamp of trash detection
trashLocationsJSONList = []


# code given below is the raspi code
# the raspi will be continously receving gps data when this function is called
def getTrashLocation():

    flag = 0

    ser = serial.Serial('/dev/ttyACM0',9600) # usb port where arduino is connected
    s = [0]
    while ser.is_open:

        # sending the data f 
        s[0] = str(int (ser.readline(),16))
        if flag == 0:
            currTrashlat = s[0]
            flag = 1
            print(s[0])

        else:
            currTrashlng = s[0]
            return currTrashlat, currTrashlng




# while True:
#     ret, frame = cap.read()          # read from camera

# #           ml operations
# #           will take place 
# #           here
# # 
if True: # if ml model detects trash (obv condition will change)

    # gps sensor will be pinged to check for current location
    # currTrashlat, currTrashlng = getTrashLocation()
    currTrashlat= -20.9
    currTrashlng = 126.02

    requests.post('http://localhost:3000/sendtrashlocation', json={'lat': currTrashlat, 'lng': currTrashlng, 'timestamp': int(getUnixMillis())})

    # cv2.imshow('frame', frame)         # show image
    # if cv2.waitKey(10) == ord('q'):  # wait a bit, and see keyboard press
    #     break                        # if q pressed, quit

# release things before quiting
# cap.release()
# cv2.destroyAllWindows()