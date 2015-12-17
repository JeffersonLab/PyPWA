import pytest
import PyPWA.data.memory.sv as sv
import os

TEST_SV = os.path.join(os.path.dirname(__file__), "test_docs/sv_test_data.csv")


def test_sv_read():
    sv_read = sv.SvParser(",")

    read = sv_read.reader(TEST_SV)

    assert len(list(read)) == 6, "SV length is wrong, was expecting 6, got {0} instead!".format(len(list(read)))
    assert read["ctAD"][2] == -0.265433, "SV Data read incorrectly, got {0} " + \
                                         "was expecting -0.265433".format(read["ctAD"][2])


def test_sv_read():
    sv_write = sv.SvParser(",")
    with pytest.raises(NotImplementedError):
        sv_write.writer(TEST_SV, {"something": False})