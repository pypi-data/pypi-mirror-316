from enum import Enum


class PositionTypeEnum(Enum):
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class XPositionEnum(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class YPositionEnum(Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
