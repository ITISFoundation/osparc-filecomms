import concurrent.futures as futures
import json
import time

from osparc_filecomms import tools


def test_read_json(tmp_path):
    test_json_path = tmp_path / "test.json"

    test_json_data = {"test": "data"}
    test_json_path.write_text(json.dumps(test_json_data))

    assert tools.load_json(test_json_path, wait=False) == test_json_data


def test_wait_for_path(tmp_path):
    test_path = tmp_path / "test.json"

    executor = futures.ProcessPoolExecutor(max_workers=1)

    wait_future = executor.submit(tools.wait_for_path, test_path)

    assert wait_future.running()

    time.sleep(1)

    test_path.write_text("test")

    time.sleep(1)

    assert wait_future.done()

    executor.shutdown(wait=False, cancel_futures=True)
