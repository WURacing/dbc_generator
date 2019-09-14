class Packet:
    def __init__(self, name, id, sensor_bd_id, bus_id, length):
        self.signals = []  # signal list
        self.name = name
        self.id = id
        self.sensor_bd_id
        self.bus_id = bus_id
        self.length = length

    """
    Add signal to signals
    """
    def add_signal(self, signal):
        self.signals.append(signal)

    """
    Determine if this is a valid packet
    """
    def is_valid(self):
        pass

    """
    Custom string representation
    """
    def __repr__(self):
        pass