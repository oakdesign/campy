"""
Python implementation of Falcon BMS data structures
Converted from F4Structs.cs
"""

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import List, Optional, Union
import struct


@dataclass
class PilotInfoClass:
    """Represents pilot information in PLT files"""
    usage: int = 0
    voice_id: int = 0
    photo_id: int = 0
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'PilotInfoClass':
        """Create a PilotInfoClass from binary data"""
        instance = cls()
        instance.usage = struct.unpack('<h', data[0:2])[0]  # short is 2 bytes
        instance.voice_id = struct.unpack('<B', data[2:3])[0]  # byte is 1 byte
        instance.photo_id = struct.unpack('<B', data[3:4])[0]  # byte is 1 byte
        return instance
        
    def to_bytes(self) -> bytes:
        """Convert to binary data"""
        return struct.pack('<hBB', self.usage, self.voice_id, self.photo_id)


@dataclass
class VU_ID:
    """Represents a unique identifier in Falcon BMS"""
    num_: int = 0
    creator_: int = 0
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'VU_ID':
        """Create a VU_ID from binary data"""
        instance = cls()
        instance.num_ = struct.unpack('<I', data[0:4])[0]
        instance.creator_ = struct.unpack('<I', data[4:8])[0]
        return instance
        
    def to_bytes(self) -> bytes:
        """Convert to binary data"""
        return struct.pack('<II', self.num_, self.creator_)


@dataclass
class vector:
    """Represents a 3D vector"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'vector':
        """Create a vector from binary data"""
        instance = cls()
        instance.x = struct.unpack('<f', data[0:4])[0]
        instance.y = struct.unpack('<f', data[4:8])[0]
        instance.z = struct.unpack('<f', data[8:12])[0]
        return instance
        
    def to_bytes(self) -> bytes:
        """Convert to binary data"""
        return struct.pack('<fff', self.x, self.y, self.z)


class VuClassHierarchy(IntEnum):
    """Enumeration of VU class hierarchy levels"""
    VU_DOMAIN = 0
    VU_CLASS = 1
    VU_TYPE = 2
    VU_STYPE = 3
    VU_SPTYPE = 4
    VU_OWNER = 5


class Classtable_Domains(IntEnum):
    """Enumeration of domain types"""
    DOMAIN_ABSTRACT = 1
    DOMAIN_AIR = 2
    DOMAIN_LAND = 3
    DOMAIN_SEA = 4
    DOMAIN_SPACE = 5
    DOMAIN_UNDERGROUND = 6
    DOMAIN_UNDERSEA = 7


class Classtable_Classes(IntEnum):
    """Enumeration of class types"""
    CLASS_ABSTRACT = 0
    CLASS_ANIMAL = 1
    CLASS_FEATURE = 2
    CLASS_MANAGER = 3
    CLASS_OBJECTIVE = 4
    CLASS_SFX = 5
    CLASS_UNIT = 6
    CLASS_VEHICLE = 7
    CLASS_WEAPON = 8
    CLASS_WEATHER = 9
    CLASS_SESSION = 10
    CLASS_GAME = 11
    CLASS_GROUP = 12
    CLASS_DIALOG = 13


class Data_Types(IntEnum):
    """Enumeration of data types"""
    DTYPE_FEATURE = 1
    DTYPE_NONE = 2
    DTYPE_OBJECTIVE = 3
    DTYPE_UNIT = 4
    DTYPE_VEHICLE = 5
    DTYPE_WEAPON = 6


# Add more structures and enums as needed for your project