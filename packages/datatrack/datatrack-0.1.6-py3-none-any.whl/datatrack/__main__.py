#!/usr/bin/env python

# datatrack: tracks your data transformations.
# Copyright (C) 2024  Roman Kindruk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
Usage:
  dt configure
  dt artifact create --project=PROJECT --name=NAME SOURCE

Arguments:
  SOURCE   a location of the files, can be a local path or S3 URI

Options:
  -p, --project=PROJECT   project name
  -n, --name=NAME         artifact name
  -h, --help              display this help and exit
      --version           output version information and exit
"""

import logging
import sys
from importlib.metadata import version
from pathlib import Path

from docopt import docopt

from .artifact import Artifact
from .config import ConfigNotFound, cache_dir, config, config_path

logging.basicConfig(
    level=logging.getLevelName(logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s -- %(message)s",
)


def dt_configure(args):
    try:
        cfg = config()
    except ConfigNotFound:
        cfg = {}

    print("Configure datatrack")
    cfg_s3 = cfg.get("s3", {})
    cfg_bucket = cfg_s3.get("bucket") or ""
    cfg_prefix = cfg_s3.get("prefix") or ""

    cfg_db = cfg.get("database", {})
    cfg_psql = cfg_db.get("postgresql", {})
    cfg_conn = cfg_psql.get("conninfo", "")

    cfg_cache = cfg.get("cache", cache_dir())

    bucket = input(f"S3 bucket name [{cfg_bucket}]: ")
    prefix = input(f"S3 prefix [{cfg_prefix}]: ")
    conninfo = input(f"DB connection string [{cfg_conn}]: ")
    cachedir = input(f"File cache directory [{cfg_cache}]: ")

    toml = f"""cache = "{cachedir or cfg_cache}"

[s3]
bucket = "{bucket or cfg_bucket}"
prefix = "{prefix or cfg_prefix}"

[database.postgresql]
conninfo = "{conninfo or cfg_conn}"
"""
    cfg_path = config_path()
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg_path, "w") as f:
        f.write(toml)
    print(f"Datatrack setup is completed. The configuration file stored in {cfg_path}")


def dt_artifact_create(args):
    try:
        a = Artifact.create(args["--project"], args["--name"], args["SOURCE"])
    except ConfigNotFound:
        print('No config file found.  Please run "dt configure"', file=sys.stderr)
        sys.exit(-1)
    print(a.id)


def main():
    args = docopt(__doc__, version=version(__package__))
    if args["configure"]:
        dt_configure(args)
    elif args["artifact"] and args["create"]:
        dt_artifact_create(args)


if __name__ == "__main__":
    main()
