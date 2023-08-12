import requests
from sqlalchemy.orm import Session
from osintbuddy import load_plugin, Registry

from app import crud, schemas
from app.core.logger import get_logger
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
from .base import *  # noqa

logger = get_logger(name=__name__)

core_ob_url = 'https://raw.githubusercontent.com/jerlendds/osintbuddy-core-plugins/main/plugins/'
core_plugins = {
    'CSE Result': 'cse_result',
    'CSE Search': 'cse_search',
    'DNS': 'dns',
    'Google Cache Result': 'google_cache_result',
    'Google Cache Search': 'google_cache_search',
    'Google Result': 'google_result',
    'Google Search': 'google_search',
    'IP': 'ip',
    'IP Geolocation': 'ip_geo',
    'Subdomain': 'subdomain',
    'Telegram Websearch': 'telegram_websearch',
    'URL': 'url',
    'Username': 'username',
    'Username Profile': 'username_profile',
    'Website': 'website',
    'Whois': 'whois'
}


def load_initial_plugin(db, plugin_mod, plugin_code):
    load_plugin(plugin_mod, plugin_code)

    plugin = Registry.get_plug(plugin_mod)
    obj_in = schemas.EntityCreate(
        label=plugin.label,
        author=plugin.author,
        description=plugin.description,
        source=plugin_code
    )
    crud.entities.create(db=db, obj_in=obj_in)

def init_db(db: Session) -> None:

    entities = crud.entities.count_all(db)
    entity_count = entities[0][0]
    if entity_count < 14:
        for plugin_label, plugin_mod in core_plugins.items():
            logger.info(f'Loading core plugins: {plugin_label}')
            try:
                resp = requests.get(core_ob_url + plugin_mod + '.py')
                load_initial_plugin(db=db, plugin_mod=plugin_mod, plugin_code=resp.text)
            except requests.exceptions.ConnectionError:
                resp = requests.get(core_ob_url + plugin_mod + '.py')
                load_initial_plugin(db=db, plugin_mod=plugin_mod, plugin_code=resp.text)
            except Exception:
                pass

    return {
        "status": "success",
        "service": "[Entities: Create]",
        "message": f"{len(Registry.plugins)} initial entities (plugins) loaded",
    }
