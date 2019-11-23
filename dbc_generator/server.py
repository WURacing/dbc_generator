from bottle import Bottle, run, get, post, request, response, template, static_file
import toml
from pathlib import Path
from dbc import DBC
from parser import parse
import json
import requests
import logging


CONFIG_PATH = f"{Path(__file__).parent}/../agent_config.toml"
LOG = logging.getLogger("dbc_generator.server")
ECU_CONFIGS = {}

# find deployment port
try:
    CONFIG = toml.load(CONFIG_PATH)
    PORT = CONFIG["deployment"]["dest"]
    ECU_CONFIGS = json.load(open("ecu.json"))
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


@app.get("/ui")
def ui():
    return static_file("ui.html", "static/ui/")


@app.get("/dbcs")
def get_dbcs():
    github_response = requests.get(
        "https://api.github.com/repos/wuracing/dbc/contents/dbc"
    ).json()
    response_data = []
    for file in github_response:
        if file["name"].endswith(".dbc"):
            response_data.append(
                {"name": file["name"], "download": file["download_url"]}
            )
    response.content_type = "application/json"
    return json.dumps(response_data)


@app.post("/parse")
def parse_dbc():
    url = list(request.forms.keys())[0]
    dbc_raw = requests.get(url).text
    dbc, ecu = parse(dbc_raw, *ECU_CONFIGS.keys())
    response.content_type = "application/json"
    data = {
        "dbc": dbc.to_dict(),
        "ecu": ecu
    }
    return json.dumps(data)


@app.get("/static/<path>/<filename>")
def static(path, filename):
    return static_file(filename, "static/" + path)


@app.post("/upload")
def upload():
    for thing in request.forms:
        data = json.loads(thing)
        dbc = DBC.from_packets_list(data["dbc"]["file"][0]["packet"], ECU_CONFIGS[data["ecu"]])
        return str(dbc)


run(app, host="localhost", port=PORT, debug=True)
