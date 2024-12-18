"""
结构:
button -> container -> dropdown -> scrollbar -> inputbox -> console -> progressbar -> generator -> menu
"""

_SPEECH_RECOGNITION_ENABLED: bool = False

try:
    import speech_recognition as sr  # type: ignore

    _SPEECH_RECOGNITION_ENABLED = True
except ImportError:
    _SPEECH_RECOGNITION_ENABLED = False

from .core import *


class ButtonText(TextSurface):
    def __init__(
        self,
        text: str,
        size: int_f,
        _color: color_liked = Colors.BLACK,
        _bold: bool = False,
        _italic: bool = False,
        alpha_when_not_hover: int = 255,
    ) -> None:
        self.__text_surface_2: ImageSurface | None = None
        self.__alpha_when_not_hover: int = alpha_when_not_hover
        # 初始化文字
        super().__init__(text, 0, 0, size, _color, _bold, _italic)
        # 是否被触碰的flag
        self.__is_hovered: bool = False

    def _update_text_surface(self) -> None:
        super()._update_text_surface()
        if self.__alpha_when_not_hover != 255 and (_temp_text_surface := self._get_text_surface()) is not None:
            self.__text_surface_2 = _temp_text_surface.copy()
            self.__text_surface_2.set_alpha(self.__alpha_when_not_hover)

    def set_is_hovered(self, value: bool) -> None:
        self.__is_hovered = value

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.__text_surface_2 is None or self.__is_hovered is True:
            super().display(_surface, offSet)
        else:
            _surface.blit(self.__text_surface_2, Coordinates.add(self.pos, offSet))


# 多态按钮（请勿在引擎外实体化）
class AbstractButton(AbstractImageSurface, metaclass=ABCMeta):
    def __init__(self, img: ImageSurface, x: int, y: int, width: int = -1, height: int = -1, tag: str = ""):
        if width < 0:
            width = img.get_width()
        if height < 0:
            height = img.get_height()
        super().__init__(img, x, y, width, height, tag)
        # self.img是未被触碰时的默认图片，img2是被鼠标触碰时展示的图片
        self.__img2: ImageSurface = Surfaces.NULL

    def has_been_hovered(self) -> bool:
        return False

    def set_hover_img(self, img: ImageSurface) -> None:
        self.__img2 = img

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.has_been_hovered() is True and Surfaces.is_not_null(self.__img2):
            _surface.blit(Images.smoothly_resize(self.__img2, self.size), Coordinates.add(self.pos, offSet))
        elif Surfaces.is_not_null(self._get_image_reference()):
            _surface.blit(Images.smoothly_resize(self._get_image_reference(), self.size), Coordinates.add(self.pos, offSet))


# 按钮的简单实现
class ButtonComponent(AbstractButton):
    def __init__(self, img: ImageSurface, width: int = -1, height: int = -1, tag: str = ""):
        super().__init__(img, 0, 0, width=width, height=height, tag=tag)
        # 是否被触碰的flag
        self.__is_hovered: bool = False

    def has_been_hovered(self) -> bool:
        return self.__is_hovered

    def set_is_hovered(self, value: bool) -> None:
        self.__is_hovered = value

    # 加载按钮图标
    @staticmethod
    def icon(path: PoI, size: tuple[int, int], alpha_when_not_hover: int = 255) -> "ButtonComponent":
        if alpha_when_not_hover < 255:
            fading_button = ButtonComponent(Images.load(path, alpha=alpha_when_not_hover), size[0], size[1])
            img2 = fading_button.get_image_copy()
            img2.set_alpha(255)
            fading_button.set_hover_img(img2)
            return fading_button
        else:
            return ButtonComponent(Images.quickly_load(path), size[0], size[1])

    @staticmethod
    def text(
        text: str,
        size: int_f,
        _color: color_liked = Colors.BLACK,
        _bold: bool = False,
        _italic: bool = False,
        alpha_when_not_hover: int = 255,
    ) -> ButtonText:
        return ButtonText(text, size, _color, _bold, _italic, alpha_when_not_hover)


# 按钮的简单实现
class Button(AbstractButton):
    def __init__(self, img: ImageSurface, x: int, y: int, width: int = -1, height: int = -1, tag: str = ""):
        super().__init__(img, x, y, width=width, height=height, tag=tag)
        # 是否被触碰的flag
        self.__is_hovered: bool = False
        # 图标
        self.__icon: ButtonComponent | None = None
        # 文字
        self.__text: ButtonText | None = None
        # 描述
        self.__description: str = ""
        self.__description_surface: ImageSurface | None = None
        # 是否根据component自动改变宽度
        self.__resize_based_on_components: bool = False
        self.__scale_for_resizing_width: number = 1.5
        self.__scale_for_resizing_height: number = 2

    # 加载按钮
    @staticmethod
    def load(path: PoI, position: tuple[int, int], size: tuple[int, int], alpha_when_not_hover: int = 255) -> "Button":
        if alpha_when_not_hover < 255:
            fading_button: Button = Button(Images.load(path, alpha=alpha_when_not_hover), position[0], position[1], size[0], size[1])
            if path != "<NULL>":
                img2 = fading_button.get_image_copy()
                img2.set_alpha(255)
                fading_button.set_hover_img(img2)
            return fading_button
        else:
            return Button(Images.quickly_load(path), position[0], position[1], size[0], size[1])

    # 自动缩放
    def set_auto_resize(self, value: bool) -> None:
        if not self.__resize_based_on_components and value is True:
            self.__resize_based_on_components = True
            self.__check_if_resize_needed()
        else:
            self.__resize_based_on_components = value

    def set_scale_for_resizing_width(self, value: number = 1.5) -> None:
        self.__scale_for_resizing_width = value
        self.__check_if_resize_needed()

    def set_scale_for_resizing_height(self, value: number = 2) -> None:
        self.__scale_for_resizing_height = value
        self.__check_if_resize_needed()

    # 检测是否需要更新
    def __check_if_resize_needed(self) -> None:
        if self.__resize_based_on_components is True:
            if self.__icon is not None and self.__text is not None:
                self.set_size(
                    (self.__icon.get_width() + self.__text.get_width()) * self.__scale_for_resizing_width,
                    max(self.__icon.get_height(), self.__text.get_height()) * self.__scale_for_resizing_height,
                )
            elif self.__icon is not None:
                self.set_size(self.__icon.get_width() * self.__scale_for_resizing_width, self.__icon.get_height() * self.__scale_for_resizing_height)
            elif self.__text is not None:
                self.set_size(self.__text.get_width() * self.__scale_for_resizing_width, self.__text.get_height() * self.__scale_for_resizing_height)
            else:
                self.set_size(0, 0)

    # 设置图标
    def set_icon(self, _icon: ButtonComponent | None = None) -> None:
        self.__icon = _icon
        self.__check_if_resize_needed()

    # 获取图标
    def get_icon(self) -> ButtonComponent | None:
        return self.__icon

    # 获取描述
    def get_description(self) -> str:
        return self.__description

    # 设置描述
    def set_description(self, value: str = "") -> None:
        self.__description = value
        self.__description_surface = (
            ArtisticFont.render_description_box(self.__description, Colors.BLACK, self.get_height() * 2 // 5, self.get_height() // 5, Colors.WHITE)
            if len(self.__description) > 0
            else None
        )

    # 获取文字
    def get_text(self) -> ButtonText | None:
        return self.__text

    # 设置文字
    def set_text(self, text_surface: ButtonText | None = None) -> None:
        self.__text = text_surface
        self.__check_if_resize_needed()

    def has_been_hovered(self) -> bool:
        return self.__is_hovered

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            self.__is_hovered = self.is_hovered(offSet)
            super().display(_surface, offSet)
            # 计算x坐标轴
            if self.__icon is not None and self.__text is not None:
                # 计算真实尺寸
                self.__icon.set_left(self.x + (self.get_width() - self.__icon.get_width() - self.__text.get_width()) // 2 + offSet[0])
                self.__text.set_left(self.__icon.right)
            elif self.__icon is not None:
                self.__icon.set_centerx(self.centerx + offSet[0])
            elif self.__text is not None:
                self.__text.set_centerx(self.centerx + offSet[0])
            # 画出图标
            if self.__icon is not None:
                self.__icon.set_is_hovered(self.__is_hovered)
                self.__icon.set_centery(self.centery + offSet[1])
                self.__icon.draw(_surface)
            # 画出文字
            if self.__text is not None:
                self.__text.set_is_hovered(self.__is_hovered)
                self.__text.set_centery(self.centery + offSet[1])
                self.__text.draw(_surface)
            # 画出描述（如果有的话）
            if self.__is_hovered and self.__description_surface is not None:
                _surface.blit(self.__description_surface, Controller.mouse.get_pos())
        else:
            self.__is_hovered = False


# Container抽象
class AbstractGameObjectsContainer(AbstractImageSurface, metaclass=ABCMeta):
    def __init__(self, bg_img: PoI | None, x: int_f, y: int_f, width: int, height: int, tag: str = "") -> None:
        super().__init__(StaticImage(bg_img, 0, 0, width, height) if bg_img is not None else None, x, y, width, height, tag)

    # 获取物品container容器（子类需实现）
    @abstractmethod
    def _get_container(self) -> dict | list:
        EXCEPTION.fatal("_get_container()", 1)

    # 物品数量
    @property
    def item_num(self) -> int:
        return len(self._get_container())

    # 清空物品栏
    def clear(self) -> None:
        self._get_container().clear()

    # 是否为空
    def is_empty(self) -> bool:
        return self.item_num <= 0

    # 设置宽度
    def set_width(self, value: int_f) -> None:
        super().set_width(value)
        if self.is_background_init():
            self._get_image_reference().set_width(value)

    # 设置高度
    def set_height(self, value: int_f) -> None:
        super().set_height(value)
        if self.is_background_init():
            self._get_image_reference().set_height(value)

    # 更新背景（非专业人员勿碰）
    def update_background(self, newImg: Any) -> None:
        self._set_image(newImg)

    # has background been init
    def is_background_init(self) -> bool:
        return self._get_image_reference() is not None and self._get_image_reference().is_not_null()


# 使用Dict储存游戏对象的容器，类似html的div
class GameObjectsDictContainer(AbstractGameObjectsContainer):
    def __init__(self, bg_img: PoI | None, x: int_f, y: int_f, width: int, height: int, tag: str = "") -> None:
        super().__init__(bg_img, x, y, width, height, tag=tag)
        self.__items_container_dict: dict = {}
        self._item_being_hovered: str | None = None

    def __setitem__(self, key: str, new_item: object | None) -> None:
        self.__items_container_dict[key] = new_item

    def __getitem__(self, key: str) -> Any:
        return self.__items_container_dict[key]

    def __len__(self) -> int:
        return len(self.__items_container_dict)

    @property
    def item_being_hovered(self) -> str | None:
        return self._item_being_hovered

    # 获取物品合集
    def _get_container(self) -> dict:
        return self.__items_container_dict

    # 获取key的列表
    def keys(self) -> tuple:
        return tuple(self.__items_container_dict.keys())

    # 新增一个物品
    def set(self, key: str, new_item: object | None) -> None:
        self.__items_container_dict[key] = new_item

    # 获取一个物品
    def get(self, key: str) -> Any:
        return self.__items_container_dict[key]

    # 交换2个key名下的图片
    def swap(self, key1: str, key2: str) -> None:
        temp_reference = self.__items_container_dict[key1]
        self.__items_container_dict[key1] = self.__items_container_dict[key2]
        self.__items_container_dict[key2] = temp_reference

    # 移除一个物品
    def remove(self, key: str) -> None:
        del self.__items_container_dict[key]

    # 是否包括
    def contain(self, key: str) -> bool:
        return key in self.__items_container_dict

    # 更新内容
    def _update(self, new_content: dict) -> None:
        self.__items_container_dict.update(new_content)

    # 把物品画到surface上
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        self._item_being_hovered = None
        if self.is_visible():
            current_abs_pos: tuple[int, int] = Coordinates.add(self.pos, offSet)
            # 画出背景
            if self.is_background_init():
                self._get_image_reference().display(_surface, current_abs_pos)
            # 画出物品
            for key_of_game_object, game_object_t in self.__items_container_dict.items():
                game_object_t.display(_surface, current_abs_pos)
                if isinstance(game_object_t, Button):
                    if game_object_t.has_been_hovered() is True:
                        self._item_being_hovered = str(key_of_game_object)
                elif isinstance(game_object_t, GameObject2d):
                    if game_object_t.is_hovered(current_abs_pos):
                        self._item_being_hovered = str(key_of_game_object)


# 使用List储存游戏对象的容器，类似html的div
class GameObjectsListContainer(AbstractGameObjectsContainer):
    def __init__(self, bg_img: PoI | None, x: int_f, y: int_f, width: int, height: int, tag: str = "") -> None:
        super().__init__(bg_img, x, y, width, height, tag=tag)
        self.__items_container_list: list = []
        self._item_being_hovered: int = -1

    def __getitem__(self, index: int) -> Any:
        return self.__items_container_list[index]

    def __setitem__(self, index: int, new_item: object | None) -> None:
        self.__items_container_list[index] = new_item

    def __len__(self) -> int:
        return len(self.__items_container_list)

    @property
    def item_being_hovered(self) -> int:
        return self._item_being_hovered

    # 获取物品合集
    def _get_container(self) -> list:
        return self.__items_container_list

    # 新增一个物品
    def append(self, new_item: object | None) -> None:
        self.__items_container_list.append(new_item)

    # 交换2个key名下的图片
    def swap(self, index1: int, index2: int) -> None:
        temp_reference = self.__items_container_list[index1]
        self.__items_container_list[index1] = self.__items_container_list[index2]
        self.__items_container_list[index2] = temp_reference

    # 移除一个物品
    def remove(self, index: int) -> None:
        self.__items_container_list.pop(index)

    # 把物品画到surface上
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        self._item_being_hovered = -1
        if self.is_visible():
            current_abs_pos: tuple[int, int] = Coordinates.add(self.pos, offSet)
            # 画出背景
            if self.is_background_init():
                self._get_image_reference().display(_surface, current_abs_pos)
            # 画出物品
            for i, _item in enumerate(self.__items_container_list):
                _item.display(_surface, current_abs_pos)
                if isinstance(_item, Button):
                    if _item.has_been_hovered() is True:
                        self._item_being_hovered = i
                elif isinstance(_item, GameObject2d):
                    if _item.is_hovered(current_abs_pos):
                        self._item_being_hovered = i


# 下拉选项菜单
class DropDownList(GameObjectsDictContainer):
    def __init__(self, bg_img: PoI | None, x: int_f, y: int_f, font_size: int, font_color: color_liked = "black", tag: str = "") -> None:
        # 方格高度
        self.__block_height: int = font_size * 3 // 2
        # 是否折叠选项
        self.__fold_choice: bool = True
        super().__init__(bg_img, x, y, 0, 0, tag)
        self.__chosen_item_key: str = ""
        self.__DEFAULT_CONTENT: str = ""
        # 字体颜色
        self.__font_color: tuple[int, int, int, int] = Colors.get(font_color)
        # 字体
        self.__FONT = Font.create(font_size)
        # 边缘粗细
        self.outline_thickness: int = 1

    # 重新计算宽度
    def __recalculate_width(self) -> None:
        self.set_width(0)
        for item in self._get_container().values():
            self.__update_width(item)

    # 根据物品判定是否需要更新宽度
    def __update_width(self, item: str | int) -> None:
        _new_width: int = self.__FONT.estimate_text_width(item) + self.__FONT.size * 7
        if self.get_width() < _new_width:
            self.set_width(_new_width)

    # 更新font的尺寸
    def update_font_size(self, font_size: int) -> None:
        self.__FONT.update(font_size)
        self.__block_height = round(self.__FONT.size * 3 / 2)
        self.__recalculate_width()

    # 更新font的颜色
    def update_font_color(self, font_color: color_liked) -> None:
        self.__font_color = Colors.get(font_color)

    # 新增一个物品
    def set(self, key: str, new_item: str | int) -> None:  # type: ignore[override]
        super().set(key, new_item)
        self.__update_width(new_item)

    # 获取一个物品
    def get(self, key: str) -> str | int:
        return super().get(key) if not self.is_empty() else self.__DEFAULT_CONTENT

    # 获取当前选中的物品
    def get_selected_item(self) -> str:
        return self.__chosen_item_key

    # 设置当前选中的物品
    def set_selected_item(self, key: str) -> None:
        self.__chosen_item_key = key

    # 获取高度
    def get_height(self) -> int:
        return (len(self._get_container()) + 1) * self.__block_height if not self.__fold_choice else self.__block_height

    # 移除一个物品
    def remove(self, key: str) -> None:
        super().remove(key)
        self.__recalculate_width()

    # 清空物品栏
    def clear(self) -> None:
        super().clear()
        self.__recalculate_width()

    # 把物品画到surface上
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            current_abs_pos: tuple[int, int] = Coordinates.add(self.pos, offSet)
            # 画出背景
            if Surfaces.is_not_null(self._get_image_reference()):
                self._get_image_reference().display(_surface, current_abs_pos)
            else:
                Draw.rect(_surface, Colors.WHITE, (current_abs_pos, self.size))
            # 列出当前选中的选项
            current_pos: tuple[int, int] = current_abs_pos
            font_surface: ImageSurface = self.__FONT.render(self.get_selected_item(), self.__font_color)
            _surface.blit(font_surface, Coordinates.add(current_pos, (self.__FONT.size * 3, (self.__block_height - font_surface.get_height()) // 2)))
            rect_of_outline = Rectangle(current_pos[0], current_pos[1], self.width, self.__block_height)
            Draw.rect(_surface, self.__font_color, rect_of_outline.get_rect(), self.outline_thickness)
            font_surface = Images.flip(self.__FONT.render("^", self.__font_color), False, True)
            _surface.blit(
                font_surface,
                Coordinates.add(current_pos, (self.width - font_surface.get_width() * 3 // 2, (self.__block_height - font_surface.get_height()) // 2)),
            )
            if Controller.get_event("confirm"):
                if rect_of_outline.is_hovered():
                    self.__fold_choice = not self.__fold_choice
                elif not self.__fold_choice and not Controller.mouse.is_in_rect(current_abs_pos[0], current_abs_pos[1], self.get_width(), self.get_height()):
                    self.__fold_choice = True
            # 列出选择
            if not self.__fold_choice:
                index: int = 1
                for key_of_game_object, game_object_t in self._get_container().items():
                    current_pos = Coordinates.add(current_abs_pos, (0, index * self.__block_height))
                    font_surface = self.__FONT.render(game_object_t, self.__font_color)
                    _surface.blit(font_surface, Coordinates.add(current_pos, (self.__FONT.size * 3, (self.__block_height - font_surface.get_height()) // 2)))
                    rect_of_outline = Rectangle(current_pos[0], current_pos[1], self.width, self.__block_height)
                    Draw.rect(_surface, self.__font_color, rect_of_outline.get_rect(), self.outline_thickness)
                    if rect_of_outline.is_hovered() and Controller.get_event("confirm"):
                        self.__chosen_item_key = key_of_game_object
                    Draw.circle(
                        _surface,
                        self.__font_color,
                        Coordinates.add(current_pos, (self.__FONT.size * 2, self.__block_height / 2)),
                        self.__block_height * 3 // 20,
                        self.outline_thickness if key_of_game_object != self.__chosen_item_key else 0,
                    )
                    index += 1


# 同一时刻会展示2个scrollbar的Surface
class AbstractScrollBarsSurface(SurfaceWithLocalPos, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        self._button_thickness: int = 20
        self._move_speed: int = 20
        self._bar_color: tuple[int, int, int, int] = Colors.WHITE

    # 获取surface宽度（子类需要实现）
    @abstractmethod
    def get_surface_width(self) -> int:
        EXCEPTION.fatal("get_surface_width()", 1)

    # 获取surface高度（子类需要实现）
    @abstractmethod
    def get_surface_height(self) -> int:
        EXCEPTION.fatal("get_surface_height()", 1)

    # 获取x坐标（子类需实现）
    @abstractmethod
    def get_left(self) -> int:
        EXCEPTION.fatal("get_left()", 1)

    # 获取y坐标（子类需实现）
    @abstractmethod
    def get_top(self) -> int:
        EXCEPTION.fatal("get_top()", 1)

    # 获取x+width坐标（子类需实现）
    @abstractmethod
    def get_right(self) -> int:
        EXCEPTION.fatal("get_right()", 1)

    # 获取y+height坐标（子类需实现）
    @abstractmethod
    def get_bottom(self) -> int:
        EXCEPTION.fatal("get_bottom()", 1)

    # 获取宽度（子类需实现）
    @abstractmethod
    def get_width(self) -> int:
        EXCEPTION.fatal("get_width()", 1)

    # 获取高度（子类需实现）
    @abstractmethod
    def get_height(self) -> int:
        EXCEPTION.fatal("get_height()", 1)

    # 是否被鼠标触碰（子类需实现）
    @abstractmethod
    def is_hovered(self, off_set: tuple[int, int] | None = None) -> bool:
        EXCEPTION.fatal("is_hovered()", 1)

    # 获取scrollbar的颜色
    def get_bar_color(self) -> tuple[int, int, int, int]:
        return self._bar_color

    # 修改scrollbar的颜色
    def set_bar_color(self, color: color_liked) -> None:
        self._bar_color = Colors.get(color)

    # 获取滚动条的Rect
    def _get_right_scroll_bar_rect(self, off_set_x: number, off_set_y: number) -> Rectangle | None:
        return (
            Rectangle(self.get_right() - self._button_thickness + int(off_set_x), self.get_top() + int(off_set_y), self._button_thickness, self.get_height())
            if self.get_surface_height() > self.get_height()
            else None
        )

    def _get_bottom_scroll_bar_rect(self, off_set_x: number, off_set_y: number) -> Rectangle | None:
        return (
            Rectangle(self.get_left() + int(off_set_x), self.get_bottom() - self._button_thickness + int(off_set_y), self.get_width(), self._button_thickness)
            if self.get_surface_width() > self.get_width()
            else None
        )

    # 获取滚动条按钮的Rect
    def _get_right_scroll_button_rect(self, off_set_x: number, off_set_y: number) -> Rectangle | None:
        return (
            Rectangle(
                self.get_right() - self._button_thickness + int(off_set_x),
                int(self.get_top() - self.get_height() * self.local_y / self.get_surface_height() + off_set_y),
                self._button_thickness,
                self.get_height() * self.get_height() // self.get_surface_height(),
            )
            if self.get_surface_height() > self.get_height()
            else None
        )

    def _get_bottom_scroll_button_rect(self, off_set_x: number, off_set_y: number) -> Rectangle | None:
        return (
            Rectangle(
                int(self.get_left() - self.get_width() * self.local_x / self.get_surface_width() + off_set_x),
                self.get_bottom() - self._button_thickness + int(off_set_y),
                self.get_width() * self.get_width() // self.get_surface_width(),
                self._button_thickness,
            )
            if self.get_surface_width() > self.get_width()
            else None
        )

    def display_scrollbar(self, _surface: ImageSurface, off_set: tuple[int, int] = ORIGIN) -> None:
        # 获取滚轮条
        right_scroll_bar_rect: Rectangle | None = self._get_right_scroll_bar_rect(off_set[0], off_set[1])
        right_scroll_button_rect: Rectangle | None = self._get_right_scroll_button_rect(off_set[0], off_set[1])
        bottom_scroll_bar_rect: Rectangle | None = self._get_bottom_scroll_bar_rect(off_set[0], off_set[1])
        bottom_scroll_button_rect: Rectangle | None = self._get_bottom_scroll_button_rect(off_set[0], off_set[1])
        # 获取鼠标坐标
        if Controller.mouse.get_pressed(0):
            if right_scroll_bar_rect is not None and right_scroll_button_rect is not None and right_scroll_bar_rect.is_hovered():
                if right_scroll_button_rect.is_hovered():
                    self.add_local_y(Controller.mouse.get_y_moved() * (self.get_surface_height() / self.get_height()))
                else:
                    self.set_local_y(
                        (self.get_top() - Controller.mouse.y + right_scroll_button_rect.height / 2) / right_scroll_bar_rect.height * self.get_surface_height()
                    )
            if bottom_scroll_bar_rect is not None and bottom_scroll_button_rect is not None and bottom_scroll_bar_rect.is_hovered():
                if bottom_scroll_button_rect.is_hovered():
                    self.add_local_x(Controller.mouse.get_x_moved() * (self.get_surface_width() / self.get_width()))
                else:
                    self.set_local_x(
                        (self.get_left() - Controller.mouse.x + bottom_scroll_button_rect.width / 2) / bottom_scroll_bar_rect.width * self.get_surface_width()
                    )
        # 防止local坐标越界
        if self.local_y > 0:
            self.set_local_y(0)
        elif self.get_surface_height() > self.get_height():
            if (local_y_max := self.get_height() - self.get_surface_height()) > self.local_y:
                self.set_local_y(local_y_max)
        if self.local_x > 0:
            self.set_local_x(0)
        elif self.get_surface_width() > self.get_width():
            if (local_x_max := self.get_width() - self.get_surface_width()) > self.local_x:
                self.set_local_x(local_x_max)
        # 画出滚动条
        if right_scroll_button_rect is not None:
            Draw.rect(_surface, self._bar_color, right_scroll_button_rect.get_rect())
        if right_scroll_bar_rect is not None:
            Draw.rect(_surface, self._bar_color, right_scroll_bar_rect.get_rect(), 2)
        if bottom_scroll_button_rect is not None:
            Draw.rect(_surface, self._bar_color, bottom_scroll_button_rect.get_rect())
        if bottom_scroll_bar_rect is not None:
            Draw.rect(_surface, self._bar_color, bottom_scroll_bar_rect.get_rect(), 2)


# 同一时刻只会拥有一个scrollbar的Surface
class AbstractSurfaceWithScrollBar(AbstractScrollBarsSurface, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        self.axis_mode: Axis = Axis.VERTICAL
        self.__scroll_bar_pos: bool = True
        self.__is_holding_scroll_button = False

    def switch_mode(self) -> None:
        self.axis_mode = Axis.VERTICAL if self.axis_mode is not Axis.VERTICAL else Axis.HORIZONTAL
        self.set_local_pos(0, 0)

    # 滚动条位置
    @property
    def scroll_bar_pos(self) -> str:
        return self.get_scroll_bar_pos()

    def get_scroll_bar_pos(self) -> str:
        if self.axis_mode is Axis.VERTICAL:
            return "right" if not self.__scroll_bar_pos else "left"
        else:
            return "bottom" if not self.__scroll_bar_pos else "top"

    def set_scroll_bar_pos(self, pos: str) -> None:
        if pos == "left":
            if self.axis_mode is Axis.VERTICAL:
                self.__scroll_bar_pos = True
            else:
                EXCEPTION.fatal("You cannot put the scroll bar on the left during horizontal mode!")
        elif pos == "right":
            if self.axis_mode is Axis.VERTICAL:
                self.__scroll_bar_pos = False
            else:
                EXCEPTION.fatal("You cannot put the scroll bar on the right during horizontal mode!")
        elif pos == "top":
            if self.axis_mode is Axis.HORIZONTAL:
                self.__scroll_bar_pos = True
            else:
                EXCEPTION.fatal("You cannot put the scroll bar on the top during vertical mode!")
        elif pos == "bottom":
            if self.axis_mode is Axis.HORIZONTAL:
                self.__scroll_bar_pos = False
            else:
                EXCEPTION.fatal("You cannot put the scroll bar on the bottom during vertical mode!")
        else:
            EXCEPTION.fatal(f'Scroll bar position "{pos}" is not supported! Try sth like "right" or "bottom" instead.')

    # 获取滚动条按钮的Rect
    def _get_scroll_button_rect(self, off_set_x: number, off_set_y: number) -> Rectangle | None:
        if self.axis_mode is Axis.VERTICAL:
            if not self.__scroll_bar_pos:
                return self._get_right_scroll_button_rect(off_set_x, off_set_y)
            elif self.get_surface_height() > self.get_height():
                return Rectangle(
                    self.abs_x + int(off_set_x),
                    int(self.get_top() - self.get_height() * self.local_y / self.get_surface_height() + off_set_y),
                    self._button_thickness,
                    self.get_height() * self.get_height() // self.get_surface_height(),
                )
        else:
            if not self.__scroll_bar_pos:
                return self._get_bottom_scroll_button_rect(off_set_x, off_set_y)
            elif self.get_surface_width() > self.get_width():
                return Rectangle(
                    int(self.get_left() - self.get_width() * self.local_x / self.get_surface_width() + off_set_x),
                    self.abs_y + int(off_set_y),
                    self.get_width() * self.get_width() // self.get_surface_width(),
                    self._button_thickness,
                )
        return None

    # 获取滚动条的Rect
    def _get_scroll_bar_rect(self, off_set_x: number, off_set_y: number) -> Rectangle | None:
        if self.axis_mode is Axis.VERTICAL:
            if not self.__scroll_bar_pos:
                return self._get_right_scroll_bar_rect(off_set_x, off_set_y)
            elif self.get_surface_height() > self.get_height():
                return Rectangle(self.abs_x + int(off_set_x), self.get_top() + int(off_set_y), self._button_thickness, self.get_height())
        else:
            if not self.__scroll_bar_pos:
                return self._get_bottom_scroll_bar_rect(off_set_x, off_set_y)
            elif self.get_surface_width() > self.get_width():
                return Rectangle(self.get_left() + int(off_set_x), self.abs_y + int(off_set_y), self.get_width(), self._button_thickness)
        return None

    def display_scrollbar(self, _surface: ImageSurface, off_set: tuple[int, int] = ORIGIN) -> None:
        # 获取滚轮条
        scroll_bar_rect: Rectangle | None = self._get_scroll_bar_rect(off_set[0], off_set[1])
        scroll_button_rect: Rectangle | None = self._get_scroll_button_rect(off_set[0], off_set[1])
        if scroll_bar_rect is not None and scroll_button_rect is not None:
            # 如果没有按下的事件，则重置holding_scroll_button的flag
            if not Controller.mouse.get_pressed(0):
                self.__is_holding_scroll_button = False
            # 如果有按下的事件
            if self.is_hovered(off_set):
                if Controller.mouse.get_pressed(0) is True and not self.__is_holding_scroll_button and scroll_bar_rect.is_hovered():
                    # 根据按钮位置调整本地坐标
                    if scroll_button_rect.is_hovered():
                        self.__is_holding_scroll_button = True
                    elif self.axis_mode is Axis.VERTICAL:
                        self.set_local_y(
                            (self.get_top() - Controller.mouse.y + scroll_button_rect.height / 2) / scroll_bar_rect.height * self.get_surface_height()
                        )
                    else:
                        self.set_local_x(
                            (self.get_left() - Controller.mouse.x + scroll_button_rect.width / 2) / scroll_bar_rect.width * self.get_surface_width()
                        )
                if Controller.get_event("scroll_up"):
                    if self.axis_mode is Axis.VERTICAL:
                        self.add_local_y(self._move_speed)
                    else:
                        self.subtract_local_x(self._move_speed)
                if Controller.get_event("scroll_down"):
                    if self.axis_mode is Axis.VERTICAL:
                        self.subtract_local_y(self._move_speed)
                    else:
                        self.add_local_x(self._move_speed)
        # 需要调整本地坐标
        if self.__is_holding_scroll_button is True:
            if self.axis_mode is Axis.VERTICAL:
                self.add_local_y(Controller.mouse.get_y_moved() * self.get_surface_height() / self.get_height())
            else:
                self.add_local_x(Controller.mouse.get_x_moved() * self.get_surface_width() / self.get_width())
        # 防止local坐标越界
        if self.axis_mode is Axis.VERTICAL:
            if self.local_y > 0:
                self.set_local_y(0)
            elif self.get_surface_height() > self.get_height() and (local_y_max := self.get_height() - self.get_surface_height()) > self.local_y:
                self.set_local_y(local_y_max)
        elif self.local_x > 0:
            self.set_local_x(0)
        elif self.get_surface_width() > self.get_width() and (local_x_max := self.get_width() - self.get_surface_width()) > self.local_x:
            self.set_local_x(local_x_max)
        # 画出滚动条
        if scroll_button_rect is not None:
            Draw.rect(_surface, self._bar_color, scroll_button_rect.get_rect())
        if scroll_bar_rect is not None:
            Draw.rect(_surface, self._bar_color, scroll_bar_rect.get_rect(), 2)


# 带有滚动条的Surface容器
class SurfaceContainerWithScrollBar(GameObjectsDictContainer, AbstractSurfaceWithScrollBar):
    def __init__(self, img: PoI | None, x: int_f, y: int_f, width: int, height: int, mode: Axis = Axis.HORIZONTAL, tag: str = "") -> None:
        GameObjectsDictContainer.__init__(self, img, x, y, width, height, tag)
        AbstractSurfaceWithScrollBar.__init__(self)
        self.__surface_width: int = 0
        self.__surface_height: int = 0
        self.padding: int = 0
        self.distance_between_item: int = 20
        self.axis_mode = mode
        self.__item_per_line: int = 1

    def get_surface_width(self) -> int:
        return self.__surface_width

    def get_surface_height(self) -> int:
        return self.__surface_height

    # 每一行放多少个物品
    @property
    def item_per_line(self) -> int:
        return self.__item_per_line

    def get_item_per_line(self) -> int:
        return self.__item_per_line

    def set_item_per_line(self, value: int) -> None:
        self.__item_per_line = value

    def switch_mode(self) -> None:
        super().switch_mode()
        self.clear()

    # 把素材画到屏幕上
    def display(self, _surface: ImageSurface, off_set: tuple[int, int] = ORIGIN) -> None:
        self._item_being_hovered = None
        if self.is_visible():
            # 如果有背景图片，则画出
            if Surfaces.is_not_null(self._get_image_reference()):
                _surface.blit(self._get_image_reference(), Coordinates.add(self.pos, off_set))
            # 计算出基础坐标
            current_x: int = self.abs_x + off_set[0]
            current_y: int = self.abs_y + off_set[1]
            if self.axis_mode is Axis.VERTICAL:
                current_x += self.padding
            else:
                current_y += self.padding
            # 定义部分用到的变量
            abs_local_y: int
            crop_height: int
            new_height: int
            abs_local_x: int
            crop_width: int
            new_width: int
            item_has_been_dawn_on_this_line: int = 0
            # 画出物品栏里的图片
            for key, item in self._get_container().items():
                if item is not None:
                    if self.axis_mode is Axis.VERTICAL:
                        abs_local_y = current_y - self.y
                        if 0 <= abs_local_y < self.get_height():
                            new_height = self.get_height() - abs_local_y
                            if new_height > item.get_height():
                                new_height = item.get_height()
                            new_width = item.get_width()
                            if new_width > self.get_width():
                                new_width = self.get_width()
                            subsurface_rect = Rectangle(0, 0, new_width, new_height)
                            _surface.blit(get_img_subsurface(item, subsurface_rect), (current_x, current_y))
                            if subsurface_rect.is_hovered((current_x, current_y)):
                                self._item_being_hovered = str(key)
                        elif -(item.get_height()) <= abs_local_y < 0:
                            crop_height = -abs_local_y
                            new_height = item.get_height() - crop_height
                            if new_height > self.get_height():
                                new_height = self.get_height()
                            new_width = item.get_width()
                            if new_width > self.get_width():
                                new_width = self.get_width()
                            subsurface_rect = Rectangle(0, crop_height, new_width, new_height)
                            _surface.blit(get_img_subsurface(item, subsurface_rect), (current_x, current_y + crop_height))
                            if subsurface_rect.is_hovered((current_x, current_y)):
                                self._item_being_hovered = str(key)
                        # 换行
                        if item_has_been_dawn_on_this_line >= self.__item_per_line - 1:
                            current_y += self.distance_between_item + item.get_height()
                            current_x = self.abs_x + off_set[0] + self.padding
                            item_has_been_dawn_on_this_line = 0
                        else:
                            current_x += self.distance_between_item + item.get_width()
                            item_has_been_dawn_on_this_line += 1
                    else:
                        abs_local_x = current_x - self.x
                        if 0 <= abs_local_x < self.get_width():
                            new_width = self.get_width() - abs_local_x
                            if new_width > item.get_width():
                                new_width = item.get_width()
                            new_height = item.get_height()
                            if new_height > self.get_height():
                                new_height = self.get_height()
                            subsurface_rect = Rectangle(0, 0, new_width, new_height)
                            _surface.blit(get_img_subsurface(item, subsurface_rect), (current_x, current_y))
                            if subsurface_rect.is_hovered((current_x, current_y)):
                                self._item_being_hovered = str(key)
                        elif -(item.get_width()) <= abs_local_x < 0:
                            crop_width = -abs_local_x
                            new_width = item.get_width() - crop_width
                            if new_width > self.get_width():
                                new_width = self.get_width()
                            new_height = item.get_height()
                            if new_height > self.get_height():
                                new_height = self.get_height()
                            subsurface_rect = Rectangle(crop_width, 0, new_width, new_height)
                            _surface.blit(get_img_subsurface(item, subsurface_rect), (current_x + crop_width, current_y))
                            if subsurface_rect.is_hovered((current_x, current_y)):
                                self._item_being_hovered = str(key)
                        # 换行
                        if item_has_been_dawn_on_this_line >= self.__item_per_line - 1:
                            current_x += self.distance_between_item + item.get_width()
                            current_y = self.abs_y + off_set[1] + self.padding
                            item_has_been_dawn_on_this_line = 0
                        else:
                            current_y += self.distance_between_item + item.get_height()
                            item_has_been_dawn_on_this_line += 1
            # 处理总长宽
            if self.axis_mode is Axis.VERTICAL:
                self.__surface_height = current_y - self.abs_y - off_set[1]
                if item_has_been_dawn_on_this_line > 0:
                    self.__surface_height += item.get_height()
                self.__surface_width = self.get_width()
            else:
                self.__surface_width = current_x - self.abs_x - off_set[0]
                if item_has_been_dawn_on_this_line > 0:
                    self.__surface_width += item.get_width()
                self.__surface_height = self.get_height()
            self.display_scrollbar(_surface, off_set)


# 输入框Abstract，请勿实体化
class AbstractInputBox(GameObject2d, metaclass=ABCMeta):
    def __init__(self, x: int_f, y: int_f, font_size: int, txt_color: color_liked, default_width: int) -> None:
        super().__init__(x, y)
        self._FONT: FontGenerator = Font.create(font_size)
        self._default_width: int = default_width
        self._default_height: int = self._FONT.size * 3 // 2
        self._input_box: Rectangle = Rectangle(x, y, default_width, self._default_height)
        self._color: tuple[int, int, int, int] = Colors.LIGHT_SKY_BLUE
        self._text_color: tuple[int, int, int, int] = Colors.get(txt_color)
        self._active: bool = False
        self._holder: ImageSurface = self._FONT.render("|", self._text_color)
        self._holder_index: int = 0
        # display holder
        self._display_holder_timer: BoolTickTimer = BoolTickTimer(500)
        self.need_save: bool = False

    def get_width(self) -> int:
        return self._input_box.width

    def get_height(self) -> int:
        return self._input_box.height

    def get_fontsize(self) -> int:
        return self._FONT.size

    def set_fontsize(self, font_size: int) -> None:
        self._FONT.update(font_size)

    def set_pos(self, x: int_f, y: int_f) -> None:
        super().set_pos(x, y)
        self._input_box = Rectangle(x, y, self._default_width, self._FONT.size * 3 // 2)


# 单行输入框
class SingleLineInputBox(AbstractInputBox):
    def __init__(self, x: int_f, y: int_f, font_size: int, txt_color: color_liked, default_width: int = 150) -> None:
        super().__init__(x, y, font_size, txt_color, default_width)
        self._text: str = ""
        self._left_ctrl_pressing: bool = False
        self._padding: int = (self._input_box.height - self._holder.get_height()) // 2

    def get_text(self) -> str:
        self.need_save = False
        return self._text

    def set_text(self, new_txt: str = "") -> None:
        self._text = new_txt
        self._holder_index = len(self._text)
        self._reset_inputbox_width()

    def _add_text(self, _content: str) -> None:
        if len(_content) > 0:
            self._text = self._text[: self._holder_index] + _content + self._text[self._holder_index :]
            self._holder_index += len(_content)
            self._reset_inputbox_width()
        elif Debug.get_developer_mode():
            EXCEPTION.inform("The value of event.unicode is empty!")

    def _remove_char(self, action: Locations) -> None:
        if action is Locations.BEGINNING:
            if self._holder_index > 0:
                self._text = self._text[: self._holder_index - 1] + self._text[self._holder_index :]
                self._holder_index -= 1
        elif action is Locations.END:
            if self._holder_index < len(self._text):
                self._text = self._text[: self._holder_index] + self._text[self._holder_index + 1 :]
        elif action is Locations.EVERYWHERE:
            self.set_text()
        else:
            EXCEPTION.fatal("Action has to be either 'ahead' or 'behind'!")
        self._reset_inputbox_width()

    def _reset_holder_index(self, mouse_x: int) -> None:
        last_width: int = 0
        local_x: int = mouse_x - self.x
        new_width: int = 0
        i: int = 0
        for i in range(len(self._text)):
            new_width = self._FONT.estimate_text_width(self._text[:i]) + self._FONT.size // 4
            if new_width > local_x:
                break
            else:
                last_width = new_width
        if (new_width - local_x) < (local_x - last_width):
            self._holder_index = i
        else:
            self._holder_index = i - 1

    def _reset_inputbox_width(self) -> None:
        if self._text is not None and len(self._text) > 0:
            self._input_box.set_width(max(self._default_width, self._FONT.estimate_text_width(self._text) + self._FONT.size * 3 // 5))
        else:
            self._input_box.set_width(self._default_width)

    def _check_key_down(self, event: PG_Event) -> bool:
        if event.key == Keys.BACKSPACE:
            self._remove_char(Locations.BEGINNING)
            return True
        elif event.key == Keys.DELETE:
            self._remove_char(Locations.END)
            return True
        elif event.key == Keys.ARROW_LEFT:
            if self._holder_index > 0:
                self._holder_index -= 1
                return True
        elif event.key == Keys.ARROW_RIGHT:
            if self._holder_index < len(self._text):
                self._holder_index += 1
                return True
        else:
            if (event.unicode == "v" and Keys.get_pressed("v") and Keys.get_pressed(Keys.LEFT_CTRL)) or (
                event.key == Keys.LEFT_CTRL and Keys.get_pressed("v") and Keys.get_pressed(Keys.LEFT_CTRL)
            ):
                self._add_text(Keys.get_clipboard())
                return True
        return False

    # 画出文字内容
    def _draw_content(self, _surface: ImageSurface, with_holder: bool = True) -> None:
        if self._text is not None and len(self._text) > 0:
            font_t = self._FONT.render(self._text, self._text_color)
            _surface.blit(font_t, (self.x + self._padding, self.y + (self._input_box.height - font_t.get_height()) // 2))
        if with_holder is True:
            self._display_holder_timer.tick()
            if self._display_holder_timer.get_status():
                _surface.blit(self._holder, (self.x + self._padding + self._FONT.estimate_text_width(self._text[: self._holder_index]), self.y + self._padding))

    # 画出内容
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        for event in Controller.get_events():
            if event.type == Events.KEY_DOWN:
                if self._active is True:
                    if self._check_key_down(event):
                        pass
                    elif event.key == Keys.ESCAPE:
                        self._active = False
                        self.need_save = True
                    else:
                        self._add_text(event.unicode)
            elif event.type == Events.MOUSE_BUTTON_DOWN:
                if event.button == 1:
                    if self._active is True:
                        if self.is_hovered(offSet):
                            self._reset_holder_index(Controller.mouse.x)
                        else:
                            self._active = False
                            self.need_save = True
                    elif self.is_hovered(offSet):
                        self._active = True
                        self._reset_holder_index(Controller.mouse.x)
        # 画出输入框
        if self._active:
            Draw.rect(_surface, self._color, self._input_box.get_rect(), 2)
        self._draw_content(_surface, self._active)


# 多行输入框
class MultipleLinesInputBox(AbstractInputBox):
    def __init__(self, x: int_f, y: int_f, font_size: int, txt_color: color_liked, default_width: int = 150) -> None:
        super().__init__(x, y, font_size, txt_color, default_width)
        self._text: list[str] = [""]
        self.__lineId: int = 0
        # start dictate button
        self.__start_dictating: Button | None = None
        # wether user is using dictation
        self.__is_dictating: bool = False
        if _SPEECH_RECOGNITION_ENABLED and len(sr.Microphone.list_working_microphones()) > 0:
            self.__start_dictating = Button.load("<&ui>button.png", ORIGIN, (self._FONT.size, self._FONT.size), 150)
            self.__start_dictating.set_text(ButtonComponent.text(Lang.get_text("Editor", "dictate"), font_size // 3))
            self.__start_dictating.set_auto_resize(True)

    def get_text(self) -> list:
        self.need_save = False
        return [] if (len(self._text) == 0 or self._text == [""]) else self._text

    def get_raw_text(self) -> str:
        text: str = ""
        for each_line in self._text:
            text += each_line + "\n"
        text.removesuffix("\n")
        return text

    def set_text(self, new_txt: list = []) -> None:
        if len(new_txt) > 0:
            self._text = new_txt
        else:
            self._text = [""]
        # 防止数值越界
        if self.__lineId > (line_limit := len(self._text) - 1):
            self.__lineId = line_limit
        if self._holder_index > (index_limit := len(self._text[self.__lineId])):
            self._holder_index = index_limit
        # 重置尺寸
        self._reset_inputbox_size()

    def set_fontsize(self, font_size: int) -> None:
        super().set_fontsize(font_size)
        self._reset_inputbox_size()

    def _reset_inputbox_width(self) -> None:
        width: int = self._default_width
        if self._text is not None and len(self._text) > 0:
            for txtTmp in self._text:
                new_width: int = self._FONT.estimate_text_width(txtTmp) + self._FONT.size // 2
                if new_width > width:
                    width = new_width
        self._input_box.set_width(width)

    def _reset_inputbox_height(self) -> None:
        self._input_box.set_height(self._default_height * len(self._text))

    def _reset_inputbox_size(self) -> None:
        self._reset_inputbox_width()
        self._reset_inputbox_height()

    def _add_text(self, _content: str) -> None:
        if len(_content) > 0:
            if "\n" not in _content:
                self._text[self.__lineId] = self._text[self.__lineId][: self._holder_index] + _content + self._text[self.__lineId][self._holder_index :]
                self._holder_index += len(_content)
                self._reset_inputbox_width()
            else:
                theStringAfterHolderIndex = self._text[self.__lineId][self._holder_index :]
                self._text[self.__lineId] = self._text[self.__lineId][: self._holder_index]
                for i in range(len(_content) - 1):
                    if _content[i] != "\n":
                        self._text[self.__lineId] += _content[i]
                        self._holder_index += 1
                    else:
                        self.__lineId += 1
                        self._text.insert(self.__lineId, "")
                        self._holder_index = 0
                self._text[self.__lineId] += theStringAfterHolderIndex
                self._reset_inputbox_size()
        else:
            EXCEPTION.inform("The value of event.unicode is empty!")

    # 删除对应字符
    def _remove_char(self, action: Locations) -> None:
        if action is Locations.BEGINNING:
            if self._holder_index > 0:
                self._text[self.__lineId] = self._text[self.__lineId][: self._holder_index - 1] + self._text[self.__lineId][self._holder_index :]
                self._holder_index -= 1
            elif self.__lineId > 0:
                # 如果当前行有内容
                if len(self._text[self.__lineId]) > 0:
                    self._holder_index = len(self._text[self.__lineId - 1])
                    self._text[self.__lineId - 1] += self._text[self.__lineId]
                    self._text.pop(self.__lineId)
                    self.__lineId -= 1
                else:
                    self._text.pop(self.__lineId)
                    self.__lineId -= 1
                    self._holder_index = len(self._text[self.__lineId])
        elif action is Locations.END:
            if self._holder_index < len(self._text[self.__lineId]):
                self._text[self.__lineId] = self._text[self.__lineId][: self._holder_index] + self._text[self.__lineId][self._holder_index + 1 :]
            elif self.__lineId < len(self._text) - 1:
                # 如果下一行有内容
                if len(self._text[self.__lineId + 1]) > 0:
                    self._text[self.__lineId] += self._text[self.__lineId + 1]
                self._text.pop(self.__lineId + 1)
        elif action is Locations.EVERYWHERE:
            self.set_text()
        else:
            EXCEPTION.fatal("Action has to be either 'ahead' or 'behind'!")
        self._reset_inputbox_size()

    def _reset_holder_index(self, mouse_x: int, mouse_y: int) -> None:
        self.__lineId = round((mouse_y - self.y) / self._FONT.size) - 1
        if self.__lineId < 0:
            self.__lineId = 0
        elif self.__lineId >= len(self._text):
            self.__lineId = len(self._text) - 1
        last_width: int = 0
        local_x: int = mouse_x - self.x
        new_width: int = 0
        i: int = 0
        for i in range(len(self._text[self.__lineId])):
            new_width = self._FONT.estimate_text_width(self._text[self.__lineId][:i]) + self._FONT.size // 4
            if new_width > local_x:
                break
            else:
                last_width = new_width
        if (new_width - local_x) < (local_x - last_width):
            self._holder_index = i
        else:
            self._holder_index = i - 1

    # 听写
    def __dictate(self) -> None:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        # Initialize audio
        _audio: sr.AudioData | None = None
        # Capture audio
        try:
            with sr.Microphone() as source:
                _audio = recognizer.listen(source)
        except OSError:
            EXCEPTION.warn("No speaker detected!")
        # try process audio
        if _audio is not None:
            # Recognize speech using Speech API
            try:
                self._add_text(recognizer.recognize_google(_audio, language=Lang.get_current_language_tag()))
            except sr.UnknownValueError:
                EXCEPTION.inform("Speech API could not understand the audio")
            except sr.RequestError as e:
                EXCEPTION.inform(f"Could not request results from Speech API; {e}")
        self.__is_dictating = False

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if not self.__is_dictating:
            for event in Controller.get_events():
                if self._active:
                    if event.type == Events.KEY_DOWN:
                        if event.key == Keys.BACKSPACE:
                            self._remove_char(Locations.BEGINNING)
                        elif event.key == Keys.DELETE:
                            self._remove_char(Locations.END)
                        elif event.key == Keys.ARROW_LEFT:
                            if self._holder_index > 0:
                                self._holder_index -= 1
                        elif event.key == Keys.ARROW_RIGHT:
                            if self._holder_index < len(self._text[self.__lineId]):
                                self._holder_index += 1
                        elif event.key == Keys.ARROW_UP:
                            if self.__lineId > 0:
                                self.__lineId -= 1
                                if self._holder_index > len(self._text[self.__lineId]) - 1:
                                    self._holder_index = len(self._text[self.__lineId]) - 1
                        elif event.key == Keys.ARROW_DOWN:
                            if self.__lineId < len(self._text) - 1:
                                self.__lineId += 1
                                if self._holder_index > len(self._text[self.__lineId]) - 1:
                                    self._holder_index = len(self._text[self.__lineId]) - 1
                        # ESC，关闭
                        elif event.key == Keys.ESCAPE:
                            self._active = False
                            self.need_save = True
                        elif event.key == Keys.RETURN:
                            # 如果“|”位于最后
                            if self._holder_index == len(self._text[self.__lineId]):
                                self._text.insert(self.__lineId + 1, "")
                            else:
                                self._text.insert(self.__lineId + 1, self._text[self.__lineId][self._holder_index :])
                                self._text[self.__lineId] = self._text[self.__lineId][: self._holder_index]
                            self.__lineId += 1
                            self._holder_index = 0
                            self._reset_inputbox_size()
                        else:
                            if (
                                event.unicode == "v"
                                and Keys.get_pressed("v")
                                and Keys.get_pressed(Keys.LEFT_CTRL)
                                or event.key == Keys.LEFT_CTRL
                                and Keys.get_pressed("v")
                                and Keys.get_pressed(Keys.LEFT_CTRL)
                            ):
                                self._add_text(Keys.get_clipboard())
                            else:
                                self._add_text(event.unicode)
                    elif event.type == Events.MOUSE_BUTTON_DOWN:
                        if event.button == 1:
                            if self.is_hovered(offSet):
                                self._reset_holder_index(Controller.mouse.x, Controller.mouse.y)
                elif event.type == Events.MOUSE_BUTTON_DOWN and event.button == 1 and self.is_hovered(offSet):
                    self._active = True
                    self._reset_holder_index(Controller.mouse.x, Controller.mouse.y)
        # 计算绝对坐标
        abs_pos: Final[tuple[int, int]] = Coordinates.add(self.get_pos(), offSet)
        # 如果有内容
        if self._text is not None:
            for i in range(len(self._text)):
                # 画出文字
                _surface.blit(self._FONT.render(self._text[i], self._text_color), (abs_pos[0] + self._FONT.size // 4, abs_pos[1] + i * self._default_height))
        # 如果输入模式被激活
        if self._active:
            # 画出输入框
            Draw.rect(_surface, self._color, self._input_box.get_rect(), 2)
            if self.__is_dictating:
                Draw.rect(_surface, (0, 0, 0, 150), self._input_box.get_rect())
                Draw.circle(_surface, Colors.RED, self._input_box.center, self._FONT.size // 4)
            # make sure disable button when is dictating
            else:
                # 画出 “|” 符号
                self._display_holder_timer.tick()
                if self._display_holder_timer.get_status():
                    _surface.blit(
                        self._holder,
                        (
                            abs_pos[0] + self._FONT.size // 10 + self._FONT.estimate_text_width(self._text[self.__lineId][: self._holder_index]),
                            abs_pos[1] + self.__lineId * self._default_height,
                        ),
                    )
                # voice to text
                if self.__start_dictating is not None:
                    self.__start_dictating.set_right(self._input_box.right)
                    self.__start_dictating.set_top(self._input_box.bottom)
                    self.__start_dictating.draw(_surface)
                    if self.__start_dictating.is_hovered() and Controller.get_event("confirm"):
                        self.__is_dictating = True
                        threading.Thread(target=self.__dictate).start()


# 控制台
class Console(SingleLineInputBox, Hidable, threading.Thread):
    _COMMAND_INDICATOR: str = "/"

    def __init__(self, x: int_f, y: int_f, font_size: int = 32, default_width: int = 150):
        Hidable.__init__(self, False)
        self.color_active = Colors.DODGER_BLUE
        SingleLineInputBox.__init__(self, x, y, font_size, self.color_active, default_width)
        self.color_inactive = Colors.LIGHT_SKY_BLUE
        self._color = self.color_active
        self._active: bool = True
        self._text_history: list[str] = []
        self.__backward_id: int = 1
        self._txt_output: list[str] = []
        # 初始化多线程模块
        threading.Thread.__init__(self)
        # 多线程锁
        self.__THREADING_LOCK: threading.Lock = threading.Lock()
        self.daemon = True

    # 安全地设置文字（主要用于确保多线程运行）
    def safely_set_text(self, new_txt: str) -> None:
        self.__THREADING_LOCK.acquire()
        super().set_text(new_txt)
        self.__THREADING_LOCK.release()

    # 启用基于命令行的多线程模式
    def run(self) -> None:
        self.__is_using_threading = True
        while self.__is_using_threading:
            txt: str = self._COMMAND_INDICATOR + input("> ")
            self.__THREADING_LOCK.acquire()
            self._text = txt
            self.__execute_command()
            print(self._txt_output[len(self._txt_output) - 1])
            self.__THREADING_LOCK.release()

    def _check_key_down(self, event: PG_Event) -> bool:
        if super()._check_key_down(event):
            return True
        # 向上-过去历史
        else:
            if event.key == Keys.ARROW_UP:
                if self.__backward_id < len(self._text_history):
                    self.__backward_id += 1
                    self.safely_set_text(self._text_history[-self.__backward_id])
                    return True
            # 向下-过去历史，最近的一个
            elif event.key == Keys.ARROW_DOWN:
                if self.__backward_id > 1:
                    self.__backward_id -= 1
                    self.safely_set_text(self._text_history[-self.__backward_id])
                    return True
            # 回车
            elif event.key == Keys.RETURN:
                self.__THREADING_LOCK.acquire()
                if len(self._text) > 0:
                    self.__execute_command()
                else:
                    EXCEPTION.inform("The input box is empty!")
                self.__THREADING_LOCK.release()
                return True
            # ESC，关闭
            elif event.key == Keys.ESCAPE:
                self._active = False
                # Change the current color of the input box.
                self._color = self.color_active if self._active else self.color_inactive
                return True
            return False

    # 处理命令
    def __execute_command(self) -> None:
        if self._text.startswith(self._COMMAND_INDICATOR):
            self._check_command(self._text.removeprefix(self._COMMAND_INDICATOR).split())
        else:
            self._txt_output.append(self._text)
        self._text_history.append(self._text)
        self.__backward_id = 0
        self.set_text()

    @staticmethod
    def __boolean_conversion(_status: str) -> bool | None:
        if _status.lower() in ("on", "true", "t"):
            return True
        elif _status.lower() in ("off", "false", "f"):
            return False
        else:
            return None

    # 根据参数处理命令
    def _check_command(self, command_blocks: list[str]) -> None:
        if command_blocks[0] == "cheat":
            if len(command_blocks) < 2:
                self._txt_output.append("Unknown status for cheat command.")
            else:
                if self.__boolean_conversion(command_blocks[1]) == True:
                    if Debug.get_cheat_mode() is True:
                        self._txt_output.append("Cheat mode has already been activated!")
                    else:
                        Debug.set_cheat_mode(True)
                        self._txt_output.append("Cheat mode is activated.")
                elif self.__boolean_conversion(command_blocks[1]) == False:
                    if not Debug.get_cheat_mode():
                        self._txt_output.append("Cheat mode has already been deactivated!")
                    else:
                        Debug.set_cheat_mode(False)
                        self._txt_output.append("Cheat mode is deactivated.")
                else:
                    self._txt_output.append("Unknown status for cheat command.")
        elif command_blocks[0] == "show":
            if len(command_blocks) >= 3:
                if command_blocks[1] == "fps":
                    if (_status := self.__boolean_conversion(command_blocks[2])) is not None:
                        Debug.set_show_fps(_status)
                    else:
                        self._txt_output.append("Unknown status for show command.")
                else:
                    self._txt_output.append("Unknown status for show command.")
            else:
                self._txt_output.append("Unknown status for show command.")
        elif command_blocks[0] == "say":
            self._txt_output.append(self._text[len(self._COMMAND_INDICATOR) + 4 :])
        elif command_blocks[0] == "set":
            Setting.set(*command_blocks[1 : len(command_blocks) - 1], value=command_blocks[len(command_blocks) - 1])
        elif command_blocks[0] == "setgv":
            GlobalVariables.set(*command_blocks[1 : len(command_blocks) - 1], value=command_blocks[len(command_blocks) - 1], assumeKeyExists=False)
        elif command_blocks[0] == "setpv":
            PersistentVariables.set(*command_blocks[1 : len(command_blocks) - 1], value=command_blocks[len(command_blocks) - 1])
        elif command_blocks[0] == "getgv":
            if command_blocks[1] == "*":
                for key in GlobalVariables.keys():
                    self._txt_output.append(f"{key}: {GlobalVariables.try_get(key, _deepcopy=False)}")
            else:
                gv_keys: list = command_blocks[1 : len(command_blocks) - 1]
                self._txt_output.append(f"{gv_keys}: {GlobalVariables.try_get(*gv_keys, _deepcopy=False)}")
        elif command_blocks[0] == "getpv":
            if command_blocks[1] == "*":
                for key in PersistentVariables.keys():
                    self._txt_output.append(f"{key}: {PersistentVariables.try_get(key, _deepcopy=False)}")
            else:
                pv_keys: list = command_blocks[1 : len(command_blocks) - 1]
                self._txt_output.append(f"{pv_keys}: {PersistentVariables.try_get(*pv_keys, _deepcopy=False)}")
        elif command_blocks[0] == "dev":
            if len(command_blocks) < 2:
                self._txt_output.append("Unknown status for dev command.")
            else:
                if self.__boolean_conversion(command_blocks[1]) == True:
                    if Debug.get_developer_mode() is True:
                        self._txt_output.append("Developer mode has been activated!")
                    else:
                        Debug.set_developer_mode(True)
                        self._txt_output.append("Developer mode is activated.")
                elif self.__boolean_conversion(command_blocks[1]) == False:
                    if not Debug.get_developer_mode():
                        self._txt_output.append("Developer mode has been deactivated!")
                    else:
                        Debug.set_developer_mode(False)
                        self._txt_output.append("Developer mode is deactivated.")
                else:
                    self._txt_output.append("Unknown status for dev command.")
        elif command_blocks[0] == "linpg":
            self._txt_output.append(f"Linpg Version: {Info.get_current_version()}")
        elif command_blocks[0] == "quit":
            from sys import exit

            exit()
        elif command_blocks[0] == "clear":
            self._txt_output.clear()
        else:
            self._txt_output.append("The command is unknown!")

    def draw(self, _surface: ImageSurface) -> None:
        if self.is_hidden():
            for event in Controller.get_events():
                if event.type == Events.KEY_DOWN and event.unicode == self._COMMAND_INDICATOR:
                    self.set_visible(True)
                    break
        else:
            for event in Controller.get_events():
                if event.type == Events.MOUSE_BUTTON_DOWN:
                    if self.x <= Controller.mouse.x <= self.x + self._input_box.width and self.y <= Controller.mouse.y <= self.y + self._input_box.height:
                        self._active = not self._active
                        # Change the current color of the input box.
                        self._color = self.color_active if self._active else self.color_inactive
                    else:
                        self._active = False
                        self._color = self.color_inactive
                elif event.type == Events.KEY_DOWN:
                    if self._active is True:
                        if self._check_key_down(event):
                            pass
                        else:
                            self._add_text(event.unicode)
                    else:
                        if event.key == Keys.BACKQUOTE or event.key == Keys.ESCAPE:
                            self.set_visible(False)
                            self.set_text()
            # 画出输出信息
            for i in range(len(self._txt_output)):
                _surface.blit(
                    self._FONT.render(self._txt_output[i], self._color),
                    (self.x + self._FONT.size // 4, self.y - (len(self._txt_output) - i) * self._FONT.size * 3 / 2),
                )
            # 画出输入框
            Draw.rect(_surface, self._color, self._input_box.get_rect(), 2)
            # 画出文字
            self._draw_content(_surface)


# 进度条抽象，请勿直接初始化
class AbstractProgressBar(AbstractImageSurface, metaclass=ABCMeta):
    def __init__(self, img: Any, x: int_f, y: int_f, width: int_f, height: int_f, tag: str):
        super().__init__(img, x, y, width, height, tag)
        self.__current_percentage: float = 0.0

    # 百分比
    @property
    def percentage(self) -> float:
        return self.get_percentage()

    def get_percentage(self) -> float:
        return self.__current_percentage

    def set_percentage(self, value: float) -> None:
        self.__current_percentage = round(Numbers.keep_number_in_range(value, 0, 1), 5)


# 进度条简单形式的实现
class ProgressBar(AbstractProgressBar):
    def __init__(self, x: int_f, y: int_f, max_width: int, height: int, color: color_liked, tag: str = ""):
        super().__init__(None, x, y, max_width, height, tag)
        self.__color: tuple[int, int, int, int] = Colors.get(color)

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            Draw.rect(_surface, self.__color, (Coordinates.add(self.pos, offSet), (int(self.get_width() * self.percentage), self.get_height())))


# 简单的分数百分比条的实现
class SimpleRectPointsBar(AbstractProgressBar):
    __FONT: FontGenerator = FontGenerator()

    def __init__(
        self,
        x: int_f,
        y: int_f,
        max_width: int,
        height: int,
        front_color: color_liked,
        back_color: color_liked,
        outline_color: color_liked,
        font_color: color_liked,
        tag: str = "",
    ):
        super().__init__(None, x, y, max_width, height, tag)
        self.__back_color: tuple[int, int, int, int] = Colors.get(back_color)
        self.__front_color: tuple[int, int, int, int] = Colors.get(front_color)
        self.__outline_color: tuple[int, int, int, int] = Colors.get(outline_color)
        self.__font_color: tuple[int, int, int, int] = Colors.get(font_color)
        self.__current_point: int = 0
        self.__max_point: int = 1

    # 重写百分比的计算方式
    def get_percentage(self) -> float:
        return self.__current_point / self.__max_point

    # 设置当前值
    def set_current_point(self, value: int) -> None:
        self.__current_point = Numbers.keep_int_in_range(value, 0, self.__max_point)

    # 设置最大值
    def set_max_point(self, value: int) -> None:
        self.__max_point = max(value, 1)

    # 设置颜色
    def set_color(
        self,
        front_color: color_liked,
        back_color: color_liked | None = None,
        outline_color: color_liked | None = None,
        font_color: color_liked | None = None,
    ) -> None:
        self.__front_color = Colors.get(front_color)
        if back_color is not None:
            self.__back_color = Colors.get(back_color)
        if outline_color is not None:
            self.__outline_color = Colors.get(outline_color)
        if font_color is not None:
            self.__font_color = Colors.get(font_color)

    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            # 更新文字模块
            self.__FONT.check_for_update(int(self.get_height() * 0.6))
            # 根据当前值计算条长度
            _width: int = int(self.get_width() * self.__current_point / self.__max_point)
            # 原先的绝对x
            original_x: int = self.pos[0] + offSet[0]
            # 生成一个rect用于渲染
            bar_rect = Rectangle(self.pos[0] + offSet[0], self.pos[1] + offSet[1], _width, self.get_height())
            # 渲染多个矩形
            bar_rect.draw_outline(_surface, self.__front_color, 0)
            bar_rect.move_right(_width - 1)
            bar_rect.set_width(self.get_width() - _width)
            bar_rect.draw_outline(_surface, self.__back_color, 0)
            bar_rect.set_width(self.get_width() + 1)
            bar_rect.set_left(original_x - 1)
            bar_rect.draw_outline(_surface, self.__outline_color)
            # 渲染数值文字并画出
            _text: ImageSurface = self.__FONT.render(f"{self.__current_point} / {self.__max_point}", self.__font_color)
            _surface.blit(_text, (bar_rect.x + (bar_rect.width - _text.get_width()) // 2, bar_rect.y + (bar_rect.height - _text.get_height()) // 2))


# 进度条Surface
class ProgressBarSurface(AbstractProgressBar):
    def __init__(
        self, imgOnTop: PoI | None, imgOnBottom: PoI | None, x: int_f, y: int_f, max_width: int, height: int, mode: Axis = Axis.HORIZONTAL, tag: str = ""
    ) -> None:
        if imgOnTop is not None:
            imgOnTop = Images.quickly_load(imgOnTop)
        super().__init__(imgOnTop, x, y, max_width, height, tag)
        self._img2: ImageSurface | None = Images.quickly_load(imgOnBottom) if imgOnBottom is not None else None
        # 模式
        self.axis_mode: Axis = mode

    # 返回一个复制
    def copy(self, deep_copy: bool = True) -> "ProgressBarSurface":
        return ProgressBarSurface(
            self.get_image_copy() if deep_copy else self._get_image_reference(),
            self._img2 if not deep_copy or self._img2 is None else self._img2.copy(),
            self.x,
            self.y,
            self.get_width(),
            self.get_height(),
            self.axis_mode,
        )

    # 展示
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            pos = Coordinates.add(self.pos, offSet)
            if self._img2 is not None:
                _surface.blit(Images.resize(self._img2, self.size), pos)
            if self.percentage > 0:
                imgOnTop = Images.resize(self._get_image_reference(), self.size)
                if self.axis_mode is Axis.HORIZONTAL:
                    _surface.blit(imgOnTop.subsurface(0, 0, int(self.get_width() * self.percentage), self.get_height()), pos)
                else:
                    _surface.blit(imgOnTop.subsurface(0, 0, self.get_width(), int(self.get_height() * self.percentage)), pos)


# 进度条形式的调整器
class ProgressBarAdjuster(ProgressBarSurface):
    def __init__(
        self,
        imgOnTop: PoI | None,
        imgOnBottom: PoI | None,
        indicator_img: PoI,
        x: int_f,
        y: int_f,
        max_width: int,
        height: int,
        indicator_width: int,
        indicator_height: int,
        mode: Axis = Axis.HORIZONTAL,
        tag: str = "",
    ) -> None:
        super().__init__(imgOnTop, imgOnBottom, x, y, max_width, height, mode=mode, tag=tag)
        self.__indicator: StaticImage = StaticImage(indicator_img, 0, 0, indicator_width, indicator_height)

    # 展示
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            super().display(_surface, offSet)
            abs_pos: tuple[int, int] = Coordinates.add(self.pos, offSet)
            x: int
            y: int
            if self.axis_mode is Axis.HORIZONTAL:
                x, y = Coordinates.add(
                    (int(self.get_width() * self.percentage - self.__indicator.width / 2), (self.get_height() - self.__indicator.height) // 2), abs_pos
                )
                self.__indicator.set_pos(x, y)
                self.__indicator.draw(_surface)
                value_font = Font.render(str(round(self.percentage * 100)), Colors.WHITE, self.get_height())
                _surface.blit(
                    value_font,
                    Coordinates.add(abs_pos, (self.get_width() + self.__indicator.width * 7 // 10, (self.get_height() - value_font.get_height()) / 2)),
                )
            else:
                x, y = Coordinates.add(
                    ((self.get_width() - self.__indicator.width) // 2, int(self.get_height() * self.percentage - self.__indicator.height / 2)), abs_pos
                )

                self.__indicator.set_pos(x, y)
                self.__indicator.draw(_surface)
                value_font = Font.render(str(round(self.percentage * 100)), Colors.WHITE, self.get_width())
                _surface.blit(
                    value_font,
                    Coordinates.add(abs_pos, ((self.get_width() - value_font.get_width()) / 2, self.get_height() + self.__indicator.height * 7 // 10)),
                )
            if self.is_hovered(offSet):
                if Controller.mouse.get_pressed(0):
                    self.set_percentage(
                        (Controller.mouse.x - offSet[0] - self.x) / self.get_width()
                        if self.axis_mode is Axis.HORIZONTAL
                        else (Controller.mouse.y - offSet[1] - self.y) / self.get_height()
                    )
                elif Controller.get_event("scroll_down"):
                    self.set_percentage(min(round(self.percentage + 0.01, 2), 1.0))
                elif Controller.get_event("scroll_up"):
                    self.set_percentage(max(round(self.percentage - 0.01, 2), 0.0))


# 动态进度条Surface
class DynamicProgressBarSurface(ProgressBarSurface):
    def __init__(self, imgOnTop: PoI | None, imgOnBottom: PoI | None, x: int_f, y: int_f, max_width: int, height: int, mode: Axis = Axis.HORIZONTAL):
        super().__init__(imgOnTop, imgOnBottom, x, y, max_width, height, mode)
        self._percentage_to_be: float = 0.0
        self.__percent_update_each_time: float = 0.0
        self.__total_update_intervals = 10

    # 数据准确度
    @property
    def accuracy(self) -> int:
        return self.__total_update_intervals * 100

    # 百分比
    @property
    def percentage(self) -> float:
        return self._percentage_to_be / self.accuracy

    @property
    def __real_current_percentage(self) -> number:
        return super().get_percentage() * self.accuracy

    def get_percentage(self) -> float:
        return self._percentage_to_be / self.accuracy

    def set_percentage(self, value: float) -> None:
        self._percentage_to_be = round(Numbers.keep_number_in_range(value, 0, 1) * self.accuracy, 5)
        self.__percent_update_each_time = round((self._percentage_to_be - self.__real_current_percentage) / self.__total_update_intervals, 5)

    # 返回一个复制
    def copy(self, deep_copy: bool = True) -> "DynamicProgressBarSurface":
        return DynamicProgressBarSurface(
            self.get_image_copy() if deep_copy else self._get_image_reference(),
            self._img2 if not deep_copy or self._img2 is None else self._img2.copy(),
            self.x,
            self.y,
            self.get_width(),
            self.get_height(),
            self.axis_mode,
        )

    # 获取上方图片（子类可根据需求修改）
    def _get_img_on_top(self) -> ImageSurface:
        return self._get_image_reference()  # type: ignore

    # 展示
    def display(self, _surface: ImageSurface, offSet: tuple[int, int] = ORIGIN) -> None:
        if self.is_visible():
            _abs_pos: tuple[int, int] = Coordinates.add(self.pos, offSet)
            # 画出底层图形
            if self._img2 is not None:
                _surface.blit(Images.resize(self._img2, self.size), _abs_pos)
            # 检查并更新百分比
            if (
                self.__real_current_percentage < self._percentage_to_be
                and self.__percent_update_each_time > 0
                or self.__real_current_percentage > self._percentage_to_be
                and self.__percent_update_each_time < 0
            ):
                super().set_percentage(super().get_percentage() + self.__percent_update_each_time / self.accuracy)
            elif self.__real_current_percentage != self._percentage_to_be:
                super().set_percentage(self._percentage_to_be / self.accuracy)
            # 画出图形
            if super().get_percentage() > 0:
                img_on_top_t = Images.resize(self._get_img_on_top(), self.size)
                if self.axis_mode is Axis.HORIZONTAL:
                    if self.__real_current_percentage < self._percentage_to_be:
                        img2 = img_on_top_t.subsurface((0, 0, int(self.get_width() * self._percentage_to_be / self.accuracy), self.get_height()))
                        img2.set_alpha(100)
                        _surface.blit(img2, _abs_pos)
                        _surface.blit(img_on_top_t.subsurface(0, 0, int(self.get_width() * super().get_percentage()), self.get_height()), _abs_pos)
                    else:
                        if self.__real_current_percentage > self._percentage_to_be:
                            img2 = img_on_top_t.subsurface((0, 0, int(self.get_width() * super().get_percentage()), self.get_height()))
                            img2.set_alpha(100)
                            _surface.blit(img2, _abs_pos)
                        _surface.blit(
                            img_on_top_t.subsurface((0, 0, int(self.get_width() * self._percentage_to_be / self.accuracy), self.get_height())), _abs_pos
                        )
                else:
                    if self.__real_current_percentage < self._percentage_to_be:
                        img2 = img_on_top_t.subsurface((0, 0, self.get_width(), int(self.get_height() * self._percentage_to_be / self.accuracy)))
                        img2.set_alpha(100)
                        _surface.blit(img2, _abs_pos)
                        _surface.blit(img_on_top_t.subsurface(0, 0, self.get_width(), int(self.get_height() * super().get_percentage())), _abs_pos)
                    else:
                        if self.__real_current_percentage > self._percentage_to_be:
                            img2 = img_on_top_t.subsurface((0, 0, self.get_width(), int(self.get_height() * super().get_percentage())))
                            img2.set_alpha(100)
                            _surface.blit(img2, _abs_pos)
                        _surface.blit(
                            img_on_top_t.subsurface((0, 0, self.get_width(), int(self.get_height() * self._percentage_to_be / self.accuracy))), _abs_pos
                        )


# ui编译器
class UiGenerator:
    # 获取默认ui模板
    __UI_TEMPLATES: Final[dict] = Config.load_internal_file("ui.json")
    # 加载自定义的ui数据（如果存在）
    for key, value in Config.resolve_path_and_load_file(os.path.join("Data", "ui")).items():
        if key not in __UI_TEMPLATES:
            __UI_TEMPLATES[key] = {}
        __UI_TEMPLATES[key].update(value)

    # 尝试转换特殊的string
    @classmethod
    def __try_convert_string_to_number(cls, value: str, value_in_case_percentage: int, custom_values: dict) -> int:
        # 如果是百分比
        if value.endswith("%"):
            try:
                return int(Numbers.convert_percentage(value) * value_in_case_percentage)
            except Exception:
                EXCEPTION.fatal(f'Cannot convert "{value}" because it is not a valid percentage.')
        # 如果是需要从lookup表里寻找的参数
        elif value.startswith("<!") and value.endswith(">"):
            the_value = custom_values[value.removeprefix("<!").removesuffix(">")]
            if isinstance(the_value, str):
                return cls.__try_convert_string_to_number(the_value, value_in_case_percentage, custom_values)
            else:
                try:
                    return int(the_value)
                except Exception:
                    EXCEPTION.fatal(f'Cannot convert string "{value}".')
        # 尝试将
        else:
            try:
                return int(value)
            except Exception:
                EXCEPTION.fatal(f'Cannot convert string "{value}".')

    # 检测尺寸是否合法
    @classmethod
    def __convert_number(cls, item: dict, key: str, value_in_case_percentage: int, custom_values: dict) -> int:
        if key not in item:
            EXCEPTION.fatal(f'You have to set "{key}" for "{item["name"]}".' if "name" in item else f'You have to set "{key}".')
        elif isinstance(item[key], float):
            return int(item[key])
        elif not isinstance(item[key], int):
            if isinstance(item[key], str):
                return cls.__try_convert_string_to_number(item[key], value_in_case_percentage, custom_values)
            else:
                try:
                    return int(item[key])
                except Exception:
                    EXCEPTION.fatal(
                        f'The "{key}" for "{item["name"]}" needs to an integer instead of "{item[key]}".'
                        if "name" in item
                        else f'The "{key}" needs to an integer instead of "{item[key]}".'
                    )
        else:
            return int(item[key])

    # 检测坐标是否合法
    @classmethod
    def __convert_coordinate(cls, item: dict, key: str, value_in_case_center: int, value_in_case_percentage: int, custom_values: dict) -> int:
        if key not in item:
            return 0
        elif not isinstance(item[key], int):
            if item[key] == "center":
                return value_in_case_center
            elif isinstance(item[key], str):
                return cls.__try_convert_string_to_number(item[key], value_in_case_percentage, custom_values)
            else:
                try:
                    return int(item[key])
                except Exception:
                    EXCEPTION.fatal(f"Valid value for {key}: {item[key]}.")
        else:
            return int(item[key])

    # 转换文字
    @staticmethod
    def __load_text(text: str) -> str:
        if text.startswith("{") and text.endswith("}"):
            final_text_list: list = []
            text_index: int = 0
            find_close_bracket: bool = False
            while text_index < len(text):
                if text[text_index] == "{":
                    # 寻找 "}"
                    a: int = 0
                    for a in range(text_index + 1, len(text)):
                        if text[a] == "}":
                            find_close_bracket = True
                            break
                    if find_close_bracket is True:
                        find_close_bracket = False
                        final_text_list.append(Lang.get_text_by_keys(tuple(b.strip() for b in text[text_index + 1 : a].split("."))))
                        text_index = a
                    else:
                        EXCEPTION.fatal(f"Cannot find close bracket for text: {text}")
                else:
                    final_text_list.append(text[text_index])
                text_index += 1
            return "".join(final_text_list)
        # 加载自定义参数
        elif text.startswith("<") and text.startswith(">"):
            _key: str = text[1 : len(text) - 1]
            if _key != "NULL":
                return Specification.get_str(*(b.strip() for b in _key.split(".")))
        return text

    # 生成容器类
    @classmethod
    def __generate_container(cls, data: dict, custom_values: dict, max_width: int = -1, max_height: int = -1) -> GameObjectsDictContainer:
        # 如果没有提供最大高度，则默认使用屏幕高度
        if max_height < 0:
            max_height = Display.get_height()  # 如果没有提供最大宽度，则默认使用屏幕宽度
        if max_width < 0:
            max_width = Display.get_width()
        # 转换尺寸
        object_width: int = cls.__convert_number(data, "width", max_width, custom_values)
        object_height: int = cls.__convert_number(data, "height", max_height, custom_values)
        # 如果对象是容器
        if "src" not in data:
            data["src"] = None
        # 生成容器
        container_t: GameObjectsDictContainer = GameObjectsDictContainer(
            data["src"],
            cls.__convert_coordinate(data, "x", (max_width - object_width) // 2, max_width, custom_values),
            cls.__convert_coordinate(data, "y", (max_height - object_height) // 2, max_height, custom_values),
            object_width,
            object_height,
            data["name"] if "name" in data else "",
        )
        # 加载数据
        if "visibility" in data:
            container_t.set_visible(data["visibility"])
        if "items" in data:
            for each_item in data["items"]:
                item_r = cls.__generate(each_item, custom_values, container_t.get_width(), container_t.get_height())
                if item_r.tag != "":
                    container_t.set(item_r.tag, item_r)
                else:
                    container_t.set(f"item{container_t.item_num}", item_r)
        return container_t

    # 生成UI主模块
    @classmethod
    def __generate(cls, data: dict, custom_values: dict, max_width: int = -1, max_height: int = -1) -> GameObject2d:
        # 如果对象是容器
        if data["type"] == "container":
            return cls.__generate_container(data, custom_values, max_width, max_height)
        else:
            # 如果没有提供最大高度，则默认使用屏幕高度
            if max_height < 0:
                max_height = Display.get_height()
            item_t: GameObject2d
            # 如果对象是文字
            if data["type"] == "text" or data["type"] == "text&resize_when_hovered" or data["type"] == "drop_down_single_choice_list":
                # 转换字体大小
                font_size: int = cls.__convert_number(data, "font_size", max_height, custom_values)
                # 补充可选参数
                if "color" not in data:
                    data["color"] = Colors.BLACK
                if "bold" not in data:
                    data["bold"] = False
                if "italic" not in data:
                    data["italic"] = False
                if "src" not in data:
                    data["src"] = None
                elif data["src"] is not None:
                    data["src"] = cls.__load_text(str(data["src"]))
                # 生成文字图层
                if isinstance(data["type"], str) and data["type"].startswith("text"):
                    _info: list[str] = data["type"].split("&")
                    if len(_info) < 2:
                        item_t = TextSurface(data["src"], 0, 0, font_size, data["color"], data["bold"], data["italic"])
                    elif _info[1] == "resize_when_hovered":
                        item_t = ResizeWhenHoveredTextSurface(data["src"], 0, 0, font_size, font_size * 3 / 2, data["color"], data["bold"], data["italic"])
                    else:
                        EXCEPTION.fatal(f'Unrecognized text format "{_info[1]}"')
                    if (outline_thickness := data.get("outline_thickness", 0)) > 0:
                        item_t.set_outline_thickness(outline_thickness)
                    if (outline_color := data.get("outline_color")) is not None:
                        item_t.set_outline_color(outline_color)
                else:
                    item_t = DropDownList(data["src"], 0, 0, font_size, data["color"])
            else:
                # 如果没有提供最大宽度，则默认使用屏幕宽度
                if max_width < 0:
                    max_width = Display.get_width()
                # 转换尺寸
                object_width: int = cls.__convert_number(data, "width", max_width, custom_values)
                object_height: int = cls.__convert_number(data, "height", max_height, custom_values)
                if data["type"] == "button":
                    if "alpha_when_not_hover" not in data:
                        data["alpha_when_not_hover"] = 255
                    item_t = Button.load(data["src"], ORIGIN, (object_width, object_height), data["alpha_when_not_hover"])
                    if "text" in data:
                        item_t.set_text(
                            ButtonComponent.text(
                                cls.__load_text(data["text"]["src"]),
                                object_height / 2,
                                data["text"]["color"],
                                alpha_when_not_hover=data["alpha_when_not_hover"],
                            )
                        )
                    if "icon" in data:
                        # 转换尺寸
                        _icon_width: int = cls.__convert_number(data["icon"], "width", max_width, custom_values)
                        _icon_height: int = cls.__convert_number(data["icon"], "height", max_height, custom_values)
                        item_t.set_icon(ButtonComponent.icon(data["icon"]["src"], (_icon_width, _icon_height), data["alpha_when_not_hover"]))
                    if "scale_for_resizing_width" in data:
                        item_t.set_scale_for_resizing_width(data["scale_for_resizing_width"])
                    if "scale_for_resizing_height" in data:
                        item_t.set_scale_for_resizing_height(data["scale_for_resizing_height"])
                    if "auto_resize" in data:
                        item_t.set_auto_resize(data["auto_resize"])
                    if "description" in data:
                        item_t.set_description(cls.__load_text(data["description"]))
                    if "name" not in data:
                        EXCEPTION.fatal("You have to set a name for button type.")
                elif data["type"] == "progress_bar_adjuster":
                    # 确认按钮存在
                    if "indicator" not in data:
                        EXCEPTION.fatal("You need to set a indicator for progress_bar_adjuster!")
                    # 设置模式
                    if "mode" not in data:
                        data["mode"] = Axis.HORIZONTAL
                    # 生成ProgressBarAdjuster
                    item_t = ProgressBarAdjuster(
                        data["src"][0],
                        data["src"][1],
                        data["indicator"]["src"],
                        0,
                        0,
                        object_width,
                        object_height,
                        cls.__convert_number(data["indicator"], "width", object_width, custom_values),
                        cls.__convert_number(data["indicator"], "height", object_height, custom_values),
                        data["mode"],
                    )
                    if "name" not in data:
                        EXCEPTION.fatal("You have to set a name for button type.")
                elif data["type"] == "image":
                    item_t = StaticImage(data["src"], 0, 0, object_width, object_height)
                else:
                    EXCEPTION.fatal("Current type is not supported")
            # 如果有名字，则以tag的形式进行标注
            item_t.tag = data["name"] if "name" in data else ""
            # 透明度
            if "visibility" in data:
                if isinstance(item_t, Hidable):
                    item_t.set_visible(data["visibility"])
                else:
                    EXCEPTION.fatal("This is not a subtype of Hidable!")
            # 设置坐标
            item_t.set_pos(
                cls.__convert_coordinate(data, "x", (max_width - item_t.get_width()) // 2, max_width, custom_values),
                cls.__convert_coordinate(data, "y", (max_height - item_t.get_height()) // 2, max_height, custom_values),
            )
            return item_t

    # 将数据以dict的形式返回
    @classmethod
    def __get_data_in_dict(cls, data: str | dict) -> dict:
        if isinstance(data, str):
            result: dict | None = cls.__UI_TEMPLATES.get(data)
            if result is None:
                EXCEPTION.fatal(f'The ui called "{data}" does not exist!')
            return copy.deepcopy(result)
        else:
            return copy.deepcopy(data)

    # 生成GameObject2d - 如果目标是str则视为是名称，尝试从ui数据库中加载对应的模板，否则则视为模板
    @classmethod
    def generate(cls, data: str | dict, custom_values: dict = {}) -> GameObject2d:
        return cls.__generate(cls.__get_data_in_dict(data), custom_values)

    # 生成container - 如果目标是str则视为是名称，尝试从ui数据库中加载对应的模板，否则则视为模板
    @classmethod
    def generate_container(cls, data: str | dict, custom_values: dict = {}) -> GameObjectsDictContainer:
        data_dict: dict = cls.__get_data_in_dict(data)
        if data_dict["type"] != "container":
            EXCEPTION.fatal(f'The target has to be a container, not "{data_dict["type"]}".')
        return cls.__generate_container(data_dict, custom_values)


UI: UiGenerator = UiGenerator()


# 内部菜单模块的抽象
class AbstractInternalMenu(Hidable, metaclass=ABCMeta):
    def __init__(self, menu_name: str) -> None:
        super().__init__(False)
        self._CONTENT: GameObjectsDictContainer | None = None
        self._initialized: bool = False
        self._menu_name: str = menu_name

    # 初始化
    def initialize(self) -> None:
        self._CONTENT = UI.generate_container(self._menu_name)
        self._initialized = True

    # 菜单是否被触碰
    def is_hovered(self) -> bool:
        return self._CONTENT.is_hovered() if self.is_visible() and self._CONTENT is not None else False

    # 画出内容
    def draw(self, _surface: ImageSurface) -> None:
        if self.is_visible() and self._CONTENT is not None:
            self._CONTENT.draw(_surface)


# 警告确认窗口
class ConfirmationWarningWindow(AbstractInternalMenu):
    @property
    def item_being_hovered(self) -> str | None:
        return self._CONTENT.item_being_hovered if self._CONTENT is not None else None


# 设置UI
class OptionMenu(AbstractInternalMenu):
    def __init__(self) -> None:
        super().__init__("option_menu")
        self.need_update: dict[str, bool] = {}

    # 初始化
    def initialize(self) -> None:
        super().initialize()
        if self._CONTENT is None:
            EXCEPTION.fatal("The ui has not been correctly initialized.")
        lang_drop_down: DropDownList = self._CONTENT.get("lang_drop_down")
        for lang_choice in Lang.get_available_languages():
            lang_drop_down.set(lang_choice, lang_choice)
        lang_drop_down.set_selected_item(Lang.get_current_language())

    # 确保初始化
    def __ensure_initialization(self) -> None:
        if not self._initialized:
            self.initialize()

    # 宽
    def get_width(self) -> int:
        self.__ensure_initialization()
        return self._CONTENT.get_width() if self._CONTENT is not None else 0

    # 高
    def get_height(self) -> int:
        self.__ensure_initialization()
        return self._CONTENT.get_height() if self._CONTENT is not None else 0

    # 更新背景（非专业人员勿碰）
    def update_background(self, newImg: Any) -> None:
        self.__ensure_initialization()
        if self._CONTENT is not None:
            self._CONTENT.update_background(newImg)

    # 展示
    def draw(self, _surface: ImageSurface) -> None:
        self.need_update.clear()
        if self.is_visible():
            # 检查是否初始化
            self.__ensure_initialization()
            if self._CONTENT is None:
                EXCEPTION.fatal("The ui has not been correctly initialized.")
            lang_drop_down: DropDownList = self._CONTENT.get("lang_drop_down")
            # 更新百分比
            self._CONTENT.get("global_sound_volume").set_percentage(Setting.get("Sound", "global_value") / 100)
            self._CONTENT.get("background_music_sound_volume").set_percentage(Setting.get("Sound", "background_music") / 100)
            self._CONTENT.get("effects_sound_volume").set_percentage(Setting.get("Sound", "effects") / 100)
            self._CONTENT.get("environment_sound_volume").set_percentage(Setting.get("Sound", "environment") / 100)
            # 如果背景没有被初始化或自定义，则渲染默认背景风格
            if not self._CONTENT.is_background_init():
                _surface.blit(Filters.box_blur(_surface.subsurface(self._CONTENT.get_rect()), 30), self._CONTENT.get_pos())
                # 外圈
                Draw.rect(_surface, Colors.WHITE, self._CONTENT.get_rect(), _surface.get_height() // 300, 20)
                # 内圈
                _padding: int = _surface.get_height() // 100
                Draw.rect(
                    _surface,
                    Colors.WHITE,
                    Rectangles.apply(self._CONTENT.get_rect(), (_padding, _padding, _padding * -2, _padding * -2)).get_rect(),
                    _surface.get_height() // 300,
                    20,
                )
            # 画出
            super().draw(_surface)
            # 如果需要更新语言
            if lang_drop_down.get_selected_item() != Lang.get_current_language() and lang_drop_down.get_selected_item() != "":
                # 更新语言并保存新的参数到本地
                Setting.set("Language", value=Lang.get_language_id(lang_drop_down.get_selected_item()))
                Setting.save()
                Lang.reload()
                self._initialized = False
                self.need_update["language"] = True
            # 按键的判定按钮
            if self._CONTENT.item_being_hovered is not None and not lang_drop_down.is_hovered():
                item_percentage_t: int
                # 如果碰到全局音量条
                if self._CONTENT.item_being_hovered == "global_sound_volume":
                    item_percentage_t = int(self._CONTENT.get("global_sound_volume").percentage * 100)
                    if item_percentage_t != int(Setting.get("Sound", "global_value")):
                        Setting.set("Sound", "global_value", value=item_percentage_t)
                        self.need_update["volume"] = True
                # 如果碰到背景音乐音量条
                elif self._CONTENT.item_being_hovered == "background_music_sound_volume":
                    item_percentage_t = int(self._CONTENT.get("background_music_sound_volume").percentage * 100)
                    if item_percentage_t != int(Setting.get("Sound", "background_music")):
                        Setting.set("Sound", "background_music", value=item_percentage_t)
                        Music.set_volume(Volume.get_background_music() / 100.0)
                        self.need_update["volume"] = True
                # 如果碰到音效的音量条
                elif self._CONTENT.item_being_hovered == "effects_sound_volume":
                    item_percentage_t = int(self._CONTENT.get("effects_sound_volume").percentage * 100)
                    if item_percentage_t != int(Setting.get("Sound", "effects")):
                        Setting.set("Sound", "effects", value=item_percentage_t)
                        self.need_update["volume"] = True
                # 如果碰到环境声的音量条
                elif self._CONTENT.item_being_hovered == "environment_sound_volume":
                    item_percentage_t = int(self._CONTENT.get("environment_sound_volume").percentage * 100)
                    if item_percentage_t != int(Setting.get("Sound", "environment")):
                        Setting.set("Sound", "environment", value=item_percentage_t)
                        self.need_update["volume"] = True
                # 返回
                elif self._CONTENT.item_being_hovered == "confirm":
                    if Controller.get_event("confirm") is True:
                        self.set_visible(False)
                # 保存新的参数
                if self.need_update.get("volume") is True:
                    Setting.save()
            # 关闭菜单
            if Controller.get_event("back") is True:
                self.set_visible(False)


# 暂停菜单
class PauseMenu(AbstractInternalMenu):
    def __init__(self) -> None:
        super().__init__("pause_menu")
        # 返回确认菜单
        self.__leave_warning: ConfirmationWarningWindow = ConfirmationWarningWindow("leave_without_saving_progress_warning")
        # 退出确认菜单
        self.__exit_warning: ConfirmationWarningWindow = ConfirmationWarningWindow("exit_without_saving_progress_warning")
        # 记录被按下的按钮
        self.__button_hovered: str = ""
        self.split_point: int = -1

    # 被点击的按钮
    def get_button_clicked(self) -> str:
        return self.__button_hovered

    def initialize(self) -> None:
        super().initialize()
        # 加载返回确认菜单
        self.__leave_warning.initialize()
        self.__leave_warning.set_visible(False)
        # 加载退出确认菜单
        self.__exit_warning.initialize()
        self.__exit_warning.set_visible(False)

    def set_visible(self, visible: bool) -> None:
        super().set_visible(visible)
        if self.is_hidden():
            self.__exit_warning.set_visible(False)
            self.__leave_warning.set_visible(False)

    def draw(self, _surface: ImageSurface) -> None:
        self.__button_hovered = ""
        if self.is_visible():
            if not self._initialized:
                self.initialize()
            # 画出分割线
            if self.__leave_warning.is_hidden() and self.__exit_warning.is_hidden():
                if self.split_point < 0:
                    self.split_point = int(_surface.get_width() * 0.3)
                Draw.line(_surface, Colors.WHITE, (self.split_point, 0), (self.split_point, _surface.get_height()), 5)
            # 画出选项
            if self.__leave_warning.is_hidden() and self.__exit_warning.is_hidden():
                super().draw(_surface)
            # 画出退出确认
            self.__leave_warning.draw(_surface)
            self.__exit_warning.draw(_surface)
            # 处理事件
            if Controller.get_event("back"):
                if self.__leave_warning.is_visible():
                    self.__leave_warning.set_visible(False)
                elif self.__exit_warning.is_visible():
                    self.__exit_warning.set_visible(False)
                else:
                    self.__button_hovered = "resume"
            elif Controller.get_event("confirm"):
                if self.__leave_warning.is_visible():
                    if self.__leave_warning.item_being_hovered == "confirm":
                        self.__button_hovered = "back_to_mainMenu"
                    elif self.__leave_warning.item_being_hovered == "cancel":
                        self.__leave_warning.set_visible(False)
                elif self.__exit_warning.is_visible():
                    if self.__exit_warning.item_being_hovered == "confirm":
                        from sys import exit

                        exit()
                    elif self.__exit_warning.item_being_hovered == "cancel":
                        self.__exit_warning.set_visible(False)
                elif self._CONTENT is not None and self._CONTENT.item_being_hovered is not None:
                    if self._CONTENT.item_being_hovered == "back_to_mainMenu":
                        self.__leave_warning.set_visible(True)
                    elif self._CONTENT.item_being_hovered == "exit_to_desktop":
                        self.__exit_warning.set_visible(True)
                    else:
                        self.__button_hovered = self._CONTENT.item_being_hovered


# 选取存档的菜单
class SaveOrLoadSelectedProgressMenu(Hidable):
    def __init__(self) -> None:
        super().__init__(False)
        # 行
        self.row: int = 3
        # 列
        self.colum: int = 3
        # 当前选中存档的id
        self.__slotId: int = -1
        # 存档数据
        self.__saves: dict[int, Saves.Progress] = {}
        # 当前页码
        self.__page_id: int = 1
        # 最高页码
        self.__max_pages: int = 10

    # 是否显示
    def set_visible(self, visible: bool) -> None:
        super().set_visible(visible)
        if self.is_visible() is True:
            self.__saves = Saves.get_progresses()

    def get_selected_slot(self) -> int:
        return self.__slotId

    def get_selected_save(self) -> Saves.Progress | None:
        return self.__saves.get(self.__slotId)

    # 渲染切换页面的两侧按钮
    def __process_page_switching(self, _surface: ImageSurface) -> None:
        # 初始化参数
        triangle_size: int = _surface.get_height() // 50
        padding: int = _surface.get_width() // 200
        center_y: int = _surface.get_height() // 2
        button_rect: Rectangle = Rectangle(padding, center_y - triangle_size - padding, triangle_size + padding * 2, padding * 2 + triangle_size * 2)
        _color: tuple[int, int, int, int] = Colors.WHITE
        # 渲染并处理左侧按钮
        if self.__page_id > 1:
            if button_rect.is_hovered():
                _color = Colors.YELLOW
            button_rect.draw_outline(_surface, _color)
            Draw.polygon(
                _surface,
                _color,
                (
                    (padding * 2, center_y),
                    (padding * 2 + triangle_size, center_y - triangle_size),
                    (padding * 2 + triangle_size, center_y + triangle_size),
                ),
            )
            if Controller.get_event("confirm") and button_rect.is_hovered():
                self.__page_id -= 1
        # 渲染并处理右侧按钮
        if self.__page_id < self.__max_pages:
            button_rect.set_pos(_surface.get_width() - triangle_size - padding * 3, center_y - triangle_size - padding)
            _color = Colors.WHITE if not button_rect.is_hovered() else Colors.YELLOW
            button_rect.draw_outline(_surface, _color)
            Draw.polygon(
                _surface,
                _color,
                (
                    (_surface.get_width() - padding * 2, center_y),
                    (_surface.get_width() - triangle_size - padding * 2, center_y - triangle_size),
                    (_surface.get_width() - triangle_size - padding * 2, center_y + triangle_size),
                ),
            )
            if Controller.get_event("confirm") and button_rect.is_hovered():
                self.__page_id += 1

    def draw(self, _surface: ImageSurface) -> None:
        self.__slotId = -1
        if self.is_visible() is True:
            if Controller.get_event("back") or Controller.get_event("hard_confirm"):
                self.set_visible(False)
            else:
                rect_width: int = _surface.get_width() // (self.colum + 1)
                colum_padding: int = rect_width // (self.colum + 1)
                rect_height: int = _surface.get_height() // (self.row + 1)
                row_padding: int = rect_height // (self.row + 1)
                _rect: Rectangle = Rectangle(0, 0, rect_width, rect_height)
                self.__process_page_switching(_surface)
                # 渲染页码
                pageIdText: ImageSurface = Font.render(f"- {self.__page_id} -", Colors.WHITE, row_padding // 2)
                _surface.blit(
                    pageIdText,
                    ((_surface.get_width() - pageIdText.get_width()) // 2, _surface.get_height() - row_padding + (row_padding - pageIdText.get_height()) // 2),
                )
                # 渲染存档信息
                for _y in range(self.row):
                    for _x in range(self.colum):
                        _rect.set_pos(colum_padding + (colum_padding + rect_width) * _x, row_padding + (row_padding + rect_height) * _y)
                        _slotId: int = (self.__page_id - 1) * self.colum * self.colum + _y * self.colum + _x
                        _rect.draw_outline(_surface, Colors.GRAY, 0)
                        _file: Saves.Progress | None = self.__saves.get(_slotId)
                        if _file is not None:
                            _img_height: int = int(_rect.get_height() * 0.8)
                            _surface.blit(Images.smoothly_resize_and_crop_to_fit(_file.screenshot, (_rect.get_width(), _img_height)), _rect.get_pos())
                            _createdAt: ImageSurface = Font.render(
                                f"{_file.createdAt} - Chapter {_file.data.get('chapter_id')}", Colors.WHITE, (_rect.get_height() - _img_height) // 2
                            )
                            _surface.blit(
                                _createdAt,
                                (
                                    _rect.x + (_rect.get_width() - _createdAt.get_width()) // 2,
                                    _rect.y + _img_height + (_rect.get_height() - _img_height - _createdAt.get_height()) // 2,
                                ),
                            )
                        if not _rect.is_hovered():
                            _rect.draw_outline(_surface, Colors.WHITE, 4)
                        else:
                            _rect.draw_outline(_surface, Colors.YELLOW, 4)
                            if Controller.get_event("confirm"):
                                self.__slotId = _slotId


# 暂停菜单处理模块
class PauseMenuModuleForGameSystem(AbstractInternalMenu):
    # 引擎本体的选项菜单
    OPTION_MENU: OptionMenu = OptionMenu()

    def __init__(self) -> None:
        super().__init__("")
        # 暂停菜单
        self.__pause_menu: PauseMenu | None = None
        # 存档选择
        self.__select_progress_menu: SaveOrLoadSelectedProgressMenu = SaveOrLoadSelectedProgressMenu()
        # 是保存进程还是读取存档
        self.__save_or_load: bool = False

    # 获取需要保存的数据（子类必须实现）
    @abstractmethod
    def _get_data_need_to_save(self) -> dict:
        EXCEPTION.fatal("_get_data_need_to_save()", 1)

    # 加载进度（子类需实现）
    @abstractmethod
    def load_progress(self, _data: dict) -> None:
        EXCEPTION.fatal("load_progress()", 1)

    # 淡入或淡出（建议子类重写）
    def _fade(self, _surface: ImageSurface) -> None:
        Media.unload()

    # 停止播放（子类需实现）
    @abstractmethod
    def stop(self) -> None:
        EXCEPTION.fatal("stop()", 1)

    # 更新音量（子类需实现）
    @abstractmethod
    def _update_sound_volume(self) -> None:
        EXCEPTION.fatal("_update_sound_volume()", 1)

    # 更新语言（子类需实现）
    @abstractmethod
    def update_language(self) -> None:
        EXCEPTION.fatal("update_language()", 1)

    # 启用暂停菜单
    def _enable_pause_menu(self) -> None:
        self.__pause_menu = PauseMenu()

    # 禁用暂停菜单
    def _disable_pause_menu(self) -> None:
        self.__pause_menu = None

    # 暂停菜单是否启用
    def _is_pause_menu_enabled(self) -> bool:
        return self.__pause_menu is not None

    # 初始化暂停菜单
    def _initialize_pause_menu(self) -> None:
        if self.__pause_menu is not None:
            self.__pause_menu.initialize()

    # 关闭菜单（并确保所有相关子菜单正常关闭）
    def __close_menus(self) -> None:
        self.OPTION_MENU.set_visible(False)
        if self.__pause_menu is not None:
            self.__pause_menu.set_visible(False)
        self.__select_progress_menu.set_visible(False)

    # 渲染暂停页面
    def _show_pause_menu(self, _surface: ImageSurface) -> None:
        if self.__pause_menu is not None:
            # 暂停背景音乐
            Media.pause()
            # 用于存档的截图
            _screenshot: ImageSurface = _surface.copy()
            # 用于背景的毛玻璃效果图
            _background: ImageSurface = Filters.gaussian_blur(_screenshot)
            # 启用菜单
            self.__pause_menu.set_visible(True)
            # 主循环
            while self.__pause_menu.is_visible():
                Display.flip()
                _surface.blit(_background, ORIGIN)
                # 存档选择系统
                if self.__select_progress_menu.is_visible():
                    self.__select_progress_menu.draw(_surface)
                    if self.__select_progress_menu.get_selected_slot() >= 0:
                        # 新建存档
                        if self.__save_or_load is True:
                            Saves.save(self._get_data_need_to_save(), _screenshot, self.__select_progress_menu.get_selected_slot())
                            self.__select_progress_menu.set_visible(True)
                        # 读取存档
                        else:
                            _save: Saves.Progress | None = self.__select_progress_menu.get_selected_save()
                            if _save is not None:
                                self.__close_menus()
                                self.load_progress(_save.data)
                # 设置选项菜单
                elif self.OPTION_MENU.is_visible():
                    self.OPTION_MENU.draw(_surface)
                    # 更新音量
                    if self.OPTION_MENU.need_update.get("volume") is True:
                        self._update_sound_volume()
                    # 更新语言
                    if self.OPTION_MENU.need_update.get("language") is True:
                        self.update_language()
                # 暂停选项菜单
                else:
                    self.__pause_menu.draw(_surface)
                    if self.__pause_menu.get_button_clicked() == "resume":
                        self.__close_menus()
                    elif self.__pause_menu.get_button_clicked() == "save":
                        self.__select_progress_menu.set_visible(True)
                        self.__save_or_load = True
                    elif self.__pause_menu.get_button_clicked() == "load":
                        self.__select_progress_menu.set_visible(True)
                        self.__save_or_load = False
                    elif self.__pause_menu.get_button_clicked() == "option_menu":
                        self.OPTION_MENU.set_visible(True)
                    elif self.__pause_menu.get_button_clicked() == "back_to_mainMenu":
                        self.__close_menus()
                        self._fade(_surface)
                        self.stop()
            # 继续播放背景音乐
            Media.unpause()
