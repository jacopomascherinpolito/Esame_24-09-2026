from dataclasses import dataclass

@dataclass
class Compagnia:
    ID: int
    IATA_CODE: str
    NAME: str

    def __str__(self):
        return f"{self.ID} - {self.NAME}"

    def __hash__(self):
        return hash(self.ID)