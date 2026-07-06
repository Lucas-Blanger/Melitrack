from enum import Enum as PyEnum


class HiveType(str, PyEnum):
    box = "caixa"
    trap = "isca"


class ColonyHealth(str, PyEnum):
    excellent = "excelente"
    good = "boa"
    fair = "regular"
    poor = "ruim"
    critical = "crítica"


class AnalysisStatus(str, PyEnum):
    pending = "pending"
    processed = "processed"
    failed = "failed"


class HarvestProduct(str, PyEnum):
    honey = "mel"
    propolis = "própolis"
    wax = "cera"
