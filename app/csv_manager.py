import csv
from enum import Enum

class OsiLayer(Enum):
    DATA_LINK = "camada2.csv"
    NETWORK   = "camada3.csv"
    TRANSPORT = "camada4.csv"

class CSVManager:
    def __init__(self):
        self.c2_file = open(OsiLayer.DATA_LINK.value, "w", newline="")
        self.c3_file = open(OsiLayer.NETWORK.value,   "w", newline="")
        self.c4_file = open(OsiLayer.TRANSPORT.value, "w", newline="")

        self.c2_writer = csv.writer(self.c2_file)
        self.c3_writer = csv.writer(self.c3_file)
        self.c4_writer = csv.writer(self.c4_file)

        self.c2_writer.writerow(["Timestamp", "Source_MAC", "Destination_MAC", "Ethertype", "Packet_Size"])
        self.c3_writer.writerow(["Timestamp", "Protocol", "Source_IP", "Destination_IP", "Protocol_ID", "Packet_Size"])
        self.c4_writer.writerow(["Timestamp", "Protocol", "Source_IP", "Source_Port", "Destination_IP", "Destination_Port", "Packet_Size"])

    def write(self, layer: OsiLayer, data : list):
        print (f"Writing to {layer.value}: {data}")
        match layer:
            case OsiLayer.DATA_LINK:
                self.c2_writer.writerow(data)
                self.c2_file.flush()
            case OsiLayer.NETWORK:
                self.c3_writer.writerow(data)
                self.c3_file.flush()
            case OsiLayer.TRANSPORT:
                self.c4_writer.writerow(data)
                self.c4_file.flush()
            case _:
                raise ValueError("Invalid OSI layer specified.")

    def close(self):
        self.c2_file.close()
        self.c3_file.close()
        self.c4_file.close()
