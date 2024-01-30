"""
Welcome to DotSplit!
"""
from project import figletText, InvalidMsg, amountDivider
import pyfiglet

def test_slantText():
    assert figletText("abc", "lcd") == pyfiglet.figlet_format("abc", font="lcd")
    assert figletText("123", "larry3d") == pyfiglet.figlet_format("123", font="larry3d")
    assert figletText("DotSplit", "slant") == pyfiglet.figlet_format("DotSplit", font="slant")
    assert figletText("Help", "contessa") == pyfiglet.figlet_format("Help", font="contessa")

def test_InvalidMsg():
    assert InvalidMsg(0) == ""
    assert InvalidMsg(1) == "\n   Invalid Input, Please Select Again!\n"
    assert InvalidMsg(2) == "\nInvalid Input, Please Select Again!\n"
    assert InvalidMsg(6) == "\n         Database Not Found!\n"
    assert InvalidMsg(4) == "\n          Database Created!\n"

def test_amountDivider():
    assert amountDivider(5000, 3) == 1666
    assert amountDivider(7213, 5) == 1442
    assert amountDivider(9000, 9) == 1000