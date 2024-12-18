import asyncio
from collections import defaultdict
from typing import Any, Optional

from nats.aio.msg import Msg

from nats_app.middlewares.validation import validate_args


async def test_rpc_call(nc):
    @nc.push_subscribe("app.subject.echo", queue="worker")
    async def rpc_func_echo(m: Msg) -> str:
        return f"Response: {m.data}"

    await nc.connect()

    res = await nc.request("app.subject.echo", "test")
    assert isinstance(res, str)
    assert res == "Response: b'\"test\"'"


async def test_rpc_call_w_validate(nc):
    @nc.push_subscribe("app.subject.validate_echo", queue="worker")
    @validate_args(by_pass_msg="msg")
    async def rpc_func_echo(data: str, msg: Any) -> str:
        return f"Response: {data} Msg.data: {msg.data}"

    await nc.connect()

    res = await nc.request("app.subject.validate_echo", {"args": ["test"]})
    assert isinstance(res, str)
    assert res == 'Response: test Msg.data: b\'{"args":["test"]}\''


async def test_rpc_call_w_validate_wo_param(nc):
    @nc.push_subscribe("app.subject.validate_echo", queue="worker")
    @validate_args
    async def rpc_func_echo(data: str) -> str:
        return f"Response: {data}"

    await nc.connect()

    res = await nc.request("app.subject.validate_echo", {"args": ["test"]})
    assert isinstance(res, str)
    assert res == "Response: test"


async def test_rpc_call_invalid_args(nc):
    @nc.push_subscribe("app.subject.validate_echo", queue="worker")
    @validate_args(by_pass_msg="msg")
    async def rpc_func_echo(data: str, val: int, key: bool, var1: Optional[float], var2: float, msg: Any) -> str:
        return f"Response: {data} Msg.data: {msg.data}"

    await nc.connect()

    res = await nc.request(
        "app.subject.validate_echo",
        {"args": ["test", "wow"], "kwargs": {"var1": "oto", "var2": 3.14}},
    )
    assert isinstance(res, dict)
    assert res == {
        "errors": [
            {
                "loc": [1],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "type": "int_parsing",
            },
            {
                "loc": ["key"],
                "msg": "Missing required argument",
                "type": "missing_argument",
            },
            {
                "loc": ["var1"],
                "msg": "Input should be a valid number, unable to parse string as a number",
                "type": "float_parsing",
            },
        ]
    }


async def test_publish_w_validate(nc):
    result = {}

    @nc.push_subscribe("app.subject.pub")
    @validate_args()
    async def rpc_func_echo(data: str, data1: int) -> None:
        result["data"] = data
        result["data1"] = data1

    await nc.connect()

    await nc.publish("app.subject.pub", {"args": ["test"], "kwargs": {"data1": 1}})
    assert result["data"] == "test"
    assert result["data1"] == 1


async def test_publish_wo_validate(nc):
    result = {}

    @nc.push_subscribe("app.subject.pub_raw")
    async def rpc_func_echo(m: Msg) -> None:
        result["data"] = m.data

    await nc.connect()

    await nc.publish("app.subject.pub_raw", {"args": ["test"], "kwargs": {"data1": 1}})
    assert result["data"] == b'{"args":["test"],"kwargs":{"data1":1}}'


async def test_publish_w_queue(nc):
    c = defaultdict(int)
    result = {}

    @nc.push_subscribe("app.subject.pub_raw", queue="worker")
    async def rpc_func_echo(m: Msg) -> None:
        c["call"] += 1
        result["data"] = m.data

    @nc.push_subscribe("app.subject.pub_raw", queue="worker")
    async def rpc_func_echo_v2(m: Msg) -> None:
        c["call"] += 1
        result["data"] = m.data

    await nc.connect()

    await nc.publish("app.subject.pub_raw", {"args": ["test"], "kwargs": {"data1": 1}})
    assert result["data"] == b'{"args":["test"],"kwargs":{"data1":1}}'
    assert c["call"] == 1


async def test_publish_wo_queue(nc):
    c = defaultdict(int)
    result = {}

    @nc.push_subscribe("app.subject.pub_raw")
    async def rpc_func_echo(m: Msg) -> None:
        c["call"] += 1
        result["data"] = m.data

    @nc.push_subscribe("app.subject.pub_raw")
    async def rpc_func_echo_v2(m: Msg) -> None:
        c["call"] += 1
        result["data"] = m.data

    await nc.connect()

    await nc.publish("app.subject.pub_raw", {"args": ["test"], "kwargs": {"data1": 1}})
    assert result["data"] == b'{"args":["test"],"kwargs":{"data1":1}}'
    assert c["call"] == 2


async def test_push_subscription(nc):
    result = None

    @nc.js_push_subscribe("app.subject.validate_echo", queue="worker")
    async def handler(msg: Msg):
        nonlocal result
        result = msg.data
        await msg.ack()

    await nc.connect()

    await nc.js.publish("app.subject.validate_echo", b"TEST123")
    assert isinstance(result, bytes)
    assert result == b"TEST123"


async def test_pull_subscription(nc):
    result = None

    @nc.js_pull_subscribe("app.subject.validate_echo", batch=1)
    async def handler(msgs: list[Msg]):
        assert isinstance(msgs, list)
        assert len(msgs) == 1
        nonlocal result
        result = msgs[0].data

    try:
        await nc.connect()
        await nc.js.publish("app.subject.validate_echo", b"TEST123")
        await asyncio.sleep(1)
        assert isinstance(result, bytes)
        assert result == b"TEST123"
    finally:
        nc._js_pull_subscriber_stop()
