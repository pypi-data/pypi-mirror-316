from typing import Any

from ruamel.yaml import YAML


class YAMLManager:
    def __init__(self, path: str) -> None:
        self.__file: YAML = YAML()
        self.__path: str = path
        self.__data: Any = None
        self.__configure()
        self.__load()

    @property
    def data(self) -> Any:
        return self.__data

    @data.setter
    def data(self, value: dict) -> None:
        self.__data = value

    def __configure(self) -> None:
        self.__file.indent(sequence=4)
        self.__file.preserve_quotes = True

    def __load(self) -> None:
        with open(self.__path, encoding="utf-8") as f:
            self.__data = self.__file.load(f.read())

    def dump(self) -> None:
        with open(self.__path, "w", encoding="utf-8") as f:
            self.__file.dump(self.data, f)
