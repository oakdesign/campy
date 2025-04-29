import struct
from dataclasses import dataclass
from .base_reader import BaseReader

@dataclass
class PilotInfoClass:
    usage: int = 0
    voice_id: int = 0
    photo_id: int = 0


class PltFile(BaseReader):
    def __init__(self, filepath=None):
        self.num_pilots = 0
        self.pilot_info = []
        self.num_callsigns = 0
        self.callsign_data = []
        
        if filepath:
            self.read(filepath)
    
    def read(self, filepath):
        with open(filepath, 'rb') as f:
            # Read number of pilots (short/int16)
            self.num_pilots = struct.unpack('<h', f.read(2))[0]
            
            # Read pilot information
            self.pilot_info = []
            for _ in range(self.num_pilots):
                pilot = PilotInfoClass()
                pilot.usage = struct.unpack('<h', f.read(2))[0]
                pilot.voice_id = struct.unpack('<B', f.read(1))[0]
                pilot.photo_id = struct.unpack('<B', f.read(1))[0]
                self.pilot_info.append(pilot)
            
            # Read callsign information
            self.num_callsigns = struct.unpack('<h', f.read(2))[0]
            self.callsign_data = list(f.read(self.num_callsigns))
    
    def write(self, filepath):
        with open(filepath, 'wb') as f:
            # Write number of pilots
            f.write(struct.pack('<h', self.num_pilots))
            
            # Write pilot information
            for pilot in self.pilot_info:
                f.write(struct.pack('<h', pilot.usage))
                f.write(struct.pack('<B', pilot.voice_id))
                f.write(struct.pack('<B', pilot.photo_id))
            
            # Write callsign information
            f.write(struct.pack('<h', self.num_callsigns))
            f.write(bytes(self.callsign_data))
    
    def __str__(self):
        output = f"Number of pilots: {self.num_pilots}\n"
        for i, pilot in enumerate(self.pilot_info):
            output += f"Pilot {i}: Usage={pilot.usage}, Voice ID={pilot.voice_id}, Photo ID={pilot.photo_id}\n"
        output += f"Number of callsigns: {self.num_callsigns}\n"
        output += f"Callsign data: {self.callsign_data}"
        return output