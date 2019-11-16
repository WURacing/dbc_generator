from dataclasses import asdict
from packet import Packet


class DBC:

    # if provided filepath, load DBC tree structure from path
    def __init__(self, filepath=None, packets=None):
        if packets is not None:
            self.packets = packets
            self.bus_ids = set()
            for packet in packets:
                self.bus_ids.add(packet.bus_id)
            return

        self.packets = []  # packet list
        self.bus_ids = set()
        if filepath is not None:
            pass

    @classmethod
    def from_packets_list(cls, packets_data: list) -> "DBC":
        packets = []
        for data in packets_data:
            packet = Packet.from_dict(data)
            packets.append(packet)

        return cls(packets=packets)

    def to_dict(self):
        data = {"packet": []}

        for packet in self.packets:
            data["packet"].append(asdict(packet))

        return {"file": [data]}

    def add_packet(self, packet):
        """
        Add packet to dbc
        """
        self.bus_ids.add(packet.bus_id)
        self.packets.add(packet)

    def is_valid(self):
        """
        Determine if this is a valid dbc
        """
        pass  # we don't have invalid dbcs. duh

    def __repr__(self):
        """
        Custom string representation
        """
        packet_strs = []
        for packet in self.packets:
            packet_strs.append(str(packet))

        return """VERSION ""


NS_ : 
	NS_DESC_
	CM_
	BA_DEF_
	BA_
	VAL_
	CAT_DEF_
	CAT_
	FILTER
	BA_DEF_DEF_
	EV_DATA_
	ENVVAR_DATA_
	SGTYPE_
	SGTYPE_VAL_
	BA_DEF_SGTYPE_
	BA_SGTYPE_
	SIG_TYPE_REF_
	VAL_TABLE_
	SIG_GROUP_
	SIG_VALTYPE_
	SIGTYPE_VALTYPE_
	BO_TX_BU_
	BA_DEF_REL_
	BA_REL_
	BA_DEF_DEF_REL_
	BU_SG_REL_
	BU_EV_REL_
	BU_BO_REL_
	SG_MUL_VAL_

BS_:

BU_: {bus_ids}

{packets}



BA_DEF_ BU_  "TpNodeBaseAddress" HEX 0 65535;
BA_DEF_ BO_  "GenMsgSendType" STRING ;
BA_DEF_  "ProtocolType" STRING ;
BA_DEF_  "NmType" STRING ;
BA_DEF_ BO_  "GenMsgCycleTime" INT 1 10000;
BA_DEF_ BO_  "GenMsgILSupport" ENUM  "No","Yes";
BA_DEF_ BU_  "ILUsed" ENUM  "No","Yes";
BA_DEF_  "VersionNumber" INT 0 10000;
BA_DEF_  "VersionDay" INT 1 31;
BA_DEF_  "VersionMonth" INT 1 12;
BA_DEF_  "VersionYear" INT 2016 3000;
BA_DEF_  "BusType" STRING ;
BA_DEF_ BO_  "DBC_Author_Contact" STRING ;
BA_DEF_DEF_  "DBC_Author_Contact" "CANbusInfo@AEMelectronics.com";
BA_DEF_DEF_  "TpNodeBaseAddress" 0;
BA_DEF_DEF_  "GenMsgSendType" "Cyclic";
BA_DEF_DEF_  "ProtocolType" "";
BA_DEF_DEF_  "NmType" "";
BA_DEF_DEF_  "GenMsgCycleTime" 20;
BA_DEF_DEF_  "GenMsgILSupport" "Yes";
BA_DEF_DEF_  "ILUsed" "Yes";
BA_DEF_DEF_  "VersionNumber" 0;
BA_DEF_DEF_  "VersionDay" 1;
BA_DEF_DEF_  "VersionMonth" 1;
BA_DEF_DEF_  "VersionYear" 2016;
BA_DEF_DEF_  "BusType" "Can";
BA_ "ProtocolType" "AEM Net";
BA_ "NmType" "AEM Net";
BA_ "VersionNumber" 3;
BA_ "VersionDay" 28;
BA_ "VersionMonth" 11;
BA_ "BusType" "CAN";
BA_ "GenMsgCycleTime" BO_ 2180030470 50;
BA_ "GenMsgCycleTime" BO_ 2180030466 16;
BA_ "GenMsgCycleTime" BO_ 2180030465 16;
BA_ "GenMsgCycleTime" BO_ 2180030464 16;

""".format(
            bus_ids=" ".join(self.bus_ids), packets="\n\n".join(packet_strs)
        )
