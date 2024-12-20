import re

from airfold_common.error import AirfoldError
from airfold_common.utils import is_uuid


class FormatError(AirfoldError):
    pass


class Format:
    def __init__(self) -> None:
        self.AIRFOLD_CORE: str = "core.airfold.co"
        self.DEFAULT_VERSION: str = f"{self.AIRFOLD_CORE}/v1"
        self.SUPPORTED_VERSIONS: list[str] = [f"{self.AIRFOLD_CORE}/v1"]
        self.SOURCE_TYPES: list[str] = ["Table"]
        self.IMPORTABLE_TYPES: list[str] = ["Table"]
        self.PIPE_TYPES: list[str] = ["Pipe"]
        self.SPEC_TYPES: list[str] = ["Spec"]
        self.GROUP_TYPES: list[str] = ["PipeGroup"]

    def _get_core_version(self) -> str:
        return self.DEFAULT_VERSION.split("/", 1)[0]

    @property
    def SUPPORTED_TYPES(self) -> list[str]:
        return self.SOURCE_TYPES + self.PIPE_TYPES + self.SPEC_TYPES + self.GROUP_TYPES

    def normalize(self, data: dict, name: str) -> dict:
        data["version"] = self.normalize_version(data)
        data["type"] = self.normalize_type(data)
        data["name"] = self.normalize_name(data, name)
        if data.get("using"):
            data["using"] = self.normalize_using(data)
        return data

    def normalize_version(self, data: dict) -> str:
        ver: str | None = data.get("version")
        if ver is None or ver == "":
            ver = self.DEFAULT_VERSION
        assert ver
        res = ver.split("/", 1)
        if len(res) == 1:
            res.insert(0, self._get_core_version())
        elif len(res) > 2:
            raise FormatError(f"Error parsing version: {ver}")
        norm_ver = "/".join(res)
        if norm_ver not in self.SUPPORTED_VERSIONS:
            raise FormatError(f"Unknown or not supported version: {norm_ver}")
        return norm_ver

    def guess_type(self, data: dict) -> str:
        data_type: str = ""
        if "spec" in data:
            data_type = "Spec"
        elif "cols" in data or "sql" in data:
            data_type = "Table"
        elif "nodes" in data:
            data_type = "Pipe"
        elif "pipes" in data:
            data_type = "PipeGroup"
        if not data_type:
            raise FormatError("Type is not set, and failed to guess it")
        return data_type

    def normalize_type(self, data: dict) -> str:
        data_type: str | None = data.get("type")
        if data_type is None or data_type == "":
            data_type = self.guess_type(data)
        if data_type not in self.SUPPORTED_TYPES:
            raise FormatError(f"Unknown or not supported type definition: {data_type}")
        return data_type

    def normalize_name(self, data: dict, name: str) -> str:
        norm_name = data.get("name", name)
        if not norm_name or is_uuid(norm_name):
            raise FormatError(f"Object name is invalid: '{norm_name}'")
        return norm_name

    def normalize_using(self, data: dict) -> dict:
        if not self.is_importable(data):
            raise FormatError(f"Object is not importable. Allowed types: {self.IMPORTABLE_TYPES}")
        using = data["using"]
        if not using.get("table"):
            raise FormatError(f"Imported table name is not set in 'using' section")
        if not using.get("database"):
            raise FormatError(f"Imported table database is not set in 'using' section")

        return using

    def is_source(self, data: dict) -> bool:
        return data["type"] in self.SOURCE_TYPES

    def is_pipe(self, data: dict) -> bool:
        return data["type"] in self.PIPE_TYPES

    def is_importable(self, data: dict) -> bool:
        return data["type"] in self.IMPORTABLE_TYPES

    def is_foreign_source(self, data: dict) -> bool:
        return self.is_source(data) and data.get("using") is not None

    def is_spec(self, data: dict) -> bool:
        return data["type"] in self.SPEC_TYPES

    def is_group(self, data: dict) -> bool:
        return data["type"] in self.GROUP_TYPES

    def get_version(self, data: dict) -> str:
        return data.get("version", self.normalize_version(data))

    def get_type(self, data: dict) -> str:
        return data.get("type", self.normalize_type(data))


class ChFormat(Format):
    SUPPORTED_NAME_RE = re.compile(r"[a-zA-Z_]\w*")

    def __init__(self):
        super().__init__()
        self.DEFAULT_VERSION = "clickhouse.airfold.co/v1"
        self.SUPPORTED_VERSIONS += ["clickhouse.airfold.co/v1"]
        self.SOURCE_TYPES += ["Dictionary"]

    def normalize_name(self, data: dict, name: str) -> str:
        name = super().normalize_name(data, name)
        if not name or not self.SUPPORTED_NAME_RE.fullmatch(name):
            raise FormatError(f"Object name is invalid: '{name}'")
        return name

    def normalize_using(self, data: dict) -> dict:
        if not self.is_importable(data):
            raise FormatError(f"Object is not importable. Allowed types: {self.IMPORTABLE_TYPES}")

        using = data["using"].copy()
        if not using.get("table"):
            raise FormatError(f"Imported table name is not set in 'using' section")

        if not using.get("database"):
            using["database"] = "default"

        return using


class AIFormat(ChFormat):
    def __init__(self):
        super().__init__()
        self.SOURCE_TYPES += ["AITable", "S3Table", "SnowflakeTable"]
        self.SPEC_TYPES += ["AISpec"]

    def guess_type(self, data: dict) -> str:
        data_type: str = ""
        if "cols" in data and "ai_cols" in data:
            data_type = "AITable"
        elif "cols" in data and "s3" in data:
            data_type = "S3Table"
        elif "cols" in data and "snowflake" in data:
            data_type = "SnowflakeTable"
        if data_type:
            return data_type
        return super().guess_type(data)
