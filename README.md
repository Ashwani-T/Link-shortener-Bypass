# 🔗 Link-shortener-Bypass

A minimalist Telegram bot designed to bypass multiple link shorteners and provide direct target URLs. This project uses an asynchronous architecture to bridge a user interface bot with backend bypass services.

## 🚀 Key Features

* **Async Queueing**: Efficiently handles multiple user requests using a background worker and `asyncio.Queue`.
* **Dual-Client System**: Integrates the Telegram Bot API for user interactions and Telethon for backend service communication.
* **Live Queue Tracking**: Automatically calculates and notifies users of their current position in the processing queue.
* **URL Validation**: Ensures only properly formatted URLs are processed via regex-based validation.

## 🛠️ Quick Setup

1.  **Environment Variables**: Create a `.env` file with the following keys:
    * `API_ID` & `API_HASH`: Your Telegram API credentials.
    * `BOT_TOKEN`: Your interface bot's token from @BotFather.
    * `TARGET_BOT_TOKEN`: The username of the backend bypasser bot.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Authenticate**: Run the login test to authorize your Telegram User Client:
    ```bash
    python test_login.py
    ```

4.  **Start the Bot**: Launch the main application:
    ```bash
    python main.py
    ```

## 📂 Project Structure

* `main.py`: Entry point that initializes the bot, client, and worker.
* `bot_handler.py`: Manages user commands and message queueing.
* `bypass_service.py`: Core logic for interacting with external bypass services.
* `worker.py`: Background task handler that processes the link queue.

---

*Note: This project is for educational and personal use only.*
