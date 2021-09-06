# Copyright (C) 2021-2022 Team Repondeur.
#
# Licensed under the Team Repondeur Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

import sys
from importlib import import_module
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from .modules import *
from userbot import LOGS, bot


INVALID_PH = (
    "\nError: Invalid phone number."
    "\nTip: Prefix number with country code"
    "\nor check your phone number and try again."
)

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)


for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

amanpro = suc_msg = """
            ----------------------------------------------------------------------
                Repondeur has been deployed! Visit @Reponduer for updates!!
            ----------------------------------------------------------------------
"""
LOGS.info(amanpro)
bot.run_until_disconnected()
