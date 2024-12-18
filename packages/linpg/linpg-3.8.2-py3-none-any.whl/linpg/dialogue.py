"""
结构:
component -> render -> abstract -> dialog -> editor
"""

import pyvns

from .ui import *


# 对话模块Node
class DialogNode(Button):
    def __init__(self, key_name: str, font_size: int, next_keys: list[str], tag: str = ""):
        self.__key_name: str = key_name
        button_surface = ArtisticFont.render_description_box(self.__key_name, Colors.BLACK, font_size, font_size // 2, Colors.WHITE)
        super().__init__(button_surface, 0, 0, width=button_surface.get_width(), height=button_surface.get_height(), tag=tag)
        self.__next_keys: tuple[str, ...] = tuple(next_keys)
        self.has_been_displayed: bool = False

    # 下一个keys
    @property
    def next_keys(self) -> tuple[str, ...]:
        return self.__next_keys

    # 展示（注意，你无法在此输入off_set，你必须提前设置）
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if offSet != ORIGIN:
            EXCEPTION.fatal("You cannot set off set for DialogNode object!")
        super().display(_surface, offSet)


# 对话key向导窗口
class DialogNavigationWindow(AbstractFrame):
    def __init__(self, x: int_f, y: int_f, width: int_f, height: int_f, tag: str = ""):
        super().__init__(x, y, width, height, tag=tag)
        self.__nodes_map: dict[str, DialogNode] = {}
        self.__current_selected_key: str = "head"
        self.__font_size: int = 10
        self.__most_right: int = 0
        self.__most_top: int = 0
        self.__most_bottom: int = 0

    # 新增node
    def add_node(self, key: str, next_keys: list[str]) -> None:
        self.__nodes_map[key] = DialogNode(key, self.__font_size, next_keys)
        self._if_update_needed = True

    # 重新添加全部的key
    def read_all(self, dialogs_data: dict[str, pyvns.Dialogue]) -> None:
        self.__nodes_map.clear()
        for key, theDialog in dialogs_data.items():
            next_keys: list[str] = []
            if not theDialog.next.is_null():
                if theDialog.next.has_multi_targets():
                    for next_keys_options in theDialog.next.get_targets():
                        next_keys.append(next_keys_options["id"])
                else:
                    next_keys.append(theDialog.next.get_target())
            self.add_node(key, next_keys)

    # 更新选中的key
    def update_selected(self, new_current_select: str) -> None:
        self.__current_selected_key = new_current_select
        self._if_update_needed = True

    # 获取当前选中的key
    def get_selected_key(self) -> str:
        return self.__current_selected_key

    def __update_node_pos(self, key: str = "head", offset_x: int = 0, offset_y: int = 0) -> int:
        key_node: DialogNode = self.__nodes_map[key]
        if not key_node.has_been_displayed:
            # 设置坐标并展示
            key_node.set_pos(offset_x, offset_y)
            key_node.has_been_displayed = True
            padding: int = 4 * self.__font_size
            if len(key_node.next_keys) > 1:
                offset_y = key_node.y - len(key_node.next_keys) * self.__font_size - padding
            for child_key in key_node.next_keys:
                offset_y = self.__update_node_pos(child_key, key_node.x + self.__font_size * 10, offset_y)
                offset_y += padding
            if self.__most_right < key_node.right:
                self.__most_right = key_node.right
            if self.__most_bottom < key_node.bottom:
                self.__most_bottom = key_node.bottom
            if self.__most_top > key_node.top:
                self.__most_top = key_node.top
        return offset_y

    def __draw_node(self, _surface: ImageSurface, key: str = "head") -> None:
        key_node: DialogNode = self.__nodes_map[key]
        if not key_node.has_been_displayed:
            # 设置坐标并展示
            key_node.display(_surface)
            key_node.has_been_displayed = True

            if self.__current_selected_key == key:
                Draw.rect(_surface, Colors.RED, key_node.get_rect(), 4)

            for child_key in key_node.next_keys:
                self.__draw_node(_surface, child_key)
                Draw.line(_surface, Colors.BLACK, key_node.right_center, self.__nodes_map[child_key].left_center, 3)

    def _update(self) -> None:
        if "head" in self.__nodes_map:
            for key in self.__nodes_map:
                self.__nodes_map[key].has_been_displayed = False
            self.__most_right = 0
            self.__most_bottom = 0
            self.__update_node_pos()
            for key in self.__nodes_map:
                self.__nodes_map[key].has_been_displayed = False
                self.__nodes_map[key].move_upward(self.__most_top)
            self._content_surface = Surfaces.transparent((self.__most_right, self.__most_bottom - self.__most_top))
            self.__draw_node(self._content_surface)
            self._if_update_needed = False
        else:
            EXCEPTION.fatal("Head is missing")

    def _any_content_container_event(self) -> bool:
        for key, value in self.__nodes_map.items():
            if Controller.mouse.is_in_rect(
                value.x + self.x - self.get_local_x(), value.y + self.y + self._get_bar_height() - self.get_local_y(), value.get_width(), value.get_height()
            ):
                self.update_selected(key)
                return True
        return False


# 对话框模块基础框架
class AbstractDialogBox(Hidable, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        # 对胡框数据
        self._dialogue_box_max_height: int = Display.get_height() // 4
        self._dialogue_box_max_y: int = Display.get_height() * 65 // 100
        # 对胡框图片
        self._dialogue_box: StaticImage = StaticImage("<&ui>dialoguebox.png", Display.get_width() * 13 // 100, 0, Display.get_width() * 74 // 100)

    # 画出（子类需实现）
    @abstractmethod
    def draw(self, _surface: ImageSurface) -> None:
        EXCEPTION.fatal("draw()", 1)

    # 更新内容（子类需实现）
    @abstractmethod
    def update(self, narrator: str, contents: list) -> None:
        EXCEPTION.fatal("update()", 1)


# 对话开发模块
class EditableDialogBox(AbstractDialogBox):
    def __init__(self, fontSize: int):
        super().__init__()
        self.__contents: MultipleLinesInputBox = MultipleLinesInputBox(
            Display.get_width() * 2 / 10, Display.get_height() * 73 // 100, fontSize, Colors.WHITE, fontSize * 8
        )
        self.__narrator: SingleLineInputBox = SingleLineInputBox(
            Display.get_width() * 2 / 10, self._dialogue_box_max_y + fontSize, fontSize, Colors.WHITE, fontSize * 4
        )
        # 设置对话框高度和坐标
        self._dialogue_box.set_top(self._dialogue_box_max_y)
        self._dialogue_box.set_height(self._dialogue_box_max_height)

    # 是否内容相比上次有任何改变
    def any_changed_was_made(self) -> bool:
        return self.__narrator.need_save or self.__contents.need_save

    # 获取当前讲述人
    def get_narrator(self) -> str:
        return self.__narrator.get_text()

    # 获取当前内容
    def get_content(self) -> list:
        return self.__contents.get_text()

    # 更新内容
    def update(self, narrator: str | None, contents: list | None) -> None:
        if narrator is None:
            self.__narrator.set_text()
        else:
            self.__narrator.set_text(narrator)
        if contents is None:
            self.__contents.set_text()
        else:
            self.__contents.set_text(contents)

    # 画出
    def draw(self, _surface: ImageSurface) -> None:
        if self.is_visible():
            # 画上对话框图片
            self._dialogue_box.draw(_surface)
            # 将文字画到屏幕上
            self.__narrator.draw(_surface)
            self.__contents.draw(_surface)


# 对话框和对话框内容
class DialogBox(AbstractDialogBox):
    # 翻页指示动态图标数据管理模块
    class __NextPageIndicatorIcon:
        def __init__(self) -> None:
            self.__status: bool = False
            self.__x_offset: float = 0
            self.__y_offset: float = 0

        def draw_to(self, _surface: ImageSurface, _x: int, _y: int, _width: int) -> None:
            # 更新坐标数值
            if not self.__status:
                self.__x_offset += Display.get_delta_time() / 30
                self.__y_offset += Display.get_delta_time() / 20
                if self.__y_offset >= _width / 2:
                    self.__status = True
            else:
                self.__x_offset -= Display.get_delta_time() / 30
                self.__y_offset -= Display.get_delta_time() / 20
                if self.__y_offset <= 0:
                    self.__status = False
            final_y: int = int(_y + self.__y_offset)
            # 渲染
            Draw.polygon(
                _surface,
                Colors.WHITE,
                ((_x + int(self.__x_offset), final_y), (_x + _width - int(self.__x_offset), final_y), (_x + _width // 2, final_y + _width)),
            )

    def __init__(self, fontSize: int):
        super().__init__()
        self.FONT: FontGenerator = Font.create(fontSize)
        self.__contents: list = []
        self.__narrator: str = ""
        self.__text_index: int = 0
        self.__next_text_index_count: int = 0
        self.__next_text_index_count_required: int = 10
        self.__displayed_lines: int = 0
        self.__textPlayingSound: Sound | None = None
        if os.path.exists(_path := Specification.get_directory("sound", "ui", "dialog_words_playing.ogg")):
            self.__textPlayingSound = Sounds.load(_path)
        self.__READING_SPEED: int = max(int(Setting.get("ReadingSpeed")), 1)
        # 翻页指示动态图标
        self.__next_page_indicator_icon = self.__NextPageIndicatorIcon()
        # 自动播放时参考的总阅读时间
        self.__read_time: int = 0
        # 总共的字数
        self.__total_letters: int = 0
        # 是否处于自动播放模式
        self.__auto_mode: bool = False
        # 是否处于淡出阶段
        self.__fade_out_stage: bool = False
        # 设置对话框高度和坐标
        self._dialogue_box.set_top(-1)
        self._dialogue_box.set_height(0)

    # 重置
    def reset(self) -> None:
        self.__fade_out_stage = False
        self._dialogue_box.set_height(0)
        self._dialogue_box.set_top(-1)

    # 是否所有内容均已展出
    def is_all_played(self) -> bool:
        # 如果self.__contents是空的，也就是说没有任何内容，那么应当视为所有内容都被播放了
        return len(self.__contents) == 0 or (
            self.__displayed_lines >= len(self.__contents) - 1 and self.__text_index >= len(self.__contents[self.__displayed_lines]) - 1
        )

    # 立刻播出所有内容
    def play_all(self) -> None:
        if not self.is_all_played():
            self.__displayed_lines = max(len(self.__contents) - 1, 0)
            self.__text_index = max(len(self.__contents[self.__displayed_lines]) - 1, 0)
            self.__next_text_index_count = self.__next_text_index_count_required

    # 更新内容
    def update(self, narrator: str | None, contents: list | None, forceNotResizeDialogueBox: bool = False) -> None:
        self.stop_playing_text_sound()
        # 重设部分参数
        self.__text_index = 0
        self.__next_text_index_count = 0
        self.__displayed_lines = 0
        self.__total_letters = 0
        self.__read_time = 0
        # 更新文字内容
        self.__contents = contents if contents is not None else []
        for text in self.__contents:
            self.__total_letters += len(text)
        # 更新讲述者名称
        if narrator is None:
            narrator = ""
        if self.__narrator != narrator and not forceNotResizeDialogueBox:
            self.__fade_out_stage = True
        self.__narrator = narrator

    # 获取文字播放时的音效的音量
    def get_sound_volume(self) -> float:
        if self.__textPlayingSound is not None:
            return self.__textPlayingSound.get_volume()
        else:
            return 0.0

    # 修改文字播放时的音效的音量
    def set_sound_volume(self, volume: number) -> None:
        if self.__textPlayingSound is not None:
            self.__textPlayingSound.set_volume(volume)

    # 是否开启自动播放模式
    def set_playing_automatically(self, value: bool) -> None:
        self.__auto_mode = value

    # 是否需要更新
    def is_update_needed(self) -> bool:
        return self.__auto_mode is True and self.__read_time >= self.__total_letters * 100

    # 如果音效还在播放则停止播放文字音效
    @staticmethod
    def stop_playing_text_sound() -> None:
        if LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL is not None and LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL.get_busy():
            LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL.stop()

    def set_visible(self, visible: bool) -> None:
        super().set_visible(visible)
        # 如果声音在播放时模块被隐藏，则停止播放音效
        if self.is_hidden():
            self.stop_playing_text_sound()

    # 展示
    def draw(self, _surface: ImageSurface) -> None:
        if self.is_visible():
            # 渐入
            if not self.__fade_out_stage:
                # 如果当前对话框图片的y坐标不存在（一般出现在对话系统例行初始化后），则根据屏幕大小设置一个
                if self._dialogue_box.y < 0:
                    self._dialogue_box.set_top(self._dialogue_box_max_y + self._dialogue_box_max_height / 2)
                # 画出对话框
                self._dialogue_box.draw(_surface)
                # 如果对话框图片还在放大阶段
                if self._dialogue_box.height < self._dialogue_box_max_height:
                    self._dialogue_box.set_height(
                        min(self._dialogue_box.height + self._dialogue_box_max_height * Display.get_delta_time() // 200, self._dialogue_box_max_height)
                    )
                    self._dialogue_box.move_upward(self._dialogue_box_max_height * Display.get_delta_time() // 400)
                # 如果已经放大好了，则将文字画到屏幕上
                else:
                    self._dialogue_box.set_top(self._dialogue_box_max_y)
                    x: int = _surface.get_width() * 2 // 10
                    y: int = _surface.get_height() * 73 // 100
                    # 写上当前讲话人的名字
                    if len(self.__narrator) > 0:
                        _surface.blit(self.FONT.render(self.__narrator, Colors.WHITE), (x, self._dialogue_box.y + self.FONT.size))
                    # 对话框已播放的内容
                    for i in range(self.__displayed_lines):
                        _surface.blit(self.FONT.render(self.__contents[i], Colors.WHITE), (x, y + self.FONT.size * 3 * i // 2))
                    # make sure self.__contents is not empty
                    if self.__displayed_lines < len(self.__contents):
                        # 对话框正在播放的内容
                        _surface.blit(
                            self.FONT.render(self.__contents[self.__displayed_lines][: self.__text_index], Colors.WHITE),
                            (x, y + self.FONT.size * 3 * self.__displayed_lines // 2),
                        )
                        # 如果当前行的字符还没有完全播出
                        if self.__text_index < len(self.__contents[self.__displayed_lines]):
                            # 播放文字音效
                            if (
                                LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL is not None
                                and not LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL.get_busy()
                                and self.__textPlayingSound is not None
                            ):
                                LINPG_RESERVED_CHANNELS.SOUND_EFFECTS_CHANNEL.play(self.__textPlayingSound)
                            if self.__next_text_index_count < self.__next_text_index_count_required:
                                self.__next_text_index_count += Display.get_delta_time()
                            else:
                                self.__text_index += 1
                                self.__next_text_index_count = 0
                        # 当前行的所有字都播出后，播出下一行
                        elif self.__displayed_lines < len(self.__contents) - 1:
                            self.__text_index = 0
                            self.__next_text_index_count = 0
                            self.__displayed_lines += 1
                        # 当所有行都播出后
                        else:
                            self.stop_playing_text_sound()
                            if self.__auto_mode is True and self.__read_time < self.__total_letters * 100:
                                self.__read_time += Display.get_delta_time() * self.__READING_SPEED
                    # 画出翻页指示动态图标
                    _width: int = self.FONT.size * 2 // 3
                    self.__next_page_indicator_icon.draw_to(_surface, self._dialogue_box.right - _width * 4, self._dialogue_box.bottom - _width * 3, _width)
            # 淡出
            else:
                # 画出对话框图片
                self._dialogue_box.draw(_surface)
                height_t: int = self._dialogue_box.height - int(self._dialogue_box_max_height * Display.get_delta_time() // 200)
                if height_t > 0:
                    self._dialogue_box.set_height(height_t)
                    self._dialogue_box.move_downward(self._dialogue_box_max_height * Display.get_delta_time() // 400)
                else:
                    self.reset()


# update naming database
pyvns.Naming.update_database(DataBase.get("Npc"))


# 视觉小说脚本编译器
class ScriptCompiler(pyvns.Compiler):

    # compile
    @classmethod
    def compile(cls, path: str, out_dir: str | None = None) -> None:
        if not os.path.isdir(path) and path.endswith(".vns"):
            _data: dict[str, Any] = cls.load(path)
            Config.save(
                os.path.join(
                    out_dir if out_dir is not None else os.path.dirname(path), f"chapter{_data['id']}_dialogs_{_data['language']}.{Config.get_file_type()}"
                ),
                _data,
            )
        else:
            for _file in glob(os.path.join(path, "*")):
                cls.compile(_file, out_dir)

    # 从有效的视觉小说文件路径中读取信息
    @staticmethod
    def extract_info_from_path(_path: str) -> tuple[int, str]:
        _path = os.path.basename(_path)
        if not _path.startswith("chapter"):
            EXCEPTION.fatal("Invalid path!")
        # 返回 id, 语言
        return int(_path[7 : _path.index("_")]), _path[_path.rfind("_") + 1 : _path.rfind(".")]


class DialoguesManager(pyvns.DialoguesManager):

    # 指向上一个对话数据的指针
    @property
    def previous(self) -> pyvns.Dialogue | None:
        return self.get_previous()

    # 指向当前对话数据的指针
    @property
    def current(self) -> pyvns.Dialogue:
        return self.get_current()

    @property
    def section(self) -> str:
        return self.get_section()


# 角色立绘滤镜
class AbstractVisualNovelCharacterImageFilterEffect(ABC):
    # 将滤镜应用到立绘上并渲染到屏幕上
    @abstractmethod
    def render(self, characterImage: StaticImage, _surface: ImageSurface, is_silent: bool) -> None:
        EXCEPTION.fatal("render()", 1)


# 角色立绘系统
class VisualNovelCharacterImageManager:
    # 用于存放立绘的字典
    __character_image: Final[dict[str, tuple[StaticImage, ...]]] = {}
    # 存放前一对话的参与角色名称
    __previous_characters: tuple[pyvns.Naming, ...] = tuple()
    __last_round_image_alpha: int = 2550
    # 存放当前对话的参与角色名称
    __current_characters: tuple[pyvns.Naming, ...] = tuple()
    __this_round_image_alpha: int = 0
    # 滤镜
    FILTERS: Final[dict[str, AbstractVisualNovelCharacterImageFilterEffect]] = {}
    # 暗度
    DARKNESS: int = 50
    # 移动的x
    __x_correction_offset_index: int = 0
    # x轴offset
    __x_offset_for_this_round: int = 0
    __x_offset_for_last_round: int = 0
    # 开发者模式
    dev_mode: bool = False
    # 被点击的角色
    character_get_click: str | None = None

    # 立绘边长
    @staticmethod
    def __GET_WIDTH() -> int:
        return Display.get_width() // 2

    # 重置并卸载占用的内存
    @classmethod
    def reset(cls) -> None:
        cls.__previous_characters = tuple()
        cls.__last_round_image_alpha = 2550
        cls.__current_characters = tuple()
        cls.__this_round_image_alpha = 0
        cls.__character_image.clear()

    # 画出角色
    @classmethod
    def __display_character(cls, _name_data: pyvns.Naming, x: int, alpha: int, _surface: ImageSurface) -> None:
        if alpha > 0:
            # 确保角色存在
            if _name_data.get_name() not in cls.__character_image:
                # 如果不能存在，则加载角色
                imgTemp: StaticImage = StaticImage(
                    Specification.get_directory("character_image", _name_data.get_name()), 0, 0, cls.__GET_WIDTH(), cls.__GET_WIDTH()
                )
                # 以tuple的形式保存立绘，index 0 是正常图片， index 1 是深色图片
                cls.__character_image[_name_data.get_name()] = (imgTemp, imgTemp.copy())
                # 生成深色图片
                cls.__character_image[_name_data.get_name()][1].add_darkness(cls.DARKNESS)
            # 是否角色沉默
            isNpcSilent: bool = _name_data.contains_tag("silent")
            # 获取npc立绘的指针
            img: StaticImage = cls.__character_image[_name_data.get_name()][1 if isNpcSilent else 0]
            img.set_size(cls.__GET_WIDTH(), cls.__GET_WIDTH())
            img.set_alpha(alpha)
            img.set_pos(x, Display.get_height() - cls.__GET_WIDTH())
            # 获取tag长度
            _tags_len = len(_name_data.get_tags())
            # 不需要渲染silent标签
            if isNpcSilent is True:
                _tags_len -= 1
            if _tags_len > 0:
                for _tag in _name_data.get_tags():
                    if _tag != "silent":
                        cls.FILTERS[_tag].render(img, _surface, isNpcSilent)
            else:
                img.set_crop_rect(None)
                img.draw(_surface)
            # 如果是开发模式
            if cls.dev_mode is True and img.is_hovered():
                img.draw_outline(_surface)
                cls.character_get_click = _name_data.to_string()

    # 根据参数计算立绘的x坐标
    @staticmethod
    def __estimate_x(_width: int, _num: int, _index: int) -> int:
        if _num == 1:
            return _width // 4
        elif _num == 2:
            return _index * _width // _num
        elif _num > 2:
            return int((_index + 1) * _width / (_num + 1) - _width / 4) if _num % 2 == 0 else int((_index - _num // 2) * _width / _num + _width / 4)
        else:
            return 0

    # 渐入name1角色的同时淡出name2角色
    @classmethod
    def __fade_in_and_out_characters(cls, name1: pyvns.Naming, name2: pyvns.Naming, x: int, _surface: ImageSurface) -> None:
        cls.__display_character(name1, x, cls.__last_round_image_alpha // 10, _surface)
        cls.__display_character(name2, x, cls.__this_round_image_alpha // 10, _surface)

    # 渐入所有当前的角色
    @classmethod
    def __fade_in_characters_this_round(cls, _surface: ImageSurface, _start: int = 0) -> None:
        for i in range(_start, len(cls.__current_characters)):
            cls.__display_character(
                cls.__current_characters[i],
                cls.__estimate_x(_surface.get_width(), len(cls.__current_characters), i) + cls.__x_offset_for_this_round,
                cls.__this_round_image_alpha // 10,
                _surface,
            )

    # 淡出所有之前的角色
    @classmethod
    def __fade_out_characters_last_round(cls, _surface: ImageSurface, _start: int = 0) -> None:
        for i in range(_start, len(cls.__previous_characters)):
            cls.__display_character(
                cls.__previous_characters[i],
                cls.__estimate_x(_surface.get_width(), len(cls.__previous_characters), i) + cls.__x_offset_for_last_round,
                cls.__last_round_image_alpha // 10,
                _surface,
            )

    # 更新立绘
    @classmethod
    def update(cls, characterNameList: Sequence[str] | None) -> None:
        cls.__previous_characters = cls.__current_characters
        cls.__current_characters = tuple(pyvns.Naming(_name) for _name in characterNameList) if characterNameList is not None else tuple()
        cls.__last_round_image_alpha = 2550
        cls.__this_round_image_alpha = 50
        cls.__x_correction_offset_index = 0

    # 将立绘画到屏幕上
    @classmethod
    def draw(cls, _surface: ImageSurface) -> None:
        # 更新alpha值，并根据alpha值计算offset
        if cls.__last_round_image_alpha > 0:
            cls.__last_round_image_alpha -= Display.get_delta_time() * 8
            cls.__x_offset_for_last_round = int(cls.__GET_WIDTH() / 4 - cls.__GET_WIDTH() / 4 * cls.__last_round_image_alpha / 2550)
        else:
            cls.__x_offset_for_last_round = 0
        if cls.__this_round_image_alpha < 2550:
            cls.__this_round_image_alpha += Display.get_delta_time() * 15
            cls.__x_offset_for_this_round = int(cls.__GET_WIDTH() / 4 * cls.__this_round_image_alpha / 2550 - cls.__GET_WIDTH() / 4)
        else:
            cls.__x_offset_for_this_round = 0
        # 初始化被选择的角色名字
        cls.character_get_click = None
        # 画上上一幕的立绘
        if len(cls.__previous_characters) == len(cls.__current_characters):
            for i, _characterName in enumerate(cls.__previous_characters):
                npcImg_x: int = cls.__estimate_x(_surface.get_width(), len(cls.__previous_characters), i)
                # 渲染立绘
                if _characterName.equal(cls.__current_characters[i], True):
                    cls.__display_character(cls.__current_characters[i], npcImg_x, 255, _surface)
                else:
                    cls.__display_character(_characterName, npcImg_x, cls.__last_round_image_alpha // 10, _surface)
                    cls.__display_character(cls.__current_characters[i], npcImg_x, cls.__this_round_image_alpha // 10, _surface)
        elif len(cls.__current_characters) == 0:
            cls.__fade_out_characters_last_round(_surface)
        elif len(cls.__previous_characters) == 0:
            cls.__fade_in_characters_this_round(_surface)
        else:
            # 初始化previous_x坐标
            previous_x: int
            if len(cls.__previous_characters) == 1 and len(cls.__current_characters) == 2:
                previous_x = cls.__estimate_x(_surface.get_width(), len(cls.__previous_characters), 0)
                # 如果之前的中间变成了现在的左边，则立绘应该先向左移动
                if cls.__previous_characters[0].equal(cls.__current_characters[0]):
                    if cls.__x_correction_offset_index < 100:
                        cls.__x_correction_offset_index += 10
                    # 渐入左边立绘
                    cls.__fade_in_and_out_characters(
                        cls.__previous_characters[0],
                        cls.__current_characters[0],
                        cls.__x_correction_offset_index * (cls.__estimate_x(_surface.get_width(), len(cls.__current_characters), 0) - previous_x) // 100
                        + previous_x,
                        _surface,
                    )
                    # 显示右边立绘
                    cls.__display_character(cls.__current_characters[1], _surface.get_width() // 2, cls.__this_round_image_alpha // 10, _surface)
                # 如果之前的中间变成了现在的右边，则立绘应该先向右移动
                elif cls.__previous_characters[0].equal(cls.__current_characters[1]):
                    if cls.__x_correction_offset_index < 100:
                        cls.__x_correction_offset_index += 10
                    # 显示左边立绘
                    cls.__display_character(cls.__current_characters[0], 0, cls.__this_round_image_alpha // 10, _surface)
                    # 渐入右边立绘
                    cls.__fade_in_and_out_characters(
                        cls.__previous_characters[0],
                        cls.__current_characters[1],
                        cls.__x_correction_offset_index * (cls.__estimate_x(_surface.get_width(), len(cls.__current_characters), 1) - previous_x) // 100
                        + previous_x,
                        _surface,
                    )
                # 之前的中间和现在两边无任何关系，先隐藏之前的立绘，然后显示现在的立绘
                elif cls.__last_round_image_alpha > 0:
                    cls.__this_round_image_alpha -= Display.get_delta_time() * 15
                    cls.__fade_out_characters_last_round(_surface)
                else:
                    cls.__fade_in_characters_this_round(_surface)
            elif len(cls.__previous_characters) == 2 and len(cls.__current_characters) == 1:
                current_x: int = cls.__estimate_x(_surface.get_width(), len(cls.__current_characters), 0)
                # 如果之前的左边变成了现在的中间，则立绘应该先向右边移动
                if cls.__previous_characters[0].equal(cls.__current_characters[0]):
                    if cls.__x_correction_offset_index < 100:
                        cls.__x_correction_offset_index += 10
                        previous_x = cls.__estimate_x(_surface.get_width(), len(cls.__previous_characters), 0)
                        # 左边立绘向右移动
                        cls.__fade_in_and_out_characters(
                            cls.__previous_characters[0],
                            cls.__current_characters[0],
                            cls.__x_correction_offset_index * (current_x - previous_x) // 100 + previous_x,
                            _surface,
                        )
                    else:
                        # 显示左方立绘
                        cls.__display_character(cls.__current_characters[0], current_x, cls.__this_round_image_alpha // 10, _surface)
                    # 右边立绘消失
                    cls.__display_character(cls.__previous_characters[1], _surface.get_width() // 2, cls.__last_round_image_alpha // 10, _surface)
                # 如果之前的右边变成了现在的中间，则立绘应该先向左边移动
                elif cls.__previous_characters[1].equal(cls.__current_characters[0]):
                    if cls.__x_correction_offset_index < 100:
                        cls.__x_correction_offset_index += 10
                        previous_x = cls.__estimate_x(_surface.get_width(), len(cls.__previous_characters), 1)
                        # 右边立绘向左移动
                        cls.__fade_in_and_out_characters(
                            cls.__previous_characters[1],
                            cls.__current_characters[0],
                            cls.__x_correction_offset_index * (current_x - previous_x) // 100 + previous_x,
                            _surface,
                        )
                    else:
                        # 显示右方立绘
                        cls.__display_character(cls.__current_characters[0], current_x, cls.__this_round_image_alpha // 10, _surface)
                    # 左边立绘消失
                    cls.__display_character(cls.__previous_characters[0], 0, cls.__last_round_image_alpha // 10, _surface)
                elif cls.__last_round_image_alpha > 0:
                    cls.__this_round_image_alpha -= Display.get_delta_time() * 15
                    cls.__fade_out_characters_last_round(_surface)
                else:
                    cls.__fade_in_characters_this_round(_surface)
            elif cls.__last_round_image_alpha > 0:
                cls.__this_round_image_alpha -= Display.get_delta_time() * 15
                cls.__fade_out_characters_last_round(_surface)
            else:
                cls.__fade_in_characters_this_round(_surface)


# 视觉小说系统接口
class AbstractVisualNovelPlayer(AbstractGameSystem, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        self._content: DialoguesManager = DialoguesManager()
        # 黑色Void帘幕
        self._black_bg = StaticImage(Surfaces.colored(Display.get_size(), Colors.BLACK), 0, 0, Display.get_width(), Display.get_height())
        # 对话文件路径
        self._dialog_folder_path: str = "Data"
        # 背景图片
        self.__background_image_name: str = ""
        self.__background_image_surface: StaticImage | VideoSurface = self._black_bg.copy()
        # 是否静音
        self._is_muted: bool = False
        # 选项菜单
        self._dialog_options_container: GameObjectsListContainer = GameObjectsListContainer("<NULL>", 0, 0, 0, 0)
        self._dialog_options_container.set_visible(False)
        # 更新背景音乐音量
        self.set_bgm_volume(Volume.get_background_music() / 100)
        # 文字大小
        self._FONT_SIZE: int = Display.get_width() * 3 // 200
        # 初始化滤镜系统
        VisualNovelCharacterImageManager.reset()

    # 获取对话框模块（子类需实现）
    @abstractmethod
    def _get_dialog_box(self) -> AbstractDialogBox:
        return EXCEPTION.fatal("_dialogBox()", 1)

    # 获取对话文件所在的文件夹目录
    def get_dialog_folder_location(self) -> str:
        return (
            os.path.join(self._dialog_folder_path, self._chapter_type)
            if self._project_name is None
            else os.path.join(self._dialog_folder_path, self._chapter_type, self._project_name)
        )

    # 获取对话文件所在的具体路径
    def get_dialog_file_location(self, lang: str) -> str:
        return os.path.join(self.get_dialog_folder_location(), f"chapter{self._chapter_id}_dialogs_{lang}.{Config.get_file_type()}")

    # 获取对话文件所在的具体路径
    def get_data_file_path(self) -> str:
        return self.get_dialog_file_location(Setting.get_language())

    # 获取对话文件的主语言
    def get_default_lang(self) -> str:
        # 读取项目信息
        _data: dict = Config.load_file(
            os.path.join(self._dialog_folder_path, self._chapter_type, f"info.{Config.get_file_type()}")
            if self._project_name is None
            else os.path.join(self._dialog_folder_path, self._chapter_type, self._project_name, f"info.{Config.get_file_type()}")
        )
        # 自3.7起使用default_language，出于兼容目的尝试读取default_lang（3.6前的key）
        return str(_data.get("default_language", _data.get("default_lang", "English")))

    # 返回需要保存数据
    def _get_data_need_to_save(self) -> dict:
        return self.get_data_of_parent_game_system() | {
            "dialog_id": self._content.get_current_dialogue_id(),
            "section": self._content.get_section(),
            "type": "dialog",
            "linpg": Info.get_current_version(),
        }

    # 读取存档
    def load_progress(self, _data: dict) -> None:
        self.new(_data["chapter_type"], _data["chapter_id"], _data["section"], _data.get("project_name"), _data.get("dialog_id", "head"))

    # 新读取章节
    def new(self, chapterType: str, chapterId: int, section: str, projectName: str | None = None, dialogId: str = "head") -> None:
        # 初始化关键参数
        self._initialize(chapterType, chapterId, projectName)
        # load the dialogue content data
        self._load_content()
        # select the section
        self._content.set_section(section)
        # select the base on given dialogue id
        self._content.set_current_dialogue_id(dialogId)
        # 将数据载入刚初始化的模块中
        self._update_scene(self._content.get_current_dialogue_id())

    # 载入数据
    def _load_content(self) -> None:
        # 如果玩家所选择的语种有对应的翻译，则优先读取，否则使用开发者的默认语种
        content_data: dict = Config.load_file(
            self.get_data_file_path() if os.path.exists(self.get_data_file_path()) else self.get_dialog_file_location(self.get_default_lang())
        )
        # try fetch "dialogs" for backward compatibility
        self._content.update(content_data.get("dialogues", content_data.get("dialogs")))

    # 更新背景图片
    def _update_background_image(self, image_name: str) -> None:
        if self.__background_image_name != image_name:
            # 更新背景的名称
            self.__background_image_name = image_name
            # 如果背景是视频，则应该停止，以防止内存泄漏
            if isinstance(self.__background_image_surface, VideoSurface):
                self.__background_image_surface.stop()
            # 更新背景的图片数据
            if len(self.__background_image_name) > 0:
                # 尝试加载图片式的背景
                if os.path.exists((img_path := Specification.get_directory("background_image", self.__background_image_name))):
                    self.__background_image_surface = StaticImage(img_path, 0, 0)
                    self.__background_image_surface.disable_cropping()
                # 如果在背景图片的文件夹里找不到对应的图片，则查看是否是视频文件
                elif os.path.exists(_path := Specification.get_directory("movie", self.__background_image_name)):
                    self.__background_image_surface = VideoSurface(_path, with_audio=False)
                else:
                    EXCEPTION.fatal(f"Cannot find a background image or video file called '{self.__background_image_name}'.")
            else:
                self.__background_image_surface = self._black_bg.copy()

    # 更新场景
    def _update_scene(self, dialog_id: str) -> None:
        # 更新dialogId
        self._content.set_current_dialogue_id(dialog_id)
        # 更新立绘和背景
        VisualNovelCharacterImageManager.update(self._content.current.character_images)
        self._update_background_image(self._content.current.background_image)
        # 更新对话框
        self._get_dialog_box().update(self._content.current.narrator, self._content.current.contents)
        # 更新背景音乐
        if len(self._content.current.background_music) > 0:
            self.set_bgm(Specification.get_directory("music", self._content.current.background_music))
        else:
            self.unload_bgm()
        # 隐藏选项菜单
        self._dialog_options_container.clear()
        self._dialog_options_container.set_visible(False)

    # 更新语言
    def update_language(self) -> None:
        super().update_language()
        # 保存原来的数据
        currentSect: str = self._content.get_section()
        currentId: str = self._content.get_current_dialogue_id()
        # reload data
        self._load_content()
        # select the section
        if self._content.contains_section(currentSect):
            self._content.set_section(currentSect)
            # select the base on given dialogue id
            if self._content.contains_dialogue(currentSect, currentId):
                self._content.set_current_dialogue_id(currentId)
        # update the scene
        self._update_scene(self._content.get_current_dialogue_id())

    # 停止播放
    def stop(self) -> None:
        # 如果背景是多线程的VideoSurface，则应该退出占用
        if isinstance(self.__background_image_surface, VideoSurface):
            self.__background_image_surface.stop()
        # 释放立绘渲染系统占用的内存
        VisualNovelCharacterImageManager.reset()
        # 设置停止播放
        super().stop()

    # 将背景图片画到surface上
    def display_background_image(self, _surface: ImageSurface) -> None:
        if self.__background_image_surface is not None:
            if isinstance(self.__background_image_surface, StaticImage):
                self.__background_image_surface.set_width_with_original_image_size_locked(_surface.get_width())
                self.__background_image_surface.set_left(0)
                self.__background_image_surface.set_centery(_surface.get_height() // 2)
            self.__background_image_surface.draw(_surface)

    def _get_dialog_options_container_ready(self) -> None:
        self._dialog_options_container.clear()
        if self._content.current.next.has_multi_targets():
            optionBox_y_base: int = Display.get_height() * 3 // 16 - len(self._content.current.next.get_targets()) * self._FONT_SIZE
            for i, _target in enumerate(self._content.current.next.get_targets()):
                optionButton: Button = Button.load("<&ui>option.png", (0, 0), (0, 0))
                optionButton.set_hover_img(Images.quickly_load("<&ui>option_selected.png"))
                optionButton.set_auto_resize(True)
                optionButton.set_text(ButtonComponent.text(str(_target["text"]), self._FONT_SIZE, Colors.WHITE))
                optionButton.set_pos((Display.get_width() - optionButton.get_width()) / 2, (i + 1) * 4 * self._FONT_SIZE + optionBox_y_base)
                self._dialog_options_container.append(optionButton)
            self._dialog_options_container.set_visible(True)

    # 把基础内容画到surface上
    def draw(self, _surface: ImageSurface) -> None:
        # 检测章节是否初始化
        if self._chapter_id is None:
            EXCEPTION.fatal("The dialog has not been initialized!")
        # 展示背景图片和npc立绘
        self.display_background_image(_surface)
        VisualNovelCharacterImageManager.draw(_surface)
        self._get_dialog_box().draw(_surface)
        # 如果不处于静音状态
        if not self._is_muted:
            # 播放背景音乐
            self.play_bgm()


# 视觉小说系统模块
class VisualNovelPlayer(AbstractVisualNovelPlayer, PauseMenuModuleForGameSystem):
    __CHOICE_TEXT: str = str(Lang.get_texts("Dialog", "choice"))

    def __init__(self) -> None:
        AbstractVisualNovelPlayer.__init__(self)
        PauseMenuModuleForGameSystem.__init__(self)
        # 加载对话框系统
        self.__dialog_txt_system: DialogBox = DialogBox(self._FONT_SIZE)
        # UI按钮
        self.__buttons_container: GameObjectsDictContainer | None = None
        # 是否要显示历史对白页面
        self.__is_showing_history: bool = False
        self.__history_bg_surface: ImageSurface = Surfaces.colored(Display.get_size(), Colors.BLACK)
        self.__history_bg_surface.set_alpha(150)
        self.__history_text_surface: ImageSurface | None = None
        self.__history_surface_local_y: int = 0
        # 展示历史界面-返回按钮
        self.__history_back: Button | None = None
        # 是否取消背景渲染
        self.__disable_background_image_rendering: bool = False
        # 初始化音量
        self._update_sound_volume()
        # 玩家做出的选项
        self.__dialog_options: Final[dict] = {}
        # 是否正在淡出的flag
        self.__is_fading_out: bool = True
        # 是否已经完成最后一个Node
        self.__has_reached_the_end: bool = False

    # 禁用基本功能
    def disable_basic_features(self) -> None:
        self.__disable_background_image_rendering = True
        self.__history_back = None
        self.__buttons_container = None
        self._disable_pause_menu()

    # 启用基本功能
    def enable_basic_features(self) -> None:
        self.__disable_background_image_rendering = False
        self.__history_back = Button.load(
            "<&ui>back.png",
            Coordinates.convert((Display.get_width() * 0.04, Display.get_height() * 0.04)),
            Coordinates.convert((Display.get_width() * 0.03, Display.get_height() * 0.04)),
            150,
        )
        # UI按钮
        self.__buttons_container = UI.generate_container("dialog_buttons", {"button_size": self._FONT_SIZE * 2})
        # 暂停菜单
        self._enable_pause_menu()

    # 返回需要保存数据
    def _get_data_need_to_save(self) -> dict:
        return super()._get_data_need_to_save() | {"dialog_options": self.__dialog_options}

    # 获取对话框模块（按照父类要求实现）
    def _get_dialog_box(self) -> DialogBox:
        return self.__dialog_txt_system

    # 是否已经完成最后一个Node
    def _has_reached_the_end(self) -> bool:
        return self.__has_reached_the_end

    # 载入数据
    def _load_content(self) -> None:
        super()._load_content()
        # 将npc立绘系统设置为普通模式
        VisualNovelCharacterImageManager.dev_mode = False
        # 重置对话框
        self.__dialog_txt_system.reset()
        # 重置播放完成的flag
        self.__has_reached_the_end = False

    # 读取存档
    def load_progress(self, _data: dict) -> None:
        super().load_progress(_data)
        # 载入玩家之前做出的选项
        self.__dialog_options.clear()
        self.__dialog_options.update(_data.get("dialog_options", {}))

    # 新读取章节
    def new(self, chapterType: str, chapterId: int, section: str, projectName: str | None = None, dialogId: str = "head") -> None:
        super().new(chapterType, chapterId, section, projectName, dialogId)
        # 初始化重要ui组件
        if not self.__disable_background_image_rendering:
            self.enable_basic_features()

    # 更新场景
    def _update_scene(self, dialog_id: str) -> None:
        # 如果dialog Id存在
        if self._content.contains_dialogue(self._content.section, dialog_id):
            super()._update_scene(dialog_id)
        else:
            EXCEPTION.fatal(f"The dialog id {dialog_id} does not exist!")

    # 更新音量
    def _update_sound_volume(self) -> None:
        self.set_bgm_volume(Volume.get_background_music() / 100)
        self.__dialog_txt_system.set_sound_volume(Volume.get_effects() / 100)

    # 更新语言
    def update_language(self) -> None:
        super().update_language()
        if self.__buttons_container is not None:
            self.__buttons_container = UI.generate_container("dialog_buttons", {"button_size": self._FONT_SIZE * 2})
            self.__buttons_container.set_visible(self.__dialog_txt_system.is_visible())
        self.__CHOICE_TEXT = str(Lang.get_texts("Dialog", "choice"))
        self._initialize_pause_menu()

    def continue_scene(self, dialog_id: str) -> None:
        self._continue()
        self._update_scene(dialog_id)

    # 前往下一个对话
    def __go_to_next(self, _surface: ImageSurface) -> None:
        self.__is_fading_out = True
        if not self._content.current.has_next():
            self._fade(_surface)
            self.__has_reached_the_end = True
            self.stop()
        else:
            # 默认转到下一个对话
            if self._content.current.next.get_type() == "default":
                self._update_scene(self._content.current.next.get_target())
            # 如果是多选项，则不用处理
            elif self._content.current.next.get_type() == "option":
                pass
            # 如果是切换场景
            elif self._content.current.next.get_type() == "scene":
                self._fade(_surface)
                # 更新场景
                self._update_scene(str(self._content.current.next.get_target()))
                self.__dialog_txt_system.reset()
                self.__is_fading_out = False
                self._fade(_surface)
            # 如果是需要播放过程动画
            elif self._content.current.next.get_type() == "cutscene":
                self._fade(_surface)
                self.stop()
                self.play_cutscene(_surface)
            # break被视为立刻退出，没有淡出动画
            elif self._content.current.next.get_type() == "break":
                self.stop()
            # 非法type
            else:
                EXCEPTION.fatal(f'Current dialog "{self._content.current.id}" has a valid next type.')

    def __check_button_event(self, _surface: ImageSurface) -> bool:
        if self.__buttons_container is not None:
            if self.__buttons_container.is_hidden():
                self.__buttons_container.set_visible(True)
                self.__dialog_txt_system.set_visible(True)
            else:
                if self.__buttons_container.item_being_hovered == "hide":
                    self.__buttons_container.set_visible(False)
                    self.__dialog_txt_system.set_visible(False)
                # 如果接来下没有文档了或者玩家按到了跳过按钮, 则准备淡出并停止播放
                elif self.__buttons_container.item_being_hovered == "skip":
                    self.__is_fading_out = True
                    self._fade(_surface)
                    self.__has_reached_the_end = True
                    self.stop()
                elif self.__buttons_container.item_being_hovered == "is_auto":
                    self.__dialog_txt_system.set_playing_automatically(False)
                    self.__buttons_container.get("not_auto").set_visible(True)
                    self.__buttons_container.get("is_auto").set_visible(False)
                elif self.__buttons_container.item_being_hovered == "not_auto":
                    self.__dialog_txt_system.set_playing_automatically(True)
                    self.__buttons_container.get("not_auto").set_visible(False)
                    self.__buttons_container.get("is_auto").set_visible(True)
                elif self.__buttons_container.item_being_hovered == "history":
                    self.__is_showing_history = True
                else:
                    return False
            return True
        return False

    # 过场动画
    def play_cutscene(self, _surface: ImageSurface, fade_out_in_ms: int = 3000) -> None:
        # 初始化部分参数
        is_skip: bool = False
        is_playing: bool = True
        # 初始化跳过按钮的参数
        skip_button: StaticImage = StaticImage(
            "<&ui>next.png", _surface.get_width() * 23 // 25, _surface.get_height() // 20, _surface.get_width() * 11 // 200, _surface.get_height() * 3 // 50
        )
        # 进度条
        bar_height: int = _surface.get_height() // 100
        white_progress_bar: ProgressBar = ProgressBar(
            bar_height, _surface.get_height() - bar_height * 2, _surface.get_width() - bar_height * 2, bar_height, Colors.WHITE
        )
        # 生成黑色帘幕
        BLACK_CURTAIN: ImageSurface = Surfaces.colored(_surface.get_size(), Colors.BLACK)
        BLACK_CURTAIN.set_alpha(0)
        # 创建视频文件
        VIDEO: VideoPlayer = VideoPlayer(Specification.get_directory("movie", self._content.current.next.get_target()))
        VIDEO.pre_init()
        # 播放主循环
        while is_playing is True and VIDEO.is_playing() is True:
            VIDEO.draw(_surface)
            skip_button.draw(_surface)
            white_progress_bar.set_percentage(VIDEO.get_percentage_played())
            white_progress_bar.draw(_surface)
            if skip_button.is_hovered() and Controller.mouse.get_pressed(0) and not is_skip:
                is_skip = True
                Music.fade_out(fade_out_in_ms)
            if is_skip is True:
                temp_alpha = BLACK_CURTAIN.get_alpha()
                if temp_alpha is not None and temp_alpha < 255:
                    BLACK_CURTAIN.set_alpha(temp_alpha + Display.get_delta_time())
                else:
                    is_playing = False
                    VIDEO.stop()
                _surface.blit(BLACK_CURTAIN, ORIGIN)
            Display.flip()

    # 淡入或淡出
    def _fade(self, _surface: ImageSurface) -> None:
        if not self.__disable_background_image_rendering:
            _alpha: int = 0
            _alpha_max: Final[int] = 1275
            if self.__is_fading_out is True:
                Media.fade_out(1000)
                while _alpha <= _alpha_max:
                    self._black_bg.set_alpha(_alpha // 20)
                    self._black_bg.draw(_surface)
                    _alpha += Display.get_delta_time()
                    Display.flip()
            else:
                _alpha = _alpha_max
                while _alpha >= 0:
                    self.display_background_image(_surface)
                    self._black_bg.set_alpha(_alpha // 5)
                    self._black_bg.draw(_surface)
                    _alpha -= Display.get_delta_time() * 2
                    Display.flip()
                # 重设black_bg的alpha值以便下一次使用
                self._black_bg.set_alpha(255)

    # 重写父类的display_background_image方法使其在背景被disable后不会继续渲染背景图片
    def display_background_image(self, _surface: ImageSurface) -> None:
        if not self.__disable_background_image_rendering:
            super().display_background_image(_surface)

    def draw(self, _surface: ImageSurface) -> None:
        super().draw(_surface)
        # 按钮
        if self.__buttons_container is not None and not self.__is_showing_history:
            self.__buttons_container.draw(_surface)
        # 按键判定
        if Controller.get_event("confirm"):
            if self.__history_back is not None and self.__history_back.is_hovered() and self.__is_showing_history is True:
                self.__is_showing_history = False
                self.__history_text_surface = None
            elif self.__is_showing_history is True or self.__check_button_event(_surface) is True:
                pass
            # 如果所有行都没有播出，则播出所有行
            elif not self.__dialog_txt_system.is_all_played():
                self.__dialog_txt_system.play_all()
            # 如果玩家需要并做出了选择
            elif self._dialog_options_container.item_being_hovered >= 0:
                # 获取下一个对话的id
                _option: dict = self._content.current.next.get_targets()[self._dialog_options_container.item_being_hovered]
                # 记录玩家选项
                self.__dialog_options[self._content.get_current_dialogue_id()] = {
                    "id": self._dialog_options_container.item_being_hovered,
                    "target": _option["id"],
                }
                # 更新场景
                self._update_scene(_option["id"])
            else:
                self.__go_to_next(_surface)
        if Controller.get_event("previous") and self._content.previous is not None:
            self._update_scene(self._content.previous.id)
        # 暂停菜单
        if (Controller.get_event("back") or Controller.get_event("hard_confirm")) and self._is_pause_menu_enabled():
            if self.__is_showing_history is True:
                self.__is_showing_history = False
                self.__history_text_surface = None
            else:
                self._show_pause_menu(_surface)

        if (
            self.__dialog_txt_system.is_all_played()
            and self.__dialog_txt_system.is_visible()
            and self._content.current.next.get_type() == "option"
            and self._dialog_options_container.is_hidden()
        ):
            self._get_dialog_options_container_ready()
        # 展示历史
        if self.__is_showing_history is True:
            if Controller.get_event("scroll_up") and self.__history_surface_local_y < 0:
                self.__history_text_surface = None
                self.__history_surface_local_y += Display.get_height() // 10
            if Controller.get_event("scroll_down"):
                self.__history_text_surface = None
                self.__history_surface_local_y -= Display.get_height() // 10
            if self.__history_text_surface is None:
                self.__history_text_surface = Surfaces.transparent(Display.get_size())
                dialogIdTemp: str = "head"
                local_y: int = self.__history_surface_local_y
                while True:
                    dialogContent: pyvns.Dialogue = self._content.get_dialogue(self._content.section, dialogIdTemp)
                    has_narrator: bool = len(dialogContent.narrator) > 0
                    if has_narrator:
                        narratorTemp: ImageSurface = self.__dialog_txt_system.FONT.render(dialogContent.narrator + ":", Colors.WHITE)
                        self.__history_text_surface.blit(
                            narratorTemp, (Display.get_width() * 0.14 - narratorTemp.get_width(), Display.get_height() // 10 + local_y)
                        )
                    for i, _text in enumerate(dialogContent.contents):
                        if has_narrator:
                            if i == 0:
                                _text = '[ "' + _text
                            # 这里不用elif，以免当对话行数为一的情况
                            if i == len(dialogContent.contents) - 1:
                                _text += '" ]'
                        self.__history_text_surface.blit(
                            self.__dialog_txt_system.FONT.render(_text, Colors.WHITE), (Display.get_width() * 0.15, Display.get_height() // 10 + local_y)
                        )
                        local_y += self.__dialog_txt_system.FONT.size * 3 // 2
                    if dialogIdTemp != self._content.get_current_dialogue_id():
                        if dialogContent.next.get_type() in ("default", "scene"):
                            if dialogContent.has_next():
                                dialogIdTemp = dialogContent.next.get_target()
                            else:
                                break
                        elif dialogContent.next.get_type() == "option":
                            narratorTemp = self.__dialog_txt_system.FONT.render(self.__CHOICE_TEXT + ":", (0, 191, 255))
                            self.__history_text_surface.blit(
                                narratorTemp, (Display.get_width() * 0.14 - narratorTemp.get_width(), Display.get_height() // 10 + local_y)
                            )
                            self.__history_text_surface.blit(
                                self.__dialog_txt_system.FONT.render(
                                    str(dialogContent.next.get_targets()[int(self.__dialog_options[dialogIdTemp]["id"])]["text"]),
                                    (0, 191, 255),
                                ),
                                (Display.get_width() * 0.15, Display.get_height() // 10 + local_y),
                            )
                            local_y += self.__dialog_txt_system.FONT.size * 3 // 2
                            if (target_temp := self.__dialog_options[dialogIdTemp]["target"]) is not None and local_y < Display.get_height():
                                dialogIdTemp = str(target_temp)
                            else:
                                break
                        else:
                            break
                    else:
                        break
            _surface.blit(self.__history_bg_surface, ORIGIN)
            _surface.blit(self.__history_text_surface, ORIGIN)
            if self.__history_back is not None:
                self.__history_back.draw(_surface)
                self.__history_back.is_hovered()
        else:
            # 显示对话选项
            if self.__buttons_container is None or self.__buttons_container.is_visible():
                self._dialog_options_container.display(_surface)
            # 当自动播放系统告知需要更新，如果对话被隐藏，则无视进入下一个对白的操作，反之则进入
            if self.__buttons_container is not None and self.__buttons_container.is_visible() and self.__dialog_txt_system.is_update_needed():
                self.__go_to_next(_surface)


# 对话制作器
class VisualNovelEditor(AbstractVisualNovelPlayer):
    # deselect选中的背景
    __BACKGROUND_DESELECT_IMAGE: Final[StaticImage] = StaticImage.new_place_holder()
    __IS_BACKGROUND_DESELECT_IMAGE_INIT: bool = False

    def __init__(self) -> None:
        super().__init__()
        # 导航窗口
        self.__dialog_navigation_window: DialogNavigationWindow = DialogNavigationWindow(
            Display.get_width() // 10, Display.get_height() // 5, Display.get_width() // 10, Display.get_height() // 10
        )
        # 加载对话框系统
        self.__dialog_txt_system: EditableDialogBox = EditableDialogBox(self._FONT_SIZE)
        # 存放并管理编辑器上方所有按钮的容器
        self.__buttons_ui_container: GameObjectsDictContainer | None = None
        # 背景音乐选择 DropDown ui
        self.__dialog_bgm_select: DropDownList = DropDownList(None, 0, 0, 1)
        # 背景图片编辑模块
        self.__UIContainerRight_bg: SurfaceContainerWithScrollBar = SurfaceContainerWithScrollBar(None, 0, 0, 0, 0, Axis.VERTICAL)
        # npc立绘编辑模块
        self.__UIContainerRight_npc: SurfaceContainerWithScrollBar = SurfaceContainerWithScrollBar(None, 0, 0, 0, 0, Axis.VERTICAL)
        # 控制容器转换的按钮
        self.__button_select_background: Button = Button.load("<&ui>button.png", (0, 0), (0, 0), 150)
        self.__button_select_npc: Button = Button.load("<&ui>button.png", (0, 0), (0, 0), 150)
        # 未保存数据时警告的窗口
        self.__no_save_warning: GameObjectsDictContainer = UI.generate_container("leave_without_saving_warning")
        # 当前选择的背景的名称
        self.__current_select_bg_name: str = ""
        # 当前选择的背景的复制品
        self.__current_select_bg_copy: ImageSurface | None = None
        # 用于选择小说脚本的key的下拉菜单
        self.__dialog_section_selection: DropDownList = DropDownList(None, 0, 0, 1)
        # 检测并初始化deselect选中的背景
        if not self.__IS_BACKGROUND_DESELECT_IMAGE_INIT:
            self.__BACKGROUND_DESELECT_IMAGE.update_image("<&ui>deselect.png")
        # 默认不播放音乐
        # self._is_muted = True

    # 获取对话框模块（按照父类要求实现）
    def _get_dialog_box(self) -> EditableDialogBox:
        return self.__dialog_txt_system

    # 加载数据
    def new(self, chapterType: str, chapterId: int, section: str, projectName: str | None = None, dialogId: str = "head") -> None:
        # 加载容器
        container_width: int = Display.get_width() // 5
        self.__UIContainerRightImage = Images.load("<&ui>container.png", (container_width, Display.get_height()))
        # 右侧容器尺寸
        RightContainerRect: Rectangle = Rectangle(
            container_width * 3 // 40, Display.get_height() // 10, container_width * 17 // 20, Display.get_height() * 17 // 20
        )
        # 重置背景图片编辑模块
        self.__UIContainerRight_bg.clear()
        self.__UIContainerRight_bg.move_to(RightContainerRect.get_pos())
        self.__UIContainerRight_bg.set_size(RightContainerRect.width, RightContainerRect.height)
        self.__UIContainerRight_bg.set_scroll_bar_pos("right")
        # 加载背景图片
        self.__UIContainerRight_bg.set("current_select", None)
        # 加载静态背景图片
        for imgPath in glob(Specification.get_directory("background_image", "*")):
            self.__UIContainerRight_bg.set(os.path.basename(imgPath), Images.load(imgPath, (container_width * 4 // 5, None)))
        # 加载动态背景图片
        if os.path.exists(Specification.get_directory("movie")):
            for imgPath in glob(Specification.get_directory("movie", "*")):
                self.__UIContainerRight_bg.set(os.path.basename(imgPath), Images.resize(Videos.get_thumbnail(imgPath), (container_width * 4 // 5, None)))
        self.__UIContainerRight_bg.distance_between_item = Display.get_height() // 50
        self.__current_select_bg_name = ""
        self.__current_select_bg_copy = None
        # 重置npc立绘编辑模块
        self.__UIContainerRight_npc.clear()
        self.__UIContainerRight_npc.move_to(RightContainerRect.get_pos())
        self.__UIContainerRight_npc.set_size(RightContainerRect.width, RightContainerRect.height)
        self.__UIContainerRight_npc.set_scroll_bar_pos("right")
        # 加载npc立绘
        for imgPath in glob(Specification.get_directory("character_image", "*")):
            self.__UIContainerRight_npc.set(os.path.basename(imgPath), Images.load(imgPath, (container_width * 4 // 5, None)))
        self.__UIContainerRight_npc.set_visible(False)
        self.__UIContainerRight_npc.distance_between_item = 0
        # 容器按钮
        button_width: int = Display.get_width() // 25
        self.__UIContainerRightButton = MovableStaticImage(
            "<&ui>container_button.png",
            Display.get_width() - button_width,
            Display.get_height() * 2 // 5,
            Display.get_width() - button_width - container_width,
            Display.get_height() * 2 // 5,
            container_width // 10,
            0,
            button_width,
            Display.get_height() // 5,
        )
        self.__UIContainerRightButton.rotate(90)
        # UI按钮
        button_y: int = Display.get_height() * 3 // 100
        font_size: int = button_width // 3
        # 重置控制容器转换的按钮
        self.__button_select_background.set_pos(0, button_y * 3 // 2)
        self.__button_select_background.set_text(ButtonComponent.text(Lang.get_text("Editor", "background"), font_size * 2 / 3, alpha_when_not_hover=150))
        self.__button_select_background.set_auto_resize(True)
        self.__button_select_npc.set_pos(0, button_y * 3 // 2)
        self.__button_select_npc.set_text(ButtonComponent.text(Lang.get_text("Editor", "npc"), font_size * 2 // 3, alpha_when_not_hover=150))
        self.__button_select_npc.set_auto_resize(True)
        padding: int = (container_width - self.__button_select_background.get_width() - self.__button_select_npc.get_width()) // 3
        self.__button_select_background.set_left(padding)
        self.__button_select_npc.set_left(self.__button_select_background.get_right() + padding)
        # 页面右上方的一排按钮
        custom_values: dict[str, int] = {
            "button_size": button_width,
            "button_y": button_y,
            "mute_button_x": button_width * 85 // 10,
            "save_button_x": button_width * 725 // 100,
            "reload_button_x": button_width * 6,
            "add_and_next_button_x": button_width * 475 // 100,
            "previous_button_x": button_width * 35 // 10,
            "delete_button_x": button_width * 225 // 100,
            "back_button_x": button_width,
        }
        self.__buttons_ui_container = UI.generate_container("dialog_editor_buttons", custom_values)
        # 更新可选择的背景音乐
        self.__dialog_bgm_select.clear()
        self.__dialog_bgm_select.set_pos(button_width * 11, button_y + font_size * 3)
        self.__dialog_bgm_select.update_font_size(font_size)
        self.__dialog_bgm_select.set("", Lang.get_text("Editor", "no_bgm"))
        for file_name in os.listdir(Specification.get_directory("music")):
            self.__dialog_bgm_select.set(file_name, file_name)
        # 移除按钮
        self.__delete_npc_prompt = ArtisticFont.render_description_box(
            Lang.get_text("Editor", "delete_npc"), Colors.BLACK, self._FONT_SIZE, self._FONT_SIZE // 5, Colors.WHITE
        )
        # 初始化用于选择小说脚本的key的下拉菜单
        self.__dialog_section_selection.clear()
        self.__dialog_section_selection.set_pos(button_width * 11, button_y + font_size)
        self.__dialog_section_selection.update_font_size(font_size)

        # 初始化数据
        super().new(chapterType, chapterId, section, projectName, dialogId)

        # 将脚本的不同部分的key载入到ui中
        for key in self._content.get_sections():
            self.__dialog_section_selection.set(key, key)
        self.__dialog_section_selection.set_selected_item(self._content.get_section())

    # 返回需要保存数据
    def _get_data_need_to_save(self) -> dict:
        original_data: dict = Config.try_load_file_if_exists(self.get_data_file_path())
        # remove "dialogs" as "dialogs" keyword is deprecated
        if "dialogs" in original_data:
            original_data.pop("dialogs")
        # save data
        original_data["dialogues"] = self.__get_the_stuff_need_save()
        return original_data

    # 更新背景选项栏
    def _update_background_image(self, image_name: str) -> None:
        super()._update_background_image(image_name)
        if len(image_name) > 0:
            if len(self.__current_select_bg_name) > 0:
                self.__UIContainerRight_bg.set("current_select", self.__current_select_bg_copy)
                self.__UIContainerRight_bg.swap("current_select", self.__current_select_bg_name)
            self.__UIContainerRight_bg.swap("current_select", image_name)
            self.__current_select_bg_name = image_name
            current_select_bg: ImageSurface = self.__UIContainerRight_bg.get("current_select")
            self.__current_select_bg_copy = current_select_bg.copy()
            self.__BACKGROUND_DESELECT_IMAGE.set_size(current_select_bg.get_width(), current_select_bg.get_height())
            self.__BACKGROUND_DESELECT_IMAGE.draw(current_select_bg)
        else:
            if len(self.__current_select_bg_name) > 0:
                self.__UIContainerRight_bg.set(self.__current_select_bg_name, self.__current_select_bg_copy)
            self.__UIContainerRight_bg.set("current_select", None)
            self.__current_select_bg_name = ""
            self.__current_select_bg_copy = None

    # 加载默认模板
    def _load_template(self) -> None:
        self._content.set_section("dialog_example")
        self._content.set_current_section_dialogues({"head": self._get_template()})

    # get template
    @staticmethod
    def _get_template() -> pyvns.dialogue_data_t:
        return {"contents": [Lang.get_text("Editor", "please_enter_content")], "narrator": Lang.get_text("Editor", "please_enter_name")}

    # 读取章节信息
    def _load_content(self) -> None:
        # 将npc立绘系统设置为开发者模式
        VisualNovelCharacterImageManager.dev_mode = True
        # 加载内容数据
        self._content.clear()
        dialogs_data: dict = Config.try_load_file_if_exists(self.get_data_file_path())
        if "dialogues" in dialogs_data:
            self._content.update(dialogs_data["dialogues"])
        elif "dialogs" in dialogs_data:
            self._content.update(dialogs_data["dialogs"])
        else:
            # 则尝试加载后仍然出现内容为空的情况
            EXCEPTION.inform("No valid dialog content found.")
            # 则加载默认模板
            self._load_template()
        # 更新场景
        self._update_scene(self._content.get_current_dialogue_id())

    # 分离需要保存的数据
    def __get_the_stuff_need_save(self) -> dict[str, dict[str, dict]]:
        self._content.current.narrator = self.__dialog_txt_system.get_narrator()
        self._content.current.contents = self.__dialog_txt_system.get_content()
        return self._content.to_dict()

    # 更新UI
    def __update_ui(self) -> None:
        # 更新背景音乐选项菜单
        self.__dialog_bgm_select.set_selected_item(self._content.current.background_music)
        # 更新按钮
        if self.__buttons_ui_container is not None:
            if self._content.current.has_next() is True:
                self.__buttons_ui_container.get("add").set_visible(False)
                self.__buttons_ui_container.get("next").set_visible(True)
            else:
                self.__buttons_ui_container.get("add").set_visible(True)
                self.__buttons_ui_container.get("next").set_visible(False)
        else:
            EXCEPTION.fatal("The ui has not been correctly initialized.")
        # 更新dialog navigation窗口
        self.__dialog_navigation_window.read_all(self._content.get_current_section_dialogues())
        self.__dialog_navigation_window.update_selected(self._content.get_current_dialogue_id())

    # 更新场景
    def _update_scene(self, dialog_id: str) -> None:
        # 确保当前版块有对话数据。如果当前版块为空，则加载默认模板
        if len(self._content.get_current_section_dialogues()) <= 0:
            self._content.set_current_section_dialogues(self._get_template())
        # 如果id存在，则加载对应数据
        if dialog_id in self._content.get_current_section_dialogues():
            super()._update_scene(dialog_id)
            self.__update_ui()
        # 如果id不存在，则新增一个
        elif dialog_id != "head":
            self.__add_dialog(str(dialog_id))
        else:
            EXCEPTION.fatal("You have to setup a head.")

    # 添加新的对话
    def __add_dialog(self, dialogId: str) -> None:
        # update current dialogue id
        self._content.current.set_next("default", dialogId)
        # add new dialogue data to dialogue
        new_dialogue: pyvns.dialogue_data_t = self._content.current.to_dict() | self._get_template()
        new_dialogue["previous"] = self._content.get_current_dialogue_id()
        new_dialogue.pop("next")
        if len(self._content.current.narrator) > 0:
            new_dialogue["narrator"] = self._content.current.narrator
        self._content.set_dialogue(self._content.get_section(), dialogId, new_dialogue)
        # 更新数据
        super()._update_scene(dialogId)
        self.__update_ui()

    # 获取上一个对话的ID
    def __get_last_id(self) -> str:
        if self._content.get_current_dialogue_id() == "head":
            return ""
        elif len(self._content.get_current().previous) > 0:
            return self._content.get_current().previous
        else:
            for key, dialog_tmp in self._content.get_current_section_dialogues().items():
                if dialog_tmp.has_next():
                    if dialog_tmp.next.has_single_target():
                        if dialog_tmp.next.get_target() == self._content.get_current_dialogue_id():
                            return str(key)
                    else:
                        for optionChoice in dialog_tmp.next.get_targets():
                            if optionChoice["id"] == self._content.get_current_dialogue_id():
                                return str(key)
            return ""

    # 生产一个新的推荐id
    def __generate_a_new_recommended_key(self, index: int = 1) -> str:
        while True:
            newId: str = f"~0{index}" if index <= 9 else f"~{index}"
            if newId in self._content.get_current_section_dialogues():
                index += 1
            else:
                return newId

    # 获取下一个对话的ID
    def __try_get_next_id(self, _surface: ImageSurface) -> str:
        if self._content.current.has_next() is True:
            if self._content.current.next.has_single_target():
                return self._content.current.next.get_target()
            # for next with more than one targets
            if len(self._content.current.next.get_targets()) > 1:
                self._get_dialog_options_container_ready()
                screenshot = _surface.copy()
                while True:
                    _surface.blit(screenshot, (0, 0))
                    # 显示对话选项
                    self._dialog_options_container.display(_surface)
                    # 等待玩家选择一个选项
                    if Controller.get_event("confirm") and self._dialog_options_container.item_being_hovered >= 0:
                        # 获取下一个对话的id
                        return str(self._content.current.next.get_targets()[self._dialog_options_container.item_being_hovered]["id"])
                    elif Controller.get_event("back"):
                        self._dialog_options_container.clear()
                        self._dialog_options_container.set_visible(False)
                        break
                    Display.flip()
            elif len(self._content.current.next.get_targets()) == 1:
                return str(self._content.current.next.get_targets()[0]["id"])
        return ""

    def draw(self, _surface: ImageSurface) -> None:
        super().draw(_surface)
        # 更新对话框数据
        if self.__dialog_txt_system.any_changed_was_made():
            self._content.current.narrator = self.__dialog_txt_system.get_narrator()
            self._content.current.contents = self.__dialog_txt_system.get_content()
        # 确保按钮初始化
        if self.__buttons_ui_container is None:
            EXCEPTION.fatal("The ui has not been correctly initialized.")
        # 展示按钮
        self.__buttons_ui_container.draw(_surface)
        # 展示出当前可供使用的背景音乐
        self.__dialog_bgm_select.draw(_surface)
        if self._content.current.background_music != self.__dialog_bgm_select.get_selected_item():
            self._content.current.background_music = self.__dialog_bgm_select.get_selected_item()
            self._update_scene(self._content.get_current_dialogue_id())
        # 展示出当前可供编辑的dialog部分
        self.__dialog_section_selection.draw(_surface)
        # 切换当前正在浏览编辑的dialog部分
        if self.__dialog_section_selection.get_selected_item() != self._content.get_section():
            self._content.set_section(self.__dialog_section_selection.get_selected_item())
            self._update_scene("head")
        # 处理输入事件
        confirm_event_tag: bool = False
        lastId: str
        if not self.__dialog_navigation_window.is_hovered():
            if Controller.get_event("confirm"):
                if self.__UIContainerRightButton.is_hovered():
                    self.__UIContainerRightButton.switch()
                    self.__UIContainerRightButton.flip()
                else:
                    # 退出
                    if self.__buttons_ui_container.item_being_hovered == "back":
                        # if no change were made
                        if Config.try_load_file_if_exists(self.get_data_file_path()).get("dialogues") == self.__get_the_stuff_need_save() is True:
                            self.stop()
                        else:
                            self.__no_save_warning.set_visible(True)
                    # 前一对话
                    elif self.__buttons_ui_container.item_being_hovered == "previous":
                        lastId = self.__get_last_id()
                        if len(lastId) == 0:
                            EXCEPTION.inform("There is no last dialog id.")
                        else:
                            self._update_scene(lastId)
                    # 删除当前对话
                    elif self.__buttons_ui_container.item_being_hovered == "delete":
                        if self._content.get_current_dialogue_id() != "head" or (
                            self._content.current.has_next() and self._content.current.next.has_single_target()
                        ):
                            self._content.remove_current_dialogue()
                            self._update_scene(self._content.get_current_dialogue_id())
                    # 下一对话
                    elif self.__buttons_ui_container.item_being_hovered == "next":
                        if len(nextId := self.__try_get_next_id(_surface)) >= 0:
                            self._update_scene(str(nextId))
                        else:
                            EXCEPTION.inform("There is no next dialog id.")
                    # 新增
                    elif self.__buttons_ui_container.item_being_hovered == "add":
                        self.__add_dialog(self.__generate_a_new_recommended_key())
                    # 保存进度
                    elif self.__buttons_ui_container.item_being_hovered == "save":
                        self._save()
                    # 重新加载进度
                    elif self.__buttons_ui_container.item_being_hovered == "reload":
                        self.update_language()
                    # 停止播放背景音乐
                    elif self.__buttons_ui_container.item_being_hovered == "mute":
                        self._is_muted = not self._is_muted
                        if self._is_muted is True:
                            self.stop_bgm()
                    else:
                        confirm_event_tag = True
            # 移除角色立绘
            elif (Controller.get_event("delete") or Controller.get_event("hard_confirm")) and VisualNovelCharacterImageManager.character_get_click is not None:
                character_images = self._content.current.character_images
                # adding check to avoid removing during fade out stage
                if VisualNovelCharacterImageManager.character_get_click in character_images:
                    character_images.remove(VisualNovelCharacterImageManager.character_get_click)
                self._content.current.character_images = character_images
                self._update_scene(self._content.get_current_dialogue_id())
        # 显示移除角色的提示
        if VisualNovelCharacterImageManager.character_get_click is not None:
            _surface.blit(self.__delete_npc_prompt, Controller.mouse.get_pos())
        # 画上右侧菜单的按钮
        self.__UIContainerRightButton.draw(_surface)
        # 画上右侧菜单
        if self.__UIContainerRightButton.right < Display.get_width():
            _surface.blit(self.__UIContainerRightImage, (self.__UIContainerRightButton.right, 0))
            self.__UIContainerRight_bg.display(_surface, (self.__UIContainerRightButton.right, 0))
            self.__UIContainerRight_npc.display(_surface, (self.__UIContainerRightButton.right, 0))
            # 检测按钮
            if self.__button_select_background.is_hovered((self.__UIContainerRightButton.right, 0)) and confirm_event_tag is True:
                self.__UIContainerRight_bg.set_visible(True)
                self.__UIContainerRight_npc.set_visible(False)
                confirm_event_tag = False
            if self.__button_select_npc.is_hovered((self.__UIContainerRightButton.right, 0)) and confirm_event_tag is True:
                self.__UIContainerRight_bg.set_visible(False)
                self.__UIContainerRight_npc.set_visible(True)
                confirm_event_tag = False
            # 画出按钮
            self.__button_select_background.display(_surface, (self.__UIContainerRightButton.right, 0))
            self.__button_select_npc.display(_surface, (self.__UIContainerRightButton.right, 0))
            # 检测是否有物品被选中需要更新
            if confirm_event_tag is True:
                if self.__UIContainerRight_bg.is_visible():
                    if (imgName := self.__UIContainerRight_bg.item_being_hovered) is not None:
                        self._content.current.background_image = imgName if imgName != "current_select" else ""
                        self._update_background_image(self._content.current.background_image)
                elif self.__UIContainerRight_npc.is_visible() and self.__UIContainerRight_npc.item_being_hovered is not None:
                    character_images = self._content.current.character_images
                    character_images.append(self.__UIContainerRight_npc.item_being_hovered)
                    self._content.current.character_images = character_images
                    VisualNovelCharacterImageManager.update(self._content.current.character_images)

        # 展示dialog navigation窗口
        self.__dialog_navigation_window.present_on(_surface)
        # 如果dialog navigation窗口和当前选中的key不一致，则以dialog navigation窗口为基准进行更新
        if self.__dialog_navigation_window.get_selected_key() != self._content.get_current_dialogue_id():
            self._update_scene(self.__dialog_navigation_window.get_selected_key())

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


# 在指定目录创建项目
def create_new_project(dir_path: str, config_type: str = "json") -> None:
    # 如果项目文件夹不存在，则创建一个
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 确保目标是一个文件夹
    if os.path.isdir(dir_path):
        # 根据模块生成项目信息
        info_data: dict = {
            "author": "Put your name here",
            "default_language": Setting.get_language(),
            "link": "https://whateve-you-want/maybe-your-github-link",
            "linpg_version": Info.get_current_version(),
            "title": {},
            "version": "0.0",
        }
        info_data["title"][Setting.get_language()] = Lang.get_text("Editor", "example_project")
        Config.save(os.path.join(dir_path, f"info.{config_type}"), info_data)
    else:
        EXCEPTION.fatal(f'Target path "{dir_path}" cannot be a file path!')
