import pandas as pd

from construct_design.logger import get_logger

log = get_logger("RNAMAKE")


def fix_secondary_structures_from_rnamake(df):
    """ """
    log.info("fixing secondary structures that rnamake messed up")
    if "structure" not in df.columns:
        log.error("No structure column in dataframe")
        return df
    count = 0
    for i, row in df.iterrows():
        structure = row["structure"]
        if structure.find("(..(.)") == -1:
            continue
        structure = structure.replace("(..(.)", "(....)")
        sequence = row["sequence"]
        left_pos = sequence[0:20].find("UAUGG")
        right_pos = sequence.find("CCUAAG")
        if left_pos == -1 or right_pos == -1:
            log.error(f"Could not find receptor in sequence for {sequence}")
            continue
        structure = list(structure)
        structure[left_pos : left_pos + 5] = "(..(("
        structure[right_pos : right_pos + 6] = "))...)"
        df.at[i, "structure"] = "".join(structure)
        count += 1
    log.info(f"fixed {count}/{len(df)} structures")
    return df


def get_more_motif_info(df):
    motif_used = []
    helix_keys = []
    motif_num = []
    keys = []
    for i, row in df.iterrows():
        spl = row["motifs_uses"].split(";")
        motif_used.append(spl[1].split("/")[0])
        helices = []
        motifs = []
        key = []
        for e in spl[:-1]:
            if e.startswith("HELIX"):
                parts = e.split(".")
                result = ".".join(parts[:3])
                helices.append(result)
                key.append(result)
            else:
                motifs.append(e)
                key.append(e)
        helix_keys.append(";".join(helices))
        motif_num.append(len(motifs))
        keys.append(";".join(key))
    df["motif"] = motif_used
    df["helix_key"] = helix_keys
    df["motif_num"] = motif_num
    df["motif_str"] = keys
