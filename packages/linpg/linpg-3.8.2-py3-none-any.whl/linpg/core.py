"""
结构:
system -> module -> shape -> surface -> text -> image -> window -> video -> sprite
"""

import math

from tkinter import messagebox

from abc import ABCMeta, abstractmethod

from .basic import *


# 系统模块接口
class AbstractSystem(ABC):
    def __init__(self) -> None:
        # 判定用于判定是否还在播放的参数
        self.__is_playing: bool = True
        self.__current_language: str = Lang.get_current_language()

    # 是否正在播放
    def is_playing(self) -> bool:
        return self.__is_playing

    # 停止播放
    def stop(self) -> None:
        self.__is_playing = False

    def _continue(self) -> None:
        self.__is_playing = True

    # 是否本体语言和当前一致
    def language_need_update(self) -> bool:
        return self.__current_language != Lang.get_current_language()

    # 更新语言
    def update_language(self) -> None:
        self.__current_language = Lang.get_current_language()


# 拥有背景音乐的系统模块接口
class SystemWithBackgroundMusic(AbstractSystem):
    def __init__(self) -> None:
        super().__init__()
        self.__audio: Sound | None = None
        self.__bgm_path: str | None = None
        self.__bgm_volume: float = 1.0

    # 系统退出时，需卸载bgm
    def stop(self) -> None:
        super().stop()
        self.unload_bgm()

    # 卸载bgm
    def unload_bgm(self) -> None:
        self.stop_bgm()
        self.__bgm_path = None
        self.__audio = None

    # 设置bgm
    def set_bgm(self, path: str | None, forced: bool = False) -> None:
        # 如果path是None,则
        if path is None:
            if self.__bgm_path is not None:
                self.unload_bgm()
        # 如果路径存在
        elif os.path.exists(path):
            # 只有在音乐路径不一致或者强制更新的情况下才会更新路径（同时卸载现有音乐）
            if self.__bgm_path != path or forced is True:
                self.unload_bgm()
                self.__bgm_path = path
                self.__audio = Sounds.load(self.__bgm_path, self.__bgm_volume)
        else:
            EXCEPTION.fatal(f"Path '{path}' does not exist!")

    # 设置bgm音量
    def set_bgm_volume(self, volume: number) -> None:
        if 1 >= volume >= 0:
            self.__bgm_volume = volume
            if self.__audio is not None:
                self.__audio.set_volume(self.__bgm_volume)
        else:
            EXCEPTION.fatal(f"Volume '{volume}' is out of the range! (must between 0 and 1)")

    # 播放bgm
    def play_bgm(self) -> None:
        if (
            self.__audio is not None
            and LINPG_RESERVED_CHANNELS.BACKGROUND_MUSIC_CHANNEL is not None
            and not LINPG_RESERVED_CHANNELS.BACKGROUND_MUSIC_CHANNEL.get_busy()
        ):
            LINPG_RESERVED_CHANNELS.BACKGROUND_MUSIC_CHANNEL.play(self.__audio)

    # 停止播放
    @staticmethod
    def stop_bgm() -> None:
        if LINPG_RESERVED_CHANNELS.BACKGROUND_MUSIC_CHANNEL is not None:
            LINPG_RESERVED_CHANNELS.BACKGROUND_MUSIC_CHANNEL.stop()

    # 把内容画到surface上（子类必须实现）
    @abstractmethod
    def draw(self, _surface: ImageSurface) -> None:
        EXCEPTION.fatal("draw()", 1)

    # 直接画到屏幕上
    def draw_on_screen(self) -> None:
        self.draw(Display.get_window())


# 游戏模块接口
class AbstractGameSystem(SystemWithBackgroundMusic, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        # 参数
        self._chapter_type: str = ""
        self._chapter_id: int = 0
        self._project_name: str | None = None
        # 是否已经初始化
        self.__initialized: bool = False

    # 是否初始化
    def is_initialized(self) -> bool:
        return self.__initialized

    # 初始化关键参数
    def _initialize(self, chapterType: str, chapterId: int, projectName: str | None) -> None:
        # 类型
        self._chapter_type = chapterType
        # 章节id
        self._chapter_id = chapterId
        # 合集名称-用于dlc和创意工坊
        self._project_name = projectName
        # 初始化完成
        self.__initialized = True

    # 获取本模块的信息
    def get_data_of_parent_game_system(self) -> dict:
        return {"chapter_type": self._chapter_type, "chapter_id": self._chapter_id, "project_name": self._project_name}

    # 获取需要保存的数据（子类必须实现）
    @abstractmethod
    def _get_data_need_to_save(self) -> dict:
        EXCEPTION.fatal("_get_data_need_to_save()", 1)

    # 默认加载数据的路径（子类需实现）
    @abstractmethod
    def get_data_file_path(self) -> str:
        EXCEPTION.fatal("get_data_file_path()", 1)

    # 加载进度（子类需实现）
    @abstractmethod
    def load_progress(self, _data: dict) -> None:
        EXCEPTION.fatal("load_progress()", 1)

    # 从默认的路径加载数据
    def load(self) -> None:
        self.load_progress(Config.load_file(self.get_data_file_path()))

    # 将数据保存到加载的路径
    def _save(self) -> None:
        Config.save(self.get_data_file_path(), self._get_data_need_to_save())


# 坐标类
class Coordinate:
    def __init__(self, x: int_f, y: int_f):
        self.__x: int = int(x)
        self.__y: int = int(y)

    def __lt__(self, other: "Coordinate") -> bool:
        return self.__y + self.__x < other.y + other.x

    # x轴坐标
    @property
    def x(self) -> int:
        return self.__x

    @property
    def left(self) -> int:
        return self.__x

    def get_left(self) -> int:
        return self.__x

    def set_left(self, value: int_f) -> None:
        self.__x = int(value)

    # 向左移动
    def move_left(self, value: int_f) -> None:
        self.set_left(int(self.__x - value))

    # 向右移动
    def move_right(self, value: int_f) -> None:
        self.set_left(self.__x + int(value))

    # y轴坐标
    @property
    def y(self) -> int:
        return self.__y

    @property
    def top(self) -> int:
        return self.__y

    def get_top(self) -> int:
        return self.__y

    def set_top(self, value: int_f) -> None:
        self.__y = int(value)

    # 向上移动
    def move_upward(self, value: int_f) -> None:
        self.set_top(int(self.__y - value))

    # 向下移动
    def move_downward(self, value: int_f) -> None:
        self.set_top(self.__y + int(value))

    # 坐标信息
    @property
    def pos(self) -> tuple[int, int]:
        return self.__x, self.__y

    def get_pos(self) -> tuple[int, int]:
        return self.__x, self.__y

    # 设置坐标
    def set_pos(self, _x: int_f, _y: int_f) -> None:
        self.set_left(_x)
        self.set_top(_y)

    def move_to(self, pos: tuple[int_f, int_f]) -> None:
        self.set_pos(pos[0], pos[1])

    # 检测是否在给定的位置上
    def on_pos(self, pos: object) -> bool:
        return Coordinates.is_same(self.pos, pos)


# 坐标类 - 更精准坐标
class Position:
    def __init__(self, x: number, y: number):
        # 坐标（注意，与Coordinate不同，Position坐标使用浮点数）
        self.__x: number = x
        self.__y: number = y

    def __lt__(self, other: "Position") -> bool:
        return self.__y + self.__x < other.y + other.x

    # 坐标信息
    @property
    def x(self) -> number:
        return self.__x

    @property
    def y(self) -> number:
        return self.__y

    @property
    def pos(self) -> tuple[number, number]:
        return self.__x, self.__y

    def get_pos(self) -> tuple[number, number]:
        return self.__x, self.__y

    # 设置坐标
    def set_x(self, value: number) -> None:
        self.__x = value if isinstance(value, int) else round(value, 5)

    def set_y(self, value: number) -> None:
        self.__y = value if isinstance(value, int) else round(value, 5)

    def set_pos(self, x: number, y: number) -> None:
        self.set_x(x)
        self.set_y(y)

    def move_to(self, pos: tuple[number, number]) -> None:
        self.set_x(pos[0])
        self.set_y(pos[1])


# 2d游戏对象接口
class GameObject2d(Coordinate):
    def __init__(self, x: int_f, y: int_f):
        super().__init__(x, y)
        self.tag: str = ""

    # 宽
    @property
    def width(self) -> int:
        return self.get_width()

    @abstractmethod
    def get_width(self) -> int:
        EXCEPTION.fatal("get_width()", 1)

    # 高
    @property
    def height(self) -> int:
        return self.get_height()

    @abstractmethod
    def get_height(self) -> int:
        EXCEPTION.fatal("get_height()", 1)

    # 尺寸
    @property
    def size(self) -> tuple[int, int]:
        return self.get_width(), self.get_height()

    def get_size(self) -> tuple[int, int]:
        return self.get_width(), self.get_height()

    # 右侧位置
    @property
    def right(self) -> int:
        return self.x + self.get_width()

    def get_right(self) -> int:
        return self.x + self.get_width()

    def set_right(self, value: int_f) -> None:
        self.set_left(value - self.get_width())

    # 底部位置
    @property
    def bottom(self) -> int:
        return self.y + self.get_height()

    def get_bottom(self) -> int:
        return self.y + self.get_height()

    def set_bottom(self, value: int_f) -> None:
        self.set_top(value - self.get_height())

    # 中心位置
    @property
    def centerx(self) -> int:
        return self.x + self.get_width() // 2

    def get_centerx(self) -> int:
        return self.x + self.get_width() // 2

    def set_centerx(self, centerx: int_f) -> None:
        self.set_left(centerx - self.get_width() / 2)

    @property
    def centery(self) -> int:
        return self.y + self.get_height() // 2

    def get_centery(self) -> int:
        return self.y + self.get_height() // 2

    def set_centery(self, centery: int_f) -> None:
        self.set_top(centery - self.get_height() / 2)

    @property
    def center(self) -> tuple[int, int]:
        return self.centerx, self.centery

    def get_center(self) -> tuple[int, int]:
        return self.centerx, self.centery

    def set_center(self, centerx: int_f, centery: int_f) -> None:
        self.set_centerx(centerx)
        self.set_centery(centery)

    @property
    def left_center(self) -> tuple[int, int]:
        return self.x, self.centery

    @property
    def right_center(self) -> tuple[int, int]:
        return self.right, self.centery

    @property
    def top_center(self) -> tuple[int, int]:
        return self.centerx, self.y

    @property
    def bottom_center(self) -> tuple[int, int]:
        return self.centerx, self.bottom

    # 是否被鼠标触碰
    def is_hovered(self, off_set: tuple[int, int] | None = None) -> bool:
        if off_set is None:
            return Controller.mouse.is_in_rect(self.x, self.y, self.get_width(), self.get_height())
        else:
            return Controller.mouse.is_in_rect(self.x + off_set[0], self.y + off_set[1], self.get_width(), self.get_height())

    # 检测自身是否覆盖了另一个2d游戏对象
    def is_overlapped_with(self, _rect: "GameObject2d") -> bool:
        return max(self.left, _rect.left) < min(self.right, _rect.right) and max(self.top, _rect.top) < min(self.bottom, _rect.bottom)

    # 将图片直接画到surface上
    def draw(self, _surface: ImageSurface) -> None:
        self.display(_surface)

    # 将图片直接画到屏幕上
    def draw_on_screen(self) -> None:
        self.display(Display.get_window())

    # 根据offSet将图片展示到surface的对应位置上 - 子类必须实现
    @abstractmethod
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        EXCEPTION.fatal("display()", 1)

    # 根据offSet将图片展示到屏幕的对应位置上
    def display_on_screen(self, offSet: tuple[int, int] = ORIGIN) -> None:
        self.display(Display.get_window(), offSet)

    # 忽略现有坐标，将图片画到surface的指定位置上
    def blit(self, _surface: ImageSurface, pos: tuple[int, int]) -> None:
        old_pos = self.get_pos()
        self.move_to(pos)
        self.draw(_surface)
        self.move_to(old_pos)

    # 忽略现有坐标，将图片画到surface的指定位置上
    def blit_on_screen(self, pos: tuple[int, int]) -> None:
        old_pos = self.get_pos()
        self.move_to(pos)
        self.draw(Display.get_window())
        self.move_to(old_pos)


# 正方形类
class Square(GameObject2d):
    def __init__(self, x: int_f, y: int_f, width: int_f):
        super().__init__(x, y)
        self.__width: int = int(width)
        self.__min_width: int = 0
        self.__max_width: int = -1

    # 高度（应与宽度一致），子类如果是Rect必须重写
    def get_height(self) -> int:
        return self.__width

    # 宽度
    def get_width(self) -> int:
        return self.__width

    def set_width(self, value: int_f) -> None:
        new_width: int = int(value)
        if new_width > self.__min_width:
            if self.__max_width <= 0 or new_width < self.__max_width:
                self.__width = new_width
            else:
                self.__width = self.__max_width
        else:
            self.__width = self.__min_width

    # 最短宽度
    @property
    def min_width(self) -> int:
        return self.get_min_width()

    def get_min_width(self) -> int:
        return self.__min_width

    def set_min_width(self, value: int_f) -> None:
        new_width: int = int(value)
        if new_width >= 1:
            if self.__max_width <= 0 or new_width < self.__max_width:
                if self.__min_width != new_width:
                    self.__min_width = new_width
                    # 重置宽度
                    self.set_width(self.get_width())
            else:
                EXCEPTION.fatal(f"The minimum width has to be smaller than the maximum width, which in this case is {self.__max_width}.")
        else:
            EXCEPTION.fatal("The minimum width has to be greater than 1.")

    # 最长宽度
    @property
    def max_width(self) -> int:
        return self.get_max_width()

    def get_max_width(self) -> int:
        return self.__max_width

    def set_max_width(self, value: int_f = -1) -> None:
        new_width: int = int(value)
        if new_width >= 0:
            if new_width > self.__min_width:
                self.__max_width = new_width
            else:
                EXCEPTION.fatal(f"The maximum width has to be greater than the minimum width, which in this case is {self.__min_width}.")
        else:
            self.__max_width = -1
        # 重置宽度
        self.set_width(self.get_width())

    # 画出轮廓
    def draw_outline(self, _surface: ImageSurface, color: color_liked = "red", thickness: int = 2, radius: int = -1, offSet: tuple[int, int] = ORIGIN) -> None:
        Draw.rect(_surface, Colors.get(color), (Coordinates.add(self.pos, offSet), self.size), thickness, radius)

    # 画出轮廓 - 实现父类的要求
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        self.draw_outline(_surface, offSet=offSet)


# 用于兼容的长方类
class Rectangle(Square):
    def __init__(self, left: int_f, top: int_f, width: int_f, height: int_f):
        super().__init__(left, top, width)
        self.__height: int = int(height)
        self.__min_height: int = 0
        self.__max_height: int = -1

    # 高度
    def get_height(self) -> int:
        return self.__height

    def set_height(self, value: int_f) -> None:
        new_height: int = int(value)
        if new_height > self.__min_height:
            if self.__max_height <= 0 or new_height < self.__max_height:
                self.__height = new_height
            else:
                self.__height = self.__max_height
        else:
            self.__height = self.__min_height

    # 最短高度
    @property
    def min_height(self) -> int:
        return self.get_min_height()

    def get_min_height(self) -> int:
        return self.__min_height

    def set_min_height(self, value: int_f) -> None:
        new_height: int = int(value)
        if new_height >= 1:
            if self.__max_height <= 0 or new_height < self.__max_height:
                if self.__min_height != new_height:
                    self.__min_height = new_height
                    # 重置高度
                    self.set_height(self.get_height())
            else:
                EXCEPTION.fatal(f"The minimum height has to be smaller than the maximum height, which in this case is {self.__max_height}.")
        else:
            EXCEPTION.fatal("The minimum height has to be greater than 1.")

    # 最长高度
    @property
    def max_height(self) -> int:
        return self.get_max_height()

    def get_max_height(self) -> int:
        return self.__max_height

    def set_max_height(self, value: int_f = -1) -> None:
        new_height: int = int(value)
        if new_height >= 0:
            if new_height > self.__min_height:
                self.__max_height = new_height
            else:
                EXCEPTION.fatal(f"The maximum height has to be greater than the minimum height, which in this case is {self.__min_height}.")
        else:
            self.__max_height = -1
        # 重置高度
        self.set_height(self.get_height())

    # 尺寸
    def set_size(self, width: int_f, height: int_f) -> None:
        self.set_width(width)
        self.set_height(height)

    # 获取rect
    def get_rect(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.get_width(), self.__height

    def get_rectangle(self) -> "Rectangle":
        return Rectangle(self.x, self.y, self.get_width(), self.__height)


RectLiked = Rectangle | pygame.Rect | tuple
RectObject = Rectangle | pygame.Rect


# Rectangle方法管理
class Rectangles:
    # 转换tuple至Rectangle
    @staticmethod
    def from_tuple(tuple_rect: tuple) -> Rectangle:
        if len(tuple_rect) == 2:
            return Rectangle(tuple_rect[0][0], tuple_rect[0][1], tuple_rect[1][0], tuple_rect[1][1])
        elif len(tuple_rect) == 4:
            return Rectangle(tuple_rect[0], tuple_rect[1], tuple_rect[2], tuple_rect[3])
        EXCEPTION.fatal("Invalid length for forming a rect.")

    # 将tuple转换至RectObject以方便操作
    @classmethod
    def __comply(cls, rect: RectLiked) -> RectObject:
        if isinstance(rect, tuple):
            return cls.from_tuple(rect)
        return rect

    # 是否2个Rectangle形状一样
    @classmethod
    def equal(cls, rect1: RectLiked | None, rect2: RectLiked | None) -> bool:
        if rect1 is not None and rect2 is not None:
            rect1 = cls.__comply(rect1)
            rect2 = cls.__comply(rect2)
            return rect1.x == rect2.x and rect1.y == rect2.y and rect1.width == rect2.width and rect1.height == rect2.height
        return rect1 == rect2

    # 转换pygame的rect类至linpg引擎的rect类
    @classmethod
    def create(cls, rect: RectLiked) -> Rectangle:
        # 如果是Rect类，则没必要转换
        if isinstance(rect, Rectangle):
            return rect
        # 如果是pygame.Rect类则需转换
        elif isinstance(rect, pygame.Rect):
            return Rectangle(rect.x, rect.y, rect.width, rect.height)
        # 如果是tuple类，则需要创建
        elif isinstance(rect, tuple):
            return cls.from_tuple(rect)
        EXCEPTION.fatal(f'The rect has to be RectLiked object, not "{type(rect)}".')

    # 相加2个rect
    @classmethod
    def apply(cls, source_rect: RectLiked, apply_rect: RectLiked) -> Rectangle:
        source_rect = cls.__comply(source_rect)
        apply_rect = cls.__comply(apply_rect)
        return Rectangle(
            source_rect.x + apply_rect.x, source_rect.y + apply_rect.y, source_rect.width + apply_rect.width, source_rect.height + apply_rect.height
        )


# 转换linpg.Rect至pygame.Rect
def convert_to_pygame_rect(rect: RectLiked) -> pygame.Rect:
    # 如果是pygame.Rect类，则没必要转换
    if isinstance(rect, pygame.Rect):
        return rect
    # 确认是linpg.Rect类再转换
    elif isinstance(rect, Rectangle):
        return pygame.Rect(rect.left, rect.top, rect.width, rect.height)
    # 如果是tuple类，则需要创建
    elif isinstance(rect, tuple):
        if len(rect) == 2:
            return pygame.Rect(rect[0], rect[1])
        elif len(rect) == 4:
            return pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        else:
            EXCEPTION.fatal("Invalid length for forming a rect.")
    else:
        EXCEPTION.fatal(f'The rect has to be RectLiked object, not "{type(rect)}".')


# 检测pygame类2d模型是否被点击
def is_hovering(imgObject: ImageSurface, objectPos: tuple[int, int] = ORIGIN) -> bool:
    return Controller.mouse.is_in_rect(objectPos[0], objectPos[1], imgObject.get_width(), imgObject.get_height())


# 获取图片的subsurface
def get_img_subsurface(img: ImageSurface, rect: RectLiked) -> ImageSurface:
    return img.subsurface(rect if isinstance(rect, pygame.Rect) else convert_to_pygame_rect(rect))


# 图形接口
class AbstractImageSurface(Rectangle, Hidable, metaclass=ABCMeta):
    def __init__(self, img: Any, x: int_f, y: int_f, width: int_f, height: int_f, tag: str) -> None:
        Rectangle.__init__(self, x, y, width, height)
        Hidable.__init__(self)
        self.__img: Any = img
        # 确保长宽均已输入且为正整数
        if self.get_width() < 0 and self.get_height() < 0:
            self.set_size(self.__img.get_width(), self.__img.get_height())
        elif self.get_width() < 0 <= self.get_height():
            self.set_width(self.get_height() * self.__img.get_width() // self.__img.get_height())
        elif self.get_width() >= 0 > self.get_height():
            self.set_height(self.get_width() * self.__img.get_height() // self.__img.get_width())
        self.tag = tag

    # 路径
    @property
    def path(self) -> str:
        return self.__img.path if isinstance(self.__img, UniversalImageSurface) else ""

    # 获取图片非透明部分的rect
    def get_bounding_rect(self) -> Rectangle:
        return Rectangles.create(self.__img.get_bounding_rect()) if isinstance(self.__img, ImageSurface) else Rectangle(0, 0, 0, 0)

    """透明度"""

    @property
    def alpha(self) -> int:
        return self.get_alpha()

    def get_alpha(self) -> int:
        return int(self.__img.get_alpha())

    def set_alpha(self, value: int) -> None:
        self.__img.set_alpha(Numbers.keep_int_in_range(value, 0, 255))

    def add_alpha(self, value: int) -> None:
        self.set_alpha(self.get_alpha() + value)

    def subtract_alpha(self, value: int) -> None:
        self.set_alpha(self.get_alpha() - value)

    # 获取图片复制品
    def _get_image_reference(self) -> Any:
        return self.__img

    def get_image_copy(self) -> Any:
        return self.__img.copy() if Surfaces.is_not_null(self.__img) else self.__img

    # 更新图片
    def _set_image(self, newImage: Any) -> None:
        self.__img = newImage

    def update_image(self, img_path: PoI, ifConvertAlpha: bool = True) -> None:
        self._set_image(Images.quickly_load(img_path, ifConvertAlpha))

    # 在尺寸比例不变的情况下改变尺寸
    def set_width_with_original_image_size_locked(self, width: int_f) -> None:
        self.set_size(width, width * self.__img.get_height() / self.__img.get_width())

    def set_height_with_original_image_size_locked(self, height: int_f) -> None:
        self.set_size(height * self.__img.get_width() / self.__img.get_height(), height)

    # 自动放大2倍
    def scale_n_times(self, times: float) -> None:
        self.set_width(self.get_width() * times)
        self.set_height(self.get_height() * times)

    # 旋转
    def rotate(self, angle: int) -> None:
        self.__img = Images.rotate(self.__img, angle)

    # 不为null
    def is_not_null(self) -> bool:
        return Surfaces.is_not_null(self.__img)


# 有本地坐标的Surface (警告，子类必须实现get_left()和get_top()方法)
class SurfaceWithLocalPos:
    def __init__(self) -> None:
        self.__local_x: int = 0
        self.__local_y: int = 0

    # 获取x坐标（子类需实现）
    @abstractmethod
    def get_left(self) -> int:
        EXCEPTION.fatal("get_left()", 1)

    # 获取y坐标（子类需实现）
    @abstractmethod
    def get_top(self) -> int:
        EXCEPTION.fatal("get_top()", 1)

    # 获取本地坐标
    @property
    def local_x(self) -> int:
        return self.__local_x

    def get_local_x(self) -> int:
        return self.__local_x

    @property
    def local_y(self) -> int:
        return self.__local_y

    def get_local_y(self) -> int:
        return self.__local_y

    @property
    def local_pos(self) -> tuple[int, int]:
        return self.__local_x, self.__local_y

    def get_local_pos(self) -> tuple[int, int]:
        return self.__local_x, self.__local_y

    # 设置本地坐标
    def set_local_x(self, value: int_f) -> None:
        self.__local_x = int(value)

    def set_local_y(self, value: int_f) -> None:
        self.__local_y = int(value)

    def set_local_pos(self, local_x: int_f, local_y: int_f) -> None:
        self.set_local_x(local_x)
        self.set_local_y(local_y)

    def locally_move_to(self, local_pos: tuple[int_f, int_f]) -> None:
        self.set_local_pos(local_pos[0], local_pos[1])

    # 增加本地坐标
    def add_local_x(self, value: int_f) -> None:
        self.set_local_x(self.__local_x + value)

    def add_local_y(self, value: int_f) -> None:
        self.set_local_y(self.__local_y + value)

    def add_local_pos(self, local_x: int_f, local_y: int_f) -> None:
        self.add_local_x(local_x)
        self.add_local_y(local_y)

    # 减少本地坐标
    def subtract_local_x(self, value: int_f) -> None:
        self.set_local_x(self.__local_x - value)

    def subtract_local_y(self, value: int_f) -> None:
        self.set_local_y(self.__local_y - value)

    def subtract_local_pos(self, local_x: int_f, local_y: int_f) -> None:
        self.subtract_local_x(local_x)
        self.subtract_local_y(local_y)

    # 绝对的本地坐标
    @property
    def abs_x(self) -> int:
        return self.get_abs_x()

    def get_abs_x(self) -> int:
        return self.get_left() + self.__local_x

    @property
    def abs_y(self) -> int:
        return self.get_abs_y()

    def get_abs_y(self) -> int:
        return self.get_top() + self.__local_y

    @property
    def abs_pos(self) -> tuple[int, int]:
        return self.get_abs_x(), self.get_abs_y()

    def get_abs_pos(self) -> tuple[int, int]:
        return self.get_abs_x(), self.get_abs_y()


# 有本地坐标的图形接口
class AdvancedAbstractImageSurface(AbstractImageSurface, SurfaceWithLocalPos):
    def __init__(self, img: Any, x: int_f, y: int_f, width: int_f, height: int_f, tag: str = "") -> None:
        AbstractImageSurface.__init__(self, img, x, y, width, height, tag)
        SurfaceWithLocalPos.__init__(self)
        self._alpha: int = 255

    # 获取透明度
    def get_alpha(self) -> int:
        return self._alpha

    # 设置透明度
    def set_alpha(self, value: int) -> None:
        self._set_alpha(value)

    def _set_alpha(self, value: int, update_original: bool = True) -> None:
        self._alpha = Numbers.keep_int_in_range(value, 0, 255)
        if update_original is True and isinstance(self._get_image_reference(), ImageSurface):
            super().set_alpha(self._alpha)


# 带缓存的高级图片拟态类
class AdvancedAbstractCachingImageSurface(AdvancedAbstractImageSurface):
    def __init__(self, img: Any, x: int_f, y: int_f, width: int_f, height: int_f, tag: str = "") -> None:
        super().__init__(img, x, y, width, height, tag=tag)
        self._processed_img: ImageSurface | None = None
        self._need_update: bool = True
        self.__is_local_offset_enable: bool = True

    # 处理图片（子类必须实现）
    @abstractmethod
    def _update_img(self) -> None:
        EXCEPTION.fatal("_update_img()", 1)

    # 是否启用本地坐标
    def set_local_offset_availability(self, value: bool) -> None:
        self.__is_local_offset_enable = value

    # 绝对的本地坐标
    def get_abs_x(self) -> int:
        return super().get_abs_x() if self.__is_local_offset_enable is True else self.get_left()

    def get_abs_y(self) -> int:
        return super().get_abs_y() if self.__is_local_offset_enable is True else self.get_top()

    # 更新图片
    def update_image(self, img_path: PoI, ifConvertAlpha: bool = True) -> None:
        super().update_image(img_path, ifConvertAlpha)
        self._need_update = True

    # 设置透明度
    def set_alpha(self, value: int) -> None:
        self._set_alpha(value, False)
        if self._processed_img is not None:
            self._processed_img.set_alpha(self.get_alpha())

    # 宽度
    def set_width(self, value: int_f) -> None:
        _value: int = int(value)
        if _value != self.get_width():
            super().set_width(value)
            self._need_update = True

    # 高度
    def set_height(self, value: int_f) -> None:
        _value: int = int(value)
        if _value != self.get_height():
            super().set_height(value)
            self._need_update = True

    # 是否被鼠标触碰
    def is_hovered(self, off_set: tuple[int, int] | None = None) -> bool:
        if self._processed_img is not None:
            _x: int = self.x + self.local_x
            _y: int = self.y + self.local_y
            if off_set is not None:
                _x += off_set[0]
                _y += off_set[1]
            return Controller.mouse.is_in_rect(_x, _y, self._processed_img.get_width(), self._processed_img.get_height())
        else:
            return False

    # 加暗度
    def add_darkness(self, value: int) -> None:
        self._set_image(Filters.add_darkness(self._get_image_reference(), value))
        self._need_update = True

    # 减暗度
    def subtract_darkness(self, value: int) -> None:
        self._set_image(Filters.subtract_darkness(self._get_image_reference(), value))
        self._need_update = True

    # 旋转
    def rotate(self, angle: int) -> None:
        # 旋转图片
        super().rotate(angle)
        self._need_update = True

    # 反转原图
    def flip_original_img(self, horizontal: bool = True, vertical: bool = False) -> None:
        self._set_image(Images.flip(self._get_image_reference(), horizontal, vertical))
        self._need_update = True

    # 画出绝对轮廓
    def draw_abs_outline(self, _surface: ImageSurface, color: color_liked = "red", line_width: int = 2, offSet: tuple[int, int] = ORIGIN) -> None:
        if self._need_update is True:
            self._update_img()
        if self._processed_img is not None:
            Draw.rect(_surface, Colors.get(color), (Coordinates.add(self.abs_pos, offSet), self._processed_img.get_size()), line_width)
        else:
            EXCEPTION.fatal("The image has not been correctly processed.")

    # 展示
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            # 如果图片需要更新，则先更新
            if self._need_update is True:
                self._update_img()
            # 将已经处理好的图片画在给定的图层上
            if self._processed_img is not None:
                _surface.blit(self._processed_img, Coordinates.add(self.abs_pos, offSet))
            else:
                EXCEPTION.fatal("The image has not been correctly processed.")


# 文字类
class TextSurface(GameObject2d, Hidable):
    def __init__(self, text: str, x: int_f, y: int_f, size: int_f, _color: color_liked = Colors.BLACK, _bold: bool = False, _italic: bool = False) -> None:
        GameObject2d.__init__(self, x, y)
        Hidable.__init__(self)
        self.__text: str = text
        self.__size: int = int(size)
        self.__color: tuple[int, int, int, int] = Colors.get(_color)
        self.__bold: bool = _bold
        self.__italic: bool = _italic
        self.__alpha: int = 255
        self.__text_surface: ImageSurface | None = None
        self.__outline_thickness: int = 0
        self.__outline_color: tuple[int, int, int, int] = Colors.BLACK
        # 更新文字图层（需作为初始化的最后一步）
        self._update_text_surface()

    def get_text(self) -> str:
        return self.__text

    def get_font_size(self) -> int:
        return self.__size

    def get_color(self) -> tuple[int, int, int, int]:
        return self.__color

    def set_color(self, _color: color_liked) -> None:
        self.__color = Colors.get(_color)
        self._update_text_surface()

    def get_bold(self) -> bool:
        return self.__bold

    def get_italic(self) -> bool:
        return self.__italic

    def get_alpha(self) -> int:
        return self.__alpha

    def _update_text_surface(self) -> None:
        if len(self.get_text()) == 0:
            self.__text_surface = None
        else:
            self.__text_surface = (
                Font.render(self.get_text(), self.get_color(), self.get_font_size(), self.get_bold(), self.get_italic())
                if self.__outline_thickness <= 0
                else ArtisticFont.render_with_outline(
                    self.get_text(), self.get_color(), self.get_font_size(), self.__outline_thickness, self.__outline_color, self.get_bold(), self.get_italic()
                )
            )

    def _get_text_surface(self) -> ImageSurface | None:
        return self.__text_surface

    # 设置轮廓粗细
    def set_outline_thickness(self, _thickness: int) -> None:
        self.__outline_thickness = max(_thickness, 1)
        self._update_text_surface()

    # 设置轮廓颜色
    def set_outline_color(self, _color: color_liked) -> None:
        self.__outline_color = Colors.get(_color)
        self._update_text_surface()

    # 关闭轮廓渲染
    def disable_outline(self) -> None:
        self.__outline_thickness = 0
        self._update_text_surface()

    def set_text(self, value: str) -> None:
        if value != self.get_text():
            self.__text = value
            self._update_text_surface()
            if self.__text_surface is not None and self.get_alpha() != 255:
                self.__text_surface.set_alpha(self.get_alpha())

    def set_font_size(self, value: int) -> None:
        if value != self.__size:
            self.__size = value
            self._update_text_surface()

    def set_bold(self, value: bool) -> None:
        if self.get_bold() != value:
            self.__bold = value
            self._update_text_surface()

    def set_italic(self, value: bool) -> None:
        if self.get_italic() != value:
            self.__italic = value
            self._update_text_surface()

    def set_alpha(self, value: int) -> None:
        self.__alpha = value
        if self.__text_surface is not None:
            self.__text_surface.set_alpha(self.get_alpha())

    def get_width(self) -> int:
        return self.__text_surface.get_width() if self.__text_surface is not None else 0

    def get_height(self) -> int:
        return self.__text_surface.get_height() if self.__text_surface is not None else 0

    # 画出
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible() and self.__text_surface is not None:
            _surface.blit(self.__text_surface, Coordinates.add(self.pos, offSet, (-self.__outline_thickness, -self.__outline_thickness)))


# 动态文字类
class ResizeWhenHoveredTextSurface(TextSurface):
    def __init__(
        self,
        text: str,
        x: int_f,
        y: int_f,
        original_size: int_f,
        size_when_hovered: int_f,
        _color: color_liked = Colors.BLACK,
        _bold: bool = False,
        _italic: bool = False,
    ) -> None:
        super().__init__(text, x, y, original_size, _color, _bold, _italic)
        self.__text_when_hovered = TextSurface(text, 0, 0, size_when_hovered, _color, _bold, _italic)
        self.__text_when_hovered.set_center(self.centerx, self.centery)
        self.__is_hovered: bool = False

    def set_color(self, _color: color_liked) -> None:
        super().set_color(_color)
        self.__text_when_hovered.set_color(_color)

    def set_left(self, value: int_f) -> None:
        super().set_left(value)
        self.__text_when_hovered.set_centerx(self.centerx)

    def set_top(self, value: int_f) -> None:
        super().set_top(value)
        self.__text_when_hovered.set_centery(self.centery)

    def set_text(self, value: str) -> None:
        super().set_text(value)
        self.__text_when_hovered.set_text(value)

    def set_font_size(self, value: int) -> None:
        super().set_font_size(value)
        self.__text_when_hovered.set_font_size(value)

    def set_bold(self, value: bool) -> None:
        super().set_bold(value)
        self.__text_when_hovered.set_bold(value)

    def set_italic(self, value: bool) -> None:
        super().set_italic(value)
        self.__text_when_hovered.set_italic(value)

    def set_alpha(self, value: int) -> None:
        super().set_alpha(value)
        self.__text_when_hovered.set_alpha(value)

    # 设置轮廓粗细
    def set_outline_thickness(self, _thickness: int) -> None:
        super().set_outline_thickness(_thickness)
        self.__text_when_hovered.set_outline_thickness(_thickness)

    # 设置轮廓颜色
    def set_outline_color(self, _color: color_liked) -> None:
        super().set_outline_color(_color)
        self.__text_when_hovered.set_outline_color(_color)

    # 关闭轮廓渲染
    def disable_outline(self) -> None:
        super().disable_outline()
        self.__text_when_hovered.disable_outline()

    # 用于检测触碰的快捷
    def has_been_hovered(self) -> bool:
        return self.__is_hovered

    # 画出
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            self.__is_hovered = self.is_hovered(offSet)
            if not self.__is_hovered:
                super().display(_surface, offSet)
            else:
                self.__text_when_hovered.display(_surface, offSet)
        else:
            self.__is_hovered = False


# 用于静态图片的surface
class StaticImage(AdvancedAbstractCachingImageSurface):
    def __init__(self, img: PoI, x: int_f, y: int_f, width: int_f = -1, height: int_f = -1, tag: str = ""):
        super().__init__(Images.quickly_load(img), x, y, width, height, tag)
        self.__is_flipped_horizontally: bool = False
        self.__is_flipped_vertically: bool = False
        self.__crop_rect: Rectangle | None = None
        self.__bounding_rect: Rectangle = Rectangle(0, 0, 0, 0)
        self.__no_cropping_needed: bool = False

    # 截图的范围
    @property
    def crop_rect(self) -> Rectangle | None:
        return self.__crop_rect

    def get_crop_rect(self) -> Rectangle | None:
        return self.__crop_rect

    def disable_cropping(self) -> None:
        self.__no_cropping_needed = True

    def set_crop_rect(self, rect: Rectangle | None) -> None:
        if not Rectangles.equal(self.__crop_rect, rect):
            self.__crop_rect = rect
            self._need_update = True

    # 反转原图，并打上已反转的标记
    def flip(self, horizontal: bool = True, vertical: bool = False) -> None:
        if horizontal is True:
            self.__is_flipped_horizontally = not self.__is_flipped_horizontally
            self._need_update = True
        if vertical is True:
            self.__is_flipped_vertically = not self.__is_flipped_vertically
            self._need_update = True

    # 如果不处于反转状态，则反转
    def flip_if_not(self, horizontal: bool = True, vertical: bool = False) -> None:
        if horizontal is True and not self.__is_flipped_horizontally:
            self.__is_flipped_horizontally = True
            self._need_update = True
        if vertical is True and not self.__is_flipped_vertically:
            self.__is_flipped_vertically = True
            self._need_update = True

    # 反转回正常状态
    def flip_back_to_normal(self) -> None:
        if self.__is_flipped_horizontally is True:
            self.__is_flipped_horizontally = False
            self._need_update = True
        if self.__is_flipped_vertically is True:
            self.__is_flipped_vertically = False
            self._need_update = True

    # 返回一个复制品
    def copy(self, deep_copy: bool = True) -> "StaticImage":
        return StaticImage(self.get_image_copy() if deep_copy else self._get_image_reference(), self.x, self.y, self.get_width(), self.get_height())

    @staticmethod
    def new_place_holder() -> "StaticImage":
        return StaticImage("<NULL>", 0, 0)

    # 获取切割后的图片的rect
    def get_bounding_rect(self) -> Rectangle:
        # 如果图片需要更新，则先更新
        if self._need_update is True:
            self._update_img()
        return self.__bounding_rect

    # 更新图片
    def _update_img(self) -> None:
        # 改变尺寸
        imgTmp = (
            Images.smoothly_resize(self._get_image_reference(), self.size) if Setting.get_antialias() else Images.resize(self._get_image_reference(), self.size)
        )
        # 翻转图片
        if self.__is_flipped_horizontally is True or self.__is_flipped_vertically is True:
            imgTmp = Images.flip(imgTmp, self.__is_flipped_horizontally, self.__is_flipped_vertically)
        if not self.__no_cropping_needed:
            # 获取切割rect
            rect: Rectangle = Rectangles.create(imgTmp.get_bounding_rect())
            if self.width != rect.width or self.height != rect.height or self.__crop_rect is not None:
                if self.__crop_rect is not None:
                    new_x: int = max(rect.x, self.__crop_rect.x)
                    new_y: int = max(rect.y, self.__crop_rect.y)
                    rect.move_to((new_x, new_y))
                    rect.set_size(min(rect.right, self.__crop_rect.right) - new_x, min(rect.bottom, self.__crop_rect.bottom) - new_y)
                self.set_local_pos(rect.x, rect.y)
                self.__bounding_rect.move_to(rect.get_pos())
                self.__bounding_rect.set_size(rect.get_width(), rect.get_height())
                self._processed_img = imgTmp.subsurface(self.__bounding_rect.get_rect())
            else:
                self._processed_img = imgTmp
                self.__bounding_rect = Rectangles.create(self._processed_img.get_bounding_rect())
        else:
            self._processed_img = imgTmp
            self.__bounding_rect = Rectangles.create(self._processed_img.get_bounding_rect())
        if self._alpha < 255:
            self._processed_img.set_alpha(self._alpha)
        self._need_update = False


# 需要移动的动态图片
class MovableStaticImage(StaticImage):
    def __init__(
        self,
        img: PoI,
        default_x: int_f,
        default_y: int_f,
        target_x: int_f,
        target_y: int_f,
        move_speed_x: int_f,
        move_speed_y: int_f,
        width: int_f = -1,
        height: int_f = -1,
        tag: str = "",
    ):
        super().__init__(img, default_x, default_y, width, height, tag)
        self.__default_x: int = self.x
        self.__default_y: int = self.y
        self.__target_x: int = int(target_x)
        self.__target_y: int = int(target_y)
        self.__move_speed_x: int = int(move_speed_x)
        self.__move_speed_y: int = int(move_speed_y)
        self.__is_moving_toward_target: bool = False

    # 返回一个复制
    def copy(self, deep_copy: bool = True) -> "MovableStaticImage":
        return MovableStaticImage(
            self.get_image_copy() if deep_copy else self._get_image_reference(),
            self.x,
            self.y,
            self.__target_x,
            self.__target_y,
            self.__move_speed_x,
            self.__move_speed_y,
            self.get_width(),
            self.get_height(),
            self.tag,
        )

    # 设置目标坐标
    def set_target(self, target_x: int_f, target_y: int_f, move_speed_x: int_f, move_speed_y: int_f) -> None:
        self.__target_x = int(target_x)
        self.__target_y = int(target_y)
        self.__move_speed_x = int(move_speed_x)
        self.__move_speed_y = int(move_speed_y)

    # 控制
    def switch(self) -> None:
        self.__is_moving_toward_target = not self.__is_moving_toward_target

    def move_toward(self) -> None:
        self.__is_moving_toward_target = True

    def move_back(self) -> None:
        self.__is_moving_toward_target = False

    # 重置坐标
    def reset_position(self) -> None:
        self.set_pos(self.__default_x, self.__default_y)

    # 移动状态
    def is_moving_toward_target(self) -> bool:
        return self.__is_moving_toward_target

    def has_reached_target(self) -> bool:
        return (
            self.x == self.__target_x and self.y == self.__target_y
            if self.__is_moving_toward_target is True
            else self.x == self.__default_x and self.y == self.__default_y
        )

    # 画出
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            super().display(_surface, offSet)
            if self.__is_moving_toward_target is True:
                if self.__default_x < self.__target_x:
                    if self.x < self.__target_x:
                        self.move_right(self.__move_speed_x)
                    if self.x > self.__target_x:
                        self.set_left(self.__target_x)
                elif self.__default_x > self.__target_x:
                    if self.x > self.__target_x:
                        self.move_left(self.__move_speed_x)
                    if self.x < self.__target_x:
                        self.set_left(self.__target_x)
                if self.__default_y < self.__target_y:
                    if self.y < self.__target_y:
                        self.move_downward(self.__move_speed_y)
                    if self.y > self.__target_y:
                        self.set_top(self.__target_y)
                elif self.__default_y > self.__target_y:
                    if self.y > self.__target_y:
                        self.move_upward(self.__move_speed_y)
                    if self.y < self.__target_y:
                        self.set_top(self.__target_y)
            else:
                if self.__default_x < self.__target_x:
                    if self.x > self.__default_x:
                        self.move_left(self.__move_speed_x)
                    if self.x < self.__default_x:
                        self.set_left(self.__default_x)
                elif self.__default_x > self.__target_x:
                    if self.x < self.__default_x:
                        self.move_right(self.__move_speed_x)
                    if self.x > self.__default_x:
                        self.set_left(self.__default_x)
                if self.__default_y < self.__target_y:
                    if self.y > self.__default_y:
                        self.move_upward(self.__move_speed_y)
                    if self.y < self.__default_y:
                        self.set_top(self.__default_y)
                elif self.__default_y > self.__target_y:
                    if self.y < self.__default_y:
                        self.move_downward(self.__move_speed_y)
                    if self.y > self.__default_y:
                        self.set_top(self.__default_y)


# gif图片管理
class AnimatedImage(AdvancedAbstractImageSurface):
    def __init__(self, imgList: tuple[StaticImage, ...], x: int_f, y: int_f, width: int_f, height: int_f, fps: int_f, tag: str = "") -> None:
        super().__init__(imgList, x, y, width, height, tag)
        self.__imgId: int = 0
        self.__fps: int = max(int(fps), 0)
        self.__countDown: int = 0

    # get frame per second of
    def get_fps(self) -> int:
        return self.__fps

    # set frame per second of
    def set_fps(self, value: int_f) -> None:
        self.__fps = max(int(value), 0)

    # 返回一个复制
    def copy(self, deep_copy: bool = True) -> "AnimatedImage":
        return AnimatedImage(
            self.get_image_copy() if deep_copy else self._get_image_reference(), self.x, self.y, self.get_width(), self.get_height(), self.__fps, self.tag
        )

    # 当前图片
    def _get_image_reference(self) -> tuple[StaticImage, ...]:
        return super()._get_image_reference()  # type: ignore

    @property
    def current_image(self) -> StaticImage:
        self._get_image_reference()[self.__imgId].set_size(self.get_width(), self.get_height())
        self._get_image_reference()[self.__imgId].set_alpha(self._alpha)
        return self._get_image_reference()[self.__imgId]

    # 获取图片非透明部分的rect
    def get_bounding_rect(self) -> Rectangle:
        return self.current_image.get_bounding_rect()

    # 展示
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            self.current_image.display(_surface, Coordinates.add(self.pos, offSet))
            if self.__countDown >= 1000 // self.__fps:
                self.__countDown = 0
                self.__imgId += 1
                if self.__imgId >= len(self._get_image_reference()):
                    self.__imgId = 0
            else:
                self.__countDown += Display.get_delta_time()


# 基于ImageSurface的内部窗口
class AbstractFrame(AdvancedAbstractImageSurface, metaclass=ABCMeta):
    # 放大指示图标
    __rescale_icon_0: StaticImage = StaticImage.new_place_holder()
    __rescale_icon_45: StaticImage = StaticImage.new_place_holder()
    __rescale_icon_90: StaticImage = StaticImage.new_place_holder()
    __rescale_icon_135: StaticImage = StaticImage.new_place_holder()
    __rescale_icon_initialized: bool = False

    def __init__(self, x: int_f, y: int_f, width: int_f, height: int_f, tag: str = ""):
        super().__init__(None, x, y, width, height, tag=tag)
        # 鼠标触碰bar时的相对坐标
        self.__mouse_hovered_offset_pos: tuple[number, number] | None = None
        # 放大方向
        self.__rescale_directions: dict[str, bool] = {"left": False, "right": False, "top": False, "bottom": False}
        # 是否重新放大窗口
        self.__if_regenerate_window: bool = True
        # 用于修改并展示内容的surface
        self._content_surface: ImageSurface = Surfaces.NULL
        # 是否需要更新用于展示内容的surface
        self._if_update_needed: bool = True
        # 是否正在移动本地坐标
        self.__if_move_local_pos: bool = False

    # 窗口上方bar的高度
    @staticmethod
    def _get_bar_height() -> int:
        return Display.get_height() // 50

    # 窗口线条的粗细
    @staticmethod
    def _get_outline_thickness() -> int:
        return Display.get_height() // 500

    # 更新窗口
    def __update_window_frame(self) -> None:
        if self.__if_regenerate_window is True:
            self._set_image(Surfaces.colored(self.size, Colors.WHITE))
            Draw.rect(self._get_image_reference(), Colors.LIGHT_GRAY, (ORIGIN, (self.get_width(), self._get_bar_height())))
            Draw.rect(self._get_image_reference(), Colors.GRAY, (ORIGIN, self.size), self._get_outline_thickness())
            # 初始化图标
            if not self.__rescale_icon_initialized:
                # 更新尺寸
                theWidth: int = self._get_bar_height() * 3 // 2
                theHeight: int = self._get_bar_height() * 3 // 2
                self.__rescale_icon_0.set_size(theWidth, theHeight)
                self.__rescale_icon_45.set_size(theWidth, theHeight)
                self.__rescale_icon_90.set_size(theWidth, theHeight)
                self.__rescale_icon_135.set_size(theWidth, theHeight)
                # 更新图片
                theImg: ImageSurface = Images.quickly_load("<&ui>rescale.png")
                self.__rescale_icon_0.update_image(theImg)
                self.__rescale_icon_45.update_image(theImg)
                self.__rescale_icon_90.update_image(theImg)
                self.__rescale_icon_135.update_image(theImg)
                # 旋转
                self.__rescale_icon_45.rotate(45)
                self.__rescale_icon_45.scale_n_times(1.5)
                self.__rescale_icon_90.rotate(90)
                self.__rescale_icon_135.rotate(135)
                self.__rescale_icon_135.scale_n_times(1.5)
                # 完成
                self.__rescale_icon_initialized = True
            # 更新flag
            self.__if_regenerate_window = False

    # 更新内容surface（子类必须实现该功能）
    @abstractmethod
    def _update(self) -> None:
        EXCEPTION.fatal("_update()", 1)

    # 设置宽度
    def set_width(self, value: int_f) -> None:
        super().set_width(value)
        self.__if_regenerate_window = True
        self._if_update_needed = True

    # 设置高度
    def set_height(self, value: int_f) -> None:
        super().set_height(value)
        self.__if_regenerate_window = True
        self._if_update_needed = True

    # 角落是否被触碰
    def __is_corner_hovered(self, side1: str, side2: str | None = None) -> bool:
        if side2 is None:
            return bool(self.__rescale_directions[side1])
        else:
            return self.__rescale_directions[side1] is True and self.__rescale_directions[side2] is True

    # 是否内容窗口是任何事件被触发（默认为否，如果有需要可以在子类内重写）
    def _any_content_container_event(self) -> bool:
        return False

    # 展示
    def present_on(self, _surface: ImageSurface) -> None:
        # 如果未被隐藏
        if self.is_visible():
            # 如果鼠标之前没有被按下
            if not Controller.mouse.get_pressed_previously(0):
                abs_x = Controller.mouse.x - self.x
                abs_y = Controller.mouse.y - self.y
                if (
                    -self._get_outline_thickness() <= abs_x <= self.width + self._get_outline_thickness()
                    and -self._get_outline_thickness() <= abs_y <= self.height + self._get_outline_thickness()
                ):
                    # 查看鼠标是否触碰窗口的边缘
                    self.__rescale_directions["left"] = abs_x < self._get_outline_thickness() * 2
                    self.__rescale_directions["right"] = -self._get_outline_thickness() * 2 < abs_x - self.width
                    self.__rescale_directions["top"] = abs_y < self._get_outline_thickness() * 2
                    self.__rescale_directions["bottom"] = -self._get_outline_thickness() * 2 < abs_y - self.height
                else:
                    for key in self.__rescale_directions:
                        self.__rescale_directions[key] = False
                # 如果鼠标按住bar
                if Controller.mouse.get_pressed(0) and True not in self.__rescale_directions.values():
                    if Controller.mouse.is_in_rect(self.x, self.y, self.get_width(), self._get_bar_height()):
                        self.__mouse_hovered_offset_pos = Coordinates.subtract(Controller.mouse.get_pos(), self.pos)
                    elif self.is_hovered() and not self._any_content_container_event():
                        self.__if_move_local_pos = True
                        self.__mouse_hovered_offset_pos = Coordinates.subtract(Controller.mouse.get_pos(), self.local_pos)
            elif Controller.mouse.get_pressed(0):
                # 根据鼠标位置修改本地坐标
                if self.__mouse_hovered_offset_pos is not None:
                    if self.__if_move_local_pos is True:
                        self.locally_move_to(Coordinates.subtract(Controller.mouse.get_pos(), self.__mouse_hovered_offset_pos))
                    # 移动窗口
                    else:
                        self.move_to(Coordinates.subtract(Controller.mouse.get_pos(), self.__mouse_hovered_offset_pos))
                else:
                    # 向左放大
                    if self.__rescale_directions["left"] is True:
                        if Controller.mouse.x < self.right:
                            self.set_width(self.right - Controller.mouse.x)
                            self.set_left(Controller.mouse.x)
                        else:
                            self.__rescale_directions["left"] = False
                            self.__rescale_directions["right"] = True
                    # 向右放大
                    if self.__rescale_directions["right"] is True:
                        if Controller.mouse.x > self.left:
                            self.set_width(Controller.mouse.x - self.left)
                        else:
                            self.__rescale_directions["right"] = False
                            self.__rescale_directions["left"] = True
                    # 向上放大
                    if self.__rescale_directions["top"] is True:
                        if Controller.mouse.y < self.bottom - self._get_bar_height():
                            self.set_height(self.bottom - Controller.mouse.y)
                            self.set_top(Controller.mouse.y)
                        else:
                            self.__rescale_directions["top"] = False
                            self.__rescale_directions["bottom"] = True
                    # 向下放大
                    if self.__rescale_directions["bottom"] is True:
                        if Controller.mouse.y > self.top:
                            self.set_height(Controller.mouse.y - self.top)
                        else:
                            self.__rescale_directions["bottom"] = False
                            self.__rescale_directions["top"] = True
            else:
                for key in self.__rescale_directions:
                    self.__rescale_directions[key] = False
                self.__mouse_hovered_offset_pos = None
                self.__if_move_local_pos = False
            # 更新窗口
            self.__update_window_frame()
            # 画出窗口
            _surface.blit(self._get_image_reference(), self.pos)
            # 如果需要，则先更新内容surface
            if self._if_update_needed is True:
                self._update()
            # 画出内容
            if Surfaces.is_not_null(self._content_surface):
                # 计算坐标
                abs_pos_x: int = self.x + self._get_outline_thickness()
                abs_pos_y: int = self.y + self._get_bar_height() + self._get_outline_thickness()
                real_local_x: int = 0
                real_local_y: int = 0
                if self.local_x < 0:
                    abs_pos_x -= self.local_x
                else:
                    real_local_x = self.local_x
                if self.local_y < 0:
                    abs_pos_y -= self.local_y
                else:
                    real_local_y = self.local_y
                # 计算尺寸
                width_of_sub: int = Numbers.keep_int_in_range(
                    self.get_width() - self._get_outline_thickness() + self.local_x,
                    0,
                    min(self._content_surface.get_width() - real_local_x, self.get_width() - self._get_outline_thickness()),
                )
                height_of_sub: int = Numbers.keep_int_in_range(
                    self.get_height() - self._get_bar_height() - self._get_outline_thickness() + self.local_y,
                    0,
                    min(self._content_surface.get_height() - real_local_y, self.get_height() - self._get_bar_height() - self._get_outline_thickness()),
                )
                # 展示内容
                if width_of_sub > 0 and height_of_sub > 0:
                    _surface.blit(self._content_surface.subsurface(real_local_x, real_local_y, width_of_sub, height_of_sub), (abs_pos_x, abs_pos_y))
            # 画出放大icon
            if True in self.__rescale_directions.values():
                # 如果鼠标触碰了边框，则旋转放大icon至对应角度
                if self.__is_corner_hovered("top", "right") or self.__is_corner_hovered("bottom", "left"):
                    rescale_icon = self.__rescale_icon_45
                elif self.__is_corner_hovered("top", "left") or self.__is_corner_hovered("bottom", "right"):
                    rescale_icon = self.__rescale_icon_135
                elif self.__is_corner_hovered("top") or self.__is_corner_hovered("bottom"):
                    rescale_icon = self.__rescale_icon_90
                else:
                    rescale_icon = self.__rescale_icon_0
                rescale_icon.set_center(Controller.mouse.x, Controller.mouse.y)
                rescale_icon.draw(_surface)


# 确认窗口
class ConfirmationDialogBox:
    def __init__(self, title: str, message: str, icon: str = "question") -> None:
        self.__title: str = title
        self.__message: str = message
        self.__icon: str = icon

    @staticmethod
    def ask(title: str, message: str, icon: str = "question") -> bool:
        return messagebox.askyesno(title, message, icon=icon)

    def set_title(self, title: str) -> None:
        self.__title = title

    def set_message(self, message: str) -> None:
        self.__message = message

    def set_icon(self, icon: str) -> None:
        self.__icon = icon

    def show(self) -> bool:
        return self.ask(self.__title, self.__message, self.__icon)


# 警告窗口
class LinpgVersionChecker:
    def __init__(self, action: str, recommended_revision: int, recommended_patch: int, recommended_version: int = 3) -> None:
        if not Info.ensure_linpg_version(action, recommended_revision, recommended_patch, recommended_version):
            if not ConfirmationDialogBox.ask(
                Lang.get_text("Global", "warning"),
                Lang.get_text("LinpgVersionIncorrectMessage").format(f"3.{recommended_revision}.{recommended_patch}", Info.get_current_version()),
            ):
                from sys import exit

                exit()


# 视频抽象类
class AbstractVideo(ABC):
    def __init__(self, path: str, buffer_num: int, play_range: tuple[int, int] = (0, -1)):
        self._path: str = path
        # 确保路径存在且模块已经正常初始化
        Videos.validation(self._path)
        """视频流"""
        self.__video_stream: cv2.VideoCapture | None = None
        self._frame_rate: int = 0
        self._frame_buffer_num: int = buffer_num
        """参数"""
        # 确保play_range参数合法
        if len(play_range) < 2:
            EXCEPTION.fatal("The length of play_range parameter must >= 2.")
        self._starting_point: int = play_range[0]
        self._ending_point: int = play_range[1]
        self.__stopped: bool = False
        self.__started: bool = False
        self.__frame_index_to_set: int = -1

    # 初始化
    def _init(self) -> None:
        # 加载视频流
        self.__video_stream = cv2.VideoCapture(self._path)
        self.__video_stream.set(cv2.CAP_PROP_BUFFERSIZE, self._frame_buffer_num)
        # 如果设置了起点，则为视频设置开始播放的位置
        if self._starting_point > 0:
            self.set_frame_index(self._starting_point)
        # 获取秒帧数
        self._frame_rate = round(self.__video_stream.get(cv2.CAP_PROP_FPS))
        # 改变用于辨识视频是否开始播放的flag
        self.__started = True

    def set_starting_point(self, index: int) -> None:
        self._starting_point = index

    # 每秒帧数
    @property
    def fps(self) -> int:
        return self._frame_rate

    @property
    def frame_rate(self) -> int:
        return self._frame_rate

    def get_frame_rate(self) -> int:
        return self._frame_rate

    # 总帧数
    @property
    def frame_num(self) -> int:
        return self.get_frame_num()

    def get_frame_num(self) -> int:
        return int(self.__video_stream.get(cv2.CAP_PROP_FRAME_COUNT)) if self.__video_stream is not None else 0

    # 当前帧坐标
    @property
    def frame_index(self) -> int:
        return self.get_frame_index()

    def get_frame_index(self) -> int:
        return int(self.__video_stream.get(cv2.CAP_PROP_POS_FRAMES)) if self.__video_stream is not None else 0

    def set_frame_index(self, num: int) -> None:
        if num > self.get_frame_num():
            EXCEPTION.fatal(f'Frame index "{num}" is out of range "{self.get_frame_num()}"')
        elif num < 0:
            EXCEPTION.fatal("You cannot set negative frame index.")
        else:
            self.__frame_index_to_set = num

    # 已经播放的百分比
    def get_percentage_played(self) -> float:
        return self.get_frame_index() / max(self.get_frame_num(), 1)

    # 停止
    def stop(self) -> None:
        self.__stopped = True
        if self.__video_stream is not None:
            self.__video_stream.release()
            self.__video_stream = None

    # 是否已经开始
    @property
    def started(self) -> bool:
        return self.__started

    # 重新开始
    def restart(self) -> None:
        self.__stopped = False
        self._init()

    # 播放范围
    @property
    def play_range(self) -> tuple[int, int]:
        return self._starting_point, self._ending_point

    # 是否还在播放
    def is_playing(self) -> bool:
        return self.__started is True and self.__stopped is not True

    # 把画面画到surface上
    def draw(self, _surface: ImageSurface) -> None:
        if not self.__started:
            self._init()
        if not self.__stopped:
            if self.__frame_index_to_set >= 0:
                self.__video_stream.set(cv2.CAP_PROP_POS_FRAMES, self.__frame_index_to_set)  # type: ignore
                self.__frame_index_to_set = -1
            # 处理当前Frame
            if (current_frame := self.__video_stream.read()[1]) is not None:  # type: ignore
                current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
                if current_frame.shape[0] != _surface.get_width() or current_frame.shape[1] != _surface.get_height():
                    current_frame = cv2.resize(current_frame, _surface.get_size())
                pygame.surfarray.blit_array(_surface, current_frame.swapaxes(0, 1))


# 类似Wallpaper Engine的视频背景，但音乐不与画面同步
class VideoSurface(AbstractVideo):
    def __init__(
        self,
        path: str,
        loop: bool = True,
        with_audio: bool = True,
        play_range: tuple[int, int] = (0, -1),
        buffer_num: int = 10,
        cache_key: str | None = None,
    ) -> None:
        super().__init__(path, buffer_num, play_range)
        self.__loop: bool = loop
        self.__looped_times: int = 0
        self.__audio: Sound | None = Sounds.load_from_video(path, cache_key=cache_key) if with_audio is True else None
        self.__audio_channel: SoundChannel | None = None

    # 返回一个复制
    def copy(self) -> "VideoSurface":
        with_audio = True if self.__audio is not None else False
        new_t = VideoSurface(self._path, self.__loop, with_audio, self.play_range)
        if with_audio is True:
            new_t.set_volume(self.get_volume())
        return new_t

    # 音量
    @property
    def volume(self) -> float:
        return self.get_volume()

    def get_volume(self) -> float:
        return self.__audio.get_volume() if self.__audio is not None else -1.0

    def set_volume(self, value: float) -> None:
        if self.__audio is not None:
            self.__audio.set_volume(value)

    def stop(self) -> None:
        super().stop()
        if self.__audio_channel is not None:
            self.__audio_channel.stop()

    def _init(self) -> None:
        super()._init()
        self.__audio_channel = Sounds.find_channel()

    # 把画面画到surface上
    def draw(self, _surface: ImageSurface) -> None:
        super().draw(_surface)
        if self.is_playing():
            # 播放背景音乐
            if self.__audio_channel is not None and not self.__audio_channel.get_busy() and self.__audio is not None:
                self.__audio_channel.play(self.__audio)
            # 检测循环
            if self.get_frame_index() < self.get_frame_num():
                # 如果有设置末端且当前已经超出末端
                if 0 <= self._ending_point <= self.get_frame_index():
                    self.__looped_times += 1
                    if not self.__loop:
                        self.stop()
                    else:
                        self.set_frame_index(self._starting_point)
            else:
                # 如果不需要再次循环
                if not self.__loop:
                    self.stop()
                # 如果需要再次循环，则从self._starting_point重新开始
                else:
                    self.set_frame_index(self._starting_point)


# 视频播放器，强制视频和音乐同步
class VideoPlayer(AbstractVideo):
    def __init__(self, path: str, buffer_num: int = 6):
        super().__init__(path, buffer_num=buffer_num)
        self.__clock = pygame.time.Clock()
        self.__audio_path: str = ""

    # 返回一个复制
    def copy(self) -> "VideoPlayer":
        return VideoPlayer(self._path, self._frame_buffer_num)

    # 设置帧坐标
    def set_frame_index(self, num: int) -> None:
        super().set_frame_index(num)
        Music.restart()
        Music.set_pos(self.get_frame_index() / self._frame_rate)

    def stop(self) -> None:
        super().stop()
        Music.unload()
        os.remove(self.__audio_path)

    def _init(self) -> None:
        super()._init()
        self.__audio_path = Music.load_from_video(self._path)
        Music.play()

    # 提前初始化
    def pre_init(self) -> None:
        self._init()

    # 把画面画到surface上
    def draw(self, _surface: ImageSurface) -> None:
        super().draw(_surface)
        if self.is_playing():
            if (
                self.get_frame_index() <= self.get_frame_num()
                and (current_frame_index_based_on_music := round(Music.get_pos() * self._frame_rate / 1000)) <= self.get_frame_num()
            ):
                frame_difference: int = current_frame_index_based_on_music - self.get_frame_index()
                # 如果播放速度太慢
                if frame_difference >= self._frame_buffer_num:
                    self.set_frame_index(current_frame_index_based_on_music)
                # 如果播放速度太快
                elif frame_difference < 0:
                    self.__clock.tick(self._frame_rate)
            else:
                self.stop()


class SpriteImage:
    def __init__(self, img_path: str) -> None:
        # 路径
        self.__PATH: str = img_path
        # 加载Sprite图
        self.__SHEET: ImageSurface = Images.quickly_load(self.__PATH)
        # 加载Sprite图的数据
        self.__RECT_DICTIONARY: dict[str, list[int] | list[list[int]]] = {}
        if not self.__PATH.startswith("<"):
            self.__RECT_DICTIONARY.update(Config.load_file(self.__PATH + ".linpg.meta"))
        elif self.__PATH != "<NULL>":
            self.__RECT_DICTIONARY.update(Config.load_file(Images.generate_path_according_to_prefix(self.__PATH).removesuffix(".zip") + ".linpg.meta"))

    # get the image / images based on given name
    def get(self, name: str) -> ImageSurface | tuple[ImageSurface, ...]:
        _rect: list[int] | list[list[int]] = self.__RECT_DICTIONARY[name]
        return self.__SHEET.subsurface(_rect) if not isinstance(_rect[0], list) else tuple(self.__SHEET.subsurface(_data) for _data in _rect)  # type: ignore

    # if given name exists in the sprite
    def contain(self, name: str) -> bool:
        return name in self.__RECT_DICTIONARY

    # return all the images in the form of dict
    def to_dict(self) -> dict[str, ImageSurface | tuple[ImageSurface, ...]]:
        # 将所有Sprite图上的图片以subsurface的形式append进字典中
        result: dict[str, ImageSurface | tuple[ImageSurface, ...]] = {}
        for key in self.__RECT_DICTIONARY:
            result[key] = self.get(key)
        # 将结果以字典的形式返回
        return result

    # return a copy
    def copy(self) -> "SpriteImage":
        return SpriteImage(self.__PATH)

    # 拆分一个未知格式的像素图，字典key为动作名称，value分别为xStart, yStart, width, height, frameCount
    @staticmethod
    def split_sprite_image(_image_path: str, output_directory: str, _data: dict[str, tuple[int, int, int, int, int]]) -> None:
        _sprite_image: ImageSurface = Images.load(_image_path)
        Files.delete_if_exist(output_directory)
        os.mkdir(output_directory)
        for key, value in _data.items():
            _out_path: str = os.path.join(output_directory, key)
            os.mkdir(_out_path)
            for i in range(value[4]):
                Images.save(_sprite_image.subsurface((value[0] + i * value[2], value[1], value[2], value[3])), os.path.join(_out_path, f"{key}_{i}.png"))

    # 处理图片并返回对应的数据
    @staticmethod
    def __process_image(_path: str, max_block_size: list[int], minimize_pixels: bool) -> dict:
        _image_data: dict = {}
        _img: ImageSurface = Images.quickly_load(_path)
        if not minimize_pixels:
            # 确认最大尺寸
            if max_block_size[0] < _img.get_width():
                max_block_size[0] = _img.get_width()
            if max_block_size[1] < _img.get_height():
                max_block_size[1] = _img.get_height()
        else:
            # 获取图片的透明bounding
            _bounding: RectObject = _img.get_bounding_rect()
            # 确认最大尺寸
            if max_block_size[0] < _bounding.width:
                max_block_size[0] = _bounding.width
            if max_block_size[1] < _bounding.height:
                max_block_size[1] = _bounding.height
            # 写入bounding尺寸
            _image_data["bounding"] = _bounding
        # 放入图片
        _image_data["img"] = _img
        return _image_data

    # 将图片渲染到sheet上等待保存，并生产rect的信息
    @staticmethod
    def __put_and_document(_pos: tuple[int, int], minimize_pixels: bool, value: dict, sprite_surface: ImageSurface) -> list[int]:
        _rect: list[int]
        if not minimize_pixels:
            sprite_surface.blit(value["img"], _pos)
            # 记录下图片的最终尺寸和图片在sprite图上的坐标
            _rect = [_pos[0], _pos[1], value["img"].get_width(), value["img"].get_height()]
        else:
            _bounding = value["bounding"]
            sprite_surface.blit(value["img"].subsurface(_bounding), _pos)
            # 记录下图片的最终尺寸和图片在sprite图上的坐标
            _rect = [_pos[0], _pos[1], _bounding.width, _bounding.height]
        return _rect

    # 制作新的Sprite图片合集
    @classmethod
    def generate(
        cls,
        img_folder_path: str,
        minimize_pixels: bool = False,
        actionOnSameRow: bool = False,
        universal_width: int | None = None,
        universal_height: int | None = None,
        additional_padding: int = 0,
        resultFileType: str = "png",
    ) -> None:
        # 储存数据的字典
        _cache: dict[str, Any] = {}
        _out: dict[str, Any] = {}
        # 最大尺寸
        max_block_size: list[int] = [0, 0]
        # 图片总数
        _count: int = 0
        # 最大动作数
        _max_action_count: int = 0
        # 历遍目标文件夹中的图片
        for _path in Files.natural_sort(glob(os.path.join(img_folder_path, "*"))):
            _name: str
            if os.path.isdir(_path):
                _name = os.path.basename(_path)
                _cache[_name] = [
                    cls.__process_image(_imgPath, max_block_size, minimize_pixels) for _imgPath in Files.natural_sort(glob(os.path.join(_path, "*")))
                ]
                _count += len(_cache[_name])
                _max_action_count = max(_max_action_count, len(_cache[_name]))
            elif _path.endswith(".png") or _path.endswith(".jpg"):
                _name = os.path.basename(_path)
                _name = _name[: _name.index(".")]
                _cache[_name] = cls.__process_image(_path, max_block_size, minimize_pixels)
                _count += 1
                _max_action_count = max(_max_action_count, 1)
        # 最终sprite图
        sprite_surface: ImageSurface = Surfaces.NULL
        # 如果设置了固定尺寸
        if universal_width is not None:
            max_block_size[0] = universal_width
        if universal_height is not None:
            max_block_size[1] = universal_height
        max_block_size[0] += additional_padding * 2
        max_block_size[1] += additional_padding * 2
        # 同一动作可以不同行，方便最小化图片
        if not actionOnSameRow:
            # 列数
            columns: int = math.ceil(math.sqrt(_count))
            # 行数
            rows: int = _count // columns if _count % columns == 0 else _count // columns + 1  # math.ceil(_count / columns)
            # 为最终sprite图获取内存空间
            sprite_surface = Surfaces.transparent((columns * max_block_size[0], rows * max_block_size[1]))
            # 当前图片index
            index: int = 0
            # 将图片刷到sprite图上
            for key, value in _cache.items():
                if isinstance(value, dict):
                    _out["animations"][key] = cls.__put_and_document(
                        ((index % columns) * max_block_size[0] + additional_padding, index // columns * max_block_size[1] + additional_padding),
                        minimize_pixels,
                        value,
                        sprite_surface,
                    )
                    index += 1
                else:
                    for i in range(len(value)):
                        _out["animations"][i] = cls.__put_and_document(
                            ((index % columns) * max_block_size[0] + additional_padding, index // columns * max_block_size[1] + additional_padding),
                            minimize_pixels,
                            value[i],
                            sprite_surface,
                        )
                        index += 1
        # 同一动作必须同行，方便读取管理
        else:
            # 为最终sprite图获取内存空间
            sprite_surface = Surfaces.transparent((_max_action_count * max_block_size[0], len(_cache) * max_block_size[1]))
            current_row: int = 0
            current_column: int = 0
            is_universal_size: bool = universal_width is not None and universal_height is not None
            if is_universal_size is True:
                _out["size"] = [max_block_size[0], max_block_size[1]]
            _out["animations"] = {}
            # 将图片刷到sprite图上
            for key in sorted(_cache, key=lambda k: len(_cache[k]) if isinstance(_cache[k], list) else 1):
                value = _cache[key]
                if isinstance(value, dict):
                    _out["animations"][key] = cls.__put_and_document(
                        (current_column * max_block_size[0] + additional_padding, current_row * max_block_size[1] + additional_padding),
                        minimize_pixels,
                        value,
                        sprite_surface,
                    )
                    if is_universal_size is True:
                        _out["animations"][key] = _out["animations"][key][:2]
                        _out["animations"][key][0] //= max_block_size[0]
                        _out["animations"][key][1] //= max_block_size[1]
                    _out["animations"][key].append(1)
                    current_column += 1
                    if current_column > _max_action_count:
                        current_column = 0
                        current_row += 1
                else:
                    if current_column + len(value) > _max_action_count:
                        current_column = 0
                        current_row += 1
                    _out["animations"][key] = cls.__put_and_document(
                        (current_column * max_block_size[0] + additional_padding, current_row * max_block_size[1] + additional_padding),
                        minimize_pixels,
                        value[0],
                        sprite_surface,
                    )
                    if is_universal_size is True:
                        _out["animations"][key] = _out["animations"][key][:2]
                        _out["animations"][key][0] //= max_block_size[0]
                        _out["animations"][key][1] //= max_block_size[1]
                    _out["animations"][key].append(len(value))
                    current_column += 1
                    for i in range(1, len(value)):
                        cls.__put_and_document(
                            (current_column * max_block_size[0] + additional_padding, current_row * max_block_size[1] + additional_padding),
                            minimize_pixels,
                            value[i],
                            sprite_surface,
                        )
                        current_column += 1
            sprite_surface = sprite_surface.subsurface((0, 0, sprite_surface.get_width(), (current_row + 1) * max_block_size[1]))
        # 保存sprite图
        target_file_name: str = f"{img_folder_path}.{resultFileType}"
        Images.save(sprite_surface, target_file_name)
        # 保存sprite图数据
        Config.save(target_file_name + ".linpg.meta", _out)
