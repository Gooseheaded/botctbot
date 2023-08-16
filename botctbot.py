from dataclasses import dataclass
import os
import discord
import json

# Bot boilerplate.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Bot code.
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# Constants.
EXIT_ERROR = 1

@dataclass
class BotSettings:
    """Class for keeping track of bot settings."""
    storyteller: str
    api_token: str

# Globally accessible bot settings.
bot_settings = BotSettings()

def load_settings():
    """Bot initialization."""
    global bot_settings
    with open('settings.json', 'r') as fd_settings:
        try:
            file_settings = json.load(fd_settings)
        except Exception:
            print('ERROR: Fix `settings.json` so it is a proper json dictionary.')
            os.exit(EXIT_ERROR)

        if file_settings['storyteller'] is None:
            print('ERROR: A storyteller is required to run the game. Add a `"storyteller"` to `settings.json`.')
            os.exit(EXIT_ERROR)
        bot_settings.storyteller = file_settings['storyteller']

        if file_settings['api_token'] is None:
            print('ERROR: An API token is required to connect to discord. Add an `"api_token"` to `settings.json`. To learn more, go here: https://discord.com/developers/applications')
            os.exit(EXIT_ERROR)
        bot_settings.api_token = file_settings['api_token']

# Entry point.
def main():
    load_settings()
    client.run(bot_settings.api_token)

if __name__ == '__main__':
    main()
