import pytest
import backend
from backend import *

def test_createacct():
    x= createacct(MasterAccountList, current[0], current[2])
    assert x == MasterAccountList

def test_withdrawT1():
    x = withdraw(MasterAccountList, current[1], current[2])
    assert x[0] == current[1]

def test_withdrawT2():
    x = withdraw(MasterAccountList, current[1], current[2])
    assert x[0] is None

def test_withdrawT3():
    x = withdraw(MasterAccountList, current[1], current[2])
    assert x[1] >= current[2]

def test_withdrawT4():
    x = withdraw(MasterAccountList, current[1], current[2])
    assert x[1] >= current[2]