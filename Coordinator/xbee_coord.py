from digi.xbee.devices import *

class coord:
    def __init__(self, tempLabel, HumidityLabel, blueLabel, yellowLabel, blueImage, yellowImage, offImage):
        # stores a instance of the coordinator device object
        self.device=None
        # This list will store all the End devices in the network
        self.end_devices = []
        self.nodes=None
        self.tempLabel = tempLabel
        self.HumidityLabel = HumidityLabel
        self.blueLabel = blueLabel
        self.yellowLabel = yellowLabel
        self.blueImage = blueImage
        self.yellowImage = yellowImage
        self.offImage = offImage

    def initialize(self):
        # Instantiate an XBee device object. - communication through COM3
        self.device = XBeeDevice("COM3", 9600)
        # Open COM3 for communication
        self.device.open()

        # Establish a network with the configured PAN ID
        xnet = self.device.get_network()

        # Start discovering nodes with in the network
        xnet.start_discovery_process()
        while xnet.is_discovery_running():
            time.sleep(0.5)

        # Get the list of the nodes in the network.
        self.nodes = xnet.get_devices()

        # Store their MAC (HARDWARE) addresses and their name (We need them to send packets !)
        for x in self.nodes:
            self.end_devices.append({"MAC":str(x).split()[0], "Name":str(x).split()[2] })


    # Define callback for what to do when the Coordinator get a API frame
    def my_data_received_callback(self,xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        if str(address) == "0013A20041CC55E1":
            # decode data
            splitted_comma = data.split(",")
            #print(splitted_comma)
            self.tempLabel['text'] = "Temperature : " + splitted_comma[0].split(":")[1]
            self.HumidityLabel['text'] = "Humidity      : " + splitted_comma[1].split(":")[1]
        elif str(address) == "0013A20041CC4395":
            decoded = data.split()
            if (decoded[0] == "BLUE" ):
                if(decoded[2] == "ON"):
                    self.blueLabel.config(image=self.blueImage)
                    self.blueLabel.image = self.blueImage
                elif(decoded[2] == "OFF"):
                    self.blueLabel.config(image=self.offImage)
                    self.blueLabel.image = self.offImage
            elif(decoded[0] == "YELLOW" ):
                if (decoded[2] == "ON"):
                    self.yellowLabel.config(image=self.yellowImage)
                    self.yellowLabel.image = self.yellowImage
                elif (decoded[2] == "OFF"):
                    self.yellowLabel.config(image=self.offImage)
                    self.yellowLabel.image = self.offImage

    def data_recieved(self):
        # setup a callback on another thread to get called when device get interrupted with a API frame
        self.device.add_data_received_callback(self.my_data_received_callback)

    def send_data(self, remoteAddress, data):
        remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(remoteAddress))
        # Send data using the remote object.
        self.device.send_data(remote_device, data)

