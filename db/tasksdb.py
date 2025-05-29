import motor.motor_asyncio
from beanie import init_beanie
from db.task_model import Task
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_APP = os.environ.get("MONGO_APP")

MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER}.mongodb.net/{MONGO_DB}"
    f"?retryWrites=true&w=majority&appName={MONGO_APP}"
)

class TasksDB:
    @staticmethod
    async def init_db():
        client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get(MONGO_URI))
        await init_beanie(database=client.discord, document_models=[Task])
        
    @staticmethod
    async def insert_task(task: Task):
        await task.insert()