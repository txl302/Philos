import cv2
import itertools
import numpy as np
import time
import random
import serial
import pypot.dynamixel

AMP = 30
FREQ = 0.5
detected = 0

if __name__ == '__main__':

    sum1_i = 0
    sum1_j = 0
    count1 = 0

    temp = 0

    event = 1
    temp_now = 0
    temp = 0

    cam1 = cv2.VideoCapture(1)

    ret2 = cam1.set(3,320)
    ret2 = cam1.set(4,240)

    ret2, img2 = cam1.read()

    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    ports = pypot.dynamixel.get_available_ports()
    print('available ports:', ports)

    if not ports:
        raise IOError('No port available.')

    port = ports[1]
    print('Using the second on the list', port)

    dxl_io = pypot.dynamixel.DxlIO(port)
    print('Connected!')

    found_ids = dxl_io.scan()
    print('Found ids:', found_ids)

    if len(found_ids) < 2:
        raise IOError('You should connect at least two motors on the bus for this test.')

    ids = found_ids[2:8]

    dxl_io.enable_torque(ids)

    speed = dict(zip(ids, itertools.repeat(50)))
    dxl_io.set_moving_speed(speed)
    pos = dict(zip(ids, itertools.repeat(0)))
    dxl_io.set_goal_position(pos)

    t0 = time.time()
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  

    pos1 = [0,0,0,0,40,-40]
    dxl_io.set_goal_position(dict(zip(ids, pos1)))
    time.sleep(1)

    ret2, img2 = cam1.read()

    cv2.waitKey(5000)
    ret2, img2 = cam1.read()
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(100)
    cv2.imshow('gray2', gray2)
    while True:

	#pos0 = [0,random.randint(-45,45),0,0,40,-40]
        #dxl_io.set_goal_position(dict(zip(ids, pos0)))
	#time.sleep(3)

	ret1 = cam1.set(3,320)
	ret1 = cam1.set(4,240)

	ret1, img1 = cam1.read()

	gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

	cv2.imshow('gray1', gray1)

	det1 = np.zeros(gray1.shape, np.uint8)


	det1 = cv2.absdiff(gray1, gray2)

	for i in range (1,319,20):
		for j in range (1,219,20):
			if (det1.item(j,i)>10):
				sum1_i = sum1_i + i
				sum1_j = sum1_j + j
				count1 = count1 + 1
	if(count1 > 30):
		print "object detected from camera1"
		detected = 1
		pos1 = [random.randint(-45,45)]
        	dxl_io.set_goal_position(dict(zip(ids, pos1)))
		time.sleep(3)

	cv2.imshow('object', det1)
	count1 = 0
	if cv2.waitKey(100) == 27:
		break


	if detected == 1:

		pos1 = [20,-10,0,0,40,-40]
		dxl_io.set_goal_position(dict(zip(ids, pos1)))
		time.sleep(1)

		ser.write('0')
		time.sleep(2)

		pos2 = [0,-10,0,0,30,-90]
		dxl_io.set_goal_position(dict(zip(ids, pos2)))
		time.sleep(1)

		#ser.write('1')
		time.sleep(2)

		pos3 = [0,20,0,30,30,-90]
		dxl_io.set_goal_position(dict(zip(ids, pos3)))
		time.sleep(1)

		#ser.write('1')
		time.sleep(2)

		pos4 = [20,20,0,30,40,-40]
		dxl_io.set_goal_position(dict(zip(ids, pos4)))
		time.sleep(1)
		ser.write('1')
		time.sleep(2)

		pos5 = [0,-10,0,0,30,-90]
		dxl_io.set_goal_position(dict(zip(ids, pos5)))
		time.sleep(1)

		#ser.write('1')
		time.sleep(2)

	
	detected = 0;
	



