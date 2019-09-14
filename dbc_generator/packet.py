class Packet:
    def __init__(self, name, id, sensor_bd_id, bus_id, length):
        self.signals = []  # signal list

    """
    Add signal to signals
    """
    def add_signal(self, signal):
        pass

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