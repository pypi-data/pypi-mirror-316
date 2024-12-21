from __future__ import annotations
import logging
from labthings_fastapi.thing_server import ThingServer
from . import SangaboardThing


logging.basicConfig(level=logging.INFO)

thing_server = ThingServer()
my_thing = SangaboardThing()
my_thing.validate_thing_description()
thing_server.add_thing(my_thing, "/stage")

app = thing_server.app