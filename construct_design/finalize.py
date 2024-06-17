import os
import glob
from pathlib import Path
import pandas as pd
import shutil

from seq_tools.dataframe import transcribe

from construct_design.logger import get_logger
from construct_design.formatting import libraries_table


log = get_logger("FINALIZE-LIBRARIES")


def create_final_directory(target_dir: str) -> None:
    """
    create the final directory and subdirectories if they do not exist
    """
    if not os.path.isdir(target_dir):
        log.info(f"Creating {target_dir} directory")
        os.makedirs(target_dir, exist_ok=True)
    if not os.path.isdir(f"{target_dir}/dna"):
        log.info(
            f"Creating {target_dir}/dna directory this will store DNA sequences with "
            f"T7 promoters"
        )
        os.makedirs(f"{target_dir}/dna", exist_ok=True)
    if not os.path.isdir(f"{target_dir}/rna"):
        log.info(f"Creating {target_dir}/rna directory this will store RNA sequences")
        os.makedirs(f"{target_dir}/rna", exist_ok=True)
    if not os.path.isdir(f"{target_dir}/order"):
        log.info(f"Creating {target_dir}/order directory this will store orders")
        os.makedirs(f"{target_dir}/order", exist_ok=True)


def finalize_opools(dfs, target_dir="final"):
    """
    finalize constructs that will be ordered as opools from IDT
    """
    create_final_directory(target_dir)
    log.info(f"Finalizing {len(dfs)} opools")
    dfs_order = []
    for name, df in dfs.items():
        df.to_csv(f"{target_dir}/rna/{name}.csv", index=False)
        df = df[["name", "sequence"]]
        df["sequence"] = [
            "TTCTAATACGACTCACTATA" + x.replace("U", "T") for x in df["sequence"]
        ]
        df.to_csv(f"{target_dir}/dna/{name}.csv", index=False)
        # reset name to pool name for opool order
        df["name"] = name
        df = df.rename(columns={"name": "Pool name", "sequence": "Sequence"})
        dfs_order.append(df)

    log.info("\n" + libraries_table(list(dfs.values()), list(dfs.keys())))
    log.info(f"Writing {len(dfs)} opools to {target_dir}/order/opools.xlsx")
    df = pd.concat(dfs_order)
    df.to_excel(f"{target_dir}/order/opools.xlsx", index=False)


def finalize_agilent(dfs, target_dir="final"):
    """
    finalize constructs that will be ordered as agilent libraries
    """
    create_final_directory(target_dir)
    log.info(f"Finalizing {len(dfs)} agilent libraries")
    for name, df in dfs.items():
        df.to_csv(f"{target_dir}/rna/{name}.csv", index=False)
        df = df[["name", "sequence"]].copy()
        df["sequence"] = [
            "TTCTAATACGACTCACTATA" + x.replace("U", "T") for x in df["sequence"]
        ]
        df.to_csv(f"{target_dir}/dna/{name}.csv", index=False)
        df = df[["sequence"]]
        df.to_csv(f"{target_dir}/order/{name}.txt", index=False, header=False)
    log.info("\n" + libraries_table(dfs.values(), list(dfs.keys())))


def finalize_primer_assembly(construct_file, target_dir="final"):
    create_final_directory(target_dir)
    if os.path.isdir("pymerize_output"):
        shutil.rmtree("pymerize_output")
    df = pd.read_csv(construct_file)
    os.system(f"pymerize {construct_file}")
    xlsx_files = glob.glob("pymerize_output/*.xlsx")
    for xlsx in xlsx_files:
        shutil.copy(xlsx, "final/order")
    for _, row in df.iterrows():
        name = row["name"]
        data = [name, row["sequence"]]
        df_construct = pd.DataFrame([data], columns=["name", "sequence"])
        df_construct = transcribe(df_construct)
        df_construct.to_csv(f"final/rna/{name}.csv", index=False)
        df_construct = df_construct[["name", "sequence"]]
        df_construct["sequence"] = [
            "TTCTAATACGACTCACTATA" + x.replace("U", "T")
            for x in df_construct["sequence"]
        ]
        df_construct.to_csv(f"final/dna/{name}.csv", index=False)
