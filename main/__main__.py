# (c) Star Bots Tamil

import glob
from pathlib import Path
from main.utils import load_plugins
import logging
from . import Star_Bots_Tamil

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

path = "main/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
        
print("Bot Started Successfully!")


if __name__ == "__main__":
    Star_Bots_Tamil.run_until_disconnected()
