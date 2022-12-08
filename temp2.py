import modi
import time
modi.update_module_firmware()
bundle1 = modi.MODI(
    conn_type= 'ble',
    network_uuid='3D39547C'
)
bundle2 = modi.MODI(
    conn_type= 'ble',
    network_uuid='99CC0F3A'
)

gyro = bundle2.gyros[0]
motor1 = bundle1.motors[0]
motor2 = bundle1.motors[1]
display = bundle2.displays[0]
dial1 = bundle2.dials.get(3902)
dial2 = bundle2.dials.get(2967)
dial3 = bundle2.dials.get(3888)
led1 = bundle1.leds[0]
led2 = bundle1.leds[1]
speaker = bundle1.speakers[0]
ir1 = bundle1.irs[0]
# ir2 = bundle1.irs[1]
# ir3 = bundle1.irs[2]
new = []
IR1 = 30
max_speed = 80
cond = False


def show_speed(t, x=-1):
    display.text = t
    if x != -1:
        display.show_variable(x, 20, 30)


def saturate(x):
    if x > max_speed:
        return max_speed
    if x < -max_speed:
        return -max_speed
    return x


def go_forward(x=100):
    if x > 100:
        x = 100
    if x < 0:
        motor1.speed = -x - 12, x 
        motor2.speed = -x - 12, x 
    elif x > 0:
        motor1.speed = -x, x
        motor2.speed = -x, x
    show_speed('Speed:', abs(x))
    # time.sleep(sec)
    # stop_car()


def rotate_right(x):
    '''
        -100, -100
        -100, -100
        For rotate right by some degree
    '''
    motor1.speed = -x, -x
    motor2.speed = -x, -x
    show_speed('Right', abs(x))


def rotate_left(x):
    '''
        100, 100
        100, 100
        For rotate left by some degree
    '''
    motor1.speed = x, x
    motor2.speed = x, x
    show_speed('Left', abs(x))


def stop_car():
    '''
    Stop the car by making the speed 0
    '''
    motor1.speed = 0, 0
    motor2.speed = 0, 0
    show_speed('Speed:',0)


# def update_yaw():
#     global yaw_past, COUNTER
#     if yaw_past-gyro.yaw >= 10:
#         COUNTER += 1
#         if COUNTER == 2:
#             turn_left_90()
#             COUNTER = 0
#     if yaw_past-gyro.yaw <= -10:
#         COUNTER += 1
#         if COUNTER == 2:
#             turn_right_90()
#             COUNTER = 0
#     print(gyro.yaw)
#     yaw_past = gyro.yaw


def turn_right_90():
    rotate_right(30)
    time.sleep(5)
    stop_car()

def turn_left_90():
    rotate_left(30)
    time.sleep(5)
    stop_car()


def testgyro():
    print("gyro_pitch:", gyro.pitch, "gyro_roll:", gyro.roll, "gyro_yaw", gyro.yaw)
    time.sleep(0.1)

# def testgyro2():
#     print("gyro_pitch:", gyro2.pitch, "gyro_roll:", gyro2.roll, "gyro_yaw", gyro2.yaw)
#     time.sleep(0.1)


def go_back(some):
    a = some[::-1]
    for gyro_pitch, gyro_roll in a:
        if gyro_roll == "R":
            turn_left_90()
        elif gyro_roll == "L":
            turn_right_90()
        elif gyro_pitch > 30 and abs(gyro_pitch) > abs(gyro_roll):
            go_forward(saturate((25 + (abs(gyro_pitch) - 30)/30 * (max_speed - 25))))
        elif gyro_pitch < -30 and abs(gyro_pitch) > abs(gyro_roll):
            go_forward(saturate(-(25 + (abs(gyro_pitch) - 30)/30 * (max_speed - 25))))
        elif gyro_roll > 30 and abs(gyro_pitch) < abs(gyro_roll):
            rotate_left(saturate(25 + (abs(gyro_roll) - 30)/60 * (max_speed - 25)))
        elif gyro_roll < -30 and abs(gyro_pitch) < abs(gyro_roll):
            rotate_right(saturate(25 + (abs(gyro_roll) - 30)/60 * (max_speed - 25)))
        else:
            stop_car()

def testIr():
    print("ir1: ", ir1.proximity)
    # print("ir2: ", ir2.proximity)
    # print("ir3: ", ir3.proximity)

def testDial():
    print("dial1:", dial1.degree, "dial2:", dial2.degree, "dial3:", dial3.degree)

def stopped():
    if motor1.speed == (0, 0) and motor2.speed == (0, 0):
        return True
    return False

# def minorTurn(degree, some):
#     if stopped() and degree > 60:
#         gyro_roll = ((90 * 25)/max_speed) + ((degree-60)/40) * ((90 * 10)/max_speed)
#         gyro_pitch = 0
#         some.append((gyro_pitch, gyro_roll))
#         rotate_right(saturate(abs(gyro_roll)/90 * max_speed))
#     elif stopped() and degree < 40:
#         gyro_roll = ((90 * 25)/max_speed) + ((degree-60)/40) * ((90 * 10)/max_speed)
#         gyro_pitch = 0
#         some.append((gyro_pitch, gyro_roll))
#         rotate_right(saturate(abs(gyro_roll)/90 * max_speed))
#     else:
#         stop_car()

def led_turnOn(x = "white"):
    if x == "red":
        led1.rgb = 100, 0, 0
        led2.rgb = 100, 0, 0

    else:
        led1.turn_on()
        led2.turn_on() 

def led_turnOff():
    led1.turn_off()
    led2.turn_off()



# while True:
#     testDial()

# while True:
#     led_turnOn("red")
#     time.sleep(5)
#     led_turnOff()
#     time.sleep(5)
#     led_turnOn()
#     time.sleep(5)


while dial1.degree == 0 or dial2.degree == 0 or dial3.degree == 0:
    dial1.degree
    dial2.degree
    dial3.degree

while True:
    speaker.turn_off()
    if dial1.degree > 90:
        go_back(new)
        # break
    if dial3.degree > 90:
        turn_right_90()
        new.append((0, "R"))
    elif dial3.degree < 10:
        turn_left_90()
        new.append((0, "L"))
    temp = dial2.degree
    if 40 <= temp <= 60:
        if cond: 
            stop_car()
            new.append((0, 0))
            cond = False
            continue
        else:
            pass
    elif temp > 60 and (cond or stopped()):
        speaker.turn_off()
        gyro_roll = 30 + (temp-60) * ((600/(max_speed-25))/40)
        gyro_pitch = 0
        new.append((gyro_pitch, gyro_roll))
        rotate_right(saturate(25 + (abs(gyro_roll) - 30)/60 * (max_speed - 25)))
        cond = True
        continue
    elif temp < 40 and (cond or stopped()):
        speaker.turn_off()
        gyro_roll = -30 - (40-temp) * ((600/(max_speed-25))/40)
        gyro_pitch = 0
        new.append((gyro_pitch, gyro_roll))
        rotate_left(saturate(25 + (abs(gyro_roll) - 30)/60 * (max_speed - 25)))
        cond = True
        continue
    gyro_pitch = gyro.pitch
    gyro_roll = gyro.roll
    if ir1.proximity > IR1 and gyro_pitch > 30 and abs(gyro_pitch) > abs(gyro_roll):
        stop_car()
        speaker.tune = 2400, 100
        continue
    speaker.turn_off()
    # elif ir2.proximity > IR2 and gyro_roll > 30 and abs(gyro_pitch) < abs(gyro_roll):
    #         stop_car()
    #         continue
    # elif ir3.proximity > IR3 and gyro_roll < -30 and abs(gyro_pitch) < abs(gyro_roll):
    #         stop_car()
    #         continue
    new.append((gyro_pitch, gyro_roll))
    if gyro_pitch > 30 and abs(gyro_pitch) > abs(gyro_roll):
        go_forward(saturate(-(25 + (abs(gyro_pitch) - 30)/30 * (max_speed - 25))))
        led_turnOff()
    elif gyro_pitch < -30 and abs(gyro_pitch) > abs(gyro_roll):
        go_forward(saturate((25 + (abs(gyro_pitch) - 30)/30 * (max_speed - 25))))
        led_turnOn("white")
    elif gyro_roll > 30 and abs(gyro_pitch) < abs(gyro_roll):
        rotate_right(saturate(25 + (abs(gyro_roll) - 30)/60 * (max_speed - 25)))
        led_turnOff()
    elif gyro_roll < -30 and abs(gyro_pitch) < abs(gyro_roll):
        rotate_left(saturate(25 + (abs(gyro_roll) - 30)/60 * (max_speed - 25)))
        led_turnOff()
    else:
        stop_car()
        led_turnOn("red")
