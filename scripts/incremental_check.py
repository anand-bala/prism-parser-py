import prism_py.parser.grammar as PRISM
from arpeggio import ParserPython, NoMatch
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Check if a PRISM file is valid")
    parser.add_argument("input_file", help="Input file to parse", type=lambda d: Path(d).absolute())

    return parser.parse_args()

def main():
    args = parse_args()
    input_file = args.input_file

    parser = ParserPython(PRISM.ModelRoot, PRISM.comment, debug=True, reduce_tree=True)

    with input_file.open() as infile:
        try:
            parse_tree = parser.parse(infile.read(), file_name=input_file.name)
        except NoMatch as e:
            line, col = e.line, e.col
            logger.error(f"Parsing failed at ({line},{col})")
            return 1

if __name__ == "__main__":
    main()

