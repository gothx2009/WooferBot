##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for streamers
#    Copyright (C) 2019  Tomaae
#    (https://wooferbot.com/)
#
#    This file is part of WooferBot.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
##########################################################################

from sys import exit
from os import path
from signal import signal, SIGINT, SIGTERM, SIGBREAK
from lib.settings import Settings
from lib.overlay import Overlay
from lib.woofer import Woofer
from lib.twitch import Twitch
from lib.filewatchdog import Watchdog
from lib.cli import Cli
from lib.nanoleaf import Nanoleaf
from lib.hue import Hue
from lib.miyeelight import Yeelight


# ---------------------------
#  exit_gracefully
# ---------------------------
def exit_gracefully(signum=None, frame=None):
    print("Closing WooferBot...")
    overlay.stop()
    exit(0)


# ---------------------------
#  Main
# ---------------------------
wooferbotVersion = 'v1.3.2'
print('WooferBot ' + wooferbotVersion + '  Copyright (C) 2019  Tomaae')
print('This program comes with ABSOLUTELY NO WARRANTY.')
print('This is free software, and you are welcome to redistribute it')
print('under certain conditions.')
print('By using this program, you accept the terms of the software license agreement.')
print('')

signal(SIGINT, exit_gracefully)
signal(SIGTERM, exit_gracefully)
signal(SIGBREAK, exit_gracefully)

# Initialize settings
path_root = path.dirname(path.realpath(__file__))
settings = Settings(path_root=path_root)

# Initialize nanoleaf
nanoleaf = Nanoleaf(settings=settings)

# Initialize Philips HUE
hue = Hue(settings=settings)

# Initialize Philips HUE
yeelight = Yeelight(settings=settings)

settings.save()

# Initialize twitch chatbot
chatbot = Twitch(settings=settings, woofer=None, bot=True)
if settings.UseChatbot and len(settings.TwitchBotChannel) > 0 and settings.TwitchBotOAUTH.find('oauth:') == 0:
    chatbot.connect()

# Initialize overlay
overlay = Overlay(settings=settings, nanoleaf=nanoleaf, hue=hue, yeelight=yeelight, chatbot=chatbot)
overlay.start()

# Initialize woofer
woofer = Woofer(settings=settings, overlay=overlay, nanoleaf=nanoleaf, hue=hue, yeelight=yeelight, chatbot=chatbot)

# Initialize twitch
twitch = Twitch(settings=settings, woofer=woofer)
twitch.connect()
if settings.UseChatbot and len(settings.TwitchBotChannel) < 1 and settings.TwitchBotOAUTH.find('oauth:') != 0:
    chatbot.link_account(twitch)

# Start Watchdog
watchdog = Watchdog(settings=settings, woofer=woofer)

# Start CLI
cli = Cli(settings=settings, woofer=woofer, twitch=twitch, chatbot=chatbot)
cli.start()

# Cleanup and exit
exit_gracefully()
exit(0)
