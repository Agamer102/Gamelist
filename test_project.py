import pytest
from project import getid
from project import verify_time
from project import format_time
from project import steam_request


def test_getid():
    assert getid(filename="notexist.csv") == 1
    assert getid(filename="test_gamelist1.csv") == 2

def test_verify_time():
    assert verify_time("20h") == "20h 00m"
    assert verify_time("5m") == "0h 05m"
    assert verify_time("5h 3m") == "5h 03m"
    with pytest.raises(ValueError):
        verify_time("Invalid")
    with pytest.raises(ValueError):
        verify_time("20d 5h 5m") 
    with pytest.raises(ValueError):
        verify_time("5h 4m 3s") 
    
    assert verify_time("20h", strip=True) == (20, 0)
    assert verify_time("5m", strip=True) == (0, 5)
    assert verify_time("5h 3m", strip=True) == (5, 3)
    with pytest.raises(ValueError):
        verify_time("Invalid", strip=True)
    with pytest.raises(ValueError):
        verify_time("20d 5h 5m", strip=True) 
    with pytest.raises(ValueError):
        verify_time("5h 4m 3s", strip=True)

def test_format_time():
    assert format_time(2, 2) == "2h 02m"
    assert format_time(0, 600) == "10h 00m"
    assert format_time(0, 80) == "1h 20m"

def test_steam_request():
    assert steam_request("1091500") == {"name": "Cyberpunk 2077", "steamid": "1091500"}
    assert steam_request("753640") == {"name": "Outer Wilds", "steamid": "753640"}
    assert steam_request("264710") == {"name": "Subnautica", "steamid": "264710"}
    with pytest.raises(ValueError):
        steam_request("Subnautica")
    with pytest.raises(ValueError):
        steam_request("171909")