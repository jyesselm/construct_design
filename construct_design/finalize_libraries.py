import os
import glob
from pathlib import Path
import pandas as pd

from construct_design.logger import get_logger
from construct_design.formatting import libraries_table


log = get_logger("FINALIZE-LIBRARIES")


def create_final_directory(target_dir):
    """
    create the final directory and subdirectories if they do not exist
    """
    if not os.path.isdir(target_dir):
        log.info(f"Creating {target_dir} directory")
        os.makedirs(target_dir, exist_ok=True)
    if not os.path.isdir(f"{target_dir}/dna"):
        log.info(
            f"Creating {target_dir}/dna directory this will store DNA sequences with"
            f"T7 promoters"
        )
        os.makedirs(f"{target_dir}/dna", exist_ok=True)
    if not os.path.isdir(f"{target_dir}/rna"):
        log.info(f"Creating {target_dir}/rna directory this will store RNA sequences")
        os.makedirs(f"{target_dir}/rna", exist_ok=True)
    if not os.path.isdir(f"{target_dir}/order"):
        log.info(f"Creating {target_dir}/order directory this will store orders")
        os.makedirs(f"{target_dir}/order", exist_ok=True)


def finalize_opools(target_dir="final", csvs=None):
    """
    finalize constructs that will be ordered as opools from IDT
    """
    create_final_directory(target_dir)
    if csvs is None:
        log.info(
            "No csvs provided to finalize_opools assuming they are in final/rld_output"
        )
        csvs = glob.glob("final/rld_output/*/results-rna.csv")
        if len(csvs) == 0:
            log.error(
                "No csvs found in final/rld_output/*/results-rna.csv, skipping opools"
            )
            return
    log.info(f"Finalizing {len(csvs)} opools")
    dfs = []
    names = []
    for csv in csvs:
        name = Path(csv).parent.name
        df = pd.read_csv(csv)
        df.to_csv(f"{target_dir}/rna/{name}.csv", index=False)
        df = df[["name", "sequence"]]
        df["sequence"] = [
            "TTCTAATACGACTCACTATA" + x.replace("U", "T") for x in df["sequence"]
        ]
        df.to_csv(f"{target_dir}/dna/{name}.csv", index=False)
        # reset name to pool name for opool order
        df["name"] = name
        df = df.rename(columns={"name": "Pool name", "sequence": "Sequence"})
        dfs.append(df)
        names.append(name)
    log.info("\n" + libraries_table(dfs, names))
    log.info(f"Writing {len(dfs)} opools to {target_dir}/order/opools.xlsx")
    df.to_excel(f"{target_dir}/order/opools.xlsx", index=False)
