import itertools
import numpy
import time

import serial

import pypot.dynamixel

AMP = 30
FREQ = 0.5



if __name__ == '__main__':
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

    ids = found_ids[4:8]

    dxl_io.enable_torque(ids)

    speed = dict(zip(ids, itertools.repeat(50)))
    dxl_io.set_moving_speed(speed)
    pos = dict(zip(ids, itertools.repeat(0)))
    dxl_io.set_goal_position(pos)


    t0 = time.time()
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  

 


    while True:

	pos1 = [0,0,30,-90]
        dxl_io.set_goal_position(dict(zip(ids, pos1)))
	time.sleep(1)

	#ser.write('0')
	time.sleep(2)

	pos2 = [0,0,40,-40]
	dxl_io.set_goal_position(dict(zip(ids, pos2)))
        time.sleep(1)

	#ser.write('1')
	time.sleep(2)
	



