from abc import ABC, abstractmethod

class TrendDetector(ABC):
    @abstractmethod
    def detect(self, file) -> list:
        pass
