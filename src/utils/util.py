# coding: utf-8
import os
import sys
import shutil
import __main__
from pathlib import Path
from typing import List, Union, overload
from ..cfg import config

_APP_ROOT = None
_APP_CFG = None

def get_root() -> str:
    """
    Gets Application Root Path

    Returns:
        str: App root as string.
    """
    global _APP_ROOT
    if _APP_ROOT is None:
        _APP_ROOT = os.environ.get("project_root", str(Path(__main__.__file__).parent))
    return _APP_ROOT


def get_app_cfg() -> config.AppConfig:
    """
    Get App Config. config is cached
    """
    global _APP_CFG
    if _APP_CFG is None:
        _APP_CFG = config.read_config_default()
    return _APP_CFG


@overload
def get_path(path: str, ensure_absolute: bool = False) -> Path:
    ...


@overload
def get_path(path: List[str], ensure_absolute: bool = False) -> Path:
    ...


@overload
def get_path(path: Path, ensure_absolute: bool = False) -> Path:
    ...


def get_path(path: Union[str, Path, List[str]], ensure_absolute: bool = False) -> Path:
    """
    Builds a Path from a list of strings

    If path starts with ``~`` then it is expanded to user home dir.

    Args:
        lst (List[str], Path, str): List of path parts
        ensure_absolute (bool, optional): If true returned will have root dir prepended
            if path is not absolute

    Raises:
        ValueError: If lst is empty

    Returns:
        Path: Path of combined from ``lst``
    """
    p = None
    lst = []
    expand = None
    if isinstance(path, str):
        expand = path.startswith("~")
        p = Path(path)
    elif isinstance(path, Path):
        p = path
    else:
        lst = [s for s in path]
    if p is None:
        if len(lst) == 0:
            raise ValueError("lst arg is zero length")
        arg = lst[0]
        expand = arg.startswith("~")
        p = Path(*lst)
    else:
        if expand is None:
            pstr = str(p)
            expand = pstr.startswith("~")
    if expand:
        p = p.expanduser()
    if ensure_absolute is True and p.is_absolute() is False:
        p = Path(get_root(), p)
    return p


@overload
def mkdirp(dest_dir: str) -> None:
    ...


@overload
def mkdirp(dest_dir: Path) -> None:
    ...


def mkdirp(dest_dir: Union[str, Path]) -> None:
    """
    Creates path and subpaths not existing.

    Args:
        dest_dir (Union[str, Path]): PathLike object

    Since:
        Python 3.5
    """
    # Python ≥ 3.5
    if isinstance(dest_dir, Path):
        dest_dir.mkdir(parents=True, exist_ok=True)
    else:
        Path(dest_dir).mkdir(parents=True, exist_ok=True)


def _get_virtual_path() -> str:
    spath = os.environ.get("VIRTUAL_ENV", None)
    if spath is not None:
        return spath
    return sys.base_exec_prefix


def get_site_packeges_dir() -> Union[Path, None]:
    """
    Gets the ``site-packages`` directory for current python environment.

    Returns:
        Union[Path, None]: site-packages dir if found; Otherwise, None.
    """
    v_path = _get_virtual_path()
    p_site = Path(v_path, "Lib", "site-packages")
    if p_site.exists() and p_site.is_dir():
        return p_site

    ver = f"{sys.version_info[0]}.{sys.version_info[1]}"
    p_site = Path(v_path, "lib", f"python{ver}", "site-packages")
    if p_site.exists() and p_site.is_dir():
        return p_site
    return None