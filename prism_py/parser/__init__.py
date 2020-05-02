import prism_py.parser.grammar as PRISM
from arpeggio import ParserPython, NoMatch, ParseTreeNode
import argparse
import logging

from typing import Union
from pathlib import Path

log = logging.getLogger(__name__)

PathLike = Union[str, Path]


def parse_file(input_file: PathLike) -> ParseTreeNode:
    in_file = Path(input_file).absolute()
    parser = ParserPython(PRISM.ModelRoot, PRISM.comment)
    with in_file.open() as infile:
        return parser.parse(infile.read(), file_name=in_file.name)


def parse(input_str: str) -> ParseTreeNode:
    parser = ParserPython(PRISM.ModelRoot, PRISM.comment)
    return parser.parse(input_str)
