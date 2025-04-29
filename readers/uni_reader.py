from .base_reader import BaseReader
import os
import struct
from utils.lzss import decompress
from utils.lzsscontext import lzss_expand  # Using the Python lzss library

class UniFile(BaseReader):
    def __init__(self, filepath=None):
        self.raw_data = None
        self.decompressed_data = None
        self.filepath = None
        self.num_units = 0
        
        if filepath:
            self.read(filepath)
    
    def read(self, filepath):
        """Read UNI file and decompress it"""
        self.filepath = filepath
        
        with open(filepath, 'rb') as f:
            self.raw_data = f.read()
        
        # Parse header according to .NET code
        try:
            # Skip first 4 bytes (not used in .NET code)
            offset = 4
            
            # Read numUnits (2 bytes)
            self.num_units = struct.unpack_from('<h', self.raw_data, offset)[0]
            offset += 2
            
            # Read decompressed size (4 bytes)
            decompressed_size = struct.unpack_from('<i', self.raw_data, offset)[0]
            offset += 4
            
            # Check if decompressed_size is valid
            if decompressed_size == 0:
                print(f"Invalid decompressed size (0) in {filepath}")
                return
                
            # Extract compressed data (starts at offset 10)
            compressed_data = self.raw_data[10:]
            
            print(f"Header info: numUnits={self.num_units}, decompressedSize={decompressed_size}")
            print(f"Compressed data size: {len(compressed_data)} bytes")
            
            # Decompress using our custom implementation
            # self.decompressed_data = decompress(compressed_data, decompressed_size)
            self.decompressed_data = lzss_expand(compressed_data, decompressed_size)
            
            print(f"Successfully decompressed to {len(self.decompressed_data)} bytes")
                
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            import traceback
            traceback.print_exc()
            self.decompressed_data = None
    
    # Rest of the class remains the same...
    
    def write(self, filepath):
        """Write the decompressed data to file"""
        if self.decompressed_data:
            with open(filepath, 'wb') as f:
                f.write(self.decompressed_data)
            return True
        return False
    
    def save_decompressed(self, output_dir=None):
        """Save the decompressed data to a file with .dec extension"""
        if not self.decompressed_data:
            return False
            
        if output_dir:
            # Use the output directory with original filename
            filename = os.path.basename(self.filepath)
            output_path = os.path.join(output_dir, f"{filename}.dec")
        else:
            # Use same directory as original
            output_path = f"{self.filepath}.dec"
            
        with open(output_path, 'wb') as f:
            f.write(self.decompressed_data)
        print(f"Saved decompressed data to {output_path}")
        return True
    
    def __str__(self):
        if self.decompressed_data:
            return f"UNI file: {self.filepath}\nCompressed size: {len(self.raw_data)}\nDecompressed size: {len(self.decompressed_data)}"
        else:
            return f"UNI file: {self.filepath}\nCompressed size: {len(self.raw_data)}\nDecompression failed"