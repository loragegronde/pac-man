import argparse
import sys
from pathlib import Path
from src.graphics import Graphics
from src.parsing.parsing import Config, Parsing


class Main:
    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        _ = self.parser.add_argument("filename", type=str)
        self.args: argparse.Namespace = self.parser.parse_args()
        self.filepath: Path = Path(self.args.filename).expanduser().resolve()
        if not self.filepath.is_file():
            print(f"config file not found: {self.filepath}")
            sys.exit(1)
        self.config: Config = Parsing(self.filepath).parse()
        self.graphics: Graphics = Graphics(1900, 1200, self.config)
        self.graphics.run()


if __name__ == "__main__":
    try:
        main = Main()
    except Exception:
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
