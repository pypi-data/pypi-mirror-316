from tko.util.consts import DiffMode
from tko.util.text import Text

class AppSettings:

    def __init__(self):
        self._diff_mode = DiffMode.SIDE.value
        self._show_hidden = False
        self._use_images = True
        self._use_borders = False
        self._editor = "code"
        self._timeout = 1

    def to_dict(self):
        return self.__dict__
    
    def from_dict(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and type(getattr(self, key)) == type(value):
                setattr(self, key, value)
        return self

    def toggle_diff(self):
        if self._diff_mode == DiffMode.SIDE.value:
            self._diff_mode = DiffMode.DOWN.value
        else:
            self._diff_mode = DiffMode.SIDE.value

    def toggle_borders(self):
        self._use_borders = not self._use_borders
    
    def toggle_images(self):
        self._use_images = not self._use_images
    
    def toggle_hidden(self):
        self._show_hidden = not self._show_hidden

    def set_diff_mode(self, diff_mode: DiffMode):
        self._diff_mode = diff_mode.value
        return self

    def set_side_size_min(self, side_size_min: int):
        self._side_size_min = side_size_min
        return self

    # def set_lang_default(self, lang_default: str):
    #     self._lang_default = lang_default
    #     return self

    # def set_last_rep(self, last_rep: str):
    #     self._last_rep = last_rep
    #     return self

    def set_show_hidden(self, show_hidden: bool):
        self._show_hidden = show_hidden
        return self

    def set_borders(self, borders: bool):
        self._use_borders = borders
        return self
    
    def set_images(self, images: bool):
        self._use_images = images
        return self

    def set_editor(self, editor: str):
        self._editor = editor
        return self

    def set_timeout(self, timeout: int):
        self._timeout = timeout
        return self

    def get_diff_mode(self) -> DiffMode:
        if self._diff_mode == DiffMode.SIDE.value:
            return DiffMode.SIDE
        return DiffMode.DOWN

    # def get_lang_default(self) -> str:
    #     return self._lang_default

    # def get_last_rep(self) -> str:
    #     return self._last_rep

    def show_hidden(self) -> bool:
        return self._show_hidden

    def has_images(self) -> bool:
        return self._use_images

    def has_borders(self) -> bool:
        return self._use_borders

    def get_editor(self) -> str:
        return self._editor

    def get_timeout(self) -> int:
        return self._timeout

    def __str__(self):
        output: list[str] = []
        output.append(str(Text.format("{g}", "Configurações globais:")))
        output.append("- Diff    : {}".format(str(self.get_diff_mode().value)))
        output.append("- Editor  : {}".format(self.get_editor()))
        output.append("- Bordas  : {}".format(self.has_borders()))
        output.append("- Images  : {}".format(self.has_images()))
        output.append("- Timeout : {}".format(self.get_timeout()))
        return "\n".join(output)