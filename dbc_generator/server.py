from bottle import Bottle, run, get, post, request, template, static_file
import toml
from pathlib import Path
import logging


CONFIG_PATH = f"{Path(__file__).parent}/../agent_config.toml"
LOG = logging.getLogger("dbc_generator.server")

# find deployment port
try:
    CONFIG = toml.load(CONFIG_PATH)
    PORT = CONFIG["deployment"]["dest"]
except FileNotFoundError:
    LOG.error(f"count not find file with path {CONFIG_PATH}")
    raise SystemExit

if PORT is None or CONFIG is None:
    raise SystemExit("Failed to load required resources from agent_config")

# establish bottle app
app = Bottle()


@app.get("/")
def root():
    return "welcome to dbc generator"


# TODO: add file server route for UI
@app.get("/ui")
def ui():
    return static_file("ui.html", "static/ui/")


@app.get("/static/<path>/<filename>")
def static(path, filename):
    return static_file(filename, "static/" + path)


# TODO: add POST route for generating the file
@app.post("/upload")
def upload():
    for thing in request.forms:
        print(thing)


run(app, host="localhost", port=PORT, debug=True)
