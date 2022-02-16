from cyberpunk.processing import process_args


def test_process_args():
    output = process_args("celtic_pt2.mp3", {"reverse": "true"})

    assert output == ("processed_celtic_pt2.mp3", "audio/mp3")
