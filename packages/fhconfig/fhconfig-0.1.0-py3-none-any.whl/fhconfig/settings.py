"""AppConf - Settings."""

from pathlib import Path
import json
from typing import Any

from fhconfig.validation import validate_key


class SettingsManager():
    """App configuration settings manager."""

    def __init__(self, path: Path):
        """Initialize the instance loading the data from a settings JSON file.

        If the file doesn't exist initially, it will be created, along all its
        intermediate directories, the first time a setting key is added or
        deleted.

        :param path: Relative or absolute path of the settings JSON file. If
        it's a relative path, it's converted to its absolute path.
        """
        self._path = path.absolute()
        self._load()

    def _load(self):
        """Load the data from the settings JSON file."""
        if self._path.exists():
            with open(self._path, encoding='utf-8') as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def _save(self):
        """Save the data to the settings JSON file.

        The file and all its intermediate directories are created if they don't
        exist.
        """
        dir_path = self._path.parent

        if not dir_path.exists():
            dir_path.mkdir()

        with open(self._path, "w", encoding='utf-8') as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    @property
    def path(self) -> str:
        """Return the absolute path of the settings JSON file.

        :return: File path.
        """
        return self._path

    def get_all(self) -> list: # def get_all(self) -> list[str]:
        """Get all the setting keys.
        在python3.8及以下的版本当中，不支持在类型注解时指定容器类型的内含类型，但是这一功能在3.9以上的版本是被支持的

        :return: Keys.
        """
        return list(self._data.keys())

    def contains(self, key: str) -> bool:
        """Return whether a setting exists.

        A `KeyValidationError` exception is raised if the setting key is
        invalid.

        :param key: Setting key. It must contain at least 1 character and must
        contain and only letters, numbers, hyphens or underscores.
        :return: Whether the setting exists.
        """
        validate_key(key)  # This may raise KeyValidationError
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value of a setting.

        A `KeyValidationError` exception is raised if the setting key is
        invalid. If the setting doesn't exist, a default value is returned.

        :param key: Setting key. It must contain at least 1 character and must
        contain and only letters, numbers, hyphens or underscores.
        :param default: Value to return if the setting doesn't exist.
        :return: Setting value or `default`.
        """
        validate_key(key)
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        """Set the value of a setting.

        A `KeyValidationError` exception is raised if the setting key is
        invalid.

        :param key: Setting key. It must contain at least 1 character and must
        contain only letters, numbers, hyphens or underscores.
        :param value: Setting value. It must be serializable to JSON.
        """
        validate_key(key)

        self._data[key] = value
        self._save()

    def delete(self, key: str):
        """Delete a setting.

        A `KeyValidationError` exception is raised if the setting key is
        invalid.

        :param key: Setting key. It must contain at least 1 character and must
        contain only letters, numbers, hyphens or underscores.
        """
        validate_key(key)

        if key in self._data:
            self._data.pop(key)
            self._save()

    def delete_all(self):
        """Delete all the settings."""
        self._data = {}
        self._save()
