from JakaModbusCommunication import Jaka_Coms

jaka = Jaka_Coms(host="192.168.1.186", port=502)  # Replace with your Modbus server IP

print(jaka.get_uhi_origin_pulse())
