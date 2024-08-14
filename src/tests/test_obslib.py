import obslib

def test_obs_coerce():
    assert(obslib.coerce_value(int, "5") == 5)

