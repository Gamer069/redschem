import os
import db

from datetime import datetime

# sync flag file
SYNC_FLAG = ".redschem_bot_initialized"


async def identify_first_run(bot):
    if not os.path.exists(SYNC_FLAG):
        print("First run detected - performing initital sync...")
        await db.full_sync(bot)

        with open(SYNC_FLAG, 'w') as f:
            f.write(f"Initialized at {datetime.now().isoformat()}")
