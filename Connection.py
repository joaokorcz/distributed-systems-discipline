class Connection:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.name = None
        self.topics = []
