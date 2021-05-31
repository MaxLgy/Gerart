import time
import sys
import fsm
import Dart


def doWait():
    print("Waiting 1s ...")
    time.sleep(1)
    return "go"

def doCheckForCommand():
    a = "command" #A completer
    if a:
        return "go"
    else:
        return "wait"

def doGoToLocation():
    a = "loc"
    return "wait"





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