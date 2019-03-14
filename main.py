import argparse
import bot
import json
import os
import asyncio
import subprocess
import sys

actions = {}


def action(func):
    actions[func.__name__] = func


@action
def run(config):
    useful = bot.Useful(config, ("a!", "<@373252109753384960> "))
    useful.before_invoke(bot._check)
    useful.after_invoke(bot._closing)
    for i in os.listdir("features"):
        if i != "__pycache__":
            useful.load_extension("features." + (i if not i.endswith(".py") else i[:-3]))
    try:
        useful.run(config["token"])
    finally:
        useful.db._loop = asyncio.new_event_loop()
        useful.db._loop.run_until_complete(useful.db.commit())
        useful.db._loop.run_until_complete(useful.db.__aexit__(None, None, None))


@action
def update(config):
    proc = subprocess.Popen("git pull".split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    proc.wait()
    if not proc.returncode:
        sys.stdout.write("update successful\n")
    else:
        sys.stderr.write("error: update failed\n")
        sys.exit(1)




if __name__ == '__main__':
    argp = argparse.ArgumentParser("amadeus")
    argp.add_argument("--config", type=argparse.FileType("r"), default="config.json", dest="f")
    argp.add_argument("--database", type=argparse.FileType("r"), default="amadeus.db", dest="db")
    argp.add_argument("action", type=str, dest="action")
    conf = argp.parse_args()
    dbf = conf.db.name
    conf.db.close()
    with conf.f as f:
        config = json.load(f)
    config["invoke"] = conf
    if conf.action not in actions:
        sys.stderr.write(f"error: unknown action: {conf.action}\n")
        sys.exit(1)
    actions[conf.action](config)
