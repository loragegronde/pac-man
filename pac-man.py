from src.parsing import Parsing, Config
import argparse
from pathlib import Path
from pydantic import ValidationError

class Main:
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        _ = self.parser.add_argument("filename", type=str)
        self.args: argparse.Namespace = self.parser.parse_args()
        self.filepath: Path = Path(self.args.filename).absolute()
        self.config: Config = Parsing(self.filepath).parse()
        print(self.config)

if __name__ == "__main__":
    try:
        Main()
    except ValidationError as e:
      print("\n".join(error['msg'] for error in e.errors()))
    except Exception as e:
        print(e)
        exit(1)