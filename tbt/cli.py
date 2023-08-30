import logging
import os
import sys

import click
from click import group, option

from tbt.definitions.definition_parser import DefinitionsParser
from tbt.runner import Runner
from tbt.utils import log_details

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
LOGLEVEL = logging.getLevelName(LOGLEVEL)
if LOGLEVEL > logging.DEBUG:
    sys.tracebacklimit = 0
logging.basicConfig(
    level=LOGLEVEL,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s | %(message)s",
)


@group()
def main():
    """tbt - nlp pipeline builder"""
    pass


@main.command()
@option(
    "--dir",
    "-d",
    "root_dir",
    default=os.getcwd(),
    help="directory containing tbt*.yaml files",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
)
@log_details
def prep(root_dir: str):
    """Validate tbt definitions and run pre_steps"""
    dp = DefinitionsParser(root_dir)
    dp.parse()
    runner = Runner(dp.pipelines)
    runner.prep()


@main.command()
@option(
    "--dir",
    "-d",
    "root_dir",
    default=os.getcwd(),
    help="directory containing tbt*.yaml files",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
)
@option(
    "--select",
    "-s",
    "select",
    help="specify a single pipeline to run, will run all if not specified",
    type=str,
)
@log_details
def run(root_dir: str, select: str):
    """Run steps in pipelines"""
    dp = DefinitionsParser(root_dir)
    dp.parse()
    if select and select in dp.pipelines:
        dp.pipelines = {select: dp.pipelines[select]}
    runner = Runner(dp.pipelines)
    runner.run()


if __name__ == "__main__":
    main()
