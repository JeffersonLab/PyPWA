import PyPWA.configuratr

DATA_CONFIG = {
    "Data Location": "/some/data/location.tsv",
    "Monte Carlo Location": "/some/other/data/location.tsv",
    "QFactor List Location": "/the/place/where/quality/is/decided.txt",
    "Save Location": ["/the/place/to/save.tsv", "theplace.txt", "the/last/thing.tex"],
    "BinN Location": "/bin/N/location.txt",
    "White Noise" : "This should be logged"
}

BROKEN_DATA_CONFIG = ["not a dict", 5]


def test_data_configuratr():
    configuratr = PyPWA.configuratr.DataConfiguratr(DATA_CONFIG)

    assert configuratr.data_location() == "/some/data/location.tsv"
    assert configuratr.monte_carlo_location == "/some/other/data/location.tsv"
    assert configuratr.qfactor_location == "/the/place/where/quality/is/decided.txt"
    assert configuratr.save_location == ["/the/place/to/save.tsv", "theplace.txt", "the/last/thing.tex"]
    assert configuratr.extras == {"White Noise" : "This should be logged"}
    assert configuratr.bin_location == "/bin/N/location.txt"