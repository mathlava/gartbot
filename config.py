import os
import json

from dotenv import load_dotenv

load_dotenv(verbose=True)
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
MIYUBOT_TOKEN = os.environ.get('MIYUBOT_TOKEN')

with open(os.path.dirname(__file__) + '/config.json', 'r') as f:
    config_dict = json.load(f)

PREFIX = config_dict['prefix']
