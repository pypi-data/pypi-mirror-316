"""
结构:
coordinates -> wrapper -> images -> controller -> display -> timer -> videos -> mixer -> font -> saves
"""

from dataclasses import dataclass

import threading
from datetime import datetime

import io
import zipfile

import enum
from random import randint as RANDINT

# 粘贴板内容模块
from tkinter import Tk

# 导入pygame组件
import pygame
import pygame.gfxdraw

# 加载颜色模块
from PIL import Image as PILImage
from PIL import ImageColor as PILImageColor
from PIL import ImageFilter as PILImageFilter

import numpy

from .language import *

# 原点
ORIGIN: Final[tuple[int, int]] = (0, 0)
# int_f指参数推荐输入int, 但一开始接受时可以为float，但最后会转换为int
int_f = int | float
# number，即数字，建议int但接受float
number = int | float


# 浮点坐标
class Positions:
    # 转换坐标
    @staticmethod
    def convert(pos: Any) -> tuple[number, number]:
        # 检测坐标
        if isinstance(pos, dict):
            return pos["x"], pos["y"]
        elif isinstance(pos, (Sequence, numpy.ndarray)):
            return pos[0], pos[1]
        else:
            try:
                return pos.x, pos.y
            except Exception:
                EXCEPTION.fatal(f'Unable to convert position "{pos}".')

    # 判断2个坐标是否相同
    @staticmethod
    def is_same(pos1: object, pos2: object) -> bool:
        return Positions.convert(pos1) == Positions.convert(pos2)

    # 相加2个坐标
    @staticmethod
    def add(*positions: tuple[number, number]) -> tuple[number, number]:
        x: number = 0
        y: number = 0
        for pos in positions:
            x += pos[0]
            y += pos[1]
        return x, y

    # 相减2个坐标
    @staticmethod
    def subtract(position: tuple[number, number], *positions: tuple[number, number]) -> tuple[number, number]:
        x: number = position[0]
        y: number = position[1]
        for pos in positions:
            x -= pos[0]
            y -= pos[1]
        return x, y


# 整数坐标
class Coordinates:
    # 转换坐标
    @staticmethod
    def convert(pos: Any) -> tuple[int, int]:
        # 检测坐标
        if isinstance(pos, dict):
            return int(pos["x"]), int(pos["y"])
        elif isinstance(pos, (Sequence, numpy.ndarray)):
            return int(pos[0]), int(pos[1])
        else:
            try:
                return int(pos.x), int(pos.y)
            except Exception:
                EXCEPTION.fatal(f'Unable to convert position "{pos}".')

    # 判断2个坐标是否相同
    @staticmethod
    def is_same(pos1: object, pos2: object) -> bool:
        return Coordinates.convert(pos1) == Coordinates.convert(pos2)

    # 相加2个坐标
    @staticmethod
    def add(*positions: tuple[number, number]) -> tuple[int, int]:
        x: number = 0
        y: number = 0
        for pos in positions:
            x += pos[0]
            y += pos[1]
        return int(x), int(y)

    # 相减2个坐标
    @staticmethod
    def subtract(position: tuple[number, number], *positions: tuple[number, number]) -> tuple[int, int]:
        x: number = position[0]
        y: number = position[1]
        for pos in positions:
            x -= pos[0]
            y -= pos[1]
        return int(x), int(y)

    @staticmethod
    def get_in_diamond_shaped(_x: int, _y: int, _radius: int) -> list[tuple[int, int]]:
        if _radius == 1:
            return [(_x, _y)]
        elif _radius > 1:
            return [(x, y) for y in range(_y - _radius + 1, _y + _radius) for x in range(_x - _radius + abs(y - _y) + 1, _x + _radius - abs(y - _y))]
        return []

# 初始化pygame
pygame.init()

"""linpg自带属性"""
# 颜色类
color_liked = Sequence[int] | str
# 图形类
ImageSurface = pygame.Surface
# path or pygame.Surface
PoI = str | pygame.Surface
# 事件 type alias
PG_Event = pygame.event.Event


# 图形类
class UniversalImageSurface:
    def __init__(self, obj: pygame.Surface, file_path: str = "") -> None:
        self._wrapped_obj: pygame.Surface = obj
        self.__path: Final[str] = file_path

    def __getattr__(self, attr: str) -> Any:
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._wrapped_obj, attr)

    @property
    def path(self) -> str:
        return self.__path


# 图像库数据
class GraphicLibrary:
    PYGAME: Final[int] = 0
    PYGAME_CE: Final[int] = 1

    # 是否正在使用pygame_ce
    __IS_CE: Final[bool] = getattr(pygame, "IS_CE", False) is not False

    @classmethod
    def is_using_pygame(cls) -> bool:
        return not cls.__IS_CE

    @classmethod
    def is_using_pygame_ce(cls) -> bool:
        return cls.__IS_CE

    @classmethod
    def get_name(cls) -> str:
        return "Pygame-ce" if cls.__IS_CE else "Pygame"


# 指向pygame事件的指针
@enum.verify(enum.UNIQUE)
class Events(enum.IntEnum):
    # 鼠标
    MOUSE_BUTTON_DOWN = pygame.MOUSEBUTTONDOWN
    MOUSE_BUTTON_UP = pygame.MOUSEBUTTONUP
    # 手柄
    JOYSTICK_BUTTON_DOWN = pygame.JOYBUTTONDOWN
    JOYSTICK_BUTTON_UP = pygame.JOYBUTTONUP
    # 键盘
    KEY_DOWN = pygame.KEYDOWN
    KEY_UP = pygame.KEYUP


# 表示方向的enum
@enum.verify(enum.UNIQUE)
class Axis(enum.IntEnum):
    VERTICAL = enum.auto()
    HORIZONTAL = enum.auto()


# 表示位置
@enum.verify(enum.UNIQUE)
class Locations(enum.IntEnum):
    BEGINNING = enum.auto()
    END = enum.auto()
    MIDDLE = enum.auto()
    EVERYWHERE = enum.auto()


# 与数字有关的常用方法
class Numbers:
    # 随机数
    @staticmethod
    def get_random_int(start: int, end: int) -> int:
        return RANDINT(start, end)

    # 检测int数值是否越界
    @staticmethod
    def keep_int_in_range(_number: int, min_value: int, max_value: int) -> int:
        return max(min(max_value, _number), min_value)

    # 检测int或float数值是否越界
    @staticmethod
    def keep_number_in_range(_number: number, min_value: number, max_value: number) -> number:
        return max(min(max_value, _number), min_value)

    # 转换string形式的百分比
    @staticmethod
    def convert_percentage(percentage: str | float | int) -> float:
        if isinstance(percentage, str) and percentage.endswith("%"):
            return float(percentage.strip("%")) / 100
        elif isinstance(percentage, int):
            return float(percentage)
        elif isinstance(percentage, float):
            return percentage
        else:
            EXCEPTION.fatal(f'"{percentage}" is not a valid percentage that can be converted')


# 颜色管理
class Colors:
    """常用颜色"""

    # 白色
    WHITE: Final[tuple[int, int, int, int]] = (255, 255, 255, 255)
    # 灰色
    GRAY: Final[tuple[int, int, int, int]] = (105, 105, 105, 255)
    # 淡灰色
    LIGHT_GRAY: Final[tuple[int, int, int, int]] = (83, 83, 83, 255)
    # 黑色
    BLACK: Final[tuple[int, int, int, int]] = (0, 0, 0, 255)
    # 红色
    RED: Final[tuple[int, int, int, int]] = (255, 0, 0, 255)
    # 橙色
    ORANGE: Final[tuple[int, int, int, int]] = (255, 127, 0, 255)
    # 黄色
    YELLOW: Final[tuple[int, int, int, int]] = (255, 255, 0, 255)
    # 绿色
    GREEN: Final[tuple[int, int, int, int]] = (0, 255, 0, 255)
    # 蓝色
    BLUE: Final[tuple[int, int, int, int]] = (0, 0, 255, 255)
    # 靛蓝色
    INDIGO: Final[tuple[int, int, int, int]] = (75, 0, 130, 255)
    # 紫色
    VIOLET: Final[tuple[int, int, int, int]] = (148, 0, 211, 255)
    # 透明
    TRANSPARENT: Final[tuple[int, int, int, int]] = (0, 0, 0, 0)
    # 淡蓝色
    LIGHT_SKY_BLUE: Final[tuple[int, int, int, int]] = (135, 206, 250, 255)
    # 深蓝色
    DODGER_BLUE: Final[tuple[int, int, int, int]] = (30, 144, 255, 255)

    # 转换至rgba颜色tuple
    @staticmethod
    def __to_rgba_color(color: Sequence) -> tuple[int, int, int, int]:
        _r: int = int(color[0])
        _g: int = int(color[1])
        _b: int = int(color[2])
        _a: int = int(color[3]) if len(color) >= 4 else 255
        return _r, _g, _b, _a

    """获取颜色"""

    # 给定一个颜色的名字或序号，返回对应的RGB列表
    @classmethod
    def get(cls, color: color_liked) -> tuple[int, int, int, int]:
        if isinstance(color, str):
            try:
                return cls.__to_rgba_color(PILImageColor.getrgb(color))
            except ValueError:
                EXCEPTION.fatal(f'The color "{color}" is currently not available!')
        else:
            return cls.__to_rgba_color(color)


class Keys:
    # 按键常量
    ESCAPE: Final[int] = pygame.K_ESCAPE
    SPACE: Final[int] = pygame.K_SPACE
    BACKSPACE: Final[int] = pygame.K_BACKSPACE
    DELETE: Final[int] = pygame.K_DELETE
    LEFT_CTRL: Final[int] = pygame.K_LCTRL
    ARROW_UP: Final[int] = pygame.K_UP
    ARROW_DOWN: Final[int] = pygame.K_DOWN
    ARROW_LEFT: Final[int] = pygame.K_LEFT
    ARROW_RIGHT: Final[int] = pygame.K_RIGHT
    RETURN: Final[int] = pygame.K_RETURN
    BACKQUOTE: Final[int] = pygame.K_BACKQUOTE
    F3: Final[int] = pygame.K_F3

    __root: Final[Tk] = Tk()
    __root.withdraw()

    # key是否被按下
    @classmethod
    def get_pressed(cls, key_name: str | int) -> bool:
        return pygame.key.get_pressed()[cls.get_key_code(key_name) if isinstance(key_name, str) else key_name]

    # 获取key的代号
    @staticmethod
    def get_key_code(key_name: str) -> int:
        return pygame.key.key_code(key_name)

    # 获取粘贴板内容
    @classmethod
    def get_clipboard(cls) -> str:
        return cls.__root.clipboard_get()


class Draw:
    # 根据给与的rect画出轮廓
    @staticmethod
    def rect(
        _surface: ImageSurface,
        color: tuple[int, int, int, int],
        rect: tuple[int, int, int, int] | tuple[tuple[int, int], tuple[int, int]],
        thickness: int = 0,
        radius: int = -1,
    ) -> None:
        if thickness <= 0 and radius <= 0:
            pygame.gfxdraw.box(_surface, rect, color)
        else:
            pygame.draw.rect(_surface, color, rect, thickness, radius)

    # 根据给与的中心点画出一个圆
    @staticmethod
    def circle(_surface: ImageSurface, color: tuple[int, int, int, int], center_pos: tuple[int, int], radius: int, thickness: int = 0) -> None:
        if thickness <= 0:
            pygame.gfxdraw.filled_circle(_surface, center_pos[0], center_pos[1], radius, color)
        else:
            pygame.draw.circle(_surface, color, center_pos, radius, thickness)

    # 根据给与的中心点画出一个椭圆
    @staticmethod
    def ellipse(_surface: ImageSurface, color: tuple[int, int, int, int], center_pos: tuple[int, int], radius: tuple[int, int], thickness: int = 0) -> None:
        if thickness <= 0:
            pygame.gfxdraw.filled_ellipse(_surface, center_pos[0], center_pos[1], radius[0], radius[1], color)
        else:
            pygame.draw.ellipse(_surface, color, ((center_pos[0] - radius[0], center_pos[1] - radius[1]), (radius[0] * 2, radius[1] * 2)), thickness)

    # 画一条抗锯齿线
    @staticmethod
    def aaline(_surface: ImageSurface, color: tuple[int, int, int, int], start_pos: tuple[int, int], end_pos: tuple[int, int]) -> None:
        if start_pos[0] == end_pos[0]:
            pygame.gfxdraw.vline(_surface, start_pos[0], start_pos[1], end_pos[1], color)
        elif start_pos[1] == end_pos[1]:
            pygame.gfxdraw.hline(_surface, start_pos[0], end_pos[0], end_pos[1], color)
        else:
            pygame.draw.aaline(_surface, color, start_pos, end_pos)

    # 画一条线
    @staticmethod
    def line(_surface: ImageSurface, color: tuple[int, int, int, int], start_pos: tuple[int, int], end_pos: tuple[int, int], width: int = 1) -> None:
        if width <= 1:
            pygame.gfxdraw.line(_surface, start_pos[0], start_pos[1], end_pos[0], end_pos[1], color)
        else:
            pygame.draw.line(_surface, color, start_pos, end_pos, width)

    # 画多边形
    @staticmethod
    def polygon(_surface: ImageSurface, _color: tuple[int, int, int, int], _points: tuple[tuple[int, int], ...], thickness: int = 0) -> None:
        if thickness <= 0:
            pygame.gfxdraw.filled_polygon(_surface, _points, _color)
        else:
            pygame.draw.polygon(_surface, _color, _points, thickness)


class Surfaces:
    # null图层占位符
    NULL: Final[ImageSurface] = pygame.surface.Surface((0, 0))

    # 获取Surface
    @staticmethod
    def new(size: tuple[int, int], surface_flags: int = -1) -> ImageSurface:
        return pygame.Surface(size, flags=surface_flags) if surface_flags >= 0 else pygame.Surface(size).convert()

    # 获取透明的Surface
    @staticmethod
    def transparent(size: tuple[int, int]) -> ImageSurface:
        return pygame.Surface(size, flags=pygame.SRCALPHA).convert_alpha()

    # 获取一个带颜色的Surface
    @staticmethod
    def colored(size: tuple[int, int], color: color_liked) -> ImageSurface:
        surface_t: ImageSurface = pygame.Surface(size).convert()
        surface_t.fill(Colors.get(color))
        return surface_t

    # 根据array生成Surface
    @classmethod
    def from_array(cls, surface_array: numpy.ndarray, swap_axes: bool = True) -> ImageSurface:
        if swap_axes is True:
            surface_array = surface_array.swapaxes(0, 1)
        if surface_array.shape[2] < 4:
            return pygame.surfarray.make_surface(surface_array).convert()
        else:
            # by llindstrom
            _shape: tuple = surface_array.shape
            _surface: ImageSurface = cls.transparent((int(_shape[0]), int(_shape[1])))
            # Copy the rgb part of array to the new _surface.
            pygame.pixelcopy.array_to_surface(_surface, surface_array[:, :, 0:3])
            # Copy the alpha part of array to the _surface using a pixels-alpha
            # view of the _surface.
            surface_alpha = numpy.array(_surface.get_view("A"), copy=False)
            surface_alpha[:, :] = surface_array[:, :, 3]
            return _surface

    # 根据Surface生成array
    @staticmethod
    def to_array(_surface: ImageSurface, with_alpha: bool = True, swap_axes: bool = True) -> numpy.ndarray:
        surface_3d_rgb_array: numpy.ndarray = pygame.surfarray.array3d(_surface)
        if with_alpha is True:
            surface_3d_rgb_array = numpy.dstack((surface_3d_rgb_array, pygame.surfarray.array_alpha(_surface)))
        return surface_3d_rgb_array.swapaxes(0, 1) if swap_axes is True else surface_3d_rgb_array

    # 获取材质缺失的临时警示材质
    @classmethod
    def texture_is_missing(cls, size: tuple[int, int]) -> ImageSurface:
        texture_missing_surface: ImageSurface = cls.colored(size, Colors.BLACK)
        half_width: int = size[0] // 2
        half_height: int = size[1] // 2
        Draw.rect(texture_missing_surface, Colors.VIOLET, (half_width, 0, texture_missing_surface.get_width() - half_width, half_height))
        Draw.rect(texture_missing_surface, Colors.VIOLET, (0, half_height, half_width, texture_missing_surface.get_height() - half_height))
        return texture_missing_surface

    # 检测图层是否是任何形式的null
    @classmethod
    def is_not_null(cls, _surface: ImageSurface | None) -> bool:
        return _surface is not None and _surface is not cls.NULL


# 滤镜效果
class Filters:
    # blur a surface using gaussian blur 毛玻璃效果
    @staticmethod
    def gaussian_blur(_surface: ImageSurface, radius: int = 10, repeat_edge_pixels: bool = True, dest_surface: ImageSurface | None = None) -> ImageSurface:
        # if is using pygame-ce
        if GraphicLibrary.is_using_pygame_ce():
            return pygame.transform.gaussian_blur(
                _surface, radius, repeat_edge_pixels, dest_surface if dest_surface is not None else Surfaces.new(_surface.get_size())
            )
        # if is using pygame not ce, then use pillow GaussianBlur instead
        new_surf: ImageSurface = Surfaces.from_array(
            numpy.asarray(PILImage.fromarray(Surfaces.to_array(_surface)).filter(PILImageFilter.GaussianBlur(radius)).convert("RGBA"))
        ).convert_alpha()
        if dest_surface is not None:
            return pygame.transform.smoothscale(new_surf, dest_surface.get_size(), dest_surface)
        return new_surf

    # blur a surface using box blur
    @classmethod
    def box_blur(cls, _surface: ImageSurface, radius: int = 10, repeat_edge_pixels: bool = True, dest_surface: ImageSurface | None = None) -> ImageSurface:
        # if is using pygame-ce
        if GraphicLibrary.is_using_pygame_ce():
            return pygame.transform.box_blur(
                _surface, radius, repeat_edge_pixels, dest_surface if dest_surface is not None else Surfaces.new(_surface.get_size())
            )
        # box blur is not supported for other graphic
        if Debug.get_developer_mode():
            EXCEPTION.warn('The "box_blur" filter is only supported when using pygame-ce, gaussian_blur will be used.')
        return cls.gaussian_blur(_surface, radius, repeat_edge_pixels, dest_surface)

    # 增加图层暗度
    @staticmethod
    def add_darkness(img: ImageSurface, value: int) -> ImageSurface:
        newImg: ImageSurface = img.copy()
        newImg.fill((value, value, value), special_flags=pygame.BLEND_RGB_SUB)
        return newImg

    # 减少图层暗度
    @staticmethod
    def subtract_darkness(img: ImageSurface, value: int) -> ImageSurface:
        newImg: ImageSurface = img.copy()
        newImg.fill((value, value, value), special_flags=pygame.BLEND_RGB_ADD)
        return newImg

# 尝试导入linpgassets
_LINPGASSETS_INITIALIZED: bool = False
if bool(Specification.get("ExtraAssets")) is True:
    try:
        import linpgassets

        _LINPGASSETS_INITIALIZED = True
        # 初始化linpgassets的数据库
        DataBase.update(linpgassets.get_database())
    except Exception:
        _LINPGASSETS_INITIALIZED = False

# 初始化项目自带的数据库
DataBase.update(Config.resolve_path_and_load_file(os.path.join("Data", "database")))

_KEY: Final[bytes] = bytes("82&939DcaO6002#*", "utf-8")


# 源图形处理
class Images:
    # flag查询表
    __FLAG_LOOKUP_TABLE: Final[dict[str, str]] = {"env": "environment", "ui": "user_interface"}

    # 加载
    @staticmethod
    def __load(_file: str | io.BytesIO) -> ImageSurface:
        # return UniversalImageSurface(pygame.image.load(_file), _file if isinstance(_file, str) else "")
        return pygame.image.load(_file)

    # 根据flag
    @classmethod
    def generate_path_according_to_prefix(cls, path: str) -> str:
        flag_end_index: int = path.index(">")
        file_name: str = path[flag_end_index + 1 :]
        flag_key: str | None = cls.__FLAG_LOOKUP_TABLE.get(path[2:flag_end_index])
        if flag_key is not None:
            if path[1] == "&":
                if os.path.exists(real_path := Specification.get_directory(flag_key, file_name)):
                    return real_path
                elif _LINPGASSETS_INITIALIZED is True:
                    return os.path.join(linpgassets.IMAGE_PATH, flag_key, file_name + ".zip")
                else:
                    return ""
            elif path[1] == "!":
                return os.path.join(linpgassets.IMAGE_PATH, flag_key, file_name + ".zip") if _LINPGASSETS_INITIALIZED is True else ""
            elif path[1] == "@":
                return Specification.get_directory(flag_key, file_name)
        EXCEPTION.fatal(f'Invalid tag: "{path}"')

    # 识快速加载图片
    @classmethod
    def quickly_load(cls, path: PoI, convert_alpha: bool = True) -> ImageSurface:
        if isinstance(path, ImageSurface):
            return path
        elif isinstance(path, str):
            if path != "<NULL>":
                canBeNull: bool = False
                if path.endswith("?"):
                    canBeNull = True
                    path = path.rstrip("?")
                _imageR: ImageSurface | None = None
                # 如果正在加载不属于linpgassets的图片
                if not path.startswith("<"):
                    try:
                        _imageR = cls.__load(path)
                    except Exception:
                        if Debug.get_developer_mode() is True and not canBeNull:
                            EXCEPTION.fatal(f"Cannot load image from path: {path}")
                        _imageR = None
                # 如果需要加载属于linpgassets的图片
                elif os.path.exists(_path := cls.generate_path_according_to_prefix(path)):
                    if not _path.endswith(".zip"):
                        _imageR = cls.__load(_path)
                    elif "linpgassets" in _path:
                        _zipFile: zipfile.ZipFile = zipfile.ZipFile(_path)
                        _imageR = cls.fromBytesIO(io.BytesIO(_zipFile.read(path[path.index(">") + 1 :], pwd=_KEY)))
                        _zipFile.close()
                    elif Debug.get_developer_mode() is True and not canBeNull:
                        EXCEPTION.fatal(f"Cannot find essential image with path: {_path}")
                # 根据参数处理并返回加载好的图片
                if _imageR is not None:
                    return _imageR.convert_alpha() if convert_alpha is True else _imageR.convert()
                # 如果图片加载出错
                else:
                    return Surfaces.NULL if canBeNull else Surfaces.texture_is_missing((192, 108))
            else:
                return Surfaces.NULL
        else:
            EXCEPTION.fatal(f"The path '{path}' has to be a string or at least a ImageSurface!")

    # 图片加载模块：接收图片路径,长,高,返回对应图片
    @classmethod
    def load(cls, path: PoI, size: tuple = tuple(), alpha: int = 255, convert_alpha: bool = True) -> ImageSurface:
        # 加载图片
        img: ImageSurface = cls.quickly_load(path, convert_alpha)
        # 如果是null，则直接返回
        if not Surfaces.is_not_null(img):
            return img
        # 根据参数编辑图片
        if alpha < 255:
            img.set_alpha(alpha)
        # 如果没有给size,则直接返回Surface
        return img if len(size) == 0 else cls.smoothly_resize(img, size) if Setting.get_antialias() else cls.resize(img, size)

    # 重新编辑尺寸
    @staticmethod
    def resize(img: ImageSurface, size: tuple) -> ImageSurface:
        # 如果是null，则直接返回
        if not Surfaces.is_not_null(img):
            return img
        # 编辑图片
        if size[1] is not None and size[1] >= 0 and size[0] is None:
            return pygame.transform.scale(img, (round(size[1] / img.get_height() * img.get_width()), round(size[1])))
        elif size[1] is None and size[0] is not None and size[0] >= 0:
            return pygame.transform.scale(img, (round(size[0]), round(size[0] / img.get_width() * img.get_height())))
        elif size[0] >= 0 and size[1] >= 0:
            return pygame.transform.scale(img, (round(size[0]), round(size[1])))
        EXCEPTION.fatal("Both width and height must be positive integer!")

    # 精准地缩放尺寸
    @staticmethod
    def smoothly_resize(img: ImageSurface, size: tuple) -> ImageSurface:
        # 如果是null，则直接返回
        if not Surfaces.is_not_null(img):
            return img
        # 编辑图片
        if size[1] is not None and size[1] >= 0 and size[0] is None:
            return pygame.transform.smoothscale(img, (round(size[1] / img.get_height() * img.get_width()), round(size[1])))
        elif size[1] is None and size[0] is not None and size[0] >= 0:
            return pygame.transform.smoothscale(img, (round(size[0]), round(size[0] / img.get_width() * img.get_height())))
        elif size[0] >= 0 and size[1] >= 0:
            return pygame.transform.smoothscale(img, (round(size[0]), round(size[1])))
        EXCEPTION.fatal("Both width and height must be positive integer!")

    # 精准地缩放尺寸
    @classmethod
    def smoothly_resize_and_crop_to_fit(cls, img: ImageSurface, size: tuple[int, int]) -> ImageSurface:
        # 如果是null，则直接返回
        if not Surfaces.is_not_null(img):
            return img
        # 根据尺寸计算长宽
        if img.get_height() / img.get_width() > 1:
            img = cls.smoothly_resize(img, (None, size[1]))
            return img.subsurface(((img.get_width() - size[0]) // 2, 0), size)
        else:
            img = cls.smoothly_resize(img, (size[0], None))
            return img.subsurface((0, (img.get_height() - size[1]) // 2), size)

    # 翻转图片
    @staticmethod
    def flip(img: ImageSurface, horizontal: bool, vertical: bool) -> ImageSurface:
        return pygame.transform.flip(img, horizontal, vertical) if Surfaces.is_not_null(img) else img

    # 旋转图片
    @staticmethod
    def rotate(img: ImageSurface, angle: int) -> ImageSurface:
        return pygame.transform.rotate(img, angle) if Surfaces.is_not_null(img) else img

    # 移除掉图片周围的透明像素
    @classmethod
    def crop_bounding(cls, img: ImageSurface) -> ImageSurface:
        return img.subsurface(img.get_bounding_rect()) if Surfaces.is_not_null(img) else img

    # 保存图片
    @staticmethod
    def save(_surface: ImageSurface, path: str) -> None:
        # 如果是null，则报警
        if not Surfaces.is_not_null(_surface):
            EXCEPTION.fatal("You cannot save a null surface!")
        # 保存
        pygame.image.save(_surface, path)

    # 将BytesIO转换为图片
    @classmethod
    def fromBytesIO(cls, _bytes: io.BytesIO) -> ImageSurface:
        return cls.__load(_bytes)

# 如果pygame的手柄组件没有初始化，则初始化
if not pygame.joystick.get_init():
    pygame.joystick.init()


# 输入管理组件
class Controller:
    # 手柄控制组件
    class __JoystickController:
        __input: pygame.joystick.JoystickType | None = None

        # 手柄是否初始化
        @classmethod
        def get_init(cls) -> bool:
            return cls.__input.get_init() if cls.is_active() is True else False  # type: ignore

        # 获取该按钮的详情
        @classmethod
        def get_button(cls, buttonId: int) -> bool:
            return cls.__input.get_button(buttonId) if cls.get_init() is True else False  # type: ignore

        @classmethod
        def get_axis(cls, buttonId: int) -> float:
            return round(cls.__input.get_axis(buttonId), 1) if cls.get_init() is True else 0.0  # type: ignore

        # 是否启动
        @classmethod
        def is_active(cls) -> bool:
            return cls.__input is not None

        # 更新设备
        @classmethod
        def update(cls) -> None:
            # 有新的手柄连接了
            if cls.__input is None:
                if pygame.joystick.get_count() > 0:
                    cls.__input = pygame.joystick.Joystick(0)
                    cls.__input.init()
                    EXCEPTION.inform("A joystick is detected and initialized successfully.")
            # 当目前有手柄在连接
            else:
                # 失去与当前手柄的连接
                if pygame.joystick.get_count() == 0:
                    cls.__input = None
                    EXCEPTION.inform("Lost connection with the joystick.")
                # 有新的手柄
                elif cls.__input.get_id() != pygame.joystick.Joystick(0).get_id():
                    cls.__input = pygame.joystick.Joystick(0)
                    cls.__input.init()
                    EXCEPTION.inform("Joystick changed! New joystick is detected and initialized successfully.")

    # 鼠标控制
    class __MouseController:
        # 当前鼠标坐标
        x: int = 0
        y: int = 0
        # 之前的鼠标坐标
        __last_x: int = 0
        __last_y: int = 0
        # 鼠标移动速度（使用手柄时）
        __moving_speed: int = max(int(Setting.get("MouseMoveSpeed")), 1)
        # 鼠标上次更新时被按下的详情
        __mouse_get_pressed_previously: tuple[bool, ...] = (False, False, False, False, False)
        # 鼠标图标
        __icon_img: ImageSurface | None = None

        @classmethod
        def set_custom_icon(cls, path: str) -> None:
            cls.__icon_img = Images.load(path, (int(Setting.get("MouseIconWidth")), int(Setting.get("MouseIconWidth") * 1.3)))

        # 灵敏度
        @classmethod
        def get_moving_speed(cls) -> int:
            return cls.__moving_speed

        # 鼠标坐标
        @classmethod
        def get_x_moved(cls) -> int:
            return cls.__last_x - cls.x

        @classmethod
        def get_y_moved(cls) -> int:
            return cls.__last_y - cls.y

        @classmethod
        def get_pos(cls) -> tuple[int, int]:
            return cls.x, cls.y

        # 设置坐标
        @classmethod
        def set_pos(cls, pos: tuple) -> None:
            # 更新前鼠标坐标
            cls.__last_x = cls.x
            cls.__last_y = cls.y
            # 更新当前鼠标坐标
            cls.x, cls.y = Coordinates.convert(pos)
            pygame.mouse.set_pos(cls.get_pos())

        # 是否鼠标按钮被点击
        @staticmethod
        def get_pressed(button_id: int) -> bool:
            return pygame.mouse.get_pressed()[button_id]

        # 是否鼠标按钮在上一帧被点击
        @classmethod
        def get_pressed_previously(cls, button_id: int) -> bool:
            return cls.__mouse_get_pressed_previously[button_id]

        # 是否鼠标按钮在上一帧和当前帧被点击
        @classmethod
        def get_pressed_since(cls, button_id: int) -> bool:
            return cls.__mouse_get_pressed_previously[button_id] and pygame.mouse.get_pressed()[button_id]

        # 是否鼠标指针在指定的方形范围内
        @classmethod
        def is_in_rect(cls, _x: int, _y: int, _width: int, _height: int) -> bool:
            return 0 < cls.x - _x < _width and 0 < cls.y - _y < _height

        # 更新鼠标数据
        @classmethod
        def update(cls) -> None:
            # 更新前鼠标坐标
            cls.__last_x = cls.x
            cls.__last_y = cls.y
            # 更新当前鼠标坐标
            cls.x, cls.y = pygame.mouse.get_pos()

        # 完成旧数据的存储
        @classmethod
        def finish_up(cls) -> None:
            cls.__mouse_get_pressed_previously = pygame.mouse.get_pressed()

        # 画出自定义的鼠标图标
        @classmethod
        def draw_custom_icon(cls, _surface: ImageSurface) -> None:
            if cls.__icon_img is not None:
                _surface.blit(cls.__icon_img, (cls.x, cls.y))

    # 手柄模块
    joystick = __JoystickController
    # 鼠标模块
    mouse = __MouseController
    # 输入事件
    __INPUT_EVENTS: tuple = tuple()
    # 检测特定事件
    __SPECIFIC_EVENTS: Final[dict[str, bool]] = {
        # 是否有确认事件
        "confirm": False,
        # 是否有强确认事件
        "hard_confirm": False,
        # 是否有返回事件
        "back": False,
        # 鼠标滚轮
        "scroll_up": False,
        "scroll_down": False,
        # 之前
        "previous": False,
        # 删除
        "delete": False,
    }
    # 是否需要截图
    NEED_TO_TAKE_SCREENSHOT: bool = False

    # 获取所有输入事件
    @classmethod
    def get_events(cls) -> tuple:
        return cls.__INPUT_EVENTS

    # 获取单个事件
    @classmethod
    def get_event(cls, event_type: str) -> bool:
        _result: bool | None = cls.__SPECIFIC_EVENTS.get(event_type)
        if _result is None:
            EXCEPTION.fatal(f'The event type "{event_type}" is not supported!')
        return _result

    # 获取单个事件
    @classmethod
    def set_event(cls, event_type: str, value: bool) -> None:
        cls.__SPECIFIC_EVENTS[event_type] = value

    # 完成这一帧的收尾工作
    @classmethod
    def finish_up(cls) -> None:
        cls.mouse.finish_up()

    # 更新输入
    @classmethod
    def update(cls) -> None:
        # 更新手柄输入事件
        cls.joystick.update()
        # 更新鼠标输入事件
        cls.mouse.update()
        # 根据手柄情况调整鼠标位置（如果手柄启动）
        if cls.joystick.is_active():
            x_axis_value: float = cls.joystick.get_axis(0)
            is_x_need_update: bool = not 0.5 > x_axis_value > -0.5
            y_axis_value: float = cls.joystick.get_axis(1)
            is_y_need_update: bool = not 0.5 > y_axis_value > -0.5
            if is_x_need_update is True and is_y_need_update is True:
                cls.mouse.set_pos(
                    (int(cls.mouse.x + cls.mouse.get_moving_speed() * x_axis_value), int(cls.mouse.y + cls.mouse.get_moving_speed() * y_axis_value))
                )
            elif is_x_need_update is True:
                cls.mouse.set_pos((int(cls.mouse.x + cls.mouse.get_moving_speed() * x_axis_value), cls.mouse.y))
            elif is_y_need_update is True:
                cls.mouse.set_pos((cls.mouse.x, int(cls.mouse.y + cls.mouse.get_moving_speed() * y_axis_value)))
        # 更新综合输入事件
        cls.__INPUT_EVENTS = tuple(pygame.event.get())
        # 重设用于判断常见事件的参数
        for key in cls.__SPECIFIC_EVENTS:
            cls.__SPECIFIC_EVENTS[key] = False
        for event in cls.__INPUT_EVENTS:
            if event.type == Events.MOUSE_BUTTON_DOWN:
                if event.button == 1:
                    cls.__SPECIFIC_EVENTS["confirm"] = True
                elif event.button == 2:
                    cls.__SPECIFIC_EVENTS["hard_confirm"] = True
                elif event.button == 3:
                    cls.__SPECIFIC_EVENTS["previous"] = True
                elif event.button == 4:
                    cls.__SPECIFIC_EVENTS["scroll_up"] = True
                elif event.button == 5:
                    cls.__SPECIFIC_EVENTS["scroll_down"] = True
            elif event.type == Events.JOYSTICK_BUTTON_DOWN:
                if cls.joystick.get_button(0) is True:
                    cls.__SPECIFIC_EVENTS["confirm"] = True
                elif cls.joystick.get_button(1) is True:
                    cls.__SPECIFIC_EVENTS["previous"] = True
            elif event.type == Events.KEY_DOWN:
                if event.key == Keys.ESCAPE:
                    cls.__SPECIFIC_EVENTS["back"] = True
                elif event.key == Keys.F3:
                    cls.NEED_TO_TAKE_SCREENSHOT = True
                elif event.key == Keys.DELETE:
                    cls.__SPECIFIC_EVENTS["delete"] = True


# 控制器输入组件初始化
Controller.update()


# 画面更新控制器
class Display:
    # 帧率控制器
    __CLOCK: Final[pygame.time.Clock] = pygame.time.Clock()
    # 帧率
    __MAX_FPS: int = min(max(int(Setting.get("MaxFps")), 30), 1000)
    # 窗口比例
    __SCALE: int = Numbers.keep_int_in_range(int(Setting.get("Resolution", "scale")), 0, 100)
    # 主要的窗口
    __SCREEN_WINDOW: ImageSurface = Surfaces.NULL
    # 窗口尺寸
    __STANDARD_WIDTH: int = max(int(Setting.get("Resolution", "width")), 1) * __SCALE // 100
    __STANDARD_HEIGHT: int = max(int(Setting.get("Resolution", "height")), 1) * __SCALE // 100
    # 信息渲染使用的文字模块
    __FONT: Final[pygame.font.Font] = pygame.font.SysFont("arial", __STANDARD_HEIGHT // 40)
    # 时间增量
    __TICKS: int = 0
    __DELTA_TIME: int = 1

    # 帧数
    @classmethod
    def get_current_fps(cls) -> float:
        return cls.__CLOCK.get_fps()

    @classmethod
    def get_max_fps(cls) -> int:
        return cls.__MAX_FPS

    # 时间增量(ms)
    @classmethod
    def get_delta_time(cls) -> int:
        return cls.__DELTA_TIME

    # 截图
    @classmethod
    def __save_screenshot(cls) -> None:
        if not os.path.exists(Specification.get_directory("screenshots")):
            os.mkdir(Specification.get_directory("screenshots"))
        Images.save(cls.__SCREEN_WINDOW, Specification.get_directory("screenshots", f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"))

    # 更新屏幕
    @classmethod
    def flip(cls) -> None:
        Controller.finish_up()
        # 展示帧率信息
        if Debug.get_show_fps():
            _text: ImageSurface = cls.__FONT.render(
                f"fps: {round(cls.get_current_fps(), 2)} delta time (ms): {cls.__DELTA_TIME}", Setting.get_antialias(), Colors.WHITE
            )
            cls.__SCREEN_WINDOW.blit(_text, (cls.__STANDARD_WIDTH - cls.__FONT.get_height() - _text.get_width(), cls.__FONT.get_height()))
        # 使用clock进行tick
        cls.__CLOCK.tick(cls.__MAX_FPS)
        pygame.display.flip()
        # 如果需要截图
        if Controller.NEED_TO_TAKE_SCREENSHOT is True:
            Controller.NEED_TO_TAKE_SCREENSHOT = False
            threading.Thread(target=cls.__save_screenshot).start()
        # 更新控制器
        Controller.update()
        Controller.mouse.draw_custom_icon(cls.__SCREEN_WINDOW)
        # 计算新的时间增量
        new_ticks: int = pygame.time.get_ticks()
        cls.__DELTA_TIME = max(new_ticks - cls.__TICKS, 1)
        cls.__TICKS = new_ticks

    # 设置窗口标题
    @staticmethod
    def set_caption(title: str) -> None:
        pygame.display.set_caption(title)

    # 设置窗口图标
    @staticmethod
    def set_icon(path: str) -> None:
        pygame.display.set_icon(Images.quickly_load(path, False))

    # 窗口宽度
    @classmethod
    def get_width(cls) -> int:
        return cls.__STANDARD_WIDTH

    # 窗口高度
    @classmethod
    def get_height(cls) -> int:
        return cls.__STANDARD_HEIGHT

    # 窗口尺寸
    @classmethod
    def get_size(cls) -> tuple[int, int]:
        return cls.__STANDARD_WIDTH, cls.__STANDARD_HEIGHT

    # 初始化屏幕
    @classmethod
    def init(cls, flags: int = 0) -> ImageSurface:
        monitorId: int = int(Setting.get("MonitorToDisplay"))
        # 如果是全屏模式
        if cls.__SCALE >= 100:
            if flags <= 0:
                flags = pygame.FULLSCREEN | pygame.SCALED
            if Setting.get("EnableOpenGL") is True:
                flags |= pygame.OPENGL
            # 如果分辨率与设置中的参数不符，则更新设置中的分辨率参数
            theSelectedScreenSize: tuple[int, int] = pygame.display.get_desktop_sizes()[monitorId]
            if cls.__STANDARD_WIDTH != theSelectedScreenSize[0] or cls.__STANDARD_HEIGHT != theSelectedScreenSize[1]:
                cls.__STANDARD_WIDTH = theSelectedScreenSize[0]
                cls.__STANDARD_HEIGHT = theSelectedScreenSize[1]
                Setting.set("Resolution", "width", value=cls.__STANDARD_WIDTH)
                Setting.set("Resolution", "height", value=cls.__STANDARD_HEIGHT)
                Setting.save()
        # 生成screen
        cls.__SCREEN_WINDOW = pygame.display.set_mode(cls.get_size(), flags, display=monitorId, vsync=1 if Setting.get("EnableVerticalSync") is True else 0)
        cls.__SCREEN_WINDOW.set_alpha(None)
        cls.__SCREEN_WINDOW.fill(Colors.BLACK)
        return cls.__SCREEN_WINDOW

    # 获取屏幕
    @classmethod
    def get_window(cls) -> ImageSurface:
        return cls.__SCREEN_WINDOW

    # 直接画到屏幕上
    @classmethod
    def blit(cls, surface_to_draw: ImageSurface, pos: Sequence) -> None:
        cls.__SCREEN_WINDOW.blit(surface_to_draw, Coordinates.convert(pos))


# bool timer use for tick checking
class BoolTickTimer:
    def __init__(self, time_ms: int, default_status: bool = True) -> None:
        self.__time_to_wait = time_ms
        self.__current_time: int = 0
        self.__status: bool = default_status
        self.__prev_status: bool = self.__status

    def tick(self) -> None:
        self.__current_time += Display.get_delta_time()
        self.__prev_status = self.__status
        if self.__current_time > self.__time_to_wait:
            self.__current_time = 0
            self.__status = not self.__status

    def is_status_changed(self) -> bool:
        return self.__prev_status != self.__status

    def get_status(self) -> bool:
        return self.__status

# 导入pyav
import av

# 尝试导入opencv
_OPENCV_INITIALIZED: bool = False
try:
    import cv2

    _OPENCV_INITIALIZED = True
except ImportError:
    pass


# 视频转换系统
class Videos:
    # 是否opencv模块已经初始化且路径存在
    @staticmethod
    def validation(_path: str) -> None:
        # 如果opencv没有成功地导入
        if not _OPENCV_INITIALIZED:
            EXCEPTION.fatal("You cannot use any video module unless you install opencv!", 4)
        # 确保路径存在
        elif not os.path.exists(_path):
            EXCEPTION.fatal(f'Cannot find file on path: "{_path}"')

    # 获取视频封面
    @classmethod
    def get_thumbnail(cls, path: str, size: tuple[int, int] | None = None) -> ImageSurface:
        # 检测
        cls.validation(path)
        # 获取视频流
        video_stream = cv2.VideoCapture(path)
        video_stream.set(cv2.CAP_PROP_POS_FRAMES, video_stream.get(cv2.CAP_PROP_FRAME_COUNT) // 10)
        # 获取帧图像
        current_frame = cv2.cvtColor(video_stream.read()[1], cv2.COLOR_BGR2RGB)
        # 释放流
        video_stream.release()
        # 如果有必要，则改变图片尺寸
        if size is not None and (current_frame.shape[0] != size[0] or current_frame.shape[1] != size[1]):
            current_frame = cv2.resize(current_frame, size)
        # 以Surface的形式返回封面
        return Surfaces.from_array(current_frame)

    # 获取视频的音频 （返回路径）
    @classmethod
    def split_audio(cls, path: str, audio_format: str = "ogg", codecs: str = "libvorbis") -> str:
        # 检测
        cls.validation(path)
        # 产生不重名的output文件名称
        output_file_name_t: str = os.path.basename(path).replace(".", "_") + "{0}.{1}"
        output_file_name: str
        index: int = 0
        while True:
            output_file_name = output_file_name_t.format(index, audio_format)
            if not os.path.exists(output_file_name):
                break
            index += 1
        # 生成output路径
        output_path: str = os.path.join(Cache.get_directory(), output_file_name)
        # 使用pyav导出音频
        with av.open(path, "r") as inp:
            with av.open(output_path, "w", audio_format) as out:
                out_stream = out.add_stream(codecs)
                for frame in inp.decode(audio=0):
                    frame.pts = None
                    for packets in out_stream.encode(frame):
                        out.mux(packets)
                for packets in out_stream.encode(None):
                    out.mux(packets)
        # 返回output路径
        return output_path

# 频道 type alias
SoundChannel = pygame.mixer.Channel


# 声音类
class Sound(pygame.mixer.Sound):
    def __init__(self, _input: Any) -> None:
        self.__input: Any = _input
        self.__init: bool = False
        self.__volume: float = 1.0
        self.__try_init()

    # 尝试初始化
    def __try_init(self) -> None:
        if not self.__init and pygame.mixer.get_init() is not None:
            super().__init__(self.__input)
            self.set_volume(self.__volume)
            self.__init = True

    def play(self, loops: int = 0, max_time: int = 0, fade_ms: int = 0) -> SoundChannel | None:  # type: ignore[override]
        self.__try_init()
        if self.__init is True:
            return super().play(loops, max_time, fade_ms)
        return None

    def set_volume(self, value: float) -> None:
        if self.__init is True:
            super().set_volume(value)
        else:
            self.__volume = value

    def get_volume(self) -> float:
        if self.__init is True:
            return super().get_volume()
        else:
            return self.__volume

    def stop(self) -> None:
        if self.__init is True:
            super().stop()

    def fadeout(self, time: int) -> None:
        if self.__init is True:
            super().fadeout(time)


# 音效管理模块-列表
class SoundsManager:
    def __init__(self, channel_id: int):
        self.__channel_id: int = channel_id
        self.__index: int = 0
        self.__sounds: list[Sound] = []

    @property
    def channel_id(self) -> int:
        return self.__channel_id

    def get_channel_id(self) -> int:
        return self.__channel_id

    # 添加音乐
    def add(self, path: str) -> None:
        self.__sounds.append(Sounds.load(path))

    # 清空列表释放内存
    def clear(self) -> None:
        self.__sounds.clear()

    # 播放音乐
    def play(self, sound_id: int = -1) -> None:
        if len(self.__sounds) > 0 and Sounds.get_init() is True and not SoundChannel(self.__channel_id).get_busy():
            self.__index = Numbers.get_random_int(0, len(self.__sounds) - 1) if sound_id < 0 else sound_id
            SoundChannel(self.__channel_id).play(self.__sounds[self.__index])

    # 停止播放
    def stop(self) -> None:
        if Sounds.get_init() is True:
            SoundChannel(self.__channel_id).stop()

    # 获取音量
    @property
    def volume(self) -> float:
        return self.get_volume()

    def get_volume(self) -> float:
        return self.__sounds[0].get_volume()

    # 设置音量
    def set_volume(self, volume: number) -> None:
        for _sound in self.__sounds:
            _sound.set_volume(volume)


# 音效管理
class Sounds:
    # 是否成功初始化
    @staticmethod
    def get_init() -> bool:
        return pygame.mixer.get_init() is not None

    # 加载音效
    @staticmethod
    def load(path: str, volume: float | None = None) -> Sound:
        soundTmp: Sound = Sound(path)
        if volume is not None:
            soundTmp.set_volume(volume)
        return soundTmp

    # 从一个视频中加载音效
    @classmethod
    def load_from_video(cls, path: str, volume: float | None = None, cache_key: str | None = None) -> Sound:
        # 如果给定了cache_key，则先尝试从缓存中读取音乐文件
        if cache_key is not None and len(cache_key) > 0 and Cache.match(cache_key, path) is True:
            try:
                return cls.load(Cache.get_cache_path(cache_key), volume)
            except Exception:
                pass
        # 如果读取失败或者没有缓存key或者match失败，则应根据给定的路径生成音乐文件并返回
        path_of_sound: str = Videos.split_audio(path)
        sound_audio: Sound = cls.load(path_of_sound, volume)
        # 如果给了缓存key，则应该生成缓存联系并保留缓存文件
        if cache_key is not None and len(cache_key) > 0:
            Cache.new(cache_key, path, path_of_sound)
        # 如果没有缓存key，则删除缓存文件
        else:
            os.remove(path_of_sound)
        return sound_audio

    # 从一个文件夹中加载音效
    @classmethod
    def load_from_directory(cls, folder_path: str) -> tuple[Sound, ...]:
        if not os.path.isdir(folder_path):
            EXCEPTION.fatal("The path is not a valid directory!")
        return tuple(cls.load(_path) for _path in glob(os.path.join(folder_path, "*")))

    # 播放音效
    @classmethod
    def play(cls, sound: Sound, channel_id: int) -> None:
        if cls.get_init() is True:
            SoundChannel(channel_id).play(sound)

    # 停止播放
    @classmethod
    def stop(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.stop()

    # 是否有任何音乐在播放
    @classmethod
    def get_busy(cls) -> bool:
        return pygame.mixer.get_busy() if cls.get_init() is True else True

    # 暂停正在播放的音乐
    @classmethod
    def pause(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.pause()

    # 继续播放暂停的音乐
    @classmethod
    def unpause(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.unpause()

    # 淡出音效
    @classmethod
    def fade_out(cls, time: int) -> None:
        if cls.get_init() is True:
            pygame.mixer.fadeout(time)

    # 寻找一个可用的频道
    @classmethod
    def find_channel(cls, force: bool = False) -> SoundChannel | None:
        return pygame.mixer.find_channel(force) if cls.get_init() is True else None

    # 获取频道的数量
    @staticmethod
    def get_num_channels() -> int:
        return max(pygame.mixer.get_num_channels() - 3, 0)

    # 获取对应id的频道
    @classmethod
    def get_channel(cls, channel_id: int) -> SoundChannel:
        if channel_id < cls.get_num_channels():
            return SoundChannel(channel_id)
        else:
            EXCEPTION.fatal(f'The channel_id "{channel_id}" is out of bound of {cls.get_num_channels()}')


# 音乐管理
class Music:
    # 是否成功初始化
    @staticmethod
    def get_init() -> bool:
        return pygame.mixer.get_init() is not None

    # 加载背景音乐（但不播放）
    @staticmethod
    def load(path: str) -> None:
        pygame.mixer.music.load(path)

    # 从一个视频中加载音乐
    @staticmethod
    def load_from_video(path: str) -> str:
        Music.unload()
        path_of_music: str = Videos.split_audio(path)
        Music.load(path_of_music)
        return path_of_music

    # 卸载背景音乐
    @classmethod
    def unload(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.unload()

    # 重新开始播放背景音乐
    @classmethod
    def restart(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.rewind()

    # 播放背景音乐
    @classmethod
    def play(cls, loops: int = 0, start: float = 0.0, fade_ms: int = 0) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.play(loops, start, fade_ms)

    # 暂停正在播放的音乐
    @classmethod
    def pause(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.pause()

    # 继续播放暂停的音乐
    @classmethod
    def unpause(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.unpause()

    # 停止播放
    @classmethod
    def stop(cls) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.stop()

    # 淡出背景音乐
    @classmethod
    def fade_out(cls, time: int) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.fadeout(time)

    # 获取背景音乐播放的位置
    @classmethod
    def get_pos(cls) -> int:
        return pygame.mixer.music.get_pos() if cls.get_init() is True else 0

    # 设置背景音乐播放的位置
    @classmethod
    def set_pos(cls, time: float) -> None:
        if cls.get_init():
            pygame.mixer.music.set_pos(time)

    # 获取背景音乐的音量
    @classmethod
    def get_volume(cls) -> float:
        return pygame.mixer.music.get_volume() if cls.get_init() is True else 0

    # 调整背景音乐的音量
    @classmethod
    def set_volume(cls, volume: float) -> None:
        if cls.get_init() is True:
            pygame.mixer.music.set_volume(volume)

    # 是否忙碌
    @classmethod
    def get_busy(cls) -> bool:
        return pygame.mixer.music.get_busy() if cls.get_init() is True else True


# 音量管理
class Volume:
    __sound_unit: Final[int] = 100

    @classmethod
    def get_global_value(cls) -> int:
        return Numbers.keep_int_in_range(round(Setting.get("Sound", "global_value")), 0, cls.__sound_unit)

    @classmethod
    def get_background_music(cls) -> int:
        return round(
            Numbers.keep_number_in_range(round(Setting.get("Sound", "background_music"), 2), 0, cls.__sound_unit) * cls.get_global_value() / cls.__sound_unit
        )

    @classmethod
    def get_effects(cls) -> int:
        return round(Numbers.keep_number_in_range(round(Setting.get("Sound", "effects"), 2), 0, cls.__sound_unit) * cls.get_global_value() / cls.__sound_unit)

    @classmethod
    def get_environment(cls) -> int:
        return round(
            Numbers.keep_number_in_range(round(Setting.get("Sound", "environment"), 2), 0, cls.__sound_unit) * cls.get_global_value() / cls.__sound_unit
        )


# 多媒体全局管理
class Media:
    # 是否有任何音乐在播放
    @staticmethod
    def get_busy() -> bool:
        return Sounds.get_busy() or Music.get_busy()

    # 暂停正在播放的音乐
    @staticmethod
    def pause() -> None:
        Sounds.pause()
        Music.pause()

    # 继续播放暂停的音乐
    @staticmethod
    def unpause() -> None:
        Sounds.unpause()
        Music.unpause()

    # 卸载所有音乐
    @staticmethod
    def unload() -> None:
        Sounds.stop()
        Music.unload()

    # 淡出所有音乐
    @staticmethod
    def fade_out(time: int) -> None:
        Sounds.fade_out(time)
        Music.fade_out(time)


# linpg引擎保留的频道
class LINPG_RESERVED_CHANNELS:
    # 根据设置参数改变声道数量
    __MIXER_CHANNEL_NUM: Final[int] = max(int(Setting.get("NumberOfChannels")), 8) + 3
    # 背景音乐
    __BACKGROUND_MUSIC_CHANNEL_ID: Final[int] = __MIXER_CHANNEL_NUM - 3
    BACKGROUND_MUSIC_CHANNEL: SoundChannel | None = None
    # 音效
    __SOUND_EFFECTS_CHANNEL_ID: Final[int] = __MIXER_CHANNEL_NUM - 2
    SOUND_EFFECTS_CHANNEL: SoundChannel | None = None
    # 环境
    __ENVIRONMENTAL_SOUND_CHANNEL_ID: Final[int] = __MIXER_CHANNEL_NUM - 1
    ENVIRONMENTAL_SOUND_CHANNEL: SoundChannel | None = None

    # 初始化对应频道
    @classmethod
    def init(cls) -> None:
        if Sounds.get_init() is True:
            pygame.mixer.set_num_channels(cls.__MIXER_CHANNEL_NUM)
            cls.BACKGROUND_MUSIC_CHANNEL = SoundChannel(cls.__BACKGROUND_MUSIC_CHANNEL_ID)
            cls.SOUND_EFFECTS_CHANNEL = SoundChannel(cls.__SOUND_EFFECTS_CHANNEL_ID)
            cls.ENVIRONMENTAL_SOUND_CHANNEL = SoundChannel(cls.__ENVIRONMENTAL_SOUND_CHANNEL_ID)
        else:
            EXCEPTION.inform("Mixer has not been initialized correctly!")
            print("One possible cause could be no output device, anyway, please double check your output device(s)!")


# 初始化引擎保留频道
LINPG_RESERVED_CHANNELS.init()


# 文字渲染模块
class FontGenerator:
    __FONT_IS_NOT_INITIALIZED_MSG: Final[str] = "Font is not initialized!"

    def __init__(self) -> None:
        self.__FONT: pygame.font.Font | None = None
        self.__size: int = 0

    # 是否加粗
    @property
    def bold(self) -> bool:
        if self.__FONT is not None:
            return self.__FONT.bold
        else:
            EXCEPTION.fatal(self.__FONT_IS_NOT_INITIALIZED_MSG)

    # 是否斜体
    @property
    def italic(self) -> bool:
        if self.__FONT is not None:
            return self.__FONT.italic
        else:
            EXCEPTION.fatal(self.__FONT_IS_NOT_INITIALIZED_MSG)

    # 文字大小
    @property
    def size(self) -> int:
        if self.__FONT is not None:
            return self.__size
        else:
            EXCEPTION.fatal(self.__FONT_IS_NOT_INITIALIZED_MSG)

    # 更新文字模块
    def update(self, size: int_f, ifBold: bool = False, ifItalic: bool = False) -> None:
        if size <= 0:
            EXCEPTION.fatal("Font size must be greater than 0!")
        self.__size = int(size)
        # 根据类型处理
        if Setting.get_font_type() == "default":
            self.__FONT = pygame.font.SysFont(Setting.get_font(), self.__size)
        elif Setting.get_font_type() == "custom":
            font_path: str = Specification.get_directory("font", f"{Setting.get_font()}.ttf")
            if not os.path.exists(font_path):
                EXCEPTION.fatal(f"Cannot find the {Setting.get_font()}.ttf file!")
            self.__FONT = pygame.font.Font(font_path, self.__size)
        else:
            EXCEPTION.fatal("FontType option in setting file is incorrect!")
        self.__FONT.bold = ifBold
        self.__FONT.italic = ifItalic

    # 估计文字的宽度
    def estimate_text_width(self, text: str | int) -> int:
        if self.__FONT is not None:
            return self.__FONT.size(str(text))[0]
        else:
            EXCEPTION.fatal(self.__FONT_IS_NOT_INITIALIZED_MSG)

    # 估计文字的高度
    def estimate_text_height(self, text: str | int) -> int:
        if self.__FONT is not None:
            return self.__FONT.size(str(text))[1]
        else:
            EXCEPTION.fatal(self.__FONT_IS_NOT_INITIALIZED_MSG)

    # 检测是否需要更新
    def check_for_update(self, _size: int, ifBold: bool = False, ifItalic: bool = False) -> None:
        if self.__FONT is None or _size != self.__size:
            self.update(_size, ifBold, ifItalic)
        else:
            self.__FONT.bold = ifBold
            self.__FONT.italic = ifItalic

    # 渲染文字
    def render(self, txt: str | int, color: color_liked, background_color: color_liked | None = None) -> ImageSurface:
        if not isinstance(txt, (str, int)):
            EXCEPTION.fatal(f"The text must be a unicode or bytes, not {txt}")
        if self.__FONT is None:
            EXCEPTION.fatal(self.__FONT_IS_NOT_INITIALIZED_MSG)
        return self.__FONT.render(str(txt), Setting.get_antialias(), Colors.get(color), Colors.get(background_color) if background_color is not None else None)


# 文字渲染器管理模块
class Font:
    # 引擎标准文件渲染器
    __LINPG_GLOBAL_FONTS: Final[dict[str, FontGenerator]] = {}
    # 上一次render的字体
    __LINPG_LAST_FONT: Final[FontGenerator] = FontGenerator()

    # 设置全局文字
    @classmethod
    def set_global_font(cls, key: str, size: int, ifBold: bool = False, ifItalic: bool = False) -> None:
        if isinstance(size, int) and size > 0:
            if key not in cls.__LINPG_GLOBAL_FONTS:
                cls.__LINPG_GLOBAL_FONTS[key] = FontGenerator()
            cls.__LINPG_GLOBAL_FONTS[key].update(size, ifBold, ifItalic)
        else:
            EXCEPTION.fatal(f"Font size must be positive integer not {size}!")

    # 获取全局文字
    @classmethod
    def get_global_font(cls, key: str) -> FontGenerator:
        _font: FontGenerator | None = cls.__LINPG_GLOBAL_FONTS.get(key)
        if _font is not None:
            return _font
        else:
            EXCEPTION.fatal(f'You did not set any font named "{key}".')

    # 获取全局文字
    @classmethod
    def get_global_font_size(cls, key: str) -> int:
        return cls.get_global_font(key).size

    # 获取全局文字
    @classmethod
    def render_global_font(cls, key: str, txt: str, color: color_liked, background_color: color_liked | None = None) -> ImageSurface:
        return cls.get_global_font(key).render(txt, color, background_color)

    # 删除全局文字
    @classmethod
    def remove_global_font(cls, key: str) -> None:
        if key in cls.__LINPG_GLOBAL_FONTS:
            del cls.__LINPG_GLOBAL_FONTS[key]

    # 创建字体
    @staticmethod
    def create(size: int_f, ifBold: bool = False, ifItalic: bool = False) -> FontGenerator:
        new_font_t = FontGenerator()
        new_font_t.update(size, ifBold, ifItalic)
        return new_font_t

    # 接受文字，颜色，文字大小，样式等信息，返回制作完的文字
    @classmethod
    def render(
        cls, txt: str | int, color: color_liked, size: int_f, ifBold: bool = False, ifItalic: bool = False, background_color: color_liked | None = None
    ) -> ImageSurface:
        cls.__LINPG_LAST_FONT.check_for_update(int(size), ifBold, ifItalic)
        return cls.__LINPG_LAST_FONT.render(txt, color, background_color)


# 艺术字效果
class ArtisticFont:
    # 描述框效果
    @staticmethod
    def render_description_box(
        txt: str | int,
        color: color_liked,
        size: int,
        padding: int,
        background_color: color_liked,
        ifBold: bool = False,
        ifItalic: bool = False,
        outline_color: color_liked | None = None,
        thickness: int = 2,
    ) -> ImageSurface:
        font_surface: ImageSurface = Font.render(txt, color, size, ifBold, ifItalic)
        des_surface: ImageSurface = Surfaces.colored((font_surface.get_width() + padding * 2, font_surface.get_height() + padding * 2), background_color)
        Draw.rect(des_surface, Colors.get(color if outline_color is None else outline_color), (ORIGIN, des_surface.get_size()), thickness)
        des_surface.blit(font_surface, (padding, padding))
        return des_surface

    # 渲染有轮廓的文字
    @staticmethod
    def render_with_outline(
        _text: str | int,
        color: color_liked,
        size: int,
        outline_thickness: int = 1,
        outline_color: color_liked = Colors.BLACK,
        ifBold: bool = False,
        ifItalic: bool = False,
    ) -> ImageSurface:
        # 文字图层
        text_surface: ImageSurface = Font.render(_text, color, size, ifBold, ifItalic).convert_alpha()
        # 外框图层
        outline_surface: ImageSurface = Font.render(_text, outline_color, size, ifBold, ifItalic).convert_alpha()
        # 用于返回最终结果的图层
        result_surface: ImageSurface = Surfaces.transparent(
            (text_surface.get_width() + 2 * outline_thickness, text_surface.get_height() + 2 * outline_thickness)
        )
        # 生成圆角的像素坐标
        x: int = outline_thickness
        y: int = 0
        e: int = 1 - outline_thickness
        points: set[tuple[int, int]] = set()
        while x >= y:
            points.add((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points.update([(y, x) for x, y in points if x > y], [(-x, y) for x, y in points if x], [(x, -y) for x, y in points if y])
        # 多次渲染外框图层
        for dx, dy in points:
            result_surface.blit(outline_surface, (dx + outline_thickness, dy + outline_thickness))
        # 渲染文字图层
        result_surface.blit(text_surface, (outline_thickness, outline_thickness))
        # 返回结果
        return result_surface


# 持久数据管理IO
class PersistentVariables(TypeSafeGetter, TypeSafeSetter):
    __DATA: Final[dict[str, Any]] = {}
    __PATH: Final[str] = Specification.get_directory("save", "persistent." + Config.get_file_type())

    @classmethod
    def _get_data(cls) -> dict:
        return cls.__DATA

    @classmethod
    def set(cls, *_key: str, value: Any, assumeKeyExists: bool = False) -> None:
        super().set(*_key, value=value, assumeKeyExists=assumeKeyExists)
        cls.save()

    @classmethod
    def reload(cls) -> None:
        cls.__DATA.clear()
        if os.path.exists(cls.__PATH):
            cls.__DATA.update(Config.load_file(cls.__PATH))

    @classmethod
    def save(cls) -> None:
        if len(cls.__DATA) > 0:
            Config.save(cls.__PATH, cls.__DATA)
        else:
            Files.delete_if_exist(cls.__PATH)


# 初始化持久数据库
PersistentVariables.reload()


# 存档系统
class Saves:
    # 存档数据
    @dataclass
    class Progress:
        data: dict
        screenshot: ImageSurface
        createdAt: str
        slotId: int

    # 是否有至少一个存档存在
    @staticmethod
    def any_progress_exists() -> bool:
        return len(glob(Specification.get_directory("save", "*.linpg.save"))) > 0

    # 获取全部存档
    @classmethod
    def get_progresses(cls) -> dict[int, Progress]:
        progresses: dict[int, Saves.Progress] = {}
        for _save in glob(Specification.get_directory("save", "*.linpg.save")):
            _file: Saves.Progress = cls.load(_save)
            progresses[_file.slotId] = _file
        return progresses

    # 获取最近的一次存档
    @classmethod
    def get_latest_progresses(cls) -> Progress:
        progresses: dict[int, Saves.Progress] = cls.get_progresses()
        latest: Saves.Progress | None = None
        for _progress in progresses.values():
            if latest is None or datetime.strptime(latest.createdAt, "%Y-%m-%d %H:%M %p") < datetime.strptime(_progress.createdAt, "%Y-%m-%d %H:%M %p"):
                latest = _progress
        if latest is None:
            EXCEPTION.fatal("No progress exists!")
        return latest

    # 保存存档
    @classmethod
    def __save(cls, _path: str, _data: dict, _screenshot: ImageSurface, slotId: int) -> None:
        # 保存存档文件到本地
        Config.save("data.json", _data)
        Config.save("info.json", {"createdAt": datetime.now().strftime("%Y-%m-%d %H:%M %p"), "slotId": slotId})
        Images.save(_screenshot, "screenshot.png")
        # 将存档文件写入zip文件中
        with zipfile.ZipFile(_path, "w") as zipped_f:
            zipped_f.write("data.json")
            zipped_f.write("info.json")
            zipped_f.write("screenshot.png")
        # 删除本地文件
        Files.delete_if_exist("data.json")
        Files.delete_if_exist("info.json")
        Files.delete_if_exist("screenshot.png")

    @classmethod
    def save(cls, _data: dict, _screenshot: ImageSurface, slotId: int) -> None:
        # 确保储存数据的文件夹存在
        os.makedirs(Specification.get_directory("save"), exist_ok=True)
        save_thread = threading.Thread(
            target=cls.__save, args=(Specification.get_directory("save", f"save_{slotId}.linpg.save"), _data, _screenshot, slotId), daemon=True
        )
        # 多线程保存数据
        save_thread.start()
        save_thread.join()

    # 取得存档
    @classmethod
    def load(cls, _path: str) -> Progress:
        # 打开zip文件并读取信息
        zipFile: zipfile.ZipFile = zipfile.ZipFile(_path)
        _data: dict = json.load(io.BytesIO(zipFile.read("data.json")))
        _screenshot: ImageSurface = Images.fromBytesIO(io.BytesIO(zipFile.read("screenshot.png")))
        _info: dict = json.load(io.BytesIO(zipFile.read("info.json")))
        # 断开对zip文件的访问
        zipFile.close()
        # 返回数据
        return cls.Progress(_data, _screenshot, str(_info["createdAt"]), int(_info["slotId"]))


# achievements management system
class Achievements:

    __NAME: Final[str] = "__achievements__"
    __DATABASE: Final[dict[str, dict[str, bool | int]]] = Specification.get_dict_ref("Achievements")

    # lock a achievement
    @classmethod
    def lock(cls, achievement: str) -> None:
        if PersistentVariables.contains(cls.__NAME):
            PersistentVariables.set(cls.__NAME, achievement, value=False)

    # unlock a achievement
    @classmethod
    def unlock(cls, achievement: str) -> None:
        if not PersistentVariables.contains(cls.__NAME):
            PersistentVariables.set(cls.__NAME, value={})
        PersistentVariables.set(cls.__NAME, achievement, value=True)

    # is achievement hidden to player
    @classmethod
    def is_hidden(cls, achievement: str) -> bool:
        return bool(cls.__DATABASE[achievement].get("hidden", False))

    # whether a achievement has been achieved
    @classmethod
    def has_achieved(cls, achievement: str) -> bool:
        if not PersistentVariables.contains(cls.__NAME):
            return False
        result: bool | None = PersistentVariables.try_get_bool(cls.__NAME, achievement)
        return result if result is not None else False

    @classmethod
    def get_list(cls) -> list[str]:
        return sorted(cls.__DATABASE, key=lambda x: cls.__DATABASE[x]["id"])
