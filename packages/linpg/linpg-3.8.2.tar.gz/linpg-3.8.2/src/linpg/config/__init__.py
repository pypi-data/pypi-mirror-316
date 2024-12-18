"""
结构:
base -> setting -> modules
"""

import hashlib
import re
import shutil
from typing import Callable

import json
from glob import glob

from ..abstracts import *
from ..exception import os

# 尝试导入yaml库
_YAML_INITIALIZED: bool = False
try:
    import yaml

    _YAML_INITIALIZED = True
except Exception:
    pass


# 配置文件管理模块
class Config:
    # 支持的配置文件后缀
    __EXTENSIONS_SUPPORTED: Final[tuple[str, ...]] = (".json", ".yml", ".yaml")

    # 获取默认配置文件类型
    @staticmethod
    def get_file_type() -> str:
        return Specification.get_str("ConfigFileType")

    # 加载配置文件
    @staticmethod
    def __load_file(path: str) -> dict:
        # 如果路径不存在
        if not os.path.exists(path):
            EXCEPTION.fatal(f"Cannot find file on path: {path}")
        else:
            # 按照类型加载配置文件
            with open(path, "r", encoding="utf-8") as f:
                # 使用yaml模块加载配置文件
                if path.endswith(".yaml") or path.endswith(".yml"):
                    if _YAML_INITIALIZED is True:
                        _result: Any = yaml.load(f.read(), Loader=yaml.Loader)
                        return dict(_result) if _result is not None else {}
                    else:
                        EXCEPTION.fatal("You cannot load YAML file because yaml is not imported successfully.", 4)
                # 使用json模块加载配置文件
                elif path.endswith(".json") or path.endswith(".linpg.meta"):
                    return dict(json.load(f))
                else:
                    EXCEPTION.fatal("Linpg can only load json and yaml (when pyyaml is installed).")

    # 加载配置文件
    @classmethod
    def load_file(cls, path: str) -> dict:
        return cls.__load_file(path)

    # 尝试加载可能不存在的配置文件，如果不存在则返回一个空字典
    @classmethod
    def try_load_file_if_exists(cls, _path: str, _default: dict = {}) -> dict:
        return cls.__load_file(_path) if os.path.exists(_path) else _default

    # 加载配置文件，并根据key（s）返回对应的数据
    @classmethod
    def load(cls, path: str, *key: str) -> Any:
        return TypeSafeGetter.get_by_keys(cls.__load_file(path), key)

    # 加载内部配置文件
    @classmethod
    def load_internal_file(cls, path: str) -> dict:
        return cls.__load_file(os.path.join(os.path.dirname(__file__), path))

    # 配置文件保存
    @staticmethod
    def save(path: str, data: dict) -> None:
        # 确保用于储存的文件夹存在
        dir_path: str = os.path.dirname(path)
        if len(dir_path) > 0 and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 保存文件
        with open(path, "w", encoding="utf-8") as f:
            if path.endswith(".yaml") or path.endswith(".yml"):
                if _YAML_INITIALIZED is True:
                    yaml.dump(data, f, allow_unicode=True)
                else:
                    EXCEPTION.fatal("You cannot save .yaml file because yaml is not imported successfully. Maybe try to reinstall PyYaml and try again.")
            elif path.endswith(".json") or path.endswith(".linpg.meta"):
                json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
            else:
                EXCEPTION.fatal("Linpg cannot save this kind of config, and can only save json and yaml (if pyyaml is installed).")

    # 整理配置文件（读取了再存）
    @classmethod
    def organize(cls, pathname: str) -> None:
        for configFilePath in glob(pathname):
            cls.save(configFilePath, cls.load_file(configFilePath))

    # 整理内部配置文件
    @classmethod
    def organize_internal(cls) -> None:
        cls.organize(os.path.join(os.path.dirname(__file__), "*.json"))

    # 解决路径冲突
    @classmethod
    def resolve_path(cls, file_location: str) -> str:
        path: str
        for fileType in cls.__EXTENSIONS_SUPPORTED:
            if os.path.exists(path := file_location + fileType):
                return path
        return ""

    # 解决路径冲突并加载
    @classmethod
    def resolve_path_and_load_file(cls, file_location: str) -> dict:
        path: str = cls.resolve_path(file_location)
        return cls.load_file(path) if len(path) > 0 else {}


# 使用引擎的开发者可以自定义的参数
class Specification(TypeSafeGetter):
    __SPECIFICATIONS: Final[dict] = Config.load_internal_file("specifications.json")
    # 尝试加载项目自定义的参数
    __SPECIFICATIONS.update(Config.resolve_path_and_load_file(os.path.join("Data", "specifications")))

    @classmethod
    def _get_data(cls) -> dict:
        return cls.__SPECIFICATIONS

    @classmethod
    def get_directory(cls, category: str, *_sub: str) -> str:
        return str(os.path.join(*cls.__SPECIFICATIONS["Directory"][category], *_sub))


# 数据库
class DataBase(TypeSafeGetter):
    # 用于存放数据库数据的字典
    __DATA_BASE_DICT: Final[dict] = {"Tiles": {}, "Decorations": {}, "Npc": {}}

    @classmethod
    def _get_data(cls) -> dict:
        return cls.__DATA_BASE_DICT

    @classmethod
    def update(cls, _value: dict) -> None:
        for key, value in _value.items():
            if key not in cls.__DATA_BASE_DICT:
                cls.__DATA_BASE_DICT[key] = value
            else:
                cls.__DATA_BASE_DICT[key].update(value)


# 全局数据
class GlobalVariables(TypeSafeGetter, TypeSafeSetter):
    # 用于存放全局数据的字典
    __GLOBAL_VARIABLES_DICT: Final[dict] = {}

    @classmethod
    def _get_data(cls) -> dict:
        return cls.__GLOBAL_VARIABLES_DICT

    # 删除特定的全局数据
    @classmethod
    def remove(cls, _key: str) -> None:
        cls.__GLOBAL_VARIABLES_DICT.pop(_key, None)

    # 如果不是对应的值，则设置为对应的值，返回是否对应
    @classmethod
    def if_get_set(cls, _key: str, valueToGet: object, valueToSet: object) -> bool:
        if cls.__GLOBAL_VARIABLES_DICT[_key] == valueToGet:
            cls.__GLOBAL_VARIABLES_DICT[_key] = valueToSet
            return True
        else:
            return False


# 设置参数管理系统
class Setting(TypeSafeGetter, TypeSafeSetter):
    # 储存设置配置文件的数据
    __SETTING_DATA: Final[dict] = {}
    # 当前配置文件保存路径的参数
    __SETTING_FILE_NAME: Final[str] = Specification.get_directory("setting", "setting." + Config.get_file_type())

    @classmethod
    def _get_data(cls) -> dict:
        return cls.__SETTING_DATA

    # 重新加载设置数据
    @classmethod
    def reload(cls) -> None:
        # 加载内部默认的设置配置文件
        cls.__SETTING_DATA.clear()
        cls.__SETTING_DATA.update(dict(Specification.get("DefaultSetting")))
        cls.__SETTING_DATA["Font"] = Specification.get("DefaultFont")
        # 如果自定义的设置配置文件存在，则加载
        if os.path.exists(cls.__SETTING_FILE_NAME):
            cls.__SETTING_DATA.update(Config.load_file(cls.__SETTING_FILE_NAME))
        # 如果不存在自定义的设置配置文件,则读取默认
        else:
            # 导入local,查看默认语言
            import locale

            # 默认语言为英文， 但如果用户系统环境语言是中文
            if locale.getdefaultlocale()[0] == "zh_CN":
                cls.__SETTING_DATA["Language"] = "SimplifiedChinese"
            elif locale.getdefaultlocale()[0] in ("zh_TW", "zh_HK"):
                cls.__SETTING_DATA["Language"] = "TraditionalChinese"

    # 保存设置数据
    @classmethod
    def save(cls) -> None:
        Config.save(cls.__SETTING_FILE_NAME, cls.__SETTING_DATA)

    """其他常用的重要参数"""

    # 文字名称
    @classmethod
    def get_font(cls) -> str:
        return str(cls.__SETTING_DATA["Font"]["font"])

    # 设置文字名称
    @classmethod
    def set_font(cls, font_name: str) -> None:
        cls.__SETTING_DATA["Font"]["font"] = font_name

    # 文字类型
    @classmethod
    def get_font_type(cls) -> str:
        return str(cls.__SETTING_DATA["Font"]["type"])

    # 设置文字类型
    @classmethod
    def set_font_type(cls, font_type: str) -> None:
        cls.__SETTING_DATA["Font"]["type"] = font_type

    # 抗锯齿参数
    @classmethod
    def get_antialias(cls) -> bool:
        return bool(cls.__SETTING_DATA["AntiAlias"])

    # 语言
    @classmethod
    def get_language(cls) -> str:
        return str(cls.__SETTING_DATA["Language"])

    # 低内存模式
    @classmethod
    def get_low_memory_mode(cls) -> bool:
        return bool(cls.__SETTING_DATA["LowMemoryMode"])


# 初始化
Setting.reload()


# debug模块
class Debug:
    # 是否开启开发者模式
    __ENABLE_DEVELOPER_MODE: bool = False
    # 是否开启作弊
    __ENABLE_CHEATING: bool = False
    # 是否展示Fps
    __SHOW_FPS: bool = False

    # 开发者模式
    @classmethod
    def get_developer_mode(cls) -> bool:
        return cls.__ENABLE_DEVELOPER_MODE

    @classmethod
    def set_developer_mode(cls, value: bool) -> None:
        cls.__ENABLE_DEVELOPER_MODE = value

    # 作弊模式
    @classmethod
    def get_cheat_mode(cls) -> bool:
        return cls.__ENABLE_CHEATING

    @classmethod
    def set_cheat_mode(cls, value: bool) -> None:
        cls.__ENABLE_CHEATING = value

    # 展示Fps
    @classmethod
    def get_show_fps(cls) -> bool:
        return cls.__SHOW_FPS

    @classmethod
    def set_show_fps(cls, value: bool) -> None:
        cls.__SHOW_FPS = value


# 版本信息管理模块
class Info:
    # 引擎主版本号
    __VERSION: Final[int] = 3
    # 引擎次更新版本号
    __REVISION: Final[int] = 8
    # 引擎补丁版本
    __PATCH: Final[int] = 1

    # 确保linpg版本
    @classmethod
    def ensure_linpg_version(cls, action: str, revision: int, patch: int, version: int = 3) -> bool:
        if action == "==":
            return cls.__VERSION == version and cls.__REVISION == revision and cls.__PATCH == patch
        elif action == ">=":
            return cls.__VERSION >= version and cls.__REVISION >= revision and cls.__PATCH >= patch
        elif action == "<=":
            return cls.__VERSION <= version and cls.__REVISION <= revision and cls.__PATCH <= patch
        else:
            EXCEPTION.fatal(f'Action "{action}" is not supported!')

    # 获取当前版本号
    @classmethod
    def get_current_version(cls) -> str:
        return f"{cls.__VERSION}.{cls.__REVISION}.{cls.__PATCH}"

    # 获取github项目地址
    @classmethod
    def get_repository_url(cls) -> str:
        return "https://github.com/LinpgFoundation/linpg"


class Files:
    # 一个简单的 natural sort 实现
    @staticmethod
    def natural_sort(_files: list[str]) -> list[str]:
        convert: Callable[[str], int | str] = lambda text: int(text) if text.isdigit() else text.lower()
        _key: Callable[[str], list[int | str]] = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
        return sorted(sorted(_files), key=_key)

    # 删除特定patten的文件夹
    @classmethod
    def search_and_remove_folder(cls, folder_to_search: str, stuff_to_remove: str) -> None:
        # 确保folder_to_search是一个目录
        if not os.path.isdir(folder_to_search):
            raise NotADirectoryError("You can only search a folder!")
        # 移除当前文件夹符合条件的目录/文件
        for path in glob(os.path.join(folder_to_search, "*")):
            if path.endswith(stuff_to_remove):
                shutil.rmtree(path)
            elif os.path.isdir(path):
                cls.search_and_remove_folder(path, stuff_to_remove)

    # 根据地址删除文件夹
    @staticmethod
    def delete_if_exist(path: str) -> None:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    # 为一个文件生成hash值
    @staticmethod
    def hash(path: str) -> str:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return hashlib.new(Specification.get_str("HashingAlgorithm"), f.read()).hexdigest()
        else:
            EXCEPTION.fatal(f"Cannot generate {Specification.get_str('HashingAlgorithm')} for a file that does not exist in path: {path}")


class Cache:
    # 缓存文件夹路径
    __CACHE_FOLDER: Final[str] = Specification.get_directory("cache")
    # 缓存文件清单路径
    __CACHE_FILES_DATA_PATH: Final[str] = os.path.join(__CACHE_FOLDER, f"files.{Config.get_file_type()}")
    # 如果缓存文件目录存在, 则加载数据， 否则初始化一个新的空字典
    __CACHE_FILES_DATA: Final[dict[str, dict]] = Config.try_load_file_if_exists(__CACHE_FILES_DATA_PATH)

    # 获取缓存文件夹路径
    @classmethod
    def get_directory(cls) -> str:
        # 如果缓存文件夹不存在， 则创建缓存文件夹
        if not os.path.exists(cls.__CACHE_FOLDER):
            os.mkdir(cls.__CACHE_FOLDER)
        # 返回文件夹路径
        return cls.__CACHE_FOLDER

    # 新建一个对比关系
    @classmethod
    def new(cls, _key: str, source_file_path: str, target_file_path: str) -> None:
        if _key not in cls.__CACHE_FILES_DATA:
            cls.__CACHE_FILES_DATA[_key] = {
                "source": {"path": source_file_path, Specification.get_str("HashingAlgorithm"): Files.hash(source_file_path)},
                "target": {"path": target_file_path, Specification.get_str("HashingAlgorithm"): Files.hash(target_file_path)},
                "version": Info.get_current_version(),
            }
            # 保存缓存文件的相关数据
            Config.save(cls.__CACHE_FILES_DATA_PATH, cls.__CACHE_FILES_DATA)
        else:
            EXCEPTION.fatal(f'The key named "{_key}" already exists. Please create a new unique one!')

    # 移除
    @classmethod
    def remove(cls, _key: str) -> None:
        Files.delete_if_exist(cls.__CACHE_FILES_DATA[_key]["target"]["path"])
        del cls.__CACHE_FILES_DATA[_key]
        Config.save(cls.__CACHE_FILES_DATA_PATH, cls.__CACHE_FILES_DATA)

    @classmethod
    def get_cache_path(cls, _key: str) -> str:
        return str(cls.__CACHE_FILES_DATA[_key]["target"]["path"])

    # 对比数据
    @classmethod
    def match(cls, _key: str, source_file_path: str) -> bool:
        cache_info: dict | None = cls.__CACHE_FILES_DATA.get(_key)
        if cache_info is not None:
            if (
                Info.get_current_version() == cache_info["version"]
                and os.path.exists(source_file_path)
                and source_file_path == cache_info["source"]["path"]
                and Files.hash(source_file_path) == cache_info["source"].get(Specification.get_str("HashingAlgorithm"))
                and os.path.exists(cache_info["target"]["path"])
                and Files.hash(cache_info["target"]["path"]) == cache_info["target"].get(Specification.get_str("HashingAlgorithm"))
            ):
                return True
            else:
                cls.remove(_key)
        return False
