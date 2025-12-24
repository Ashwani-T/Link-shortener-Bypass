import asyncio
from bypass_service import bypass_url
from queue_state import lock

async def queue_worker(app):
    while True:
        update, context, short_url, status_message = await app.bot_data["queue"].get()

        try:
            result = await bypass_url(short_url)

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
            async with lock:
                app.bot_data["processed_counter"] += 1
            app.bot_data["queue"].task_done()
