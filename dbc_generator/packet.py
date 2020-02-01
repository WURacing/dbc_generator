from dataclasses import dataclass
from signal import Signal


@dataclass
class Packet:
    name: str
    id: str
    bus_id: str
    length: str
    signals: list = None

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
        signals = []
        if "signals" in data:
            for signal in data["signals"]:
                signals.append(Signal.from_dict(signal))

        return cls(
            name=data["name"],
            id=data["id"],
            bus_id=data["bus_id"],
            length=data["length"],
            signals=signals,
        )

    @classmethod
    def from_message(cls, message, signals):
        frame_id = (
            message.frame_id | 0x80000000
            if message.is_extended_frame
            else message.frame_id
        )
        return cls(
            name=message.name,
            id=frame_id,
            bus_id=message.senders[0],
            length=message.length,
            signals=signals,
        )

    def __repr__(self):
        """
        Custom string representation
        """
        signal_string = ""
        for signal in self.signals:
            signal_string += "\n " + str(signal)

        return (
            "BO_ {id} {name}: {length} {bus_id}".format(
                id=self.id, name=self.name, length=self.length, bus_id=self.bus_id
            )
            + signal_string
        )
