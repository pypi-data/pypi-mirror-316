import argparse
import sys

from dataclasses import dataclass, field

from neurosymbolic.bashtool import BashTool
from neurosymbolic.z3tool import Z3Tool
from langchain_community.tools import ReadFileTool, WriteFileTool

from .blocks import compute


def main():
    """Simple neurosymbolic solver with bash/z3/read/write file capabilities."""
    parser = argparse.ArgumentParser(description="Neurosymbolic solver")
    parser.add_argument("goal", help="Goal for the neurosymbolic solver")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    user_input = args.goal
    verbose = args.verbose
    debug = args.debug

    toolbox = [
        BashTool(verbose=verbose),
        Z3Tool(verbose=verbose),
        ReadFileTool(verbose=verbose),
        WriteFileTool(verbose=verbose)
    ]
    result, messages = compute(prompt=user_input, toolbox=toolbox) #, schema=Secret)
    if debug:
        for message in messages:
            print(message)
    print(result.result)


__all__ = ["main"]
