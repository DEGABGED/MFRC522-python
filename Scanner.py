import time

from MFRC522 import MFRC522

class Scanner:
    def __init__(self, pi_id, scanner_id, dev='/dev/spidev0.0', rst=22):
        self.card_id = ''
        self.last_scanned = time.time()
        self.scanner_id = '{0}-{1}'.format(pi_id, scanner_id)
        self.MIFAREReader = MFRC522(dev, rst)

    def request():
        return self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

    def uid():
        return self.MIFAREReader.MFRC522_Anticoll_String()

