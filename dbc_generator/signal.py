from dataclasses import dataclass


@dataclass
class Signal:
    name: str
    pos_start: int
    pos_end: int
    scale: float
    offset: float
    min: int
    max: int
    units: str
    sender: str = "Vector__XXX"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_signal(cls, signal):
        return cls(
            name=signal.name,
            pos_start=signal.start,
            pos_end=signal.length,
            scale=signal.scale,
            offset=signal.offset,
            min=signal.minimum,
            max=signal.maximum,
            units=signal.unit,
        )

    def __repr__(self):
        """
        Custom string representation
        """
        return 'SG_ {name} : {pos_start}|{pos_end}@0+ ({scale},{offset}) [{min}|{max}] "{units}" {sender}'.format(
            name=self.name,
            pos_start=self.pos_start,
            pos_end=self.pos_end,
            scale=self.scale,
            offset=self.offset,
            min=self.min,
            max=self.max,
            units=self.units,
            sender=self.sender,
        )
