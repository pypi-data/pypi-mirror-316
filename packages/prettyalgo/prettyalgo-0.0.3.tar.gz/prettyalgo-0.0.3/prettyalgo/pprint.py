"""Pretty printing module."""

import os
import re
import sys
from collections.abc import Sequence
from time import sleep
from typing import List

from termcolor import colored

NEW_LINE = "\n"
H_SEP = "-"
V_SEP = "|"
EDGE_CHAR = "+"
EMPTY_STR = "<Empty List>"


def build_vpad(s):
    """Helper method to build the vertical padding for a list,
    given the primary string representation already constructed.

    """
    return re.sub(r"[^\s|]", " ", s)


class PrettyListPrinter:
    def __init__(
        self,
        padding=1,
        v_padding=0,
        h_sep=H_SEP,
        v_sep=V_SEP,
        edge_char=EDGE_CHAR,
        caption=None,
        animate=False,
        animate_fps=1,
        clear=True,
        interactive=False,
    ):
        """A pretty printer for list objects useful in particular for visualizing algorithms involving
        iteration over lists with one or more pointers.

        Implements an interface similar to the native Python pprint module.

        """
        self.padding = padding
        self.v_padding = v_padding
        self.h_sep = h_sep
        self.v_sep = v_sep
        self.edge_char = edge_char
        self.caption = caption
        self.animate = animate
        self.animate_fps = animate_fps
        self.clear = clear
        self.interactive = interactive

        # used to track state as a context manager
        self.using_context = False

    def __enter__(self):
        self.using_context = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.using_context = False

    def pformat(self, lst: List, ptrs=None, context=None) -> str:
        """Return a formatted string representation of the given list,
        along with given optional parameters such as pointers into
        positions in list and variables used to hold various contextual
        information we wish to display in tandem.

        Args:
            lst (List): list
            ptrs (dict, optional): dictionary of pointers giving their display name and value. Defaults to None.
            context (dict, optional): dictionary of context variables giving their display name and value. Defaults to None.

        Returns:
            str: formatted string

        """
        if not lst:
            return EMPTY_STR
        if not isinstance(lst, Sequence):
            raise TypeError(f"input must be a sequence type. Got: {type(lst)=}")

        # our formatted string is made out of three separable parts:
        # - some preamble, e.g. optional captioning and such ("the tray")
        # - the variables display including optional contextual variables ("the soda")
        # - the main list itself ("the sandwich")
        # - the (optional) pointers display ("the fries").
        #   These need to know a bit more about the sandwich innards, hence "the ham".
        tray = self._tray(lst)
        sando, ham = self._sando(lst)
        fries = self._fries(lst, ham, ptrs=ptrs)
        soda = self._soda(lst, ptrs=ptrs, context=context)

        return tray + soda + sando + fries

    def pprint(self, lst: List, fp=None, *args, **kwargs):
        """Wrapper around `pformat()` that will print to given file pointer
        or to sys.stdout if none is provided. All other arguments are passed
        as is into the `pformat()` call.

        Args:
            lst (List): list
            fp (file object, optional): file object to write to. Defaults to None which will route to sys.stdout.

        """
        fp = fp if fp else sys.stdout
        if self.animate:
            sleep(1 / self.animate_fps)
        if self.clear:
            os.system("clear")

        fp.write(self.pformat(lst, *args, **kwargs))

        if self.interactive:
            input(NEW_LINE + "Press Enter to continue...")

    # alias for pprint
    pp = pprint

    def _tray(self, lst):
        """The tray is the preamble: optional captioning and such."""
        tray = []
        if self.caption:
            tray.append(self.caption)
            tray.append(self.h_sep * len(self.caption))

        tray_str = NEW_LINE.join(tray) + NEW_LINE

        return tray_str

    def _sando(self, lst):
        """The sandwich is the actual list display."""
        pad = " " * self.padding
        ham = (
            f"{self.v_sep}{pad}"
            + f"{pad}|{pad}".join(str(x) for x in lst)
            + f"{pad}{self.v_sep}"
        )
        cheese = (
            NEW_LINE.join((build_vpad(ham) for i in range(self.v_padding)))
            if self.v_padding
            else None
        )
        bun = self.edge_char + self.h_sep * (len(ham) - 2) + self.edge_char

        sando = [bun, cheese, ham, cheese, bun]
        sando_str = NEW_LINE + NEW_LINE.join(elem for elem in sando if elem) + NEW_LINE

        return sando_str, ham

    def _fries(self, lst, ham, ptrs):
        """The fries are the various pointers we display positionally with respect to the list."""
        fries, fries_str = [], ""
        if ptrs:
            # given some pointers to list to display
            cell_border_pos = [pos for pos, char in enumerate(ham) if char == V_SEP]

            for name, value in ptrs.items():
                if value < 0:
                    # Out of bounds to the left
                    fries.append(f"^ {name}={value} " + colored("(OOB)", "red"))
                elif value > len(lst) - 1:
                    # Out of bounds to the right
                    fries.append(
                        (" " * len(ham))
                        + f"^ {name}={value} "
                        + colored("(OOB)", "red")
                    )
                else:
                    display_pos = (
                        cell_border_pos[value] + cell_border_pos[value + 1]
                    ) // 2
                    fries.append(" " * display_pos + f"^ {name}={value}")

        fries_str = NEW_LINE.join(fries) + NEW_LINE

        return fries_str

    def _soda(self, lst, ptrs=None, context=None):
        """The soda is additional meta-data e.g. contextual parameters we display alongside."""
        soda = []

        soda.append(f"{'len(lst):':<12}{len(lst):>8}")
        if ptrs:
            for name, value in ptrs.items():
                soda.append(f"{name:<12}{value:>8}")
        if context:
            for name, value in context.items():
                soda.append(f"{name:<12}{value:>8}")

        soda_str = NEW_LINE.join(elem for elem in soda if elem) + NEW_LINE

        return soda_str


class PrettyList(list):
    def __str__(self):
        return PrettyListPrinter(padding=1).pprint(self)
