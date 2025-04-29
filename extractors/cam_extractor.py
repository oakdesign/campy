import os
import struct

class EmbeddedFileInfo:
    def __init__(self, filename, offset, size):
        self.filename = filename
        self.offset = offset
        self.size = size


class CamFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_bytes = None
        self.file_table = []

    def load(self):
        with open(self.filepath, 'rb') as f:
            self.raw_bytes = f.read()

        directory_offset = struct.unpack_from('<I', self.raw_bytes, 0)[0]
        num_files = struct.unpack_from('<I', self.raw_bytes, directory_offset)[0]
        pos = directory_offset + 4

        for _ in range(num_files):
            name_len = self.raw_bytes[pos]
            pos += 1
            filename = self.raw_bytes[pos:pos+name_len].decode('ascii')
            pos += name_len
            file_offset = struct.unpack_from('<I', self.raw_bytes, pos)[0]
            pos += 4
            file_size = struct.unpack_from('<I', self.raw_bytes, pos)[0]
            pos += 4

            self.file_table.append(EmbeddedFileInfo(filename, file_offset, file_size))

    def extract_all(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for f in self.file_table:
            data = self.raw_bytes[f.offset:f.offset+f.size]
            output_path = os.path.join(output_dir, f.filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as out_file:
                out_file.write(data)
            print(f"Extracted: {f.filename}")
            
    def get_extracted_files(self):
        """Return list of files in the CAM archive"""
        return [f.filename for f in self.file_table]