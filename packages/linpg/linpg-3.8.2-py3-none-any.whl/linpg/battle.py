"""
结构:
image -> decoration -> entity -> map -> battle -> editor
"""

from collections import deque

from PIL import ImageSequence as PILImageSequence

from .dialogue import *


# 地图贴图的管理模块
class TileMapImagesModule:
    # 暗度（仅黑夜场景有效，为0时视为白天）
    DARKNESS: int = 0
    # 引擎自带的地图贴图，默认为空的sheet
    DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET: SpriteImage = SpriteImage("<NULL>")
    # 引擎自带的地图贴图是否被加载
    __DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET_INITIALIZED: bool = False
    # 环境
    __ENV_IMAGE_DICT: Final[dict[str, StaticImage | tuple[StaticImage, ...]]] = {}
    __ENV_IMAGE_DICT_DARK: Final[dict[str, StaticImage | tuple[StaticImage, ...]]] = {}
    # 标准Tile尺寸
    TILE_SIZE: int = 0
    TILE_TEMPLE_WIDTH: int = 0
    TILE_TEMPLE_HEIGHT: int = 0

    # 确认sheet已经初始化
    @classmethod
    def init(cls) -> None:
        # 如果SPRITE SHEET未被初始化，则初始化
        if not cls.__DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET_INITIALIZED:
            if os.path.exists(Images.generate_path_according_to_prefix("<!env>tiles.png")):
                cls.DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET = SpriteImage("<!env>tiles.png")
            cls.__DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET_INITIALIZED = True

    # 调整尺寸
    @classmethod
    def update_size(cls, _size: int) -> None:
        cls.TILE_SIZE = _size
        # 调整地图方块尺寸
        for _imgRef in cls.__ENV_IMAGE_DICT.values():
            if not isinstance(_imgRef, tuple):
                _imgRef.set_width_with_original_image_size_locked(cls.TILE_SIZE)
            else:
                for _temp in _imgRef:
                    _temp.set_width_with_original_image_size_locked(cls.TILE_SIZE)
        # 调整黑夜模式下的地图方块尺寸
        for _imgRef in cls.__ENV_IMAGE_DICT_DARK.values():
            if not isinstance(_imgRef, tuple):
                _imgRef.set_width_with_original_image_size_locked(cls.TILE_SIZE)
            else:
                for _temp in _imgRef:
                    _temp.set_width_with_original_image_size_locked(cls.TILE_SIZE)
        # 根据Template计算tile标准尺寸和offset
        cls.TILE_TEMPLE_WIDTH, cls.TILE_TEMPLE_HEIGHT = cls.get_image("template", False).get_bounding_rect().get_size()
        cls.TILE_TEMPLE_HEIGHT = cls.TILE_TEMPLE_HEIGHT * 2 // 5

    # 加载图片
    @classmethod
    def add_image(cls, _id: str) -> None:
        # 确保初始化
        cls.init()
        # 根据id决定如何处理图片加载
        _id = _id.split(":")[0]
        if cls.DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET.contain(_id):
            _temp: list[StaticImage]
            _imgTemp: StaticImage
            if _id not in cls.__ENV_IMAGE_DICT:
                _img: ImageSurface | tuple[ImageSurface, ...] = cls.DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET.get(_id)
                if isinstance(_img, tuple):
                    _temp = [StaticImage(_imgRef, 0, 0) for _imgRef in _img]
                    for _imgRef in _temp:
                        _imgRef.set_width_with_original_image_size_locked(cls.TILE_SIZE)
                    cls.__ENV_IMAGE_DICT[_id] = tuple(_temp)
                else:
                    _imgTemp = StaticImage(_img, 0, 0)
                    _imgTemp.set_width_with_original_image_size_locked(cls.TILE_SIZE)
                    cls.__ENV_IMAGE_DICT[_id] = _imgTemp
            # 如果是夜战模式
            if cls.DARKNESS > 0:
                _imgRefTemp: StaticImage | tuple[StaticImage, ...] = cls.__ENV_IMAGE_DICT[_id]
                if isinstance(_imgRefTemp, tuple):
                    _temp = []
                    for _imgRef in _imgRefTemp:
                        _imgCopy = _imgRef.copy()
                        _imgCopy.add_darkness(cls.DARKNESS)
                        _temp.append(_imgCopy)
                    cls.__ENV_IMAGE_DICT_DARK[_id] = tuple(_temp)
                else:
                    _imgTemp = _imgRefTemp.copy()
                    _imgTemp.add_darkness(cls.DARKNESS)
                    cls.__ENV_IMAGE_DICT_DARK[_id] = _imgTemp
        else:
            EXCEPTION.fatal(f'Cannot find tile map image "{_id}"')

    # 获取图片
    @classmethod
    def get_image(cls, _id: str, darkMode: bool = False) -> StaticImage:
        # 获取参数
        _absId: list[str] = _id.split(":")
        # 尝试获取图片
        result: StaticImage | tuple[StaticImage, ...]
        possible_result: StaticImage | tuple[StaticImage, ...] | None = (
            cls.__ENV_IMAGE_DICT_DARK.get(_absId[0]) if darkMode is True else cls.__ENV_IMAGE_DICT.get(_absId[0])
        )
        if possible_result is not None:
            result = possible_result
        else:
            if Debug.get_developer_mode():
                EXCEPTION.inform(f"Cannot find tile image '{_id}', we will try to load it for you right now, but please by aware.")
            cls.add_image(_absId[0])
            result = cls.__ENV_IMAGE_DICT_DARK[_absId[0]] if darkMode is True else cls.__ENV_IMAGE_DICT[_absId[0]]
        return result if not isinstance(result, tuple) else result[0 if len(_absId) <= 1 else int(_absId[1])]


# 装饰物的图片管理模块
class DecorationImagesModule:
    # 引擎自带的场景装饰物，默认为空的sheet
    DEFAULT_DECORATION_IMAGE_SPRITE_SHEET: SpriteImage = SpriteImage("<NULL>")
    # 引擎自带的场景装饰物是否被加载
    __IS_DEFAULT_DECORATION_IMAGE_SPRITE_SHEET_INITIALIZED: bool = False
    # 项目自带的场景装饰物，默认为空的sheet
    CUSTOM_DECORATION_IMAGE_SPRITE_SHEET: SpriteImage = SpriteImage("<NULL>")
    # 项目自带的场景装饰物是否被加载
    __IS_CUSTOM_DECORATION_IMAGE_SPRITE_SHEET_INITIALIZED: bool = False
    # 经过处理的场景装饰物
    __DECORATION_IMAGE_DICT: Final[dict[str, StaticImage | tuple[StaticImage, ...]]] = {}
    __DECORATION_IMAGE_DICT_DARK: Final[dict[str, StaticImage | tuple[StaticImage, ...]]] = {}

    # 确认sheet已经初始化
    @classmethod
    def init(cls) -> None:
        # 如果自带的SPRITE SHEET未被初始化，则初始化
        if not cls.__IS_DEFAULT_DECORATION_IMAGE_SPRITE_SHEET_INITIALIZED:
            if os.path.exists(Images.generate_path_according_to_prefix("<!env>decorations.png")):
                cls.DEFAULT_DECORATION_IMAGE_SPRITE_SHEET = SpriteImage("<!env>decorations.png")
            cls.__IS_DEFAULT_DECORATION_IMAGE_SPRITE_SHEET_INITIALIZED = True
        # 如果开发者自定义的SPRITE SHEET未被初始化，则初始化
        if not cls.__IS_CUSTOM_DECORATION_IMAGE_SPRITE_SHEET_INITIALIZED:
            if os.path.exists(Images.generate_path_according_to_prefix("<@env>decorations.png")):
                cls.CUSTOM_DECORATION_IMAGE_SPRITE_SHEET = SpriteImage("<@env>decorations.png")
            cls.__IS_CUSTOM_DECORATION_IMAGE_SPRITE_SHEET_INITIALIZED = True

    # 获取当前装饰物种类的数量
    @classmethod
    def count_variations(cls, _type: str) -> int:
        _ref: StaticImage | tuple[StaticImage, ...] | None = cls.__DECORATION_IMAGE_DICT.get(_type)
        if _ref is None:
            EXCEPTION.fatal(f'Cannot find decoration image "{_type}"')
        return len(_ref) if isinstance(_ref, tuple) else 1

    # 加载场景装饰物图片
    @classmethod
    def add_image(cls, _type: str) -> None:
        # 确保初始化
        cls.init()
        # 查看图片是否在自带或自定义的SPRITE SHEET中存在，不存在则为None
        sheet_ref: SpriteImage | None = (
            cls.DEFAULT_DECORATION_IMAGE_SPRITE_SHEET
            if cls.DEFAULT_DECORATION_IMAGE_SPRITE_SHEET.contain(_type)
            else cls.CUSTOM_DECORATION_IMAGE_SPRITE_SHEET if cls.CUSTOM_DECORATION_IMAGE_SPRITE_SHEET.contain(_type) else None
        )
        # 如果图片存在，则reference不为None
        if sheet_ref is not None:
            # 最后确认一下是不是需要加载
            if _type not in cls.__DECORATION_IMAGE_DICT:
                # 从sheet中读取装饰物图片
                _img: ImageSurface | tuple[ImageSurface, ...] = sheet_ref.get(_type)
                # 将图片转换成对应格式后存入字典中
                cls.__DECORATION_IMAGE_DICT[_type] = (
                    tuple(StaticImage(_imgRef, 0, 0) for _imgRef in _img) if isinstance(_img, tuple) else StaticImage(_img, 0, 0)
                )
            # 如果是夜战模式
            if TileMapImagesModule.DARKNESS > 0:
                _imgRefTemp: StaticImage | tuple[StaticImage, ...] = cls.__DECORATION_IMAGE_DICT[_type]
                if isinstance(_imgRefTemp, tuple):
                    _temp: list[StaticImage] = []
                    for _imgRef in _imgRefTemp:
                        _imgCopy = _imgRef.copy()
                        _imgCopy.add_darkness(TileMapImagesModule.DARKNESS)
                        _temp.append(_imgCopy)
                    cls.__DECORATION_IMAGE_DICT_DARK[_type] = tuple(_temp)
                else:
                    _imgTemp: StaticImage = _imgRefTemp.copy()
                    _imgTemp.add_darkness(TileMapImagesModule.DARKNESS)
                    cls.__DECORATION_IMAGE_DICT_DARK[_type] = _imgTemp
        else:
            EXCEPTION.fatal(f'Cannot find decoration image "{_type}"')

    # 获取图片
    @classmethod
    def get_image(cls, _id: str, darkMode: bool = False) -> StaticImage:
        # 获取参数
        _absId: list[str] = _id.split(":")
        # 尝试获取图片
        result: StaticImage | tuple[StaticImage, ...]
        possible_result: StaticImage | tuple[StaticImage, ...] | None = (
            cls.__DECORATION_IMAGE_DICT_DARK.get(_absId[0]) if darkMode is True else cls.__DECORATION_IMAGE_DICT.get(_absId[0])
        )
        if possible_result is not None:
            result = possible_result
        else:
            if Debug.get_developer_mode():
                EXCEPTION.inform(f"Cannot find decoration image '{_id}', we will try to load it for you right now, but please by aware.")
            cls.add_image(_absId[0])
            result = cls.__DECORATION_IMAGE_DICT_DARK[_absId[0]] if darkMode is True else cls.__DECORATION_IMAGE_DICT[_absId[0]]
        return result if not isinstance(result, tuple) else result[0 if len(_absId) <= 1 else int(_absId[1])]


# 管理单个动作所有对应图片的模块
class _EntityImagesCollection:
    def __init__(self, imagesList: tuple[StaticImage, ...], crop_size: list[int], offset: list[int], original_img_size: list[int]) -> None:
        self.__images: tuple[StaticImage, ...] = imagesList
        self.__current_image_pointer: StaticImage = self.__images[0]
        self.__width: int = 0
        self.__height: int = 0
        self.__cropped_image_width: int = crop_size[0]
        self.__cropped_image_height: int = crop_size[1]
        self.__left_offset_x: int = offset[0]
        self.__offset_y: int = offset[1]
        self.__real_width: int = original_img_size[0]
        self.__real_height: int = original_img_size[1]
        self.__right_offset_x: int = self.__real_width - self.__cropped_image_width - self.__left_offset_x

    def __len__(self) -> int:
        return len(self.__images)

    # 获取指定index的图片
    def get_image(self, index: int) -> StaticImage:
        return self.__images[index]

    # 设置尺寸
    def set_size(self, width: int_f, height: int_f) -> None:
        self.__width = round(width * self.__cropped_image_width / self.__real_width)
        self.__height = round(height * self.__cropped_image_height / self.__real_height)

    # 设置要播放图片的index
    def set_index(self, index: int) -> None:
        self.__current_image_pointer = self.__images[index]

    # 反转所有列表内的图片
    def flip_all(self) -> None:
        for _image in self.__images:
            _image.flip_original_img()
        temp: int = self.__right_offset_x
        self.__right_offset_x = self.__left_offset_x
        self.__left_offset_x = temp

    # 获取当前图片的rect
    def get_rectangle(self) -> Rectangle:
        return self.__current_image_pointer.get_rectangle()

    # 展示
    def render(self, _surface: ImageSurface, pos: tuple[int, int], alpha: int, ifFlip: bool, draw_outline: bool) -> None:
        self.__current_image_pointer.set_size(self.__width, self.__height)
        self.__current_image_pointer.set_alpha(alpha)  # 翻转图片
        self.__current_image_pointer.set_top(self.__offset_y * self.__height / self.__cropped_image_height + pos[1])
        if ifFlip:
            self.__current_image_pointer.flip_if_not()
            self.__current_image_pointer.set_left(self.__right_offset_x * self.__width / self.__cropped_image_width + pos[0])
        else:
            self.__current_image_pointer.flip_back_to_normal()
            self.__current_image_pointer.set_left(self.__left_offset_x * self.__width / self.__cropped_image_width + pos[0])
        self.__current_image_pointer.draw(_surface)
        if draw_outline is True:
            self.__current_image_pointer.draw_outline(_surface)


# 角色图片管理模块
class EntitySpriteImageManager:
    # 用于存放角色图片的字典
    __CHARACTERS_IMAGES: Final[dict[str, dict[str, _EntityImagesCollection]]] = {}
    # 角色图片文件夹路径
    SPRITES_PATH: Final[str] = Specification.get_directory("sprite")

    # 获取图片
    @classmethod
    def get_images(cls, characterType: str, action: str) -> _EntityImagesCollection:
        return cls.__CHARACTERS_IMAGES[characterType][action]

    # 尝试获取图片
    @classmethod
    def try_get_image_references(cls, faction: str, characterType: str, action: str) -> _EntityImagesCollection:
        if characterType not in cls.__CHARACTERS_IMAGES or action not in cls.__CHARACTERS_IMAGES[characterType]:
            cls.load(faction, characterType, "dev")
        return cls.get_images(characterType, action)

    # 是否图片存在
    @classmethod
    def does_action_exist(cls, characterType: str, action: str) -> bool:
        return action in cls.__CHARACTERS_IMAGES[characterType]

    # 生成webp动态图片
    @classmethod
    def generate(cls, entityFaction: str, entityType: str) -> None:
        # 储存数据的字典
        _data: dict = {}
        # 目录路径
        folder_path: str = os.path.join(cls.SPRITES_PATH, entityFaction, entityType)
        # 暂时存放图片的列表
        imgTempList: list = []
        # 历遍目标文件夹中的图片
        for _action_folder in os.listdir(folder_path):
            if os.path.isdir(_action_folder_path := os.path.join(folder_path, _action_folder)):
                # 单个sprite图切割点
                crop_rect: list[int] = []
                # 重置存放图片的列表
                imgTempList.clear()
                # 获取所有当前动作图片的目录
                img_list: list[str] = glob(os.path.join(_action_folder_path, "*.png"))
                if len(img_list) > 0:
                    img_list.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
                    _image: ImageSurface | None = None
                    # 加载所有图片
                    for _path in img_list:
                        # 加载单个图片
                        _image = Images.quickly_load(_path)
                        # 如果切割rect未被初始化
                        if len(crop_rect) <= 0:
                            crop_rect = [_image.get_width(), _image.get_height(), 0, 0]
                        # 获取图片的bounding，并和现有的bounding进行比较
                        _bounding: RectObject = _image.get_bounding_rect()
                        if _bounding.x < crop_rect[0]:
                            crop_rect[0] = _bounding.x
                        if _bounding.y < crop_rect[1]:
                            crop_rect[1] = _bounding.y
                        if _bounding.right > crop_rect[2]:
                            crop_rect[2] = _bounding.right
                        if _bounding.bottom > crop_rect[3]:
                            crop_rect[3] = _bounding.bottom
                        # 放入图片
                        imgTempList.append(_image)
                    # 计算universal的尺寸
                    crop_rect[2] -= crop_rect[0]
                    crop_rect[3] -= crop_rect[1]
                    # 写入信息
                    if _image is None:
                        EXCEPTION.fatal("Empty folder!")
                    _data[_action_folder] = {"count": len(imgTempList), "subrect": crop_rect, "size": list(_image.get_size())}
                    # 生成当前动作的webp图
                    for i in range(len(imgTempList)):
                        imgTempList[i] = PILImage.fromarray(Surfaces.to_array(imgTempList[i].subsurface(crop_rect)))
                    # 保存当前动作的webp图
                    target_file_name: str = _action_folder + ".webp"
                    imgTempList[0].save(os.path.join(folder_path, target_file_name), save_all=True, append_images=imgTempList[1:], duration=0, lossless=True)
                    # 删除原先的文件夹
                    shutil.rmtree(os.path.join(folder_path, _action_folder))
        # 保存sprite图数据
        if len(_data) > 0:
            Config.save(os.path.join(folder_path, entityType + ".linpg.meta"), _data)

    # 为Sprite文件夹中的所有角色生成webp动态图片
    @classmethod
    def generate_all(cls) -> None:
        _path: str = cls.SPRITES_PATH
        for faction in os.listdir(_path):
            for key in os.listdir(os.path.join(_path, faction)):
                cls.generate(faction, key)

    # 加载sprite图片模块：接受一个友方角色名，返回对应的动图字典
    @classmethod
    def load(cls, faction: str, characterType: str, mode: str) -> dict:
        sprite_image_meta_data: dict = Config.load_file(os.path.join(cls.SPRITES_PATH, faction, characterType, characterType + ".linpg.meta"))
        imgId_dict: dict = {}
        # 默认模式下，加载所有动作
        if mode == "default":
            for key in sprite_image_meta_data:
                imgId_dict[key] = cls.__load_action(faction, characterType, key, sprite_image_meta_data[key])
        # 在开发模式下仅加载idle动作
        elif mode == "dev":
            imgId_dict["wait"] = cls.__load_action(faction, characterType, "wait", sprite_image_meta_data["wait"])
        else:
            EXCEPTION.fatal("Mode is not supported")
        return imgId_dict

    # 动图制作模块：接受一个友方角色名和动作,当前的方块标准长和高，返回对应角色动作list或者因为没图片而返回None
    # 810*810 position:405/567
    @classmethod
    def __load_action(cls, faction: str, characterType: str, action: str, action_meta_data: dict) -> dict:
        # 为尚未初始化的角色init一个字典
        if characterType not in cls.__CHARACTERS_IMAGES:
            cls.__CHARACTERS_IMAGES[characterType] = {}
        # 如果动作已被初始化，则返回对应字典
        elif action in cls.__CHARACTERS_IMAGES[characterType]:
            return {"imgId": 0, "alpha": 255}
        # 加载图片
        cls.__CHARACTERS_IMAGES[characterType][action] = _EntityImagesCollection(
            tuple(
                StaticImage(Surfaces.from_array(numpy.asarray(frame.convert("RGBA"))).convert_alpha(), 0, 0)
                for frame in PILImageSequence.Iterator(PILImage.open(os.path.join(cls.SPRITES_PATH, faction, characterType, action + ".webp")))
            ),
            action_meta_data["subrect"][2:],
            action_meta_data["subrect"][:2],
            action_meta_data["size"],
        )
        # 如果是敌人模块，则flip所有图片
        if faction == "enemy":
            cls.__CHARACTERS_IMAGES[characterType][action].flip_all()
        # 返回数据
        return {"imgId": 0, "alpha": 255}


# 管理场景装饰物的类
class DecorationObject(GameObject2d):
    def __init__(self, x: int, y: int, _type: str, _variation: int, status: dict = {}):
        super().__init__(x, y)
        self.__type: Final[str] = _type
        self._variation: int = _variation
        self.__status: Final[dict] = status
        self.__alpha: int = 255
        self.__is_dark_mode: bool = False

    # 确保图片已经被存档
    def ensure_image_cached(self) -> None:
        DecorationImagesModule.add_image(self.__type)

    @property
    def id(self) -> str:
        return self.__type if self._variation <= 0 else self.__type + ":" + str(self._variation)

    @property
    def type(self) -> str:
        return self.__type

    @property
    def variation(self) -> int:
        return self._variation

    def get_alpha(self) -> int:
        return self.__alpha

    def set_alpha(self, value: int) -> None:
        self.__alpha = value

    def set_dark_mode(self, value: bool) -> None:
        self.__is_dark_mode = value

    def to_dict(self) -> dict:
        data_t: dict = {"x": self.x, "y": self.y, "id": self.id}
        if len(self.__status) > 0:
            data_t["status"] = copy.deepcopy(self.__status)
        return data_t

    @staticmethod
    def from_dict(_data: dict) -> "DecorationObject":
        index_args: list[str] = str(_data["id"]).split(":")
        if not isinstance(_data.get("status"), dict):
            _data["status"] = {}
        theDecoration: DecorationObject = DecorationObject(
            _data["x"], _data["y"], index_args[0], int(index_args[1]) if len(index_args) > 1 else 0, _data["status"]
        )
        return theDecoration

    def is_on_pos(self, pos: object) -> bool:
        return Coordinates.is_same(self.get_pos(), pos)

    def _has_status(self, key: str) -> bool:
        return key in self.__status

    def get_status(self, key: str) -> object:
        return self.__status[key]

    def set_status(self, key: str, value: object) -> None:
        self.__status[key] = value

    def remove_status(self, key: str) -> None:
        if key in self.__status:
            del self.__status[key]
        else:
            EXCEPTION.fatal(f'Cannot remove status "{key}" because it does not exist')

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        abs_pos: Final[tuple[int, int]] = Coordinates.add(self.get_pos(), offSet)
        imgToBlit = DecorationImagesModule.get_image(self.id, self.__is_dark_mode)
        imgToBlit.set_width_with_original_image_size_locked(TileMapImagesModule.TILE_TEMPLE_WIDTH // 2)
        imgToBlit.set_alpha(self.__alpha)
        imgToBlit.set_left(abs_pos[0] + TileMapImagesModule.TILE_TEMPLE_WIDTH // 4)
        imgToBlit.set_bottom(abs_pos[1] + TileMapImagesModule.TILE_TEMPLE_HEIGHT * 0.85)
        imgToBlit.draw(_surface)

    def get_width(self) -> int:
        return 0

    def get_height(self) -> int:
        return 0


# 人形模块
class Entity(Position):
    # 存放音效的字典
    __SOUNDS: Final[dict[str, dict[str, tuple]]] = {}
    # 角色数据库
    __DATABASE: Final[dict[str, dict]] = Config.try_load_file_if_exists(os.path.join("Data", "character_data." + Config.get_file_type()))
    # idle动作
    __IDLE_ACTION: Final[str] = "wait"

    def __init__(self, DATA: dict, mode: str):
        super().__init__(DATA["x"], DATA["y"])
        # 攻击范围
        self.__attack_coverage: int = int(DATA["attack_coverage"])
        # 最大血量
        self.__max_hp: int = max(int(DATA["max_hp"]), 1)
        # 当前血量
        self.__current_hp: int = int(DATA.get("current_hp", self.__max_hp))
        # 不可再生的护甲值
        self.__irrecoverable_armor: int = int(DATA.get("irrecoverable_armor", 0))
        # 最大可再生的护甲值
        self.__max_recoverable_armor: int = int(DATA.get("max_recoverable_armor", 0))
        # 当前可再生的护甲值
        self.__current_recoverable_armor: int = int(DATA.get("current_recoverable_armor", self.__max_recoverable_armor))
        # 攻击范围
        self.__effective_range: tuple[int, ...] = tuple(DATA["effective_range"])
        # 最大攻击力
        self.__max_damage: int = int(DATA["max_damage"])
        # 最小攻击力
        self.__min_damage: int = int(DATA["min_damage"])
        # 武器类型
        self.__kind: str = str(DATA["kind"])
        # 阵营
        self.__faction: str = str(DATA["faction"])
        # 态度： 友方 - 1；敌对 - -1；中立 - 0
        self.__attitude: int = 0
        # 角色名称
        self.__type: str = str(DATA["type"])
        # 是否图片镜像
        self._if_flip: bool = bool(DATA.get("if_flip", False))
        # 当前动作
        self.__current_action: str = str(DATA.get("current_action", self.__IDLE_ACTION))
        # 动作是否重复
        self.__if_action_loop: bool = bool(DATA.get("if_action_loop", True))
        # 是否动作完成后返回idle
        self.__if_switch_to_idle_afterwards: bool = bool(DATA.get("if_switch_to_idle_afterwards", True))
        # 动作是正序列播放还是反序播放
        self._if_play_action_in_reversing: bool = bool(DATA.get("if_play_action_in_reversing", False))
        # 需要移动的路径
        self.__moving_path: deque[tuple[int, int]] = deque(DATA.get("moving_path", []))
        self.__moving_complete: bool = bool(DATA.get("moving_complete", len(self.__moving_path) <= 0))
        # 是否无敌
        self.__if_invincible: bool = bool(DATA.get("if_invincible", False))
        # gif图片管理
        self.__imgId_dict: dict[str, dict[str, float]] = EntitySpriteImageManager.load(self.__faction, self.__type, mode)
        # 加载角色的音效
        if (
            mode != "dev"
            and self.__type not in self.__SOUNDS
            and os.path.exists(_sound_directory := Specification.get_directory("character_sound", self.__type))
        ):
            self.__SOUNDS[self.__type] = {
                soundType: Sounds.load_from_directory(os.path.join(_sound_directory, soundType)) for soundType in os.listdir(_sound_directory)
            }
        # 是否刚进入一个新的tile
        self.__just_entered_a_new_tile: bool = False
        # 当前图片的rect
        self.__current_image_rect: Rectangle | None = None
        # 是否被选中
        self.__is_selected: bool = False
        # 移动速率
        self._move_speed_scale = 0.02

    """修改父类的方法"""

    def to_dict(self) -> dict:
        data: dict[str, Any] = {
            "x": self.x,
            "y": self.y,
            "attack_coverage": self.__attack_coverage,
            "max_hp": self.__max_hp,
            "effective_range": list(self.__effective_range),
            "kind": self.__kind,
            "type": self.__type,
            "max_damage": self.__max_damage,
            "min_damage": self.__min_damage,
        }
        """以下是可选数据"""
        if self._if_flip is True:
            data["if_flip"] = self._if_flip
        if self.__current_action != self.__IDLE_ACTION:
            data["current_action"] = self.__current_action
            data["if_action_loop"] = self.__if_action_loop
            data["if_play_action_in_reversing"] = self._if_play_action_in_reversing
            data["if_switch_to_idle_afterwards"] = self.__if_switch_to_idle_afterwards
        if self.__current_hp != self.__max_hp:
            data["current_hp"] = self.__current_hp
        if self.__max_recoverable_armor > 0:
            data["max_recoverable_armor"] = self.__max_recoverable_armor
        if self.__irrecoverable_armor > 0:
            data["irrecoverable_armor"] = self.__irrecoverable_armor
        if self.__current_recoverable_armor > 0:
            data["current_recoverable_armor"] = self.__current_recoverable_armor
        if self.__if_invincible is True:
            data["if_invincible"] = self.__if_invincible
        if len(self.__moving_path) > 0:
            data["moving_path"] = [list(pos) for pos in self.__moving_path]
        if not self.__moving_complete:
            data["moving_complete"] = self.__moving_complete
        return data

    def just_entered_a_new_tile(self) -> bool:
        return self.__just_entered_a_new_tile

    def get_coordinate(self) -> tuple[int, int]:
        return round(self.x), round(self.y)

    """重要方法与参数"""

    # 查询特点角色的数据
    @classmethod
    def get_entity_data(cls, _type: str) -> dict:
        return cls.__DATABASE[_type]

    # 阵营
    @property
    def faction(self) -> str:
        return self.__faction

    # 态度
    @property
    def attitude(self) -> int:
        return self.__attitude

    def set_attitude(self, value: int) -> None:
        self.__attitude = Numbers.keep_int_in_range(value, -1, 1)

    # 武器类型
    @property
    def kind(self) -> str:
        return self.__kind

    # 角色武器名称
    @property
    def type(self) -> str:
        return self.__type

    """
    攻击
    """

    # 攻击覆盖范围
    @property
    def attack_coverage(self) -> int:
        return self.__attack_coverage

    # 攻击范围
    @property
    def effective_range(self) -> tuple[int, ...]:
        return self.__effective_range

    # 最大攻击力
    @property
    def max_damage(self) -> int:
        return self.__max_damage

    # 最小攻击力
    @property
    def min_damage(self) -> int:
        return self.__min_damage

    # 攻击另一个Entity
    def attack(self, another_entity: "Entity") -> int:
        damage = Numbers.get_random_int(self.__min_damage, self.__max_damage)
        another_entity.injury(damage)
        return damage

    # 获取选中状态
    def get_selected(self) -> bool:
        return self.__is_selected

    # 设置选中状态
    def set_selected(self, value: bool) -> None:
        self.__is_selected = value

    # 是否角色被鼠标触碰
    def is_hovered(self) -> bool:
        return self.__current_image_rect.is_hovered() if self.__current_image_rect is not None else False

    # 是否角色纹理与另一个物体overlap
    def is_overlapped_with(self, _rect: Rectangle) -> bool:
        return self.__current_image_rect.is_overlapped_with(_rect) if self.__current_image_rect is not None else False

    """
    角色动作参数管理
    """

    # 当前动作
    @property
    def action(self) -> str:
        return self.__current_action

    # 设置动作
    def set_action(self, action: str = "wait", ifLoop: bool = True, switchToIdleAfterwards: bool = True) -> None:
        self.reset_imgId(self.__current_action)
        self.__current_action = action
        self.__if_action_loop = ifLoop
        self.__if_switch_to_idle_afterwards = switchToIdleAfterwards

    # 是否闲置
    def is_idle(self) -> bool:
        return self.__current_action == self.__IDLE_ACTION

    # 获取角色特定动作的图片播放ID
    def get_imgId(self, action: str) -> int:
        action_dict: dict[str, float] | None = self.__imgId_dict.get(action)
        return int(action_dict["imgId"]) if action_dict is not None else -1

    # 获取角色特定动作的图片总数量
    def get_imgNum(self, action: str) -> int:
        return len(EntitySpriteImageManager.get_images(self.__type, action))

    # 设定角色特定动作的图片播放ID
    def set_imgId(self, action: str, imgId: float) -> None:
        self.__imgId_dict[action]["imgId"] = imgId

    # 重置角色特定动作的图片播放ID
    def reset_imgId(self, action: str) -> None:
        self.set_imgId(action, 0)

    # 增加角色特定动作的图片播放ID
    def add_imgId(self, action: str, amount: float = 1.0) -> None:
        self.__imgId_dict[action]["imgId"] += amount

    # 获取角色特定动作的图片透明度
    def get_imgAlpha(self, action: str) -> int:
        return int(self.__imgId_dict[action]["alpha"])

    # 设定角色特定动作的图片透明度
    def set_imgAlpha(self, action: str, alpha: int) -> None:
        self.__imgId_dict[action]["alpha"] = alpha

    """
    角色血量护甲参数管理
    """

    # 是否角色还活着
    def is_alive(self) -> bool:
        return self.__current_hp > 0

    # 当前血量
    @property
    def current_hp(self) -> int:
        return self.__current_hp

    # 最大血量
    @property
    def max_hp(self) -> int:
        return self.__max_hp

    # 当前血量百分比
    @property
    def hp_percentage(self) -> float:
        return round(self.__current_hp / self.__max_hp, 5)

    # 治愈
    def heal(self, hpHealed: int) -> None:
        if hpHealed > 0:
            self.__current_hp += hpHealed
        elif hpHealed < 0:
            EXCEPTION.fatal("You cannot heal a negative value")

    # 降低血量
    def injury(self, damage: int) -> None:
        if not self.__if_invincible and damage > 0:
            # 如果有可再生的护甲
            if self.__current_recoverable_armor > 0:
                # 如果伤害大于护甲值,则以护甲值为最大护甲将承受的伤害
                if damage > self.__current_recoverable_armor:
                    damage_take_by_armor = Numbers.get_random_int(0, self.__current_recoverable_armor)
                # 如果伤害小于护甲值,则以伤害为最大护甲将承受的伤害
                else:
                    damage_take_by_armor = Numbers.get_random_int(0, damage)
                self.__current_recoverable_armor -= damage_take_by_armor
                damage -= damage_take_by_armor
            # 如果有不可再生的护甲
            if self.__irrecoverable_armor > 0 and damage > 0:
                if damage > self.__irrecoverable_armor:
                    damage_take_by_armor = Numbers.get_random_int(0, self.__irrecoverable_armor)
                # 如果伤害小于护甲值,则以伤害为最大护甲将承受的伤害
                else:
                    damage_take_by_armor = Numbers.get_random_int(0, damage)
                self.__irrecoverable_armor -= damage_take_by_armor
                damage -= damage_take_by_armor
            # 如果还有伤害,则扣除血量
            if damage > 0:
                self.__current_hp -= damage
            # 如果角色血量小等于0，进入死亡状态
            if self.__current_hp <= 0:
                self.__current_hp = 0
                self.set_action("die", False, False)
        elif self.__if_invincible or damage == 0:
            pass
        else:
            EXCEPTION.fatal("You cannot do a negative damage")

    # 回复可再生护甲
    def recover_armor(self, value: int) -> None:
        self.__current_recoverable_armor += value
        # 防止可再生护甲的数值越界
        if self.__current_recoverable_armor > self.__max_recoverable_armor:
            self.__current_recoverable_armor = self.__max_recoverable_armor
        elif self.__current_recoverable_armor < 0:
            self.__current_recoverable_armor = 0

    """
    其他
    """

    # 设置反转
    def set_flip(self, theBool: bool) -> None:
        self._if_flip = theBool

    # 播放角色声音
    def play_sound(self, kind_of_sound: str) -> None:
        if LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL is not None:
            _point: dict | None = self.__SOUNDS.get(self.__type)
            if _point is not None:
                sound_list: tuple | None = _point.get(kind_of_sound)
                if sound_list is not None and len(sound_list) > 0:
                    sound = sound_list[Numbers.get_random_int(0, len(sound_list) - 1) if len(sound_list) > 1 else 0]
                    sound.set_volume(Volume.get_effects() / 100.0)
                    LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL.play(sound)

    # 设置需要移动的路径
    def move_follow(self, path: Sequence[tuple[int, int]]) -> None:
        if isinstance(path, Sequence) and len(path) > 0:
            self.__moving_path = deque(path)
            self.__moving_complete = False
            self.set_action("move")
        else:
            EXCEPTION.fatal("Character cannot move to a invalid path!")

    # 查看是否一个Entity在该角色的附近
    def near(self, otherEntity: Position | Coordinate) -> bool:
        self_x: int = round(self.x)
        o_x: int = round(otherEntity.x)
        self_y: int = round(self.y)
        o_y: int = round(otherEntity.y)
        if self_x == o_x:
            return abs(self_y - o_y) <= 1
        elif self_y == o_y:
            return abs(self_x - o_x) <= 1
        return False

    # 根据距离确定对象所在区域
    @staticmethod
    def _identify_range(_ranges: tuple[int, ...], distanceBetween: int) -> int:
        if distanceBetween > 0:
            _total: int = 0
            for i, num in enumerate(_ranges):
                _total += num
                if distanceBetween <= _total:
                    return i
        return -1

    # 获取对象所在区域
    def range_target_in(self, otherEntity: "Entity") -> int:
        return self._identify_range(self.__effective_range, abs(round(otherEntity.x) - round(self.x)) + abs(round(otherEntity.y) - round(self.y)))

    # 根据坐标反转角色
    def set_flip_based_on_pos(self, _pos: tuple[number, number]) -> None:
        # 检测坐标
        if self.x > _pos[0]:
            self.set_flip(True)
        elif self.x == _pos[0]:
            self.set_flip(self.y <= _pos[1])
        else:
            self.set_flip(False)

    """画出角色"""

    # 角色画到surface上
    def __render(self, _surface: ImageSurface, pos: tuple[int, int], size: tuple[int, int], action: str, alpha: int) -> None:
        # 当alpha小等于0时意味着没必要渲染任何东西
        if alpha <= 0:
            # 重置角色的rect
            self.__current_image_rect = None
            return
        # 获取对应动作的图片管理模块
        _image = EntitySpriteImageManager.get_images(self.__type, action)
        _image.set_index(min(int(self.__imgId_dict[action]["imgId"]), self.get_imgNum(action) - 1))
        _image.set_size(size[0], size[1])
        # 把角色图片画到屏幕上
        _image.render(_surface, (pos[0], pos[1]), alpha, self._if_flip, self.__is_selected)
        # 更新角色的rect
        self.__current_image_rect = _image.get_rectangle()

    # 获取当前x轴速度
    def _get_current_speed_x(self) -> float:
        return TileMapImagesModule.TILE_SIZE * self._move_speed_scale * Display.get_delta_time() / 1000

    # 获取当前y轴速度
    def _get_current_speed_y(self) -> float:
        return TileMapImagesModule.TILE_SIZE * self._move_speed_scale * Display.get_delta_time() / 1000

    # 把角色画到surface上，并操控imgId以跟踪判定下一帧的动画
    def render(self, _surface: ImageSurface, pos: tuple[int, int], size: tuple[int, int], action: str | None = None, alpha: int | None = None) -> None:
        # 加载初始alpha值
        if alpha is None:
            alpha = self.get_imgAlpha(self.__current_action)
        # 不是自定义action
        if action is None:
            # 画出角色
            self.__render(_surface, pos, size, self.__current_action, alpha)
            # 如果正在播放移动动作，则需要根据现有路径更新坐标
            if self.__current_action == "move" and not self.__moving_complete:
                self.__just_entered_a_new_tile = False
                if len(self.__moving_path) > 0:
                    need_pop: bool = False
                    self.set_flip_based_on_pos(self.__moving_path[0])
                    if self.x < self.__moving_path[0][0]:
                        self.set_x(self.x + self._get_current_speed_x())
                        if self.x >= self.__moving_path[0][0]:
                            self.set_x(self.__moving_path[0][0])
                            need_pop = True
                    elif self.x > self.__moving_path[0][0]:
                        self.set_x(self.x - self._get_current_speed_x())
                        if self.x <= self.__moving_path[0][0]:
                            self.set_x(self.__moving_path[0][0])
                            need_pop = True
                    if self.y < self.__moving_path[0][1]:
                        self.set_y(self.y + self._get_current_speed_y())
                        if self.y >= self.__moving_path[0][1]:
                            self.set_y(self.__moving_path[0][1])
                            need_pop = True
                    elif self.y > self.__moving_path[0][1]:
                        self.set_y(self.y - self._get_current_speed_y())
                        if self.y <= self.__moving_path[0][1]:
                            self.set_y(self.__moving_path[0][1])
                            need_pop = True
                    if need_pop is True:
                        self.__moving_path.popleft()
                        self.__just_entered_a_new_tile = True
                elif not self.__moving_complete:
                    self.__moving_complete = True
                    if EntitySpriteImageManager.does_action_exist(self.type, "set") is True:
                        self.set_action("set", False)
                    else:
                        self.set_action()
            # 如果是正序播放
            if not self._if_play_action_in_reversing:
                # 如果角色图片还没播放完，则增加id
                if self.__imgId_dict[self.__current_action]["imgId"] < self.get_imgNum(self.__current_action) - 1:
                    self.__imgId_dict[self.__current_action]["imgId"] = min(
                        self.__imgId_dict[self.__current_action]["imgId"] + Display.get_delta_time() / 20, self.get_imgNum(self.__current_action) - 1
                    )
                # 如果角色图片播放完需要重新播
                elif self.__if_action_loop is True:
                    self.__imgId_dict[self.__current_action]["imgId"] = 0
                # 如果角色图片播放完但不打算重新播
                elif not self.__if_switch_to_idle_afterwards:
                    pass
                # 如果角色图片播放完需要回到待机状态
                elif not self.__if_action_loop:
                    self.set_action()
                else:
                    EXCEPTION.fatal(f"The self.__if_action_loop data error: {self.__if_action_loop}")
            # 如果是颠倒播放，但id还未降至0，则减去1
            elif self.__imgId_dict[self.__current_action]["imgId"] > 0:
                self.__imgId_dict[self.__current_action]["imgId"] -= Display.get_delta_time() / 20
            # 如果是颠倒播放，但id已经降至0
            else:
                self._if_play_action_in_reversing = False
                self.set_action()
        else:
            # 画出角色
            self.__render(_surface, pos, size, action, alpha)
            # 调整id，并返回对应的bool状态
            if self.__imgId_dict[action]["imgId"] < self.get_imgNum(action) - 1:
                self.__imgId_dict[action]["imgId"] += Display.get_delta_time() / 20
            # 如果需要循环，则重设播放的index
            else:
                self.__imgId_dict[action]["imgId"] = 0


# 点
class _AStarPoint(Coordinate):
    def __eq__(self, other: "_AStarPoint") -> bool:  # type: ignore[override]
        return self.x == other.x and self.y == other.y


# 描述AStar算法中的节点数据
class _AStarNode:
    def __init__(self, point: _AStarPoint, endPoint: _AStarPoint, g: number = 0):
        self.point: _AStarPoint = point  # 自己的坐标
        self.father: _AStarNode | None = None  # 父节点
        self.g: number = g  # g值，g值在用到的时候会重新算
        self.h: int = (abs(endPoint.x - point.x) + abs(endPoint.y - point.y)) * 10  # 计算h值


# 寻路模块
class AStar:
    # 寻路用的ndarray地图
    __map2d: numpy.ndarray = numpy.asarray([])
    # 行
    __row: int = 0
    # 列
    __column: int = 0
    # 终点
    __end_point: _AStarPoint = _AStarPoint(0, 0)
    # 开启表
    __open_list: deque[_AStarNode] = deque()
    # 关闭表
    __close_list: set[_AStarNode] = set()

    @classmethod
    def __update(cls, new_map2d: numpy.ndarray) -> None:
        cls.__open_list.clear()
        cls.__close_list.clear()
        cls.__map2d = new_map2d
        cls.__column, cls.__row = new_map2d.shape

    @classmethod
    def __is_out_of_bound(cls, _point: _AStarPoint) -> bool:
        return _point.y < 0 or _point.y >= cls.__row or _point.x < 0 or _point.x >= cls.__column

    # 获得OpenList中F值最小的节点
    @classmethod
    def __getMinNode(cls) -> _AStarNode:
        currentNode = cls.__open_list[0]
        for node in cls.__open_list:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    @classmethod
    def __pointInCloseList(cls, point: _AStarPoint) -> bool:
        for node in cls.__close_list:
            if node.point == point:
                return True
        return False

    @classmethod
    def __pointInOpenList(cls, point: _AStarPoint) -> _AStarNode | None:
        for node in cls.__open_list:
            if node.point == point:
                return node
        return None

    @classmethod
    def __end_pointInCloseList(cls) -> _AStarNode | None:
        for node in cls.__open_list:
            if node.point == cls.__end_point:
                return node
        return None

    # 搜索节点周围的点
    @classmethod
    def __searchNear(cls, minF: _AStarNode, offSetX: int, offSetY: int) -> None:
        minFNearByPoint: _AStarPoint = _AStarPoint(minF.point.x + offSetX, minF.point.y + offSetY)
        # 越界检测 / 如果是障碍，就忽略
        if cls.__is_out_of_bound(minFNearByPoint) or cls.__map2d[minFNearByPoint.x, minFNearByPoint.y] <= 0:
            return
        # 如果在关闭表中，就忽略
        currentPoint: _AStarPoint = _AStarPoint(minFNearByPoint.x, minFNearByPoint.y)
        if cls.__pointInCloseList(currentPoint):
            return
        # 设置单位花费
        _step: int = 10 if offSetX == 0 or offSetY == 0 else 14
        # 如果不再openList中，就把它加入OpenList
        currentNode: _AStarNode | None = cls.__pointInOpenList(currentPoint)
        if currentNode is None:
            currentNode = _AStarNode(currentPoint, cls.__end_point, minF.g + _step)
            currentNode.father = minF
            cls.__open_list.append(currentNode)
        # 如果在openList中，判断minF到当前点的G是否更小
        elif minF.g + _step < currentNode.g:  # 如果更小，就重新计算g值，并且改变father
            currentNode.g = minF.g + _step
            currentNode.father = minF

    # 开始寻路
    @classmethod
    def search(cls, map2d: numpy.ndarray, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> list[tuple[int, int]]:
        cls.__update(map2d)
        # 判断寻路终点是否是障碍
        cls.__end_point = _AStarPoint(end_pos[0], end_pos[1])
        if cls.__is_out_of_bound(cls.__end_point) or cls.__map2d[cls.__end_point.x, cls.__end_point.y] <= 0:  # 如果终点是障碍物
            return []
        # 1.将起点放入开启列表
        startNode: _AStarNode = _AStarNode(_AStarPoint(start_pos[0], start_pos[1]), cls.__end_point)
        cls.__open_list.append(startNode)
        # 2.主循环逻辑
        while True:
            # 找到F值最小的点
            minF: _AStarNode = cls.__getMinNode()
            # 把这个点加入closeList中，并且在openList中删除它
            cls.__close_list.add(minF)
            cls.__open_list.remove(minF)
            # 判断这个节点的上下左右节点
            cls.__searchNear(minF, 0, -1)
            cls.__searchNear(minF, 0, 1)
            cls.__searchNear(minF, -1, 0)
            cls.__searchNear(minF, 1, 0)
            # 如果终点在关闭表中，就返回结果
            if (_point := cls.__end_pointInCloseList()) is not None:
                cPoint = _point
                pathList: list[tuple[int, int]] = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point.get_pos())
                        cPoint = cPoint.father
                    else:
                        cls.__open_list.clear()
                        cls.__close_list.clear()
                        pathList.reverse()
                        return pathList
            if len(cls.__open_list) == 0:
                cls.__open_list.clear()
                cls.__close_list.clear()
                return []


# 地图模块
class AbstractTileMap(Rectangle, SurfaceWithLocalPos):
    # 获取方块数据库
    __TILES_DATABASE: Final[dict] = DataBase.get("Tiles")
    # 获取场景装饰物数据库
    _DECORATION_DATABASE: Final[dict] = DataBase.get("Decorations")

    def __init__(self) -> None:
        # Rectangle模块
        Rectangle.__init__(self, 0, 0, 0, 0)
        # 本地坐标模块
        SurfaceWithLocalPos.__init__(self)
        # 地图数据
        self.__MAP: numpy.ndarray = numpy.array([])
        # 障碍数据
        self.__BARRIER_MASK: numpy.ndarray = numpy.array([])
        # 地图 tile lookup table
        self.__tile_lookup_table: list[str] = []
        # 行
        self.__row: int = 0
        # 列
        self.__column: int = 0
        # 地图渲染用的图层
        self.__map_surface: ImageSurface | None = None
        # 地图旧图层以渲染渐变效果
        self.__map_surface_old: ImageSurface | None = None
        # 不要保存地图旧图层
        self.__don_save_old_map_surface_for_next_update: bool = False
        # 背景图片
        self.__background_image: StaticImage | None = None
        # 使用一个hashmap以加速根据坐标寻找装饰物
        self.__decorations: dict[str, DecorationObject] = {}
        # 追踪是否需要更新的参数
        self.__need_update_surface: bool = True
        # 追踪目前已经画出的方块
        self.__tile_on_surface: numpy.ndarray = numpy.asarray([])
        # 是否需要更新地图图层
        self.__need_to_recheck_tile_on_surface: bool = True

    # 获取坐标类型的字典key
    @staticmethod
    def __get_coordinate_format_key(_coordinate: tuple[int, int]) -> str:
        return str(_coordinate[0]) + "_" + str(_coordinate[1])

    # 初始化地图数据
    def __init_map(self, map_data: numpy.ndarray, barrier_data: numpy.ndarray | None, tile_size: int_f) -> None:
        self.__MAP = map_data
        self.__row, self.__column = self.__MAP.shape
        self.__BARRIER_MASK = barrier_data if barrier_data is not None else numpy.zeros(self.__MAP.shape, dtype=numpy.byte)
        # 初始化追踪目前已经画出的方块的2d列表
        self.__tile_on_surface = numpy.zeros(self.__MAP.shape, dtype=numpy.byte)
        # 初始化地图渲染用的图层
        self.__map_surface = None
        self.__map_surface_old = None
        # 更新地图渲染图层的尺寸
        self.set_tile_size(tile_size)

    # 标记地图需要完全更新
    def _refresh(self) -> None:
        self.__need_update_surface = True
        self.__need_to_recheck_tile_on_surface = True

    # 更新数据
    def update(self, _data: dict, _block_size: int_f) -> None:
        # 初始化地图数据
        self.__tile_lookup_table = list(_data["map"]["lookup_table"])
        barrier_data: list[list[int]] | None = _data["map"].get("barrier")
        self.__init_map(
            numpy.asarray(_data["map"].get("data", _data["map"].get("array2d")), dtype=numpy.byte),
            numpy.asarray(barrier_data, dtype=numpy.byte) if barrier_data is not None else None,
            _block_size,
        )
        # 设置本地坐标
        _local_x = _data.get("local_x")
        if _local_x is None:
            self.set_local_x(0)
        elif isinstance(_local_x, str):
            self.set_local_x(Numbers.convert_percentage(_local_x) * self.get_width())
        else:
            self.set_local_x(_local_x)
        _local_y = _data.get("local_y")
        if _local_y is None:
            self.set_local_y(0)
        elif isinstance(_local_y, str):
            self.set_local_y(Numbers.convert_percentage(_local_y) * self.get_height())
        else:
            self.set_local_y(_local_y)
        # 重置装饰物列表
        self.__decorations.clear()
        # 加载装饰物
        for _decoration in _data["decoration"]:
            self.add_decoration(_decoration)
        # 背景图片路径
        theBgiPath: str | None = _data.get("background_image")
        # 背景图片
        self.__background_image = (
            StaticImage(Images.quickly_load(Specification.get_directory("background_image", theBgiPath), False), 0, 0) if theBgiPath is not None else None
        )
        # 加载图片（确保图片模块初始化）
        for fileName in self.__tile_lookup_table:
            TileMapImagesModule.add_image(fileName)
        for decoration in self.__decorations.values():
            decoration.ensure_image_cached()

    # 装饰物
    @property
    def decorations(self) -> tuple[DecorationObject, ...]:
        return tuple(self.__decorations.values())

    # 行
    @property
    def row(self) -> int:
        return self.__row

    # 列
    @property
    def column(self) -> int:
        return self.__column

    # 列
    @property
    def shape(self) -> tuple[int, int]:
        return self.__column, self.__row

    # 设置障碍mask
    def set_barrier_mask(self, x: int, y: int, value: int) -> None:
        self.__BARRIER_MASK[y, x] = value

    # 新增轴
    def add_on_axis(self, index: int, axis: int = 0) -> None:
        axis = Numbers.keep_int_in_range(axis, 0, 1)
        if axis == 0:
            if index < 0 or index > self.row:
                EXCEPTION.fatal(f"Index {index} is out of bound at row!")
            # move entity if it is effected
            for e in self.__decorations.values():
                if e.y >= index:
                    e.move_downward(1)
        else:
            if index < 0 or index > self.column:
                EXCEPTION.fatal(f"Index {index} is out of bound at column!")
            # move entity if it is effected
            for e in self.__decorations.values():
                if e.x >= index:
                    e.move_right(1)
        self.__init_map(
            numpy.insert(self.__MAP, index, numpy.random.randint(len(self.__tile_lookup_table), size=self.__row if axis == 1 else self.__column), axis),
            numpy.insert(self.__BARRIER_MASK, index, numpy.zeros(self.__row if axis == 1 else self.__column), axis),
            TileMapImagesModule.TILE_SIZE,
        )

    # 移除轴
    def remove_on_axis(self, index: int, axis: int = 0) -> None:
        axis = Numbers.keep_int_in_range(axis, 0, 1)
        if axis == 0:
            if index < 0 or index >= self.row:
                EXCEPTION.fatal(f"Index {index} is out of bound at row!")
            for key in tuple(self.__decorations.keys()):
                # remove entity if it is on the deleted row
                if self.__decorations[key].y == index:
                    self.__decorations.pop(key)
                # move entity if it is effected
                elif self.__decorations[key].y > index:
                    self.__decorations[key].move_upward(1)
        else:
            if index < 0 or index >= self.column:
                EXCEPTION.fatal(f"Index {index} is out of bound at column!")
            for key in tuple(self.__decorations.keys()):
                # remove entity if it is on the deleted column
                if self.__decorations[key].x == index:
                    self.__decorations.pop(key)
                # move entity if it is effected
                elif self.__decorations[key].x > index:
                    self.__decorations[key].move_left(1)
        self.__init_map(numpy.delete(self.__MAP, index, axis), numpy.delete(self.__BARRIER_MASK, index, axis), TileMapImagesModule.TILE_SIZE)

    # 获取方块宽度
    @property
    def tile_width(self) -> int:
        return TileMapImagesModule.TILE_TEMPLE_WIDTH

    # 获取方块高度
    @property
    def tile_height(self) -> int:
        return TileMapImagesModule.TILE_TEMPLE_HEIGHT

    # 获取方块图片尺寸
    @property
    def tile_size(self) -> int:
        return TileMapImagesModule.TILE_SIZE

    # 以字典的形式获取地图的数据
    def to_dict(self) -> dict[str, Any]:
        # 重新生成最优 lookup table
        unique_elem_table: tuple = numpy.unique(self.__MAP, return_counts=True)
        lookup_table: dict[str, int] = {self.__tile_lookup_table[unique_elem_table[0][i]]: unique_elem_table[1][i] for i in range(len(unique_elem_table[0]))}
        sorted_lookup_table: list[str] = sorted(lookup_table, key=lookup_table.get, reverse=True)  # type: ignore
        # 返回数据
        return {
            "decoration": [_item.to_dict() for _item in sorted(self.__decorations.values())],
            "map": {
                "data": numpy.vectorize(lambda _num: sorted_lookup_table.index(self.__tile_lookup_table[_num]))(self.__MAP).tolist(),
                "lookup_table": sorted_lookup_table,
                "barrier": self.__BARRIER_MASK.tolist(),
            },
        }

    # 是否角色能通过该方块
    def is_passable(self, _x: int, _y: int, supposed: bool = False) -> bool:
        if not supposed:
            return bool(self.__BARRIER_MASK[_y, _x] == 0)
        else:
            if bool(self.__TILES_DATABASE[self.get_tile(_x, _y).split(":")[0]]["passable"]) is True:
                _decoration: DecorationObject | None = self.__decorations.get(self.__get_coordinate_format_key((_x, _y)))
                return _decoration is None or bool(self._DECORATION_DATABASE[_decoration.type]["passable"])
            return False

    # 以百分比的形式获取本地坐标（一般用于存档数据）
    def get_local_pos_in_percentage(self) -> dict[str, str]:
        return {"local_x": str(round(self.local_x * 100 / self.get_width(), 5)) + "%", "local_y": str(round(self.local_y * 100 / self.get_height(), 5)) + "%"}

    # 根据坐标寻找装饰物
    def get_decoration(self, pos: object) -> DecorationObject | None:
        return self.__decorations.get(self.__get_coordinate_format_key(Coordinates.convert(pos)))

    # 新增装饰物
    def add_decoration(self, _item: dict | DecorationObject) -> None:
        if isinstance(_item, dict):
            _item = DecorationObject.from_dict(_item)
        self.__decorations[self.__get_coordinate_format_key(_item.get_pos())] = _item

    # 移除装饰物
    def remove_decoration(self, decoration: DecorationObject) -> None:
        self.__decorations.pop(self.__get_coordinate_format_key(decoration.get_pos()))

    # 获取装饰物数量
    def count_decorations(self) -> int:
        return len(self.__decorations)

    # 控制地图放大缩小
    def set_tile_size(self, newPerBlockWidth: int_f) -> None:
        # 记录老尺寸
        old_width: int = self.get_width()
        old_height: int = self.get_height()
        # 更新尺寸
        TileMapImagesModule.update_size(round(newPerBlockWidth))
        self.set_size(self.tile_width * max(self.__column, self.__row), self.tile_height * max(self.__column, self.__row))
        self.__don_save_old_map_surface_for_next_update = True
        if self.get_width() < Display.get_width():
            self.set_width(Display.get_width())
        if self.get_height() < Display.get_height():
            self.set_height(Display.get_height())
        # 自动校准坐标
        self.add_local_x((old_width - self.get_width()) / 2)
        self.add_local_y((old_height - self.get_height()) / 2)
        # 打上需要更新的标签
        self._refresh()

    # 设置local坐标
    def set_local_x(self, value: int_f) -> None:
        old_local_x: int = self.local_x
        super().set_local_x(value)
        if self.local_x != old_local_x:
            self.__need_update_surface = True

    def set_local_y(self, value: int_f) -> None:
        old_local_y: int = self.local_y
        super().set_local_y(value)
        if self.local_y != old_local_y:
            self.__need_update_surface = True

    # 获取title image, 子类可重写
    def _get_tile_image(self, x: int, y: int) -> StaticImage:
        return TileMapImagesModule.get_image(self.get_tile(x, y))

    # 把地图画到屏幕上
    def render(self, _surface: ImageSurface, screen_to_move_x: int = 0, screen_to_move_y: int = 0) -> tuple[int, int]:
        # 检测屏幕是不是移到了不移到的地方
        _min_local_x: int = _surface.get_width() - self.get_width()
        if self.local_x < _min_local_x:
            self.set_local_x(_min_local_x)
            screen_to_move_x = 0
        elif self.local_x > 0:
            self.set_local_x(0)
            screen_to_move_x = 0
        _min_local_y: int = _surface.get_height() - self.get_height()
        if self.local_y < _min_local_y:
            self.set_local_y(_min_local_y)
            screen_to_move_y = 0
        elif self.local_y > 0:
            self.set_local_y(0)
            screen_to_move_y = 0
        # 如果需要重新绘制地图
        if self.__need_update_surface is True:
            self.__need_update_surface = False
            if self.__need_to_recheck_tile_on_surface is True:
                if self.__background_image is not None:
                    self.__background_image.set_size(_surface.get_width(), _surface.get_height())
                if TileMapImagesModule.DARKNESS > 0:
                    if not self.__don_save_old_map_surface_for_next_update:
                        self.__map_surface_old = self.__map_surface
                    else:
                        self.__don_save_old_map_surface_for_next_update = False
                self.__map_surface = Surfaces.transparent(self.get_size())
                self.__tile_on_surface.fill(0)
                self.__need_to_recheck_tile_on_surface = False
            # 画出地图
            for y in range(self.__row):
                for x in range(self.__column):
                    posTupleTemp: tuple[int, int] = self.calculate_position(x, y)
                    if -self.tile_width <= posTupleTemp[0] < _surface.get_width() and -self.tile_width <= posTupleTemp[1] < _surface.get_height():
                        if self.__tile_on_surface[y, x] == 0:
                            evn_img: StaticImage = self._get_tile_image(x, y)
                            evn_img.set_pos(posTupleTemp[0] - self.local_x, posTupleTemp[1] - self.local_y)
                            evn_img.set_local_offset_availability(False)
                            if self.__map_surface is not None:
                                evn_img.draw(self.__map_surface)
                            self.__tile_on_surface[y, x] = 1
                            if y < self.__row - 1:
                                self.__tile_on_surface[y + 1, x] = 0
                            if x < self.__column - 1:
                                self.__tile_on_surface[y, x + 1] = 0
                        else:
                            pass
                    elif posTupleTemp[0] >= _surface.get_width() or posTupleTemp[1] >= _surface.get_height():
                        break
                if self.calculate_position(0, y + 1)[1] >= _surface.get_height():
                    break
        # 画出背景
        if self.__background_image is not None:
            self.__background_image.draw(_surface)
        else:
            _surface.fill(Colors.BLACK)
        if self.__map_surface is not None:
            _surface.blit(self.__map_surface.subsurface(-self.local_x, -self.local_y, _surface.get_width(), _surface.get_height()), ORIGIN)
        if self.__map_surface_old is not None:
            _surface.blit(self.__map_surface_old.subsurface(-self.local_x, -self.local_y, _surface.get_width(), _surface.get_height()), ORIGIN)
            _alpha: int | None = self.__map_surface_old.get_alpha()
            if _alpha is None:
                EXCEPTION.fatal("Invalid alpha detected while processing self.__map_surface_old.get_alpha()")
            _alpha = max(0, _alpha - Display.get_delta_time())
            if _alpha > 0:
                self.__map_surface_old.set_alpha(_alpha)
            else:
                self.__map_surface_old = None
        # 返回offset
        return screen_to_move_x, screen_to_move_y

    # 获取方块
    def get_tile(self, _x: int, _y: int) -> str:
        return self.__tile_lookup_table[int(self.__MAP[_y, _x])]

    # 更新方块
    def set_tile(self, _x: int, _y: int, name: str) -> None:
        # 根据坐标更新地图块
        try:
            self.__MAP[_y, _x] = self.__tile_lookup_table.index(name)
        except ValueError:
            self.__tile_lookup_table.append(name)
            self.__MAP[_y, _x] = len(self.__tile_lookup_table) - 1
        # 需更新
        self._refresh()

    # 更新方块
    def replace_tiles(self, from_tile: str, to_tile: str) -> None:
        # the tile id for 'from tile' in the lookup table
        from_tile_index: int = -1
        # the tile id for 'to tile' in the lookup table
        to_tile_index: int = -1
        # if 'from tile' exists in the lookup table
        try:
            from_tile_index = self.__tile_lookup_table.index(from_tile)
        # if 'from tile' does not exist in the lookup table
        except ValueError:
            # then nothing to replace
            return
        # if 'to tile' already exists in the lookup table
        try:
            # get 'to tile' id
            to_tile_index = self.__tile_lookup_table.index(to_tile)
            # replace
            self.__MAP[self.__MAP == from_tile_index] = to_tile_index
        # if 'to tile' does not exist in the lookup table
        except ValueError:
            # replace the tile name in lookup table
            self.__tile_lookup_table[from_tile_index] = to_tile
        # refresh and we are done
        self._refresh()

    # 计算在地图中的方块
    @abstractmethod
    def calculate_coordinate(self, on_screen_pos: tuple[int, int] | None = None) -> tuple[int, int] | None:
        EXCEPTION.fatal("calculate_coordinate()", 1)

    # 计算在地图中的位置
    @abstractmethod
    def calculate_position(self, x: int_f, y: int_f) -> tuple[int, int]:
        EXCEPTION.fatal("calculate_position()", 1)

    # 寻找2点之间的最短路径
    def find_path(self, start: tuple[int, int], goal: tuple[int, int], lenMax: int | None = None, map2d: numpy.ndarray | None = None) -> list[tuple[int, int]]:
        # 初始化寻路地图
        if map2d is None:
            map2d = numpy.ones(self.shape, dtype=numpy.byte)
        # subtract mask
        map2d = numpy.subtract(map2d, self.__BARRIER_MASK.transpose())
        # 如果目标坐标合法
        if 0 <= goal[1] < self.__row and 0 <= goal[0] < self.__column and map2d[goal[0], goal[1]] == 1:
            # 开始寻路
            _path: list[tuple[int, int]] = AStar.search(map2d, start, goal)
            # 预处理路径并返回
            return _path[:lenMax] if lenMax is not None and len(_path) > lenMax else _path
        # 返回空列表
        return []


# 战斗系统接口，请勿实例化
class AbstractBattleSystem(AbstractGameSystem, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        # 用于判断是否移动屏幕的参数
        self.__mouse_move_temp_x: int = -1
        self.__mouse_move_temp_y: int = -1
        self._screen_to_move_speed_x: int | None = None
        self._screen_to_move_speed_y: int | None = None
        # 用于检测是否有方向键被按到的字典
        self.__moving_screen_in_direction_up: bool = False
        self.__moving_screen_in_direction_down: bool = False
        self.__moving_screen_in_direction_left: bool = False
        self.__moving_screen_in_direction_right: bool = False
        # 角色数据
        self._entities_data: dict[str, dict[str, Entity]] = {}
        # 地图数据
        self.__map: AbstractTileMap | None = None
        # 方格标准尺寸
        self._standard_tile_size: int = Display.get_width() // 10
        # 当前鼠标位置上的tile块
        self._tile_is_hovering: tuple[int, int] | None = None

    # 渲染出所有的entity - 子类需实现
    @abstractmethod
    def _display_entities(self, _surface: ImageSurface) -> None:
        EXCEPTION.fatal("_display_entities()", 1)

    # 加载角色的数据 - 子类需实现
    @abstractmethod
    def _load_entities(self, _entities: dict, _mode: str) -> None:
        EXCEPTION.fatal("_load_entities()", 1)

    # 初始化并加载新场景 - 子类需实现
    @abstractmethod
    def new(self, chapterType: str, chapterId: int, projectName: str | None = None) -> None:
        EXCEPTION.fatal("new()", 1)

    # 获取地图
    def get_map(self) -> AbstractTileMap:
        if self.__map is not None:
            return self.__map
        else:
            EXCEPTION.fatal("Map has not been initialized!")

    # 获取地图
    def set_map(self, _map: AbstractTileMap) -> None:
        self.__map = _map

    # 加载地图数据
    def _load_map(self, _data: dict) -> None:
        self.get_map().update(_data, self._standard_tile_size)

    # 处理数据
    def _process_data(self, _data: dict) -> None:
        # 初始化角色信息
        self._load_entities(_data.get("entities", {}), _data.get("_mode", "default"))
        # 初始化地图
        self._load_map(_data)

    # 获取地图文件所在的具体路径
    def get_data_file_path(self) -> str:
        return (
            os.path.join("Data", self._chapter_type, f"chapter{self._chapter_id}_map.{Config.get_file_type()}")
            if self._project_name is None
            else os.path.join("Data", self._chapter_type, self._project_name, f"chapter{self._chapter_id}_map.{Config.get_file_type()}")
        )

    # 返回需要保存数据
    def _get_data_need_to_save(self) -> dict:
        _data: dict = {"entities": {}, "linpg": Info.get_current_version()}
        for faction, entitiesDict in self._entities_data.items():
            _data["entities"][faction] = {}
            for key in entitiesDict:
                _data["entities"][faction][key] = entitiesDict[key].to_dict()
        _data.update(self.get_data_of_parent_game_system())
        _data.update(self.get_map().to_dict())
        return _data

    # 检测按下按键的事件
    def _check_key_down(self, event: PG_Event) -> None:
        if event.key == Keys.ARROW_UP:
            self.__moving_screen_in_direction_up = True
        elif event.key == Keys.ARROW_DOWN:
            self.__moving_screen_in_direction_down = True
        elif event.key == Keys.ARROW_LEFT:
            self.__moving_screen_in_direction_left = True
        elif event.key == Keys.ARROW_RIGHT:
            self.__moving_screen_in_direction_right = True

    # 检测按键回弹的事件
    def _check_key_up(self, event: PG_Event) -> None:
        if event.key == Keys.ARROW_UP:
            self.__moving_screen_in_direction_up = False
        elif event.key == Keys.ARROW_DOWN:
            self.__moving_screen_in_direction_down = False
        elif event.key == Keys.ARROW_LEFT:
            self.__moving_screen_in_direction_left = False
        elif event.key == Keys.ARROW_RIGHT:
            self.__moving_screen_in_direction_right = False

    # 检测手柄事件
    def _check_joystick_events(self) -> None:
        self.__moving_screen_in_direction_up = round(Controller.joystick.get_axis(4)) == -1
        self.__moving_screen_in_direction_down = round(Controller.joystick.get_axis(4)) == 1
        self.__moving_screen_in_direction_right = round(Controller.joystick.get_axis(3)) == 1
        self.__moving_screen_in_direction_left = round(Controller.joystick.get_axis(3)) == -1

    # 展示地图
    def _display_map(self, _surface: ImageSurface) -> None:
        # 处理鼠标事件
        for event in Controller.get_events():
            if event.type == Events.KEY_DOWN:
                self._check_key_down(event)
            elif event.type == Events.KEY_UP:
                self._check_key_up(event)
        # 处理手柄事件
        if Controller.joystick.get_init():
            self._check_joystick_events()
        # 检测是否使用了鼠标移动了地图的本地坐标
        if Controller.mouse.get_pressed(2):
            if self.__mouse_move_temp_x == -1 and self.__mouse_move_temp_y == -1:
                self.__mouse_move_temp_x = Controller.mouse.x
                self.__mouse_move_temp_y = Controller.mouse.y
            else:
                if self.__mouse_move_temp_x != Controller.mouse.x or self.__mouse_move_temp_y != Controller.mouse.y:
                    if self.__mouse_move_temp_x != Controller.mouse.x:
                        self.get_map().add_local_x(self.__mouse_move_temp_x - Controller.mouse.x)
                    if self.__mouse_move_temp_y != Controller.mouse.y:
                        self.get_map().add_local_y(self.__mouse_move_temp_y - Controller.mouse.y)
                    self.__mouse_move_temp_x = Controller.mouse.x
                    self.__mouse_move_temp_y = Controller.mouse.y
        else:
            self.__mouse_move_temp_x = -1
            self.__mouse_move_temp_y = -1
        # 根据按键情况设定要移动的数值
        if self.__moving_screen_in_direction_up is True:
            if self._screen_to_move_speed_y is None:
                self._screen_to_move_speed_y = self.get_map().tile_height // 4
            else:
                self._screen_to_move_speed_y += self.get_map().tile_height // 4
        if self.__moving_screen_in_direction_down is True:
            if self._screen_to_move_speed_y is None:
                self._screen_to_move_speed_y = -self.get_map().tile_height // 4
            else:
                self._screen_to_move_speed_y -= self.get_map().tile_height // 4
        if self.__moving_screen_in_direction_left is True:
            if self._screen_to_move_speed_x is None:
                self._screen_to_move_speed_x = self.get_map().tile_width // 4
            else:
                self._screen_to_move_speed_x += self.get_map().tile_width // 4
        if self.__moving_screen_in_direction_right is True:
            if self._screen_to_move_speed_x is None:
                self._screen_to_move_speed_x = -self.get_map().tile_width // 4
            else:
                self._screen_to_move_speed_x -= self.get_map().tile_width // 4
        # 如果需要移动屏幕
        # 注意，因为self._screen_to_move_speed可能是复数，所以//会可能导致问题
        temp_value: int
        if self._screen_to_move_speed_x is not None:
            temp_value = self.get_map().get_local_x() + int(self._screen_to_move_speed_x / 5)
            if Display.get_width() - self.get_map().get_width() <= temp_value <= 0:
                self.get_map().set_local_x(temp_value)
                self._screen_to_move_speed_x = int(self._screen_to_move_speed_x * 4 / 5)
                if self._screen_to_move_speed_x == 0:
                    self._screen_to_move_speed_x = None
            else:
                self._screen_to_move_speed_x = None
        if self._screen_to_move_speed_y is not None:
            temp_value = self.get_map().get_local_y() + int(self._screen_to_move_speed_y / 5)
            if Display.get_height() - self.get_map().get_height() <= temp_value <= 0:
                self.get_map().set_local_y(temp_value)
                self._screen_to_move_speed_y = int(self._screen_to_move_speed_y * 4 / 5)
                if self._screen_to_move_speed_y == 0:
                    self._screen_to_move_speed_y = None
            else:
                self._screen_to_move_speed_y = None
        # 展示地图
        self._screen_to_move_speed_x, self._screen_to_move_speed_y = self.get_map().render(
            _surface,
            self._screen_to_move_speed_x if self._screen_to_move_speed_x is not None else 0,
            self._screen_to_move_speed_y if self._screen_to_move_speed_y is not None else 0,
        )
        # 获取位于鼠标位置的tile块
        self._tile_is_hovering = self.get_map().calculate_coordinate()
        # 展示角色动画
        self._display_entities(_surface)


# 地图编辑器系统
class AbstractMapEditor(AbstractBattleSystem, metaclass=ABCMeta):
    # 修改模式
    @enum.verify(enum.UNIQUE)
    class _MODIFY(enum.IntEnum):
        DISABLE = enum.auto()
        DELETE_ENTITY = enum.auto()
        DELETE_ROW = enum.auto()
        DELETE_COLUMN = enum.auto()
        ADD_ROW_ABOVE = enum.auto()
        ADD_ROW_BELOW = enum.auto()
        ADD_COLUMN_BEFORE = enum.auto()
        ADD_COLUMN_AFTER = enum.auto()

    def __init__(self) -> None:
        # 初始化父类
        super().__init__()
        # 初始化ui
        self.__buttons_container: GameObjectsDictContainer = UI.generate_container("map_editor_buttons")
        self.__right_container_buttons: GameObjectsDictContainer = UI.generate_container("map_editor_right_container_buttons")
        self.__UIContainerRight: StaticImage = StaticImage("<&ui>container.png", 0, 0)
        self.__UIContainerRight.rotate(90)
        self.__UIContainerBottom: StaticImage = StaticImage("<&ui>container.png", 0, 0)
        self.__bottom_container_buttons: GameObjectsListContainer = GameObjectsListContainer(None, 0, 0, 0, 0)
        self.__entitiesImagesContainers: list = []
        self.__entitiesImagesContainerUsingIndex: int = -1
        self.__envImgContainer: SurfaceContainerWithScrollBar = SurfaceContainerWithScrollBar(None, 0, 0, 0, 0, Axis.VERTICAL)
        self.__decorationsImgContainer: SurfaceContainerWithScrollBar = SurfaceContainerWithScrollBar(None, 0, 0, 0, 0, Axis.VERTICAL)
        # 用于储存即将发下的物品的具体参数
        self.__object_to_put_down: dict = {}
        # 未保存离开时的警告
        self.__no_save_warning: GameObjectsDictContainer = UI.generate_container("leave_without_saving_warning")
        # 选中框
        self._select_rect: Rectangle = Rectangle(0, 0, 0, 0)
        self._select_pos: tuple = tuple()
        # 是否是修改模式
        self._modify_mode: AbstractMapEditor._MODIFY = self._MODIFY.DISABLE
        # 是否有ui容器被鼠标触碰
        self._no_container_is_hovered: bool = False
        # 是否展示barrier mask
        self._show_barrier_mask: bool = False
        # 关卡历史
        self.__level_data_history: list[dict] = []
        # 代表当前关卡历史的index
        self.__current_level_data_index: int = -1

    # 根据数据更新特定的角色 - 子类需实现
    @abstractmethod
    def update_entity(self, faction: str, key: str, data: dict) -> None:
        EXCEPTION.fatal("update_entity()", 1)

    # 返回需要保存数据
    def _get_data_need_to_save(self) -> dict:
        return Config.load_file(self.get_data_file_path()) | super()._get_data_need_to_save()

    # 是否有物品被选中
    def is_any_object_selected(self) -> bool:
        return len(self.__object_to_put_down) > 0

    # 处理关键数据
    def _process_data(self, _data: dict) -> None:
        # 确保地图初始化
        _map_p: list | None = _data.get("map")
        if _map_p is None or len(_map_p) == 0:
            lookup_table: list[str] = ["snow:2", "snow:3", "snow:4", "snow:5", "snow:6", "snow:7"]
            tile_y: int = 50
            tile_x: int = 50
            _data["map"] = {
                "array2d": [[Numbers.get_random_int(0, len(lookup_table) - 1) for _ in range(tile_x)] for _ in range(tile_y)],
                "lookup_table": lookup_table,
            }
        _data["_mode"] = "dev"
        # 开始处理数据
        super()._process_data(_data)

    # 加载地图
    def __load_level(self, data: dict) -> None:
        tempLocal_x, tempLocal_y = self.get_map().get_local_pos()
        self._process_data(data)
        self.get_map().set_local_pos(tempLocal_x, tempLocal_y)

    # 重置地图历史
    def __reset_level_history(self) -> None:
        # 重置历史
        self.__level_data_history.clear()
        self.__current_level_data_index = -1
        self.__append_level_history()

    # 新增历史
    def __append_level_history(self) -> None:
        self.__level_data_history = self.__level_data_history[: self.__current_level_data_index + 1]
        self.__level_data_history.append(self._get_data_need_to_save())
        self.__current_level_data_index += 1

    # 初始化UI
    def _init_ui(self) -> None:
        """加载右侧的界面"""
        # 加载容器图片
        container_width: int = Display.get_width() // 5
        container_height: int = Display.get_height()
        button_width: int = Display.get_width() // 25
        button_height: int = Display.get_height() // 5
        padding: int = Display.get_height() // 100
        self.__right_container_buttons.get("select_tile").set_left(
            (
                container_width
                - self.__right_container_buttons.get("select_tile").get_width()
                - self.__right_container_buttons.get("select_decoration").get_width()
                - padding
            )
            // 2
        )
        self.__right_container_buttons.get("select_decoration").set_left(self.__right_container_buttons.get("select_tile").right + padding)
        self.__UIContainerRight.set_size(container_width, container_height)
        self.__UIContainerButtonRight = MovableStaticImage(
            "<&ui>container_button.png",
            Display.get_width() - button_width,
            (Display.get_height() - button_height) // 2,
            Display.get_width() - button_width - container_width,
            (Display.get_height() - button_height) // 2,
            container_width // 10,
            0,
            button_width,
            button_height,
        )
        self.__UIContainerButtonRight.rotate(90)
        # 加载背景图片
        self.__envImgContainer.set_pos(container_width * 3 // 40, Display.get_height() // 10)
        self.__envImgContainer.set_size(container_width * 17 // 20, Display.get_height() * 17 // 20)
        if TileMapImagesModule.DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET is None:
            EXCEPTION.fatal("Image sprite sheet for tile map is not loaded correctly!")
        for key, value in TileMapImagesModule.DEFAULT_TILE_MAP_IMAGE_SPRITE_SHEET.to_dict().items():
            if not isinstance(value, tuple):
                self.__envImgContainer.set(key, Images.resize(value, (self.get_map().tile_size / 3, None)))
            else:
                for i, _ref in enumerate(value):
                    self.__envImgContainer.set(f"{key}:{i}", Images.resize(_ref, (self.get_map().tile_size / 3, None)))
        self.__envImgContainer.set_item_per_line(4)
        self.__envImgContainer.set_scroll_bar_pos("right")
        self.__envImgContainer.set_visible(True)
        self.__envImgContainer.distance_between_item = padding
        # 加载所有的装饰品
        self.__decorationsImgContainer.set_pos(container_width * 3 // 40, Display.get_height() // 10)
        self.__decorationsImgContainer.set_size(container_width * 17 // 20, Display.get_height() * 17 // 20)
        # 确保装饰物材质模块已经初始化
        DecorationImagesModule.init()
        # 加载默认装饰物
        for key, value in DecorationImagesModule.DEFAULT_DECORATION_IMAGE_SPRITE_SHEET.to_dict().items():
            if not isinstance(value, tuple):
                self.__decorationsImgContainer.set(key, Images.resize(value, (self.get_map().tile_size / 3, None)))
            else:
                for i, _ref in enumerate(value):
                    self.__decorationsImgContainer.set(f"{key}:{i}", Images.resize(_ref, (self.get_map().tile_size / 3, None)))
        # 加载自带的装饰物
        for key, value in DecorationImagesModule.CUSTOM_DECORATION_IMAGE_SPRITE_SHEET.to_dict().items():
            if not isinstance(value, tuple):
                self.__decorationsImgContainer.set(key, Images.resize(value, (self.get_map().tile_size / 3, None)))
            else:
                for i, _ref in enumerate(value):
                    self.__decorationsImgContainer.set(f"{key}:{i}", Images.resize(_ref, (self.get_map().tile_size / 3, None)))
        # 设置容器参数
        self.__decorationsImgContainer.set_item_per_line(4)
        self.__decorationsImgContainer.set_scroll_bar_pos("right")
        self.__decorationsImgContainer.set_visible(False)
        self.__decorationsImgContainer.distance_between_item = padding
        """加载下方的界面"""
        container_width = Display.get_width() * 4 // 5
        container_height = Display.get_height() * 3 // 10
        button_width = Display.get_width() * 7 // 50
        button_height = Display.get_height() // 20
        self.__UIContainerBottom.set_size(container_width, container_height)
        self.__UIContainerButtonBottom = MovableStaticImage(
            "<&ui>container_button.png",
            (container_width - button_width) // 2,
            Display.get_height() - button_height,
            (container_width - button_width) // 2,
            Display.get_height() - button_height - container_height,
            0,
            container_height // 10,
            button_width,
            button_height,
        )
        # 加载所有角色的图片文件
        for faction in os.listdir(EntitySpriteImageManager.SPRITES_PATH):
            newContainer: SurfaceContainerWithScrollBar = SurfaceContainerWithScrollBar(
                None, container_width // 40, container_height * 3 // 10, container_width * 19 // 20, container_height * 3 // 5, Axis.HORIZONTAL, faction
            )
            for img_name in os.listdir(os.path.join(EntitySpriteImageManager.SPRITES_PATH, faction)):
                newContainer.set(
                    img_name,
                    Images.smoothly_resize(
                        EntitySpriteImageManager.try_get_image_references(faction, img_name, "wait").get_image(0).get_image_copy(),
                        (None, container_height // 3),
                    ),
                )
            newContainer.set_scroll_bar_pos("bottom")
            newContainer.distance_between_item = padding
            self.__entitiesImagesContainers.append(newContainer)
            newButton: Button = Button.load("<&ui>button.png", (0, 0), (0, 0), 100)
            newButton.set_text(ButtonComponent.text(Lang.get_text("General", faction), button_height // 2, Colors.BLACK, alpha_when_not_hover=100))
            newButton.set_auto_resize(True)
            if len(self.__bottom_container_buttons) > 0:
                newButton.set_left(self.__bottom_container_buttons[len(self.__bottom_container_buttons) - 1].right + padding)
            else:
                self.__entitiesImagesContainerUsingIndex = 0
            self.__bottom_container_buttons.append(newButton)
        self.__object_to_put_down.clear()
        # 设置按钮位置
        # ----- 第一行 -----
        self.__buttons_container.get("back").set_left(self.__buttons_container.get("save").get_right() + padding)
        self.__buttons_container.get("delete_entity").set_left(self.__buttons_container.get("back").get_right() + padding)
        self.__buttons_container.get("undo").set_left(self.__buttons_container.get("delete_entity").get_right() + padding)
        self.__buttons_container.get("redo").set_left(self.__buttons_container.get("undo").get_right() + padding)
        self.__buttons_container.get("reload").set_left(self.__buttons_container.get("redo").get_right() + padding)
        # ----- 第二行 -----
        self.__buttons_container.get("add_row_above").set_left(self.__buttons_container.get("save").get_left())
        self.__buttons_container.get("add_row_below").set_left(self.__buttons_container.get("add_row_above").get_right() + padding)
        self.__buttons_container.get("add_colum_before").set_left(self.__buttons_container.get("add_row_below").get_right() + padding)
        self.__buttons_container.get("add_colum_after").set_left(self.__buttons_container.get("add_colum_before").get_right() + padding)
        self.__buttons_container.get("delete_row").set_left(self.__buttons_container.get("add_colum_after").get_right() + padding)
        self.__buttons_container.get("delete_colum").set_left(self.__buttons_container.get("delete_row").get_right() + padding)
        # ----- 第三行 -----
        self.__buttons_container.get("auto_add_barriers").set_left(self.__buttons_container.get("save").get_left())
        self.__buttons_container.get("add_barrier").set_left(self.__buttons_container.get("auto_add_barriers").get_right() + padding)

    # 初始化并加载新场景
    def new(self, chapterType: str, chapterId: int, projectName: str | None = None) -> None:
        self._initialize(chapterType, chapterId, projectName)
        self._process_data(Config.load_file(self.get_data_file_path()))
        self._init_ui()
        self.__reset_level_history()

    # 重写load_progress - 功能上应和new一直，并忽略其他数据
    def load_progress(self, _data: dict) -> None:
        self.new(_data["chapter_type"], _data["chapter_id"], _data.get("project_name"))

    # 设置装饰物
    def set_decoration(self, _item: str | None, _pos: tuple[int, int]) -> None:
        # 查看当前位置是否有装饰物
        decoration: DecorationObject | None = self.get_map().get_decoration(self._tile_is_hovering)
        # 如果发现有冲突的装饰物
        if decoration is not None:
            # 则移除
            self.get_map().remove_decoration(decoration)
        # if _item is None, then it means remove only
        if _item is None:
            return
        self.get_map().add_decoration({"id": _item, "x": _pos[0], "y": _pos[1]})

    # 删除实体
    def delete_entity(self, _filter: Callable[[Entity], bool]) -> bool:
        delete_one: bool = False
        for _value in self._entities_data.values():
            for key in tuple(_value.keys()):
                if _filter(_value[key]):
                    _value.pop(key)
                    delete_one = True
        return delete_one

    # move the entity
    def move_entity(self, _filter: Callable[[Entity], bool], x: int, y: int) -> None:
        for vl in self._entities_data.values():
            for e in vl.values():
                if _filter(e):
                    e.set_x(round(e.x) + x)
                    e.set_y(round(e.y) + y)

    # 设置实体
    def set_entity(self, _item: str | None, _pos: tuple[int, int]) -> None:
        # 尝试移除坐标冲突的实体
        self.delete_entity(lambda e: Coordinates.is_same(e, _pos))
        # if _item is None, then it means remove only
        if _item is None:
            return
        # 生成需要更新的数据
        _new_data: dict = copy.deepcopy(Entity.get_entity_data(_item))
        _new_data.update({"x": _pos[0], "y": _pos[1], "type": _item})
        the_id: int = 0
        nameTemp: str = f"{_item}_{the_id}"
        while nameTemp in self._entities_data[_new_data["faction"]]:
            the_id += 1
            nameTemp = f"{_item}_{the_id}"
        self.update_entity(_new_data["faction"], nameTemp, _new_data)

    # 设置区块
    def set_tile(self, _item: str, _pos: tuple[int, int]) -> None:
        self.get_map().set_tile(*_pos, _item)

    # 删除指定坐标上的实体
    def delete_entity_on_tile(self, _pos: tuple[int, int]) -> None:
        # 优先移除barrier mask
        if not self.get_map().is_passable(_pos[0], _pos[1]):
            self.get_map().set_barrier_mask(_pos[0], _pos[1], 0)
        else:
            # 如果发现有冲突的装饰物
            if self.get_map().get_decoration(_pos) is not None:
                self.set_decoration(None, _pos)
            else:
                self.set_entity(None, _pos)

    # 将地图制作器的界面画到屏幕上
    def draw(self, _surface: ImageSurface) -> None:
        UIContainerRight_offset_pos: tuple[int, int] = (self.__UIContainerButtonRight.right, 0)
        UIContainerBottom_offset_pos: tuple[int, int] = (0, self.__UIContainerButtonBottom.bottom)
        self._no_container_is_hovered = not self.__UIContainerRight.is_hovered(UIContainerRight_offset_pos) and not self.__UIContainerBottom.is_hovered(
            UIContainerBottom_offset_pos
        )
        # 确保无选中
        if len(self._select_pos) > 0:
            pass
        # 如果鼠标confirm
        elif Controller.get_event("confirm"):
            # 显示或隐藏右侧的容器
            if self.__UIContainerButtonRight.is_hovered():
                self.__UIContainerButtonRight.switch()
                self.__UIContainerButtonRight.flip(True)
            # 显示或隐藏下侧的容器
            elif self.__UIContainerButtonBottom.is_hovered():
                self.__UIContainerButtonBottom.switch()
                self.__UIContainerButtonBottom.flip(False, True)
            elif self._tile_is_hovering is not None and self.__buttons_container.item_being_hovered is None:
                whether_add_history: bool = True
                _tile_is_hovering: tuple[int, int] = self._tile_is_hovering
                if self._modify_mode == self._MODIFY.DELETE_ENTITY:
                    self.delete_entity_on_tile(_tile_is_hovering)
                # 移除行
                elif self._modify_mode == self._MODIFY.DELETE_ROW:
                    self.get_map().remove_on_axis(_tile_is_hovering[1])
                    self.delete_entity(lambda e: round(e.y) == _tile_is_hovering[1])
                    self.move_entity(lambda e: round(e.y) > _tile_is_hovering[1], 0, -1)
                # 移除列
                elif self._modify_mode == self._MODIFY.DELETE_COLUMN:
                    self.get_map().remove_on_axis(_tile_is_hovering[0], 1)
                    self.delete_entity(lambda e: round(e.x) == _tile_is_hovering[0])
                    self.move_entity(lambda e: round(e.x) > _tile_is_hovering[0], -1, 0)
                elif self._modify_mode == self._MODIFY.ADD_ROW_ABOVE:
                    self.get_map().add_on_axis(_tile_is_hovering[1])
                    self.move_entity(lambda e: round(e.y) >= _tile_is_hovering[1], 0, 1)
                elif self._modify_mode == self._MODIFY.ADD_ROW_BELOW:
                    self.get_map().add_on_axis(_tile_is_hovering[1] + 1)
                    self.move_entity(lambda e: round(e.y) >= _tile_is_hovering[1] + 1, 0, 1)
                elif self._modify_mode == self._MODIFY.ADD_COLUMN_BEFORE:
                    self.get_map().add_on_axis(_tile_is_hovering[0], 1)
                    self.move_entity(lambda e: round(e.x) >= _tile_is_hovering[0], 1, 0)
                elif self._modify_mode == self._MODIFY.ADD_COLUMN_AFTER:
                    self.get_map().add_on_axis(_tile_is_hovering[0] + 1, 1)
                    self.move_entity(lambda e: round(e.x) >= _tile_is_hovering[0] + 1, 1, 0)
                elif self._modify_mode == self._MODIFY.DISABLE:
                    if self.is_any_object_selected() is True and self._no_container_is_hovered is True:
                        if self.__object_to_put_down["type"] == "tile":
                            self.set_tile(self.__object_to_put_down["id"], self._tile_is_hovering)
                        elif self.__object_to_put_down["type"] == "decoration":
                            self.set_decoration(self.__object_to_put_down["id"], self._tile_is_hovering)
                        elif self.__object_to_put_down["type"] == "entity":
                            self.set_entity(self.__object_to_put_down["id"], self._tile_is_hovering)
                    else:
                        whether_add_history = False
                else:
                    EXCEPTION.fatal(f"Unknown modify mode {self._modify_mode}")
                # 保存修改后的历史
                if whether_add_history is True:
                    self.__append_level_history()
        # 如果鼠标右键
        elif (
            Controller.get_event("hard_confirm")
            and self.is_any_object_selected() is True
            and self._no_container_is_hovered is True
            and self._tile_is_hovering is not None
            and self.__buttons_container.item_being_hovered is None
        ):
            if self.__object_to_put_down["type"] == "tile":
                self.get_map().replace_tiles(self.get_map().get_tile(*self._tile_is_hovering), self.__object_to_put_down["id"])
                self.__append_level_history()
        # 取消选中
        elif Controller.get_event("back") or (self._no_container_is_hovered is True and Controller.get_event("scroll_up")):
            self.__object_to_put_down.clear()
            self._modify_mode = self._MODIFY.DISABLE
            self._show_barrier_mask = False
        # 直接用del按键
        elif Controller.get_event("delete"):
            any_deleted: bool = False
            for theEntities in self._entities_data.values():
                for e in tuple(theEntities.keys()):
                    if theEntities[e].get_selected():
                        theEntities.pop(e)
                        any_deleted = True
            if not any_deleted and self._tile_is_hovering is not None:
                self.delete_entity_on_tile(self._tile_is_hovering)

        # 画出地图
        self._display_map(_surface)

        # 画出右侧容器的UI
        self.__UIContainerButtonRight.draw(_surface)
        if self.__UIContainerButtonRight.right < _surface.get_width():
            self.__UIContainerRight.display(_surface, UIContainerRight_offset_pos)
            self.__envImgContainer.display(_surface, UIContainerRight_offset_pos)
            self.__decorationsImgContainer.display(_surface, UIContainerRight_offset_pos)
            self.__right_container_buttons.display(_surface, UIContainerRight_offset_pos)
            if Controller.get_event("confirm") is True:
                if self.__right_container_buttons.item_being_hovered == "select_tile":
                    self.__envImgContainer.set_visible(True)
                    self.__decorationsImgContainer.set_visible(False)
                elif self.__right_container_buttons.item_being_hovered == "select_decoration":
                    self.__envImgContainer.set_visible(False)
                    self.__decorationsImgContainer.set_visible(True)
                else:
                    if self.__envImgContainer.is_visible() and self.__envImgContainer.item_being_hovered is not None:
                        self.__object_to_put_down = {"type": "tile", "id": self.__envImgContainer.item_being_hovered}
                    elif self.__decorationsImgContainer.is_visible() and self.__decorationsImgContainer.item_being_hovered is not None:
                        self.__object_to_put_down = {"type": "decoration", "id": self.__decorationsImgContainer.item_being_hovered}

        # 画出下方容器的UI
        self.__UIContainerButtonBottom.draw(_surface)
        if self.__UIContainerButtonBottom.bottom < _surface.get_height():
            self.__UIContainerBottom.display(_surface, UIContainerBottom_offset_pos)
            if self.__entitiesImagesContainerUsingIndex >= 0:
                self.__entitiesImagesContainers[self.__entitiesImagesContainerUsingIndex].display(_surface, UIContainerBottom_offset_pos)
            self.__bottom_container_buttons.display(_surface, UIContainerBottom_offset_pos)
            if Controller.get_event("confirm"):
                if self.__bottom_container_buttons.item_being_hovered >= 0:
                    self.__entitiesImagesContainerUsingIndex = self.__bottom_container_buttons.item_being_hovered
                elif (
                    self.__entitiesImagesContainerUsingIndex >= 0
                    and self.__entitiesImagesContainers[self.__entitiesImagesContainerUsingIndex].item_being_hovered is not None
                ):
                    self.__object_to_put_down = {
                        "type": "entity",
                        "container_id": self.__entitiesImagesContainerUsingIndex,
                        "id": self.__entitiesImagesContainers[self.__entitiesImagesContainerUsingIndex].item_being_hovered,
                    }

        # 画出选中框
        if self._no_container_is_hovered is True and Controller.mouse.get_pressed_since(0):
            if len(self._select_pos) <= 0:
                self._select_pos = Controller.mouse.get_pos()
            # 设置宽度
            new_width: int = Controller.mouse.x - self._select_pos[0]
            self._select_rect.set_width(abs(new_width))
            self._select_rect.set_left(self._select_pos[0] if new_width >= 0 else Controller.mouse.x)
            # 设置高度
            new_height: int = Controller.mouse.y - self._select_pos[1]
            self._select_rect.set_height(abs(new_height))
            self._select_rect.set_top(self._select_pos[1] if new_height >= 0 else Controller.mouse.y)
            # 将选中框画到屏幕上
            self._select_rect.draw_outline(_surface)
        else:
            self._select_pos = tuple()

        # 画出上方按钮
        self.__buttons_container.draw(_surface)
        if Controller.get_event("confirm") and len(self.__object_to_put_down) <= 0:
            show_barrier_mask: bool = False
            if self.__buttons_container.item_being_hovered is not None:
                self._modify_mode = self._MODIFY.DISABLE
            if self.__buttons_container.item_being_hovered == "save":
                self._save()
            elif self.__buttons_container.item_being_hovered == "back":
                if Config.load(self.get_data_file_path()) == self._get_data_need_to_save():
                    self.stop()
                else:
                    self.__no_save_warning.set_visible(True)
            elif self.__buttons_container.item_being_hovered == "delete_entity":
                self.__object_to_put_down.clear()
                self._modify_mode = self._MODIFY.DELETE_ENTITY
            elif self.__buttons_container.item_being_hovered == "reload":
                self.__load_level(Config.load_file(self.get_data_file_path()))
                self.__reset_level_history()
            elif self.__buttons_container.item_being_hovered == "undo":
                if self.__current_level_data_index > 0:
                    self.__current_level_data_index -= 1
                    self.__load_level(self.__level_data_history[self.__current_level_data_index])
            elif self.__buttons_container.item_being_hovered == "redo":
                if self.__current_level_data_index < len(self.__level_data_history) - 1:
                    self.__current_level_data_index += 1
                    self.__load_level(self.__level_data_history[self.__current_level_data_index])
            elif self.__buttons_container.item_being_hovered == "add_colum_before":
                self._modify_mode = self._MODIFY.ADD_COLUMN_BEFORE
            elif self.__buttons_container.item_being_hovered == "add_colum_after":
                self._modify_mode = self._MODIFY.ADD_COLUMN_AFTER
            elif self.__buttons_container.item_being_hovered == "add_row_above":
                self._modify_mode = self._MODIFY.ADD_ROW_ABOVE
            elif self.__buttons_container.item_being_hovered == "add_row_below":
                self._modify_mode = self._MODIFY.ADD_ROW_BELOW
            elif self.__buttons_container.item_being_hovered == "delete_row":
                self._modify_mode = self._MODIFY.DELETE_ROW
            elif self.__buttons_container.item_being_hovered == "delete_colum":
                self._modify_mode = self._MODIFY.DELETE_COLUMN
            elif self.__buttons_container.item_being_hovered == "auto_add_barriers":
                # 历遍地图，设置障碍区块
                for _x in range(self.get_map().column):
                    for _y in range(self.get_map().row):
                        if not self.get_map().is_passable(_x, _y, True):
                            self.get_map().set_barrier_mask(_x, _y, 1)
                self.__append_level_history()
            elif self.__buttons_container.item_being_hovered == "add_barrier":
                show_barrier_mask = True
            else:
                show_barrier_mask = self._show_barrier_mask
                if self._show_barrier_mask is True and self._tile_is_hovering is not None:
                    self.get_map().set_barrier_mask(self._tile_is_hovering[0], self._tile_is_hovering[1], 1)
                    self.__append_level_history()
            self._show_barrier_mask = show_barrier_mask

        # 跟随鼠标显示即将被放下的物品
        if self.is_any_object_selected() is True:
            if self.__object_to_put_down["type"] == "tile":
                _surface.blit(self.__envImgContainer.get(str(self.__object_to_put_down["id"])), Controller.mouse.get_pos())
            elif self.__object_to_put_down["type"] == "decoration":
                _surface.blit(self.__decorationsImgContainer.get(str(self.__object_to_put_down["id"])), Controller.mouse.get_pos())
            elif self.__object_to_put_down["type"] == "entity":
                _surface.blit(
                    self.__entitiesImagesContainers[int(self.__object_to_put_down["container_id"])].get(self.__object_to_put_down["id"]),
                    Controller.mouse.get_pos(),
                )

        # 未保存离开时的警告
        self.__no_save_warning.draw(_surface)
        if Controller.get_event("confirm"):
            # 保存并离开
            if self.__no_save_warning.item_being_hovered == "save":
                self._save()
                self.stop()
            # 取消
            elif self.__no_save_warning.item_being_hovered == "cancel":
                self.__no_save_warning.set_visible(False)
            # 不保存并离开
            elif self.__no_save_warning.item_being_hovered == "dont_save":
                self.stop()
