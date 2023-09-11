import time
import can

db = None
keys = {}
can_data = {}
client = can.interface.Bus(bustype='serial', channel='COM3')
client_1 = can.interface.Bus(bustype='serial', channel='COM4')

a = ""
input_str = "AquickFoxJumpsOverTheBrownBall.This is a test message"
chunks = [input_str[i:i + 7] for i in range(0, len(input_str), 7)]
complete_message = ""
expected_packet_number = 1
j = 0
rec=""
while True:

    for chunk in chunks:
        rx_msg_1 = client_1.recv(0.01)
        if rx_msg_1 is not None:
            rx_data = rx_msg_1.data.decode("utf-8")
            print(rx_data)
            packet_number = rx_msg_1.data[0]
            if packet_number == expected_packet_number:
                message_content = rx_data[1:]

                complete_message += message_content
                expected_packet_number = (expected_packet_number % 5) + 1

                if len(complete_message) == len(input_str):
                    print("Received message (client_1):", complete_message)
                    complete_message = ""
        ascii_values_chunk = [ord(char) for char in chunk]
        concatenated_string = ''.join(chr(val) for val in ascii_values_chunk)

        packet_number = (j % 5) + 1

        msg = can.Message(arbitration_id=100, is_extended_id=False, dlc=len(concatenated_string.encode("utf-8"))+1,data=bytes([packet_number]) + concatenated_string.encode("utf-8"))

        client.send(msg)

        print(msg)
        j += 1
    time.sleep(1)
# change

