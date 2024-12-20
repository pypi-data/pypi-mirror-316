from czml3 import CZML_VERSION, Document, Packet


def test_document_has_expected_packets():
    preamble = Packet(version=CZML_VERSION)
    packet0 = Packet(id="id_00")
    packet1 = Packet(id="id_01")

    document = Document(packets=[preamble, packet0, packet1])

    assert document.packets == [preamble, packet0, packet1]


def test_doc_repr():
    packet = Packet(id="id_00", version=CZML_VERSION)
    expected_result = """[
    {
        "id": "id_00",
        "version": "CZML_VERSION"
    }
]""".replace("CZML_VERSION", CZML_VERSION)

    document = Document(packets=[packet])

    assert str(document) == expected_result


def test_doc_dumps():
    packet = Packet(id="id_00", version=CZML_VERSION)
    expected_result = """[{"id":"id_00","version":"CZML_VERSION"}]""".replace(
        "CZML_VERSION", CZML_VERSION
    )

    document = Document(packets=[packet])

    assert document.dumps() == expected_result
