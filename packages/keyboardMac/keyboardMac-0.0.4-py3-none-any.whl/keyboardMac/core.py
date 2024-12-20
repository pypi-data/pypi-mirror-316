from pynput.keyboard import KeyCode, Listener, Controller, Key as k
from pynput.mouse import Controller as controller, Button, Listener as listener
import time
import threading

keyb = Controller()
mouse = controller()

recording = False

key = ""
key2 = ""

p = 0

presses = []

abbreviations = {

}

key_list = {

}

hotkeys = {

}


def write(sentence):
    keyb.type(sentence)


key_presses = []

for op in range(100):
    presses.append(".")


row = 0

v = []

clicks = {

}

nbOfClicks = 0

def on_click(x, y, button, pressed):
    global clicks, nbOfClicks, p

    if recording:
        nbOfClicks += 1

        if nbOfClicks % 2 != 0:
            clicks[str(nbOfClicks)] = [x, y, time.time() - p]
            p = time.time()

def on_press(Key):
    global key, presses, abbreviations, row, key2
    for oo in hotkeys.keys():
        print(hotkeys[oo])
        if Key == KeyCode(char=oo):
            if hotkeys[oo][1] == "":
                hotkeys[oo][0]()
            else:
                print(hotkeys[oo][1])
            break

    key = Key
    key2 = ""
    presses.append(Key)

    for ab in abbreviations.keys():
        row = 0
        g = 0
        res = []
        for nnn in ab:
            g += 1
            res.insert(0, presses[len(presses) - g])

        z = []

        for t in ab:
            z.append(KeyCode(char=t))

        if str(res) == str(z):
            for dfg in range(len(ab)):
                keyb.tap(k.backspace)
            keyb.type(abbreviations[ab])
            break



def on_release(Key):
    global key, key2
    key = ""
    key2 = Key


def is_pressed(Key):
    if key == KeyCode(char=Key):
        return True
    else:
        return False


def press(Key):
    time.sleep(0.1)
    keyb.press(KeyCode(char=Key))


def release(Key):
    keyb.release(KeyCode(char=Key))


def wait_for_key(Key="]]", wait_for_release=False):
    while KeyCode(char=Key) != key:
        pass

    if wait_for_release:
        while KeyCode(char=Key) == key:
            pass


def add_abbreviation(abbrev, replacement):
    global abbreviations
    abbreviations[abbrev] = replacement


def press_and_release(key1, key2):
    keyb.press(KeyCode(char=key1))
    keyb.release(KeyCode(char=key2))

def record(Key):
    global key_list

    key_list = {

    }

    zz = 0

    m = time.time()

    b = 0

    while key != KeyCode(char=Key):
        if key != "":
            zz += 1
            key_list[str(zz)] = [key, time.time() - m, "p"]
            m = time.time()
            b = key
            while key == b:
                pass
        elif key2 != "":
            zz += 1
            key_list[str(zz)] = [key2, time.time() - m, "r"]
            m = time.time()
            b = key2
            while key2 == b:
                pass
    key_list.pop("1")

    return key_list


def play(key_dict, speed_factor=1):
    for ke in key_dict.keys():
        time.sleep(key_dict[ke][1] / speed_factor)
        if key_dict[ke][2] == "p":
            keyb.press(key_dict[ke][0])
        else:
            keyb.release(key_dict[ke][0])


def record_mouse(Key):
    global recording, clicks, p

    clicks = {

    }

    p = time.time()

    while key != KeyCode(char=Key):
        recording = True
    recording = False

    return clicks


def record_mouse_and_keyboard(Key):
    global recording, clicks, p, key_list
    zz = 0

    m = time.time()
    p = time.time()

    b = 0
    b1 = 0

    key_list = {

    }

    clicks = {

    }

    while key != KeyCode(char=Key):
        recording = True
        if key != "":
            if key != b and key != KeyCode(char=""):
                zz += 1
                #print(key)
                key_list[str(zz)] = [key, time.time() - m, "p"]
                m = time.time()
                b = key
            b1 = 0
        elif key2 != "":
            if key2 != b1:
                zz += 1
                key_list[str(zz)] = [key2, time.time() - m, "r"]
                m = time.time()
                b1 = key2
            b = 0
    recording = False

    clicks[str(nbOfClicks + 1)] = (0, 0)

    return key_list, clicks


def play_mouse(click_dict, speed_factor=1):
    for ke in click_dict.keys():
        time.sleep(click_dict[ke][2] / speed_factor)
        mouse.position = (click_dict[ke][0], click_dict[ke][1])
        time.sleep(0.01)
        mouse.click(Button.left)


def play_mouse_and_keyboard(key_dict, click_dict, speed_factor=1):
    print(key_dict)
    print(click_dict)
    def m():
        for ke in click_dict.keys():
            time.sleep(click_dict[ke][2] / speed_factor)
            mouse.position = (click_dict[ke][0], click_dict[ke][1])
            time.sleep(0.01)
            mouse.click(Button.left)

    def keybo():
        for ke in key_dict.keys():
            time.sleep(key_dict[ke][1] / speed_factor)
            if key_dict[ke][2] == "p":
                keyb.press(key_dict[ke][0])
            else:
                keyb.release(key_dict[ke][0])

    t1 = threading.Thread(target=m)
    t2 = threading.Thread(target=keybo)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def add_hotkey(Key, do, args=""):
    global hotkeys
    hotkeys[Key] = [do, args]


l = Listener(on_press=on_press, on_release=on_release)
i = listener(on_click=on_click)

l.start()
time.sleep(0.5)
i.start()