def on_button_pressed_a():
    global fadenkreuz_y
    if modus == "setzen" or modus == "angriff":
        fadenkreuz_y += 1
        if fadenkreuz_y == 5:
            fadenkreuz_y = 0
input.on_button_pressed(Button.A, on_button_pressed_a)

def LED_Setzen():
    global anschalten_array, anschalten_wert
    basic.set_led_color(Colors.BLUE)
    basic.clear_screen()
    led.plot(fadenkreuz_x, fadenkreuz_y)
    basic.pause(100)
    anschalten_array = schiffe
    anschalten_wert = 9
    doAnschalten()
    basic.pause(100)

def on_button_pressed_ab():
    global schiffe_gesetzt, modus
    if modus == "setzen":
        if schiffe[fadenkreuz_y][fadenkreuz_x] == 0:
            schiffe[fadenkreuz_y][fadenkreuz_x] = 9
            schiffe_gesetzt += 1
            music.play_tone(262, music.beat(BeatFraction.SIXTEENTH))
        else:
            music.play_tone(262, music.beat(BeatFraction.WHOLE))
    elif modus == "angriff":
        if schuesse[fadenkreuz_y][fadenkreuz_x] == 0:
            music.play_tone(262, music.beat(BeatFraction.SIXTEENTH))
            modus = "senden_angriff"
        else:
            music.play_tone(262, music.beat(BeatFraction.WHOLE))
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global fadenkreuz_x
    if modus == "setzen" or modus == "angriff":
        fadenkreuz_x += 1
        if fadenkreuz_x == 5:
            fadenkreuz_x = 0
input.on_button_pressed(Button.B, on_button_pressed_b)

def AufAngriffPruefen():
    global ergebnis, treffer, modus
    if angriff_x >= 0 and angriff_y >= 0:
        if schiffe[angriff_y][angriff_x] == 0:
            schiffe[angriff_y][angriff_x] = 1
            ergebnis = 1
        else:
            schiffe[angriff_y][angriff_x] = 2
            treffer += 1
            ergebnis = 9
        if treffer == schiffe_max:
            ergebnis = 99
            modus = "verloren"
        else:
            modus = "senden_verteidigung"
def LED_Angriff():
    global anschalten_array, anschalten_wert
    basic.set_led_color(Colors.RED)
    basic.clear_screen()
    led.plot(fadenkreuz_x, fadenkreuz_y)
    basic.pause(100)
    anschalten_array = schuesse
    anschalten_wert = 9
    doAnschalten()
    basic.pause(300)
    anschalten_wert = 1
    doAnschalten()
    basic.pause(300)

def on_received_value(name, value):
    global angriff_y, angriff_x, modus, team
    if modus == "verteidigung" and name == "afeldy":
        angriff_y = value
    elif modus == "verteidigung" and name == "afeldx":
        angriff_x = value
    elif modus == "senden_angriff" and name == "arueck":
        if value == 99:
            modus = "gewonnen"
        else:
            schuesse[fadenkreuz_y][fadenkreuz_x] = value
            basic.set_led_color(0x7f00ff)
            if value == 9:
                basic.show_icon(IconNames.YES)
            else:
                basic.show_icon(IconNames.NO)
            basic.pause(1000)
            modus = "verteidigung"
    elif (modus == "senden_verteidigung" or modus == "wahl") and name == "ende":
        modus = "angriff"
    elif modus == "setzen" and name == "team":
        team = 1
radio.on_received_value(on_received_value)

def doAnschalten():
    for y in range(5):
        for x in range(5):
            if anschalten_array[y][x] == anschalten_wert:
                led.plot(x, y)
def LED_Verteidigung():
    global anschalten_array, anschalten_wert
    basic.set_led_color(Colors.GREEN)
    basic.clear_screen()
    anschalten_array = schiffe
    anschalten_wert = 9
    doAnschalten()
    basic.pause(100)
    anschalten_wert = 2
    doAnschalten()
    basic.pause(300)
    anschalten_wert = 1
    doAnschalten()
    basic.pause(300)
team = 0
treffer = 0
ergebnis = 0
schiffe_gesetzt = 0
anschalten_wert = 0
anschalten_array: List[List[number]] = []
schiffe_max = 0
modus = ""
angriff_y = 0
angriff_x = 0
fadenkreuz_y = 0
fadenkreuz_x = 0
schuesse: List[List[number]] = []
schiffe: List[List[number]] = []
schiffe = [[0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]]
schuesse = [[0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]]
fadenkreuz_x = 2
fadenkreuz_y = 2
angriff_x = -1
angriff_y = -1
modus = "setzen"
schiffe_max = 5
radio.set_group(1)
radio.set_transmit_power(7)

def on_forever():
    global modus, fadenkreuz_x, fadenkreuz_y, angriff_x, angriff_y
    if modus == "setzen":
        if schiffe_gesetzt == schiffe_max:
            modus = "wahl"
            fadenkreuz_x = 2
            fadenkreuz_y = 2
        LED_Setzen()
    elif modus == "angriff":
        LED_Angriff()
    elif modus == "verteidigung":
        radio.send_value("ende", 0)
        AufAngriffPruefen()
        LED_Verteidigung()
    elif modus == "gewonnen":
        basic.show_icon(IconNames.HAPPY)
    elif modus == "verloren":
        radio.send_value("arueck", ergebnis)
        basic.show_icon(IconNames.SAD)
    elif modus == "senden_angriff":
        basic.set_led_color(Colors.ORANGE)
        radio.send_value("afeldy", fadenkreuz_y)
        radio.send_value("afeldx", fadenkreuz_x)
    elif modus == "senden_verteidigung":
        basic.set_led_color(Colors.BLUE)
        for index in range(21):
            led.toggle(angriff_x, angriff_y)
            basic.pause(50)
        angriff_x = -1
        angriff_y = -1
        radio.send_value("arueck", ergebnis)
    elif modus == "wahl":
        if team == 1:
            modus = "verteidigung"
        else:
            radio.send_value("team", 1)
basic.forever(on_forever)
