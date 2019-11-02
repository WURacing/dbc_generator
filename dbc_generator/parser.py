import cantools
from signal import Signal
from dbc import DBC
from packet import Packet

def parse(data: str):
    model = cantools.database.load_string(data)
    packets = []
    for message in model.messages:
        signals = []
        for signal in message.signals:
            signals.append(Signal.from_signal(signal))
        packet = Packet.from_message(message, signals)
        packets.append(packet)
    
    return DBC(packets=packets)
