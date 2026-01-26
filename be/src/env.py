import os
import config
import db

import json

from datetime import datetime
from loguru import logger

# sync flag file
SYNC_FLAG = ".redschem_bot_initialized"

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED_JSON = os.path.abspath(
    os.path.join(HERE, "../../shared/categories.json")
)


async def identify_first_run(bot):
    with open(SHARED_JSON, "r") as f:
        subcategories = json.load(f)

    config.CHANNELS = [sub for subs in subcategories.values() for sub in subs]

    if not os.path.exists(SYNC_FLAG):
        logger.info("First run detected - performing initital sync...")
        await db.full_sync(bot)

        with open(SYNC_FLAG, 'w') as f:
            f.write(f"Initialized at {datetime.now().isoformat()}")
