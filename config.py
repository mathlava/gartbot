import os
import json

from dotenv import load_dotenv

load_dotenv(verbose=True)
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

with open(os.path.dirname(__file__) + '/config.json', 'r') as f:
    config_dict = json.load(f)

PREFIX: str = config_dict['prefix']
