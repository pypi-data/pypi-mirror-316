import sys
import typing

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal


class PrettyConsole:
    """Pretty Console is a class that allows you to print colored text in the terminal in an easy way

    Features:
    ---------
        - Support for creating new custom print functions
        - Parse text between text color, background color and text style ANSI Escape Codes
        - Gives access to all text colors, background colors and text styles ANSI Escape Codes
        - Support for clearing the current text color, background color and text style
        - Support for configure and print with only one object
    """

    TextColors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "blk": "\033[30m",
        "r": "\033[31m",
        "g": "\033[32m",
        "y": "\033[33m",
        "b": "\033[34m",
        "m": "\033[35m",
        "c": "\033[36m",
        "w": "\033[37m",
    }

    BackgroundColors = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
        "blk": "\033[40m",
        "r": "\033[41m",
        "g": "\033[42m",
        "y": "\033[43m",
        "b": "\033[44m",
        "m": "\033[45m",
        "c": "\033[46m",
        "w": "\033[47m",
    }

    TextStyle = {
        "bold": "\033[1m",
        "underline": "\033[4m",
        "reversed": "\033[7m",
        "b": "\033[1m",
        "u": "\033[4m",
        "r": "\033[7m",
    }

    end = "\033[0m"

    def __init__(
        self,
        textColor: typing.Optional[
            Literal[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "blk",
                "r",
                "g",
                "y",
                "b",
                "m",
                "c",
                "w",
            ]
        ] = "",
        backgroundColor: typing.Optional[
            Literal[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "blk",
                "r",
                "g",
                "y",
                "b",
                "m",
                "c",
                "w",
            ]
        ] = "",
        textStyle: typing.Optional[
            Literal[
                "bold",
                "underline",
                "reversed",
                "b",
                "u",
                "r",
            ]
        ] = "",
    ) -> None:
        """Create a new PrettyConsole object. You can set the default text color, background color and text style.

        Args:
        ----
            - textColor (str, optional): A string representing an Available Color. Defaults to \"\".
            - backgroundColor (str, optional): A string representing an Available Color. Defaults to \"\".
            - textStyle (str, optional): A string representing an Available Style. Defaults to \"\".

        Avalible Colors:
        ---------------
            - \"\" for default console color\n
            - \"black\" or \"blk\"\n
            - \"red\" or \"r\"\n
            - \"green\" or \"g\"\n
            - \"yellow\" or \"y\"\n
            - \"blue\" or \"b\"\n
            - \"magenta\" or \"m\"\n
            - \"cyan\" or \"c\"\n
            - \"white\" or \"w\"\n
        """
        self.textColor = ""
        self.backgroundColor = ""
        self.textStyle = ""
        self.config(textColor, backgroundColor, textStyle)

    def createPrintFromObject(self) -> callable:
        """Create a new print function from the object current text color, background color and text style.

        Returns:
        --------
            callable: your new custom print function
        """
        def newPrint(data: str, onlyParse: bool = False) -> None:
            if onlyParse:
                return f"{self.textColor}{self.backgroundColor}{self.textStyle}{data}{self.end}"
            print(f"{self.textColor}{self.backgroundColor}{self.textStyle}{data}{self.end}")

        return newPrint

    def createPrint(
        textColor: typing.Optional[
            Literal[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "blk",
                "r",
                "g",
                "y",
                "b",
                "m",
                "c",
                "w",
            ]
        ] = "",
        backgroundColor: typing.Optional[
            Literal[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "blk",
                "r",
                "g",
                "y",
                "b",
                "m",
                "c",
                "w",
            ]
        ] = "",
        textStyle: typing.Optional[
            Literal[
                "bold",
                "underline",
                "reversed",
                "b",
                "u",
                "r",
            ]
        ] = "",
    ) -> callable:
        """
        Create a new print function with the given text color, background color and text style.

        Args:
        ----
            - textColor (str, optional): A string representing an Available Color. Defaults to \"\".
            - backgroundColor (str, optional): A string representing an Available Color. Defaults to \"\".
            - textStyle (str, optional): A string representing an Available Style. Defaults to \"\".

        Avalible Colors:
        ---------------
            - \"\" for default console color\n
            - \"black\" or \"blk\"\n
            - \"red\" or \"r\"\n
            - \"green\" or \"g\"\n
            - \"yellow\" or \"y\"\n
            - \"blue\" or \"b\"\n
            - \"magenta\" or \"m\"\n
            - \"cyan\" or \"c\"\n
            - \"white\" or \"w\"\n

        Returns:
        --------
            callable: your new custom print function
        """
        textColor = PrettyConsole.TextColors.get(textColor, "")
        backgroundColor = PrettyConsole.BackgroundColors.get(backgroundColor, "")
        textStyle = PrettyConsole.TextStyle.get(textStyle, "")

        def newPrint(data: str, onlyParse: bool = False) -> None:
            if onlyParse:
                return f"{textColor}{backgroundColor}{textStyle}{data}{PrettyConsole.end}"
            print(f"{textColor}{backgroundColor}{textStyle}{data}{PrettyConsole.end}")

        return newPrint

    def config(
        self,
        textColor: typing.Optional[
            Literal[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "blk",
                "r",
                "g",
                "y",
                "b",
                "m",
                "c",
                "w",
            ]
        ] = "",
        backgroundColor: typing.Optional[
            Literal[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "blk",
                "r",
                "g",
                "y",
                "b",
                "m",
                "c",
                "w",
            ]
        ] = "",
        textStyle: typing.Optional[
            Literal[
                "bold",
                "underline",
                "reversed",
                "b",
                "u",
                "r",
            ]
        ] = "",
    ) -> None:
        """Configure the current text color, background color and text style.

        Args:
        ----
            - textColor (str, optional): A string representing an Available Color. Defaults to \"\".
            - backgroundColor (str, optional): A string representing an Available Color. Defaults to \"\".
            - textStyle (str, optional): A string representing an Available Style. Defaults to \"\".

        Avalible Colors:
        ---------------
            - \"\" for default console color\n
            - \"black\" or \"blk\"\n
            - \"red\" or \"r\"\n
            - \"green\" or \"g\"\n
            - \"yellow\" or \"y\"\n
            - \"blue\" or \"b\"\n
            - \"magenta\" or \"m\"\n
            - \"cyan\" or \"c\"\n
            - \"white\" or \"w\"\n
        """
        self.textColor = self.TextColors.get(textColor, self.textColor)
        self.backgroundColor = self.BackgroundColors.get(backgroundColor, self.backgroundColor)
        self.textStyle = self.TextStyle.get(textStyle, self.textStyle)

    def clear(self) -> None:
        """
        Clear the current text color, background color and text style.
        """
        self.textColor = ""
        self.backgroundColor = ""
        self.textStyle = ""

    def parse(self, data: str) -> str:
        """
        Parse the given data with the current text color, background color and text style.

        Args:
        -----
            - data (str): The string to be parsed

        Returns:
        --------
            str: The parsed string
        """
        return f"{self.textColor}{self.backgroundColor}{self.textStyle}{data}{self.end}"

    def print(self, data: str) -> None:
        """
        Print the given data with the current text color, background color and text style.

        Args:
        -----
            - data (str): The string to printed parsed
        """
        print(self.parse(data))


if __name__ == "__main__":

    errorPrint = PrettyConsole.createPrint("r", "blk", "b")
    errorPrint("This is an errorPrint Test")
