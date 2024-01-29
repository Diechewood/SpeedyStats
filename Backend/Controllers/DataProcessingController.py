# DataProcessingController.py
from aiohttp import web
from Services.DataProcessingService import DataProcessingService
import asyncio
import json

processing_service = DataProcessingService()

async def process_data(request):
    user_id = request.match_info.get('user_id')
    await asyncio.create_task(processing_service.process_user_data(user_id))
    return web.Response(text=json.dumps({"message": "Data processing completed successfully"}), status=200)

app = web.Application()
app.router.add_get('/process_data/{user_id}', process_data)

if __name__ == '__main__':
    web.run_app(app)
