from main import zzz
import os
import pytest



print(os.getcwd())

def test_yyy() -> None:
    assert zzz() == "yyyzzz"


def test_cwd():
    """dasdasds"""
    assert r"D:\repos\small_projects\my_modules" == os.getcwd()