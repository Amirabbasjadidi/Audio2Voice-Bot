# Audio2Voice Bot

**Please star this project on GitHub to support me! Your support helps me maintain and improve this project.**

This is a simple Telegram bot built using the Pyrogram library. The bot allows users to upload audio files (`.ogg`, `.mp3`, `.wav`) or videos, which the bot then converts and sends back as a voice message or video message.

## Features

- Convert audio files (`.ogg`, `.mp3`, `.wav`) and return them as a voice message.
- Convert videos into video messages.
- The bot supports **18 different languages**.
- > The translations are powered by AI. If you are fluent in any of these languages and notice any issues with the phrasing or translation, please feel free to edit and improve it.

## How to Run

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Amirabbasjadidi/Audio2Voice-Bot.git
    cd Audio2Voice-Bot
    ```

2. **Install the required Python packages:**

    Ensure you have Python 3.x installed, then run:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install FFmpeg:**

    - **For Windows:**
      1. Download the FFmpeg executable from the [FFmpeg official website](https://ffmpeg.org/download.html).
      2. Extract the downloaded archive to a directory of your choice.
      3. Add the path to the `ffmpeg.exe` file to your system's PATH environment variable, or specify the path directly in the script.

    - **For macOS:**
      1. You can install FFmpeg using Homebrew. Run:
         ```bash
         brew install ffmpeg
         ```

    - **For Linux:**
      1. Use your package manager to install FFmpeg. For example, on Ubuntu or Debian:
         ```bash
         sudo apt update
         sudo apt install ffmpeg
         ```

4. **Set up your bot credentials:**

    - Obtain your `api_id` and `api_hash` by creating an application on [Telegram's API development page](https://my.telegram.org/auth).
    - Get your bot token by creating a bot with [BotFather](https://t.me/BotFather) on Telegram.

    Update the `api_id`, `api_hash`, and `bot_token` in the script with your credentials.

5. **Run the bot:**

    ```bash
    python __Main__.py
    ```

## Important Notes

1. **Required Libraries and Tools:**
   - **Pyrogram** and **FFmpeg** are mandatory for running this bot. If they are not installed, the bot will not work.
   - **Tgcrypto** is optional but recommended for better performance. If not installed, the bot will run slower.

2. **Connectivity:**
   - If you are in a country where Telegram access is restricted (e.g., Iran), ensure that the server running the bot can connect to Telegram.

3. **FFmpeg Configuration:**
   - If FFmpeg is not found in your system's PATH, you need to change `FFMPEG_PATH` from `None` to the correct path to the FFmpeg executable:

     ```python
     FFMPEG_PATH = "C:\path\to\your\ffmpeg\bin\ffmpeg.exe"
     ```

   - The path to FFmpeg differs based on your operating system. Ensure you provide the correct path for your environment.

   - [Download FFmpeg here](https://ffmpeg.org/download.html).

4. **Channel Setup:**
   - You need to set the `CHANNEL_USERNAME` to your desired channel's username, formatted as `"@your_channel_username"` (e.g., `"@amirabbas_jadidi"`).
   - If you don’t want to enforce mandatory joining of a channel, set `CHANNEL_USERNAME` to `None`. In this case, channel membership will not be required.
   - If a channel is configured, the bot must be added to the channel as an admin to properly check user membership.

5. **Project Updates:**
   - Support for this project is ongoing, and I will continue to add new features and improvements.

### user_languages.example.json

The `user_languages.json` file is used by the bot to store the preferred language of each user. The actual file is created automatically by the bot when users set their language preferences. To help you understand the structure, we provide a sample file named `user_languages.example.json`:

```json
{
  "1234567890": "en",
  "0987654321": "fa"
}
```

This sample file shows the format used to store user IDs and their corresponding language codes. The bot uses this information to send messages in the preferred language of each user.

## Bug Reporting

If you encounter any bugs in the bot and can fix them yourself, feel free to send a pull request. Otherwise, please report the issue through one of the contact methods on my [website](https://amirabbasjadidi.ir/).

## Stay Updated

To follow the latest updates and news about this project, join my Telegram channel: [@amirabbas_jadidi](https://t.me/amirabbas_jadidi).

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

