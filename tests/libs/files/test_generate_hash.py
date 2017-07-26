import os

from PyPWA.libs.files import generate_hash

FILE_LOCATION = os.path.join(
    os.path.dirname(__file__),
    "../../data/test_docs/sv_test_data.tsv"
)


def test_FileHash_sha512_StringReturned():
    the_hash = generate_hash.get_sha512_hash(FILE_LOCATION)
    check_hash(the_hash)


def check_hash(the_hash):
    assert isinstance(the_hash, str)
    assert len(the_hash) > 5
