import sys
import time
import asyncio
import requests
import traceback


class WebhookApiHandler:
    ENDPOINT = 'https://webhook.site/6f7c6822-4237-4e18-899b-87aaedf728a3'

    @classmethod
    def post_payload(cls, payload: dict) -> requests.Response:
        try:
            return requests.post(cls.ENDPOINT, json=payload)
        except Exception:
            exec_info = traceback.format_exception(*sys.exc_info())
            print(exec_info)


class DweetApiHandler:
    ENDPOINT = 'https://dweet.io'

    @classmethod
    def get_latest_dweet(cls, thing: str = 'thecore') -> dict:
        try:
            dweet = requests.get(f'{cls.ENDPOINT}/get/latest/dweet/for/{thing}').json()
            return dweet
        except Exception:
            exec_info = traceback.format_exception(*sys.exc_info())
            print(exec_info)

    @staticmethod
    def deserialize_dweet(dweet: dict):
        try:
            return dweet.get('with')[0].get('content')
        except Exception:
            exec_info = traceback.format_exception(*sys.exc_info())
            print(exec_info)
            return {}


class StorageHandler:

    @classmethod
    def save_dweet(cls, dweet: dict):
        with open('db.txt', 'a') as db:
            db.write(f"temp={dweet.get('temperature')} humidity={dweet.get('humidity')} \n")

    @classmethod
    def get_dweets(cls):
        return "Placeholder"


class TaskScheduler:

    @staticmethod
    async def repeat_with_timeout(timeout: int, callback, *args):
        while True:
            start_time = time.perf_counter()
            callback(*args)
            end_time = time.perf_counter()
            corrected_timeout = timeout-(end_time-start_time)
            await asyncio.sleep(corrected_timeout if corrected_timeout > 0 else 0)

    @staticmethod
    async def schedule_task(timeout: int, coro, ending_callback=None):
        try:
            await asyncio.wait_for(coro, timeout)
        except asyncio.TimeoutError:
            if ending_callback:
                ending_callback()
            print(f"Task done in {timeout}s")


def fetch_and_save_dweet():
    dweet = DweetApiHandler.deserialize_dweet(
        DweetApiHandler.get_latest_dweet()
    )
    StorageHandler.save_dweet(dweet)


def post_dweets():
    print(WebhookApiHandler.post_payload(
        {'data': StorageHandler.get_dweets()}
    ))


async def main():
    await TaskScheduler.schedule_task(
        30,
        TaskScheduler.repeat_with_timeout(5, fetch_and_save_dweet),
        post_dweets
    )


if __name__ == "__main__":
    asyncio.run(main())
