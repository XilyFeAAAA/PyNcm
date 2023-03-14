from .event import Event
from plugin import Plugin
from matcher.matcher import Matcher
from matcher.matcherManager import matcherManager

matchers = matcherManager()


def on_api(mode: bool = True,
           disposable: bool = False, 
           plugin: Plugin = None) -> Matcher:
    return matchers.new(
        type_='apiRun' if mode else 'apiClose',
        disposable=disposable,
        plugin=plugin
    )


def on_app(mode: bool = True,
           disposable: bool = False, 
           plugin: Plugin = None) -> Matcher:
    return matchers.new(
        type_='boot' if mode else 'shut',
        disposable=disposable,
        plugin=plugin
    )
