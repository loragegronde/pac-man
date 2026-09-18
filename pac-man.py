from src.parsing import Parsing, Config
import argparse
from pathlib import Path
from mazegenerator import MazeGenerator
from src.graphics import Graphics


class Main:
    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        _ = self.parser.add_argument("filename", type=str)
        self.args: argparse.Namespace = self.parser.parse_args()
        print(self.args.filename)
        self.filepath: Path = Path(self.args.filename).absolute()
        self.config: Config = Parsing(self.filepath).parse()
        self.graphics: Graphics = Graphics(1900, 1200)
        self.graphics.run()


if __name__ == "__main__":
    try:
        main = Main()
    except FileNotFoundError:
        print("config file not found")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)
