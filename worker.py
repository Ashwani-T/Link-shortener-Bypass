import asyncio
from bypass_service import bypass_url
from queue_state import lock
from bot_handler import active_users

async def queue_worker(app):
    while True:
        update, context, short_url, status_message = await app.bot_data["queue"].get()

        user_id = update.message.from_user.id

        try:
            result = await bypass_url(short_url)
            
            await asyncio.sleep(1)

            if result is None:
                await status_message.edit_text(
                    "⏱ Timeout while processing. Please try again."
                )

            elif result[0] == "success":
                await status_message.edit_text(
                    f"✅ Bypassed link:\n{result[1]}"
                )

            elif result[0] == "error":
                await status_message.edit_text(
                    f"❌ {result[1]}"
                )

        finally:
            active_users.discard(user_id)
            
            async with lock:
                app.bot_data["processed_counter"] += 1
            app.bot_data["queue"].task_done()
