from tkinter import *
from tkinter import PhotoImage
from tkinter.font import BOLD, Font
from xbee_coord import *

available_devices_label = None
tempLabel = None
humidityLabel = None
blueLED_label = None
yellowLED_label = None

yellow_LED_STATUS = False # off at first
blue_LED_STATUS = False


def main():


    window = Tk()

    window.title("Zigbee Home")
    window.geometry(f"{480}x{500}")

    blue_LED_ON = PhotoImage(file='blue_LED_ON.png')
    yellow_LED_ON = PhotoImage(file='yellow_LED_ON.png')
    LED_OFF = PhotoImage(file='LED_OFF.png')

    available_devices_label = Label(window, text="ZIGBEE module name", font=Font(window, size=10, weight=BOLD))
    available_devices_label.place(x=20, y=30)

    available_devices_label = Label(window, text="MAC address", font=Font(window, size=10, weight=BOLD))
    available_devices_label.place(x=250, y=30)

    tempLabel = Label(window, text="Temperature : ", font=Font(window, size=10))
    tempLabel.place(x=20, y=160)
    humidityLabel = Label(window, text="Humidity      : ", font=Font(window, size=10))
    humidityLabel.place(x=20, y=180)

    blueLED_label = Label(window, image=LED_OFF, font=Font(window, size=10, weight=BOLD))
    blueLED_label.place(x=20, y=260)


    Label(window, text="Blue LED", font=Font(window, size=8)).place(x=60, y=400)

    yellowLED_label = Label(window, image=LED_OFF, font=Font(window, size=10, weight=BOLD))
    yellowLED_label.place(x=140, y=260)
    Label(window, text="Yellow LED", font=Font(window, size=8)).place(x=175, y=400)

    xbee_coord = coord(tempLabel, humidityLabel, blueLED_label, yellowLED_label, blue_LED_ON, yellow_LED_ON, LED_OFF)
    xbee_coord.initialize()
    xbee_coord.data_recieved()

    blueLED_label.bind("<Button-1>",
                       lambda event,coord=xbee_coord, LED_NAME="blue": button_command(event, coord,LED_NAME))
    yellowLED_label.bind("<Button-1>",
                       lambda event, coord=xbee_coord, LED_NAME="yellow": button_command(event, coord,LED_NAME))

    spacing = 40
    for item in xbee_coord.end_devices:
        for key, value in item.items():
            if key == 'MAC':
                Label(window, text=value, font=Font(window, size=8)).place(x=250, y=30 + spacing)
            else:
                Label(window, text=value, font=Font(window, size=8)).place(x=20, y=30 + spacing)
        spacing += 20

    Label(window, text="Temperature and Humidity Information (END_DEVICE_2)", font=Font(window, size=10, weight=BOLD)).place(x=20, y=30 + spacing + 20)

    Label(window, text="LED light switch (END_DEVICE_1)",font=Font(window, size=10, weight=BOLD)).place(x=20, y=220)


    window.mainloop()


def button_command(event, xbee_coord, LED_NAME):
    global blue_LED_STATUS
    global yellow_LED_STATUS
    if(LED_NAME == "blue"):
        if blue_LED_STATUS:

            xbee_coord.send_data("0013A20041CC4395", "@")
            blue_LED_STATUS = False
        else:
            xbee_coord.send_data("0013A20041CC4395", "!")
            blue_LED_STATUS = True
    elif (LED_NAME == "yellow"):
        if yellow_LED_STATUS:
            xbee_coord.send_data("0013A20041CC4395", "#")
            yellow_LED_STATUS = False
        else:
            xbee_coord.send_data("0013A20041CC4395", "$")
            yellow_LED_STATUS = True





if __name__ == "__main__":
    main()