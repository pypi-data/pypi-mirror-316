from PrettyConsole import PrettyConsole

colorOptions = ["blk", "r", "g", "y", "b", "m", "c", "w"]
styleOptions = ["b", "u", "r"]

def test_default():
    prettyConsole = PrettyConsole()
    prettyConsole.print("Hello World")
    prettyConsole.parse("Hello World")


def test_constructor():
    prettyConsole = PrettyConsole(colorOptions[1], colorOptions[1], styleOptions[2])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[31m\033[41m\033[7mHello World\033[0m"
    prettyConsole = PrettyConsole(colorOptions[6], colorOptions[0], styleOptions[0])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[36m\033[40m\033[1mHello World\033[0m"
    prettyConsole = PrettyConsole(colorOptions[6], colorOptions[2], styleOptions[2])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[36m\033[42m\033[7mHello World\033[0m"


def test_clear():
    prettyConsole = PrettyConsole(colorOptions[3], colorOptions[2], styleOptions[1])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[33m\033[42m\033[4mHello World\033[0m"
    prettyConsole.clear()
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "Hello World\033[0m"


def test_config():
    prettyConsole = PrettyConsole(colorOptions[0], colorOptions[3], styleOptions[0])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[30m\033[43m\033[1mHello World\033[0m"
    prettyConsole.config(colorOptions[1], colorOptions[6], styleOptions[2])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[31m\033[46m\033[7mHello World\033[0m"
    prettyConsole.config(colorOptions[5], colorOptions[0], styleOptions[1])
    assert prettyConsole.print("Hello World") == None
    assert prettyConsole.parse("Hello World") == "\033[35m\033[40m\033[4mHello World\033[0m"
    prettyConsole.config(colorOptions[5], colorOptions[1], styleOptions[2])


def test_createPrintFromObject():
    prettyConsole = PrettyConsole(colorOptions[2], colorOptions[4], styleOptions[0])
    newPrint = prettyConsole.createPrintFromObject()
    assert newPrint("Hello World") == None
    assert newPrint("Hello World", True) == "\033[32m\033[44m\033[1mHello World\033[0m"


def test_createPrint():
    newPrint = PrettyConsole.createPrint(colorOptions[3], colorOptions[5], styleOptions[0])
    assert newPrint("Hello World") == None
    assert newPrint("Hello World", True) == "\033[33m\033[45m\033[1mHello World\033[0m"
    newPrint = PrettyConsole.createPrint(colorOptions[0], colorOptions[6], styleOptions[0])
    assert newPrint("Hello World") == None
    assert newPrint("Hello World", True) == "\033[30m\033[46m\033[1mHello World\033[0m"


if __name__ == "__main__":
    test_default()
    test_constructor()
    test_clear()
    test_config()
    test_createPrintFromObject()
    test_createPrint()
