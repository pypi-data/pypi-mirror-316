import asyncio
import inspect
import json
import random
import string


class Executor:
    def current(self, time, day) -> dict:
        return {
            "today": "nice",
            "time": time,
            "day": day
        }

    def this_week(self) -> list:
        l = [1, 2, 3, 4, 5]
        return l


CMD_LOGIN = 1
CMD_HEART_BEAT = 2
CMD_USER_REQUEST = 3
CMD_PIPELINE = 4

STATUS_INIT = 1
STATUS_RUNNING = 2
STATUS_CLOSE = 3


class TCPClient:
    def __init__(self, host='127.0.0.1', port=8889, instance=None, limit=2 ** 20, version="0.0.0", id=None,
                 token="default"):
        self.__class_info = get_class_methods_info(instance)
        self.__host = host
        self.__port = port
        self.__instance = instance
        self.__limit = limit
        self.__version = version
        self.__reader = None
        self.__writer = None
        self.__token = token
        self.__status = STATUS_INIT
        self.__id = id if id is not None else None
        if self.__id is None:
            self.__id = generate_random_string(8)

    def is_running(self):
        return self.__status == STATUS_RUNNING

    def is_close(self):
        return self.__status == STATUS_CLOSE

    async def execute(self):
        asyncio.create_task(self.__start())

    async def __start(self):
        while True:
            try:
                await self.__connect_server()
            except Exception as e:
                print(f'disconnect from server:{e}')
                await asyncio.sleep(2)

    async def __connect_server(self):
        reader, writer = await asyncio.open_connection(self.__host, self.__port, limit=self.__limit)

        self.__reader = reader
        self.__writer = writer

        if await self.__login():
            self.__status = STATUS_RUNNING
            print(f'connect to server success')
        else:
            print(f'connect to server fail, please check')
            writer.close()
            await writer.wait_closed()
            self.__status = STATUS_CLOSE

        try:
            while True:
                # 等待服务器的回复
                data = await reader.readuntil(b'\r\n')
                if data.__len__() == 0:
                    continue
                print(f'Received from server: {data.decode()}')
                request = json.loads(data)

                if request["command"] == "rest-api":
                    result = self.__class_info
                else:
                    try:
                        method = getattr(self.__instance, request["command"])
                        kwargs = request["request"]
                        result = method(**kwargs)
                    except Exception as e:
                        await  self.__send_to_server(CMD_USER_REQUEST, 500, {
                            "id": request["id"],
                        },
                                                     f"exec cmd[{request['command']}] fail:{e}")
                        continue

                if result is None:
                    print(f'No response')

                resp = {
                    "id": request["id"],
                    "data": result,
                }

                await  self.__send_to_server(CMD_USER_REQUEST, 0, resp, "")
        except Exception as e:
            print(f"get a exception: {e}")
        finally:
            print('Closing connection')
            writer.close()
            await writer.wait_closed()
            self.__status = STATUS_CLOSE

    async def send_to_pipeline(self, name, data):
        if self.__status != STATUS_RUNNING:
            print(f"client is not running, status is {self.__status}, please wait")
            return
        await self.__send_to_server(CMD_PIPELINE, 0, {
            "name": name,
            "data": data,
        }, "")

    async def __send_to_server(self, cmd, code, data, message):
        resp = {
            "code": code,
            "data": data,
            "message": message,
            "cmd": cmd,
        }

        resp_data = (json.dumps(resp) + '\r\n').encode()
        if resp_data.__len__() > self.__limit:
            del resp["data"]

            resp["code"] = 500
            resp[
                "message"] = f"resp data is too large[{resp_data.__len__()}], which is over limit[{self.__limit}]"
            resp_data = (json.dumps(resp) + '\r\n').encode()

        self.__writer.write(resp_data)

    async def __login(self):
        try:
            await self.__send_to_server(CMD_LOGIN, 0, {
                "id": self.__id,
                "token": self.__token,
                "version": self.__version
            }, "")
            return True
        except Exception as e:
            print(f"login fail: {e}")
            return False


def get_class_methods_info(cls):
    methods_info = []
    for name in dir(cls):
        method = getattr(cls, name)
        if callable(method) and not name.startswith("__"):  # 过滤掉私有方法
            # 获取方法的签名
            sig = inspect.signature(method)
            return_annotation = sig.return_annotation
            request = []
            for item in sig.parameters.items():
                if item[0] != "self":
                    request.append(item[0])

            # 记录方法信息
            methods_info.append({
                "path": name,
                "request": request,
                "response": str(return_annotation) if return_annotation is not inspect.Signature.empty else "None",
            })
    return methods_info


def generate_random_string(length):
    # 定义可用的字符集：大写字母、小写字母和数字
    characters = string.ascii_letters + string.digits
    # 随机选择字符并拼接成字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


client = TCPClient(instance=Executor(), version="127.0.0.1", id="1", token="xxx")


async def send():
    while True:
        if client.is_running():
            await client.send_to_pipeline("test", {})
        await asyncio.sleep(5)


async def main():
    await client.execute()
    await asyncio.create_task(send())
    await asyncio.sleep(10000)


if __name__ == "__main__":
    asyncio.run(main())
