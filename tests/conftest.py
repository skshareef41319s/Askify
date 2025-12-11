import sys
import os
import pytest
import asyncio

askify_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, askify_dir)
sys.path.insert(0, os.path.dirname(askify_dir))

pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
