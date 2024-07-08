import os
import shutil
import pandas as pd

from pymerize.cli import run as run_pymerize

from construct_design.logger import get_logger


log = get_logger("TASKS")


def pymerize_task(df, target_dir="final"):
    log.info(f"Pymerizing {construct_file}")
    if os.path.isdir("pymerize_output"):
        log.info("Removing existing pymerize_output directory")
        shutil.rmtree("pymerize_output")
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
