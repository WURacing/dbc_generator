from bottle import Bottle, run, get, post, request
import toml
from pathlib import Path

CONFIG_PATH = f'{Path(__file__).parent}/../agent_config.toml'

# find deployment port
try:
    CONFIG = toml.load(CONFIG_PATH)
    PORT = CONFIG['deployment']['dest']
except FileNotFoundError:
    LOG.error(f'count not find file with path {CONFIG_PATH}')
    raise SystemExit

if PORT is None or CONFIG is None:
    raise SystemExit('Failed to load required resources from agent_config')

# establish bottle app
app = Bottle()


@app.get('/')
def root():
    return 'welcome to dbc generator'


# TODO: add file server route for UI

# TODO: add POSt route for generating the file

run(app, host='localhost', port=PORT)