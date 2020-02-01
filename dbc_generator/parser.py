import cantools
from signal import Signal
from dbc import DBC
from packet import Packet


def parse(data: str, *args):
    model = cantools.database.load_string(data)
    packets = []
    for message in model.messages:
        signals = []
        for signal in message.signals:
            signals.append(Signal.from_signal(signal))
        packet = Packet.from_message(message, signals)
        ecu_type = []
        if all(not packet.bus_id.startswith(name) or ecu_type.append(name) for name in args):
            packets.append(packet)
    # There should be only one ecu type
    assert len(ecu_type) == 1
    return DBC(packets=packets), ecu_type[0]


if __name__ == "__main__":
    text = open("2019.1.0.dbc").read()
    print(parse(text))
