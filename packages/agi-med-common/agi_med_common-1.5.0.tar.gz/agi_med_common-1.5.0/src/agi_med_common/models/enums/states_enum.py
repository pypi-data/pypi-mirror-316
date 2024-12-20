from enum import StrEnum, auto


class StatesEnum(StrEnum):
    """
    Класс для хранения имен состояний.
    """

    BEGIN = auto()
    START = auto()
    NOT_MEDICAL = auto()
    IS_CHILD = auto()
    IS_ABSURD = auto()
    CRITICAL = auto()
    WHAT_COMPLAINTS = auto()
    ANALYSIS_CONSULTATION = auto()
    COMMON_CONSULTATION = auto()
    INFO_COLLECTION = auto()
    MAKE_DIAGNOSIS = auto()
    COMMENT_DIAGNOSIS = auto()
    EXIT_INNER_CYCLE = auto()
