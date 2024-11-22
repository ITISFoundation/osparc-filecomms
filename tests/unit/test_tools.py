import json
import pathlib as pl
import types

import osparc_filecomms.tools as tools


def test_import_tools():
    assert isinstance(tools, types.ModuleType)


def test_load_json(mocker):
    test_json_path = pl.Path("test.json")

    test_json_data = {"test": "data"}
    mocker.patch.object(
        pl.Path, "read_text", side_effect=[json.dumps(test_json_data)]
    )

    assert tools.load_json(test_json_path, wait=False) == test_json_data


def test_wait_path(mocker):
    test_json_path = pl.Path("test.json")

    # Check if it fails is path doesnt exist
    mocker.patch.object(pl.Path, "exists", side_effect=[False])
    try:
        tools.wait_for_path(test_json_path)
    except StopIteration as error:
        assert isinstance(error, StopIteration)

    # Check if it succeeds if path does exist
    mocker.patch.object(pl.Path, "exists", side_effect=[True])
    tools.wait_for_path(test_json_path)
