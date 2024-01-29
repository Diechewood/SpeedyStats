# SpeedDataCollectionController.py
from aiohttp import web
from Services.SpeedDataManagerService import SpeedDataManagerService
import asyncio
import json
import datetime

data_manager = SpeedDataManagerService()

async def record_speed(request):
    data = await request.json()
    user_id = data.get('user_id')
    speed = data.get('speed')
    timestamp = datetime.datetime.now()
    location = data.get('location')

    await asyncio.create_task(data_manager.record_speed_data(user_id, speed, timestamp, location))
    return web.Response(text=json.dumps({"message": "Speed data recorded successfully"}), status=200)

app = web.Application()
app.router.add_post('/record_speed', record_speed)

if __name__ == '__main__':
    web.run_app(app)

