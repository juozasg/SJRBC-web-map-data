from dataclasses import dataclass

@dataclass
class TimeseriesRecord:
    timestamp: int
    flow: float
    height: float | None


type Timeseries = list[TimeseriesRecord]

