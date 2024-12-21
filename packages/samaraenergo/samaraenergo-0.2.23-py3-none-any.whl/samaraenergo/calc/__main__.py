import asyncio
import datetime as dt
import logging

from . import CityConfig, HeatingType, OnlineCalculator, StoveType, Tariff

logging.basicConfig(level=logging.DEBUG)


async def main():
    config = CityConfig(
        tariff=Tariff.TWO,
        heating=HeatingType.CENTRAL,
        stove=StoveType.GAS,
    )

    print(f"Config: {config}")
    print(f"Config as string: {config.asstring}")

    async with OnlineCalculator(config) as calc:
        print(await calc.get_zones_cost(date=dt.date(2024, 1, 1)))

    async with OnlineCalculator.from_string(config.asstring) as calc:
        print(await calc.get_zones_cost(date=dt.date(2024, 7, 1)))


asyncio.run(main())
