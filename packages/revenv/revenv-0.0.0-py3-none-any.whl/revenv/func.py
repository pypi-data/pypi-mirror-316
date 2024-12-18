import os
from pathlib import Path
import re
import logging
from reenv.logging_config import setup_logger

logger = setup_logger(logging.DEBUG)


def reset(venv_path):
    venv_path = Path(venv_path).absolute()
    logger.info(f"new VIRTUAL_ENV={venv_path}")
    pathdict = {
        "posix": "bin",  # Linux
        "nt": "Scripts",  # Windows
    }
    activate_lst = [
        "activate",
        "activate.bat",
        "activate.fish",
        "activate.nu",
        "activate.ps1",
        "Activate.ps1",
        "activate.csh",
    ]
    acdir = venv_path.joinpath(pathdict[os.name])
    oldvenvpath = None
    pattern_lst = [
        r"VIRTUAL_ENV(\s*)=(\s*)(.*[\\/]{1}.*)",
        r"VIRTUAL_ENV(\s*)=(\s*)'(.*[\\/]{1}.*)'",
    ]
    repl_lst = [
        r"VIRTUAL_ENV={}",
        r"VIRTUAL_ENV='{}'",
    ]
    for acname in activate_lst:
        acpath = acdir.joinpath(acname)
        if not acpath.exists():
            continue
        with open(acpath, "r", encoding="utf8") as f:
            data = f.read()
        change = False
        for pattern, repl in zip(pattern_lst, repl_lst):
            result = re.search(pattern, data)
            if not result:
                continue
            chang = True
            logger.info(result.group())
            s = repl.format(venv_path).replace("\\", "\\\\")
            logger.debug(f"{s=}")
            data = re.sub(pattern, s, data)
        if change:
            with open(acpath, "w", encoding="utf8") as f:
                f.write(data)
            logger.info(f"reset {acpath}.")


if __name__ == "__main__":
    reset(r".")
