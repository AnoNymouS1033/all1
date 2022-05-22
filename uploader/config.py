import os
import asyncio
from collections import defaultdict


class Config:
    ACTIVE_DOWNLOADS = []
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    AUTH_USERS =  [int(i) for i in os.environ.get("AUTH_USERS", "").split(" ")]
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DB_CHANNEL_ID = -1001482542607
    PROCESS_MAX_TIMEOUT = 3600
    RESTART_TIME = []
    TG_MAX_FILE_SIZE = 2097000000
    TIME_GAP1 = {}
    TIME_GAP2 = {}
    timegap_message = {}
    TRACE_CHANNEL = -1001482542607
    last_edit = defaultdict(lambda: 0)

    # QUEUE
    WORKERS = 5
    QUEUE_MAXSIZE = 20
    normal_queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)
    queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)
    normal_tasks = []
    tasks = []
    user = []
    Library = ['aria2', 'aiohttp']
    Extension = ['mp4', 'webm', 'mkv', 'all']
