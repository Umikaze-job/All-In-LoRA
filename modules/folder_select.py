from fastapi import FastAPI, Request
import asyncio

class Folder_Select:
    async def Folder_Select_Create(request: Request):
        await asyncio.sleep(1)
        return {"message": "Hello World!!"}