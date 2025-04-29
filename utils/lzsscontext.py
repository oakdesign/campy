class LZSSContext:
    INDEX_BIT_COUNT = 12
    LENGTH_BIT_COUNT = 4
    WINDOW_SIZE = 1 << INDEX_BIT_COUNT
    RAW_LOOK_AHEAD_SIZE = 1 << LENGTH_BIT_COUNT
    BREAK_EVEN = (1 + INDEX_BIT_COUNT + LENGTH_BIT_COUNT) // 9
    LOOK_AHEAD_SIZE = RAW_LOOK_AHEAD_SIZE + BREAK_EVEN

    def __init__(self):
        self.window = bytearray(self.WINDOW_SIZE)
        self.data_buffer = bytearray(17)
        self.flag_bit_mask = 0x100  # <-- Important: Start at 0x100
        self.inc_input_string = 0

    def init_input_buffer(self, input_bytes):
        self.data_buffer[0] = input_bytes[0]
        self.flag_bit_mask = 1

    def input_bit(self, input_bytes, input_pos):
        self.inc_input_string = 0
        if self.flag_bit_mask == 0x100:
            self.data_buffer[0] = input_bytes[input_pos]
            self.flag_bit_mask = 1
            self.inc_input_string = 1
        bit = self.data_buffer[0] & self.flag_bit_mask
        self.flag_bit_mask <<= 1
        return bit != 0


def lzss_expand(input_bytes: bytes, output_size: int) -> bytes:
    ctxt = LZSSContext()
    output_bytes = bytearray()

    input_pos = 0
    ctxt.data_buffer[0] = input_bytes[input_pos]
    ctxt.flag_bit_mask = 1
    input_pos += 1
    current_position = 1

    while output_size > 0:
        if ctxt.input_bit(input_bytes, input_pos):
            if ctxt.inc_input_string:
                input_pos += 1
            c = input_bytes[input_pos]
            input_pos += 1
            output_bytes.append(c)
            output_size -= 1
            ctxt.window[current_position] = c
            current_position = (current_position + 1) & (ctxt.WINDOW_SIZE - 1)
        else:
            if ctxt.inc_input_string:
                input_pos += 1
            match_length = input_bytes[input_pos]
            input_pos += 1
            match_position = input_bytes[input_pos]
            input_pos += 1
            match_position |= (match_length & 0xF) << 8
            match_length >>= 4
            match_length += ctxt.BREAK_EVEN

            # Correct the match length if it overflows
            if match_length < output_size:
                output_size -= match_length + 1
            else:
                match_length = output_size - 1
                output_size = 0

            for i in range(match_length + 1):
                c = ctxt.window[(match_position + i) & (ctxt.WINDOW_SIZE - 1)]
                output_bytes.append(c)
                ctxt.window[current_position] = c
                current_position = (current_position + 1) & (ctxt.WINDOW_SIZE - 1)

    return bytes(output_bytes)
