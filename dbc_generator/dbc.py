class DBC:

    # if provided filepath, load DBC tree structure from path
    def __init__(self, filepath=None):
        self.packets = []  # packet list
        if filepath is not None:
            pass

    """
    Add packet to dbc
    """

    def add_packet(self, packet):
        pass

    """
    Determine if this is a valid dbc
    """

    def is_valid(self):
        pass

    """
    Custom string representation
    """

    def __repr__(self):
        pass
