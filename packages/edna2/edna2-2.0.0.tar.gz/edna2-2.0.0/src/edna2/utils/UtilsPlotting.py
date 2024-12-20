from functools import wraps
from typing import Callable

import matplotlib
import matplotlib.pyplot as plt

from edna2.utils import UtilsLogging

logger = UtilsLogging.getLogger()


def ensure_safe_plotting(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(*args, **kwargs):
        original_backend = matplotlib.get_backend()
        plt.close("all")
        matplotlib.use("Agg", force=True)

        try:
            return method(*args, **kwargs)
        finally:
            plt.close("all")
            matplotlib.use(original_backend, force=True)

    return wrapper


def set_font_size(size: int) -> None:
    matplotlib.rcParams["font.size"] = size
