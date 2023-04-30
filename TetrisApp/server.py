from fastapi import FastAPI
import threading
import uvicorn


class Server:

    def __init__(self, runTetrisParent):
        self.runParent = runTetrisParent
        self.app = FastAPI()

    def createServer(self):
        @self.app.get("/")
        async def createUser(data):
            self.runParent.userSignal.emit(data)
            return {"message": "Hello World"}

        thread = threading.Thread(target=uvicorn.run,
                                  kwargs={"app": self.app,
                                          "port": 8000})
        thread.start()
