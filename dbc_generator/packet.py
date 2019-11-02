from signal import Signal

class Packet:
    def __init__(self, name, id, bus_id, length, signals = None):
        self.signals = [] if signals is None else signals  # signal list
        self.name = name
        self.id = id
        self.bus_id = bus_id
        self.length = length

    def add_signal(self, signal):
        """
        Add signal to signals
        """
        self.signals.append(signal)

    def is_valid(self):
        """
        Determine if this is a valid packet
        """
        pass

    @classmethod
    def from_dict(cls, data: dict):
        nane = data["name"]
        signals = []
        for signal in data["signals"]:
            signals.append(Signal.from_dict(signal))
        
        return cls(name=data["name"], id=data["id"], bus_id=data["bus_id"], length=data["length"], signals=signals)
        
    @classmethod
    def from_message(cls, message, signals):
        frame_id = message.frame_id | 0x80000000 if message.is_extended_frame else message.frame_id
        return cls(name=message.name, id=frame_id, bus_id=message.senders[0], length=message.length, signals=signals)


    def __repr__(self):
        """
        Custom string representation
        """
        signal_string = ""
        for signal in self.signals:
            signal_string += "\n " + str(signal)

        return "BO_ {id} {name}: {length} {bus_id}".format(
            id=self.id,
            name=self.name,
            length=self.length,
            bus_id=self.bus_id,
        ) + signal_string
