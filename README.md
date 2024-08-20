<a id="readme-top"></a>
# Muted Notification Bot
A Discord bot that provides custom text and audio notifications on user mute/deafen, join, and leave. Supports unique notification sounds assigned to each of the three tracked actions (mute/deafen, join, leave) for individual users. Supports custom .mp3s stored locally on the host machine.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* [Discord](https://discord.com/)
* [FFmpeg](https://www.gyan.dev/ffmpeg/builds/)
* [Python and pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)
* pip packages
  * [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html)
    ```sh
    pip install discord.py
    ```
  * [python-dotenv](https://pypi.org/project/python-dotenv/)
    ```sh
    pip install python-dotenv
    ```
  * [PyNaCl](https://pypi.org/project/PyNaCl/)
    ```sh
    pip install PyNaCl
    ```

### Installation

1. Install all prerequisites listed above
2. Clone the repo
   ```sh
   git clone https://github.com/jacktswallow/muted-notification-bot.git
   ```
3. Enable developer mode for your Discord account
    1. Open Discord and click on the cog icon (user settings)
    2. Click the 'Advanced' tab
    3. Toggle 'Developer Mode' to on
4. Create a Discord bot account and get its token
    1. Visit the [Discord applications page](https://discord.com/developers/applications)
    2. Ensure you are logged in to your Discord account
    3. Click 'New Application'
    4. Name the bot and click 'Create'
    5. Go to the 'Bot' tab and click 'Add Bot' or 'Reset Token'
    6. Copy the token. Treat this like a password, do not share it with anyone.
    7. Open the '.env.example' file in the root directory of the project (If the file is not visible, make sure show hidden files is enabled (Mac: Cmd⌘ + Shift⇧ + .))
    8. Paste the token into the 'BOT_TOKEN' field and save the file
5. Enable privileged intents
    1. Navigate back to the 'Bot' tab
    2. Under 'Privileged Gateway Intents', enable all three intents ('Presence', 'Server Members', 'Message Content')
    3. Save changes
6. Invite the bot to join your server
    1. Go to the 'OAuth2' tab.
    2. Under 'scopes', check the 'bot' field
    3. Under 'bot permissions' check the following fields
        * 'View Channels' (General permissions)
        * 'Send Messages' (Text permissions)
        * 'Connect' (Voice permissions)
        * 'Speak' (Voice Permissions)
    4. Click 'copy'
    5. Paste the URL in a new browser window or tab
    6. Choose the server to invite the bot to and click 'Authorize'
7. Get the bot's user ID
    1. Open Discord and navigate to the server the bot was invited to
    2. Right click on the bot's profile in the panel on the right (if the panel isn't visible, click the 'Show Member List' icon)
    3. Click 'Copy User ID'
    4. Open the '.env.example' file in the root directory of the project
    5. Paste the ID into the BOT_USER_ID field and save the file 
8. Get the test channel ID
    1. Choose a channel to be your 'test channel'. This channel will recieve a 'running' message from the bot on startup
    2. Open Discord, right click on the desired channel and click 'Copy Channel ID'
    3. Open the '.env.example' file in the root directory of the project
    4. Paste the ID into the TEST_CHANNEL_ID field and save the file 
9. Get your personal user ID
    1. Open Discord and navigate to any server
    3. Right click on the your profile in the panel on the right (if the panel isn't visible, click the 'Show Member List' icon)
    4. Click 'Copy User ID'
    5. Open the '.env.example' file in the root directory of the project
    6. Paste the ID into the OWNER_USER_ID field and save the file
10. Get the ffmpeg.exe path
    1. Locate the ffmpeg.exe file that was downloaded earlier (Should be within the 'bin' folder in the ffmpeg download/install location)
    2. Copy the .exe's file path (eg. 'C:/ffmpeg/bin/ffmpeg.exe' or '/Users/user/ffmpeg/bin/ffmpeg.exe')
    3. Paste the path into the OWNER_USER_ID field (within quotations) and save the file
11. Change the '.env.example' file name to '.env'
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Running the bot
1. Open a new terminal window in the root directory of the project
2. Run the following command 
```sh
python muted_notification_bot.py
```
### Changing the default sound
1. Place the desired .mp3 file in the sounds/default folder (Short .mp3 file recommended, ideally 2 seconds or less)
2. Open the '.env' file in the root directory of the project
3. Replace the existing default sound path with the relative path to the desired sound (eg. './sounds/default/default.mp3')
4. Save the file
### Adding custom sounds 
1. Place the desired .mp3 file in the apropriate directory within the 'sounds' folder (Short .mp3 file recommended, ideally 2 seconds or less)
2. Open the 'sounds.json' file in the root directory of the project (The existing entries are examples only and should be replaced)
3. Open Discord and find the user you wish to assign the custom sound to
4. Right click on the user and click 'Copy User ID'
5. Paste the user ID into the 'sounds.json' file, replacing one of the example IDs
6. Replace the example paths under "mute":, "join":, and "leave": (All paths must be replaced for the bot to function correctly!)
7. Ensure the formatting is correct, eg: "123456789123456789": {"mute": "./sounds/mute/mute1.mp3", "join": "./sounds/join/join1.mp3", "leave": "./sounds/leave/leave1.mp3"},
8. Save the file

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact
Jack Swallow - jack.t.swallow@gmail.com

Project Link: [https://github.com/jacktswallow/muted-notification-bot](https://github.com/jacktswallow/muted-notification-bot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

