import logging
import typing

from fspacker.packer.base import BasePacker
from fspacker.parser.target import PackTarget
from fspacker.utils.libs import unpack_zipfile
from fspacker.utils.repo import get_libs_repo
from fspacker.utils.wheel import unpack_wheel


class LibSpecPackerMixin:
    PATTERNS: typing.Dict[str, typing.Set[str]] = {}
    EXCLUDES: typing.Dict[str, typing.Set[str]] = {}

    def pack(self, lib: str, target: PackTarget): ...


class ChildLibSpecPacker(LibSpecPackerMixin):
    def __init__(self, parent: BasePacker) -> None:
        self.parent = parent

    def pack(self, lib: str, target: PackTarget):
        specs = {k: v for k, v in self.parent.SPECS.items() if k != lib}

        logging.info(f"Use [{self.__class__.__name__}] spec")
        for libname, patterns in self.PATTERNS.items():
            if libname in target.lib_folders:
                logging.info(f"Lib [{libname}] already packed, skipping")
                continue

            if libname in specs:
                specs[libname].pack(libname, target=target)
            else:
                unpack_wheel(
                    libname.lower(),
                    target.packages_dir,
                    patterns,
                    self.EXCLUDES.setdefault(libname, set()),
                )


class DefaultLibrarySpecPacker(LibSpecPackerMixin):
    def pack(self, lib: str, target: PackTarget):
        if lib not in target.lib_folders:
            logging.info(f"Packing [{lib}], using [default] lib spec")
            info = get_libs_repo().get(lib)
            if info.filepath.suffix == ".whl":
                unpack_wheel(lib, target.packages_dir, set(), set())
            elif info.filepath.suffix == ".gz":
                unpack_zipfile(info.filepath, target.packages_dir)
        else:
            logging.info(f"Already packed, skip [{lib}]")
