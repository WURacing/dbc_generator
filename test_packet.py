from dbc_generator.packet import Packet
from dbc_generator.signal import Signal

correct_output = """BO_ 2180030470 DataLoggerBoard1: 8 DATALOGGER_19
 SG_ BrakePressureRear : 7|10@0+ (0.9775171065,0) [0|1000] "pressure:psi" Vector__XXX
 SG_ BrakePressureFront : 13|10@0+ (0.9775171065,0) [0|1000] "pressure:psi" Vector__XXX
 SG_ CGGyroscope : 19|10@0+ (0.12201,-63.1553) [-50|50] "rotation:deg/s" Vector__XXX
 SG_ CGAccelRawX : 25|10@0+ (0.012219,-6.215) [-5|5] "acceleration:G" Vector__XXX
 SG_ CGAccelRawY : 47|10@0+ (0.012219,-6.215) [-5|5] "acceleration:G" Vector__XXX
 SG_ CGAccelRawZ : 53|10@0+ (0.012219,-6.215) [-5|5] "acceleration:G" Vector__XXX"""


def test_packet_format():

    packet = Packet("DataLoggerBoard1", "2180030470", "DATALOGGER_19", 8)
    packet.add_signal(
        Signal("BrakePressureRear", 7, 10, 0.9775171065, 0, 0, 1000, "pressure:psi")
    )
    packet.add_signal(
        Signal("BrakePressureFront", 13, 10, 0.9775171065, 0, 0, 1000, "pressure:psi")
    )
    packet.add_signal(
        Signal("CGGyroscope", 19, 10, 0.12201, -63.1553, -50, 50, "rotation:deg/s")
    )
    packet.add_signal(
        Signal("CGAccelRawX", 25, 10, 0.012219, -6.215, -5, 5, "acceleration:G")
    )
    packet.add_signal(
        Signal("CGAccelRawY", 47, 10, 0.012219, -6.215, -5, 5, "acceleration:G")
    )
    packet.add_signal(
        Signal("CGAccelRawZ", 53, 10, 0.012219, -6.215, -5, 5, "acceleration:G")
    )

    generated_output = str(packet)
    assert generated_output == correct_output
