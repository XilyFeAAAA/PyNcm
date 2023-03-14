from .event import Event
from plugin import Plugin
from matcher.matcher import Matcher
from matcher.matcherManager import matcherManager

matchers = matcherManager()


def on_api(mode: bool = True,
           disposable: bool = False, 
           priority: int = 1,
           plugin: Plugin = None) -> Matcher:
    return matchers.new(
        type_='apiRun' if mode else 'apiClose',
        disposable=True,
        priority=priority,
        plugin=plugin
    )