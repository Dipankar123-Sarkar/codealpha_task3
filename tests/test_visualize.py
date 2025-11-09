import os
from pathlib import Path

from src.visualize import generate_visuals


def test_generate_visuals(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    files = generate_visuals(str(out))
    assert len(files) >= 4, "Expected at least 4 images generated"
    for f in files:
        assert os.path.exists(f), f"File missing: {f}"


if __name__ == "__main__":
    test_generate_visuals(Path("tmp_test"))
    print("Ran local test: success")
