from dataclasses import dataclass

@dataclass
class TimeseriesRecord:
    timestamp: int
    flow: float


type Timeseries = list[TimeseriesRecord]

