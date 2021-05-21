import dartv2b
import time
import fsm
import time
import sys

time_start = time.time()
time_begin = 5.
time_cound = 0.
turn_count = 0
max_turn_before_stop = 12


def doWait():
    global time_start, time_begin
    print("Waiting 1s ...")
    mybot.doNothing(1.)
    time.sleep(0.1)
    
    print(" Mode circuit [1] \n Mode calibration [2]  \n Quitter [3]")
    a = input()
    try:
        int(a)
    except:
        print("Non reconnu")
        event = 'wait'
        return event
    if int(a) == 1:
        event = 'go'
        print("Going forward ...")
        return event
    elif int(a) == 2:
        event = 'test'
        return event
    elif int(a) == 3:
        event = 'stop'
        return event
    else:
        print("Non reconnu")
        event = 'wait'
        return event


def doCalibrate():
    print("Calibrating mode ...")
    mybot.MenuCalibration()
    time.sleep(0.1)
    event = 'stop'
    return event


def doTurnLeft():
    print("Turning left ...")
    mybot.turn_angle(-90)
    mybot.recording.write("TURNINGLEFT\n")
    time.sleep(0.1)
    event = 'go'
    print("Going forward ...")
    return event


def doTurnRight():
    print("Turning right ...")
    mybot.turn_angle(90)
    mybot.recording.write("TURNINGRIGHT\n")
    time.sleep(0.1)
    event = 'go'
    print("Going forward ...")
    return event


def doFollowLeft():
    bool_wall = mybot.straight_line("left")
    time.sleep(0.1)
    event = 'go'
    return event


def doFollowRight():
    bool_wall = mybot.straight_line("right")
    time.sleep(0.1)
    event = 'go'
    return event


def doRun():
    print("Stopping regulation ...")
    mybot.goForward()
    time.sleep(0.2)
    mybot.set_speed(0,0)
    event = 'go'
    return event


def doCheckWall():
    time.sleep(0.1)
    event = mybot.check_closest_wall()
    print("Closest wall : ", event)
    return event    


def doCheckTurnDirection():
    global turn_count, max_turn_before_stop
    turn_count += 1
    mybot.set_speed(0,0)
    if turn_count > max_turn_before_stop:
        print("Turned ", max_turn_before_stop," times, robot will stop immediatly ...")
        event = "stop"
    else:
        print("Checking where to turn ...")
        clwall = mybot.check_closest_wall()
        if clwall == 'left':
            event = 'right'
        else:
            event = 'left'
    time.sleep(0.1)
    return event
    
    
def doStop():
    print("Stopping ...")
    time.sleep(0.1)
    event = None
    mybot.end()
    return event


if __name__ == "__main__":
    f = fsm.fsm()
    f.load_fsm_from_file("fsm_robot_cmd.txt")
    run = True
    while run:
        funct = f.run()
        if f.curState != f.endState:
            newEvent = funct()
            if newEvent is None:
                break
            else:
                f.set_event(newEvent)
        else:
            funct()
            run = False

else:
    mybot = dartv2b.DartV2()


# mybot.set_speed(100, 100)
# time.sleep(2)
# mybot.set_speed(0, 0)
# print(mybot.encoders.read_battery())
# print(mybot.delta_front_odometers())
# print(mybot.sonars.read_sonars())
