from abc import ABC, abstractmethod

class BaseReader(ABC):
    """Base class for all file format readers"""
    
    @abstractmethod
    def read(self, filepath):
        """Read data from file"""
        pass
        
    @abstractmethod
    def write(self, filepath):
        """Write data to file"""
        pass