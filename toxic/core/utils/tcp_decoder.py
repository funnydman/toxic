import struct
from io import BytesIO

structure = {
    'source_port': ('>H', 2),
    'destination_port': ('>H', 2),
    'sequence_number': ('>I', 4),
    'acknowledgment_number': ('>I', 4),
    'data_offset': ('>H', 2),  # read two bytes and fill flags structure ad well
    'window_size': ('>H', 2),
    'checksum': ('>H', 2),
    'urgent_pointer': ('>H', 2)
}


class TCPDecoder:
    def __init__(self) -> None:
        self._stream = BytesIO()
        self.res = {}

    def _unpack(self, fmt, num):
        return struct.unpack(fmt, self._stream.read(num))[0]

    def get_source_port(self):
        fmt, num = structure['source_port']
        return self._unpack(fmt, num)

    def get_destination_port(self):
        fmt, num = structure['destination_port']
        return self._unpack(fmt, num)

    def get_sequence_number(self):
        fmt, num = structure['sequence_number']
        return self._unpack(fmt, num)

    def get_acknowledgment_number(self):
        fmt, num = structure['acknowledgment_number']
        return self._unpack(fmt, num)

    @staticmethod
    def get_decoded_flags(flags: str):
        return {
            'NS': flags[0],
            'CWR': flags[1],
            'ECE': flags[2],
            'URG': flags[3],
            'ACK': flags[4],
            'PSH': flags[5],
            'RST': flags[6],
            'SYN': flags[7],
            'FIN': flags[8]
        }

    def get_data_offset(self):
        # header length consists of 4 bits
        fmt, num = structure['data_offset']
        _unpacked = self._unpack(fmt, num)

        data = format(_unpacked, 'b')
        self.res['data_offset'] = int(data[:4], 2)
        self.res['reserved'] = data[4:7]

        flags = data[7:]

        self.res['flags'] = self.get_decoded_flags(flags)

    def get_window_size(self):
        fmt, num = structure['window_size']
        return self._unpack(fmt, num)

    def get_checksum(self):
        fmt, num = structure['checksum']
        return hex(self._unpack(fmt, num))

    def get_urgent_pointer(self):
        fmt, num = structure['urgent_pointer']
        return hex(self._unpack(fmt, num))

    def get_options(self):
        # todo: implementation
        # The length of this field is determined by the data offset field.
        # Depending on Option-Kind value, the next two fields may be set.
        options = {
            'option_kind': None,  # required
            'option_length': None,
            'option_data': None
        }
        return options

    def decode(self, row_data: bytes):
        self._stream.write(row_data)
        self._stream.seek(0)

        self.res = dict(
            source_port=self.get_source_port(),
            destination_port=self.get_destination_port(),
            sequence_number=self.get_sequence_number(),
            acknowledgment_number=self.get_acknowledgment_number(),
        )
        self.get_data_offset()
        self.res['window_size'] = self.get_window_size()
        self.res['checksum'] = self.get_checksum()
        self.res['urgent_pointer'] = self.get_urgent_pointer()
        self.res['options'] = self.get_options()
        return self.res


tcp_decoder = TCPDecoder()
with open('data.raw', 'rb') as f:
    content = f.read()

print(tcp_decoder.decode(content))
