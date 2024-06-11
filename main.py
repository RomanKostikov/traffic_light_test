from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import asyncio

app = FastAPI()


class TrafficLight(BaseModel):
    id: int
    state: str
    pedestrian_queue: int
    vehicle_queue: int


traffic_lights = []


@app.get("/trafficlights")
async def get_traffic_lights():
    return traffic_lights


@app.put("/trafficlights/{id}")
async def update_traffic_light(id: int, traffic_light: TrafficLight):
    for light in traffic_lights:
        if light.id == id:
            light.state = traffic_light.state
            light.pedestrian_queue = traffic_light.pedestrian_queue
            light.vehicle_queue = traffic_light.vehicle_queue
            return JSONResponse(content=jsonable_encoder(light))
    return JSONResponse(status_code=404, content={"message": "Traffic light not found"})


@app.put("/trafficlights/{id}/pedestrianQueue")
async def update_pedestrian_queue(id: int, size: int):
    for light in traffic_lights:
        if light.id == id:
            light.pedestrian_queue = size
            return JSONResponse(content=jsonable_encoder(light))
    return JSONResponse(status_code=404, content={"message": "Traffic light not found"})


@app.put("/trafficlights/{id}/vehicleQueue")
async def update_vehicle_queue(id: int, size: int):
    for light in traffic_lights:
        if light.id == id:
            light.vehicle_queue = size
            return JSONResponse(content=jsonable_encoder(light))
    return JSONResponse(status_code=404, content={"message": "Traffic light not found"})


@app.on_event("startup")
async def startup_event():
    # Инициализация светофоров
    traffic_lights.append(TrafficLight(id=1, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=2, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=3, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=4, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=5, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=6, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=7, state="green", pedestrian_queue=0, vehicle_queue=0))
    traffic_lights.append(TrafficLight(id=8, state="green", pedestrian_queue=0, vehicle_queue=0))

    # Запуск асинхронных задач для обработки событий светофоров
    for light in traffic_lights:
        asyncio.create_task(process_traffic_light(light))


# Если идентификатор светофора кратен 2, то это пешеходный светофор, иначе - автомобильный. В зависимости от этого,
# определяется количество времени, которое должно пройти до следующего состояния светофора.
async def process_traffic_light(traffic_light):
    while True:
        if traffic_light.state == "green" and traffic_light.id % 2 == 0:
            await asyncio.sleep(traffic_light.vehicle_queue * 10)
            await asyncio.sleep(5)
            traffic_light.state = "red"
            await asyncio.sleep(traffic_light.pedestrian_queue * 10)
        elif traffic_light.state == "green" and traffic_light.id % 2 == 1:
            await asyncio.sleep(traffic_light.pedestrian_queue * 10)
            traffic_light.state = "yellow"
            await asyncio.sleep(5)
            traffic_light.state = "red"
            await asyncio.sleep(traffic_light.vehicle_queue * 10)
        elif traffic_light.state == "yellow":
            await asyncio.sleep(5)
            traffic_light.state = "red"
        elif traffic_light.state == "red":
            if traffic_light.id % 2 == 0:
                await asyncio.sleep(traffic_light.pedestrian_queue * 10)
                traffic_light.state = "green"
            elif traffic_light.id % 2 == 1:
                await asyncio.sleep(traffic_light.vehicle_queue * 10)
                traffic_light.state = "green"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
