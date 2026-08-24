"""index.json must stay in sync with the cases on disk (regenerate via build_index.py)."""
import importlib.util
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DI = os.path.abspath(os.path.join(_HERE, "..", "..", "docs", "detector-interop"))


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_index", os.path.join(_DI, "build_index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_index_in_sync():
    idx_path = os.path.join(_DI, "index.json")
    assert os.path.isfile(idx_path), "index.json missing — run build_index.py"
    on_disk = json.load(open(idx_path))
    regenerated = _load_builder().build()
    assert on_disk == regenerated, "index.json is stale — run `python docs/detector-interop/build_index.py`"
    assert regenerated["count"] >= 2
