#!/usr/bin/env python3
#
# Copyright 2022
#
# cogplause is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# cogplause is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.  You should have received a
# copy of the GNU General Public License along with
# cogplause.  If not, see <http://www.gnu.org/licenses/>.
#
import json
import os
import re
import signal
import socket
import subprocess
import sys

__license__ = 'GPL'
__version__ = '0.0.1-dev'

from loguru import logger
import clingo

from utils import handler

logger.remove()
logger.add(sys.stderr, level="WARNING")

# SETUP SIGNAL HANDLING
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

encoding = "encoding1.lp"

solutions = {}


def add_solution_to_list(model: clingo.Model, q):
    if not q in solutions:
        solutions[q] = []
    res = str(model).split()
    solutions[q].append(res)


expr = r"\s*query\((?P<name>\w+|\w+\(\w+\))\)."
rexp = re.compile(expr)


def run_clingo(prog):
    atom = None
    with open(prog, 'r') as f:
        for line in f.readlines():
            if line.strip().startswith("query("):
                m = rexp.match(line)
                if m:
                    atom = m.group(1)
                    logger.info(f"Query atom is '{atom}'.")
    if atom is None:
        raise RuntimeError("Program needs to specify query atom via a simple fact using 'query(atom).'")

    with open("query.lp", 'r') as f:
        query = f.read().format(atom=atom)

    # ctl = Control(arguments=[f"--models=0"])
    logger.info(f"Solving Program {prog} without assumption.")
    ctl = clingo.Control(['--warn=no-atom-undefined', '-n0'])
    ctl.load(encoding)
    ctl.load(prog)
    ctl.ground([("base", [])])
    res = ctl.solve(on_model=lambda x: add_solution_to_list(x, "denom"))
    num_denom = 1
    if res.satisfiable:
        num_denom = len(solutions['denom'])

    logger.info(f"Solving Program {prog} with assumption.")
    logger.info(f"Query was {query}")
    ctl = clingo.Control(['--warn=no-atom-undefined', '-n0'])
    ctl.load(encoding)
    ctl.load(prog)
    ctl.add("base", [], query)
    ctl.ground([("base", [])])
    res=ctl.solve(on_model=lambda x: add_solution_to_list(x, "nom"))
    num_nom = 0
    if res.satisfiable:
        num_nom = len(solutions['nom'])

    with open(f"{prog}_models", 'w') as f:
        f.write(f"% Plausibility of {atom} being true is:\n")
        f.write(f"plaus({atom}) = {num_nom/num_denom}\n")

        f.write("% SOLUTIONS WITHOUT QUERY\n")
        f.write(f"num_denom={num_denom}\n")
        for sol in solutions['denom']:
            out = " ".join(sol)
            f.write(f"{out}\n")

        f.write("% SOLUTIONS WITH QUERY\n")
        f.write(f"% QUERY WAS: {query}\n")
        f.write(f"num_nom={num_nom}\n")
        if num_nom != 0:
            for sol in solutions['nom']:
                out = " ".join(sol)
                f.write(f"{out}\n")

    # query
    # {:- not concl}

    # prg.solve()


def main(fname):
    version = subprocess.check_output(["git", "describe", "--always"]).strip().decode('utf-8')
    run_clingo(fname)

    # output = {'hostname': socket.gethostname(),  # 'seed': seed,
    #           'version': version, 'instance_path': fname,
    #           'instance': os.path.basename(fname), 'sha256_instance': sha256_checksum(fname)}
    # logger.remove()
    # logger.add(sys.stderr, level="WARNING")

    # ld = LocalDeterioration(filename=fname, output=output_path, sample_cls=sample_cls, sample_cls_vars=sample_cls_vars)
    # ld.deter(max_rounds=20000, solver_clz=solver)

    # sys.stdout.write(json.dumps(output, sort_keys=True))
    # sys.stdout.write('\n')
    sys.stdout.flush()
    exit(0)


if __name__ == "__main__":
    fname = sys.argv[1]
    main(fname=fname)
