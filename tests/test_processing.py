from cyberpunk.processing import parse_query, process_args


def test_process_args():
    output = process_args("celtic_pt2.mp3", {"reverse": "true"})

    assert output == ("processed_celtic_pt2.mp3.mp3", "audio/mp3")


def test_parse_query():
    output = parse_query(
        "audio.mp3",
        {"reverse": "true", "repeat": "3", "slice": "1000:5000"},
    )

    assert output == {
        "audio": "audio.mp3",
        "reverse": "true",
        "repeat": "3",
        "slice": "1000:5000",
    }
