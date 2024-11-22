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

    # test_json_data = {"test": "data"}
    # test_json_path.write_text(json.dumps(test_json_data))
    #
    # assert tools.load_json(test_json_path, wait=False) == test_json_data
    
    # test_input_dir = tmp_path / "test_input_dir"
    # test_output_dir = tmp_path / "test_output_dir"
    # test_input_dir.mkdir()
    # test_output_dir.mkdir()
    #
    # initiator_uuid = str(uuid.uuid4())
    # receiver_uuid = str(uuid.uuid4())
    #
    # initiator_other_uuid = executor.submit(
    #     run_handshake, initiator_uuid, test_input_dir, test_output_dir, True
    # )
    # receiver_other_uuid = executor.submit(
    #     run_handshake, receiver_uuid, test_output_dir, test_input_dir, False
    # )
    #
    # executor.shutdown()
    #
    # assert initiator_other_uuid.result() == receiver_uuid
    # assert receiver_other_uuid.result() == initiator_uuid
