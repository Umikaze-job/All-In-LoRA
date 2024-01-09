import os
from fastapi import Request

class App_Init:    
    @staticmethod
    async def Get_init_Data():
        return {"canLora":False}