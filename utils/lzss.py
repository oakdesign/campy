def decompress(compressed_data, decompressed_size):
    """
    Decompress data using LZSS algorithm based on the LzssNative implementation
    
    Args:
        compressed_data: Bytes object containing compressed data
        decompressed_size: Expected size of decompressed output
        
    Returns:
        Bytes object containing decompressed data
    """
    result = bytearray(decompressed_size)
    i_byte = 0  # Position in source buffer
    o_byte = 0  # Position in destination buffer
    
    while o_byte < decompressed_size:
        # Get flag byte (8 bits of flags. 1 = not packed, 0 = packed)
        if i_byte >= len(compressed_data):
            break
        flags = compressed_data[i_byte]
        i_byte += 1
        
        # Process 8 blocks
        for i in range(8):
            # Exit if we've completed decompression
            if o_byte >= decompressed_size:
                break
                
            # Check flag bit (moving from MSB to LSB)
            if flags & 0x80:
                # Not packed data (literal byte)
                if i_byte >= len(compressed_data):
                    break
                result[o_byte] = compressed_data[i_byte]
                i_byte += 1
                o_byte += 1
            else:
                # Packed data (reference to previous data)
                if i_byte + 1 >= len(compressed_data):
                    break
                
                # Calculate string position and length
                offset_hi = compressed_data[i_byte]
                offset_lo = compressed_data[i_byte + 1]
                
                # Analyze offset bytes in debugging
                # print(f"offset_hi: {offset_hi:02x}, offset_lo: {offset_lo:02x}")
                
                # This is the key change - correctly interpret the sliding window offset
                # The reference is a distance back from current position in the output buffer
                string_pos = ((offset_hi << 4) | (offset_lo >> 4))
                string_len = (offset_lo & 0x0F) + 3
                
                i_byte += 2
                
                # Safety check - don't reference beyond beginning of buffer
                if string_pos > o_byte:
                    print(f"Warning: Reference beyond current buffer at o_byte={o_byte}, string_pos={string_pos}")
                    # Use a filled placeholder to prevent errors
                    for j in range(string_len):
                        if o_byte >= decompressed_size:
                            break
                        result[o_byte] = 0  # Use zero as placeholder
                        o_byte += 1
                    continue
                    
                # Copy bytes from already decompressed data
                # This needs to handle overlapping copies correctly
                for j in range(string_len):
                    if o_byte >= decompressed_size:
                        break
                    # Calculate the actual position in the sliding window
                    # by going back string_pos bytes from current position
                    pos = o_byte - string_pos + j
                    if pos < 0 or pos >= o_byte:
                        print(f"Warning: Invalid reference at o_byte={o_byte}, pos={pos}")
                        result[o_byte] = 0  # Use zero as placeholder
                    else:
                        result[o_byte] = result[pos]
                    o_byte += 1
            
            # Shift to next flag bit
            flags <<= 1
    
    return bytes(result)