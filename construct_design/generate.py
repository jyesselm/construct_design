import pandas as pd
from typing import Optional
from dataclasses import dataclass

from construct_design.logger import get_logger
from rna_lib_design.structure_set import SequenceStructure

log = get_logger("GENERATE")


@dataclass(frozen=True, order=True)
class DesignSegments:
    p5: Optional[SequenceStructure]
    p3: Optional[SequenceStructure]
    p5_buffer: Optional[SequenceStructure]
    p3_buffer: Optional[SequenceStructure]

    def __init__(
        self,
        p5: Optional[SequenceStructure],
        p3: Optional[SequenceStructure],
        p5_buffer: Optional[SequenceStructure],
        p3_buffer: Optional[SequenceStructure],
    ):
        self.p5 = p5 if p5 is not None else SequenceStructure("", "")
        self.p3 = p3 if p3 is not None else SequenceStructure("", "")
        self.p5_buffer = (
            p5_buffer if p5_buffer is not None else SequenceStructure("", "")
        )
        self.p3_buffer = (
            p3_buffer if p3_buffer is not None else SequenceStructure("", "")
        )


def add_common_sequences(df: pd.DataFrame, design_segs: DesignSegments) -> pd.DataFrame:
    """ """
    data = []
    for i, row in df.iterrows():
        ss = SequenceStructure(row["sequence"], row["structure"])
        ss = design_segs.p5 + ss + design_segs.p3
        ss = ss + design_segs.p3_buffer
        ss = design_segs.p5_buffer + ss
        data.append([row["name"], ss.sequence, ss.structure])
    return pd.DataFrame(data, columns=["name", "sequence", "structure"])
