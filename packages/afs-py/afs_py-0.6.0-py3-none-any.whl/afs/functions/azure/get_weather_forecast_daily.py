import json
import os
from datetime import datetime
from textwrap import dedent
from typing import Any, ClassVar, Dict, Literal, Text, cast

import requests
from json_repair import repair_json
from pydantic import Field, SecretStr
from pydantic_core import ValidationError

from afs import AfsBaseModel, AfsConfig
from afs.config import logger
from afs.utils.get import get_safe_value

AZURE_MAPS_KEY: SecretStr = SecretStr(os.environ["AZURE_MAPS_KEY"])
AZURE_WEATHER_FORECAST_DAILY_URL = (
    "https://atlas.microsoft.com/weather/forecast/daily/json"
)
AZURE_WEATHER_FORECAST_DAILY_API_VERSION = "1.1"


get_weather_forecast_daily_config = AfsConfig.model_validate(
    {
        "name": "get_weather_forecast_daily",
        "description": dedent(
            """
            The Get Daily Forecast API is an HTTP GET request that returns detailed weather forecast such as temperature and wind by day for the next 1, 5, or 10 days for a given coordinate location. The response includes details such as temperature, wind, precipitation, air quality, and UV index
            """  # noqa: E501
        ).strip(),
        "function": "afs.functions.azure.get_weather_forecast_daily:get_weather_forecast_daily",  # noqa: E501
    }
)


class GetWeatherForecastDaily(AfsBaseModel):
    # Function config
    afs_config: ClassVar[AfsConfig] = get_weather_forecast_daily_config

    # Function arguments
    query: Text = Field(
        ...,
        description=dedent(
            """
            The applicable query specified as a comma separated string composed by latitude followed by longitude e.g. "47.641268,-122.125679".
            Weather information is generally available for locations on land, bodies of water surrounded by land, and areas of the ocean that are within approximately 50 nautical miles of a coastline.
            """  # noqa: E501
        ).strip(),
    )
    duration: Literal[1, 5, 10] = Field(
        default=1,
        description=dedent(
            """
            Specifies for how many days the daily forecast responses are returned. Available values are:
            1 - Return forecast data for the next day. Returned by default.
            5 - Return forecast data for the next 5 days.
            10 - Return forecast data for the next 10 days.
            """  # noqa: E501
        ).strip(),
    )
    language: Text = Field(
        default="en",
        description=dedent(
            """
            The applicable query specified as a comma separated string composed by latitude followed by longitude e.g. "47.641268,-122.125679".
            Weather information is generally available for locations on land, bodies of water surrounded by land, and areas of the ocean that are within approximately 50 nautical miles of a coastline.
            """  # noqa: E501
        ).strip(),
    )

    @classmethod
    def parse_content(cls, response: Dict[Text, Any]) -> Text:
        if not response:
            logger.warning("Got empty function response content")
            return cls.afs_config.error_content
        if not isinstance(response, Dict):
            logger.warning(f"Invalid response type: {type(response)}")
            return cls.afs_config.error_content
        try:
            return format_weather_article(response)
        except Exception as e:
            logger.exception(e)
            return cls.afs_config.error_content

    @classmethod
    def from_args_str(cls, args_str: Text):
        func_kwargs = (
            json.loads(repair_json(args_str)) if args_str else {}  # type: ignore
        )
        if "duration" in func_kwargs:
            try:
                duration = int(func_kwargs["duration"])
            except ValidationError as e:
                logger.warning(f"Invalid duration: {func_kwargs['duration']}")
                raise e
            if duration < 1:
                duration = 1
            elif duration >= 5:
                duration = 10
            elif duration > 1:
                duration = 5
            else:
                duration = 1
            func_kwargs["duration"] = duration
        return cls.model_validate(func_kwargs)


def get_weather_forecast_daily(request: "GetWeatherForecastDaily"):
    url = AZURE_WEATHER_FORECAST_DAILY_URL
    params = request.model_dump(exclude_none=True)
    params["api-version"] = AZURE_WEATHER_FORECAST_DAILY_API_VERSION
    params["subscription-key"] = AZURE_MAPS_KEY.get_secret_value()
    response = requests.get(url, params=params)
    return response.json()


def format_weather_article(weather_data: Dict[Text, Any]) -> Text:
    article_parts = []

    # Handle summary if exists
    if "summary" in weather_data:
        summary = weather_data["summary"]
        start_date = datetime.fromisoformat(summary.get("startDate", "")).strftime(
            "%B %d"
        )
        end_date = datetime.fromisoformat(summary.get("endDate", "")).strftime("%B %d")
        article_parts.append(f"Weather Summary ({start_date} - {end_date}):")
        article_parts.append(f"{summary.get('phrase', '')}\n")

    # Process each forecast
    for forecast in weather_data.get("forecasts", []):
        forecast = cast(Dict[Text, Any], forecast)
        try:
            # Parse date
            date_str = forecast.get("date")
            if date_str:
                date = datetime.fromisoformat(date_str)
                date_formatted = date.strftime("%A, %B %d, %Y")
                article_parts.append(f"\n=== {date_formatted} ===")

            # Temperature and Real Feel
            temp = forecast.get("temperature", {})
            real_feel = forecast.get("realFeelTemperature", {})
            min_temp = get_safe_value(temp, "minimum", "value")
            max_temp = get_safe_value(temp, "maximum", "value")
            real_min = get_safe_value(real_feel, "minimum", "value")
            real_max = get_safe_value(real_feel, "maximum", "value")

            if min_temp is not None and max_temp is not None:
                article_parts.append(f"Temperature: {min_temp}°C to {max_temp}°C")
                if real_min is not None and real_max is not None:
                    article_parts.append(f"Feels like: {real_min}°C to {real_max}°C")

            # Sun and UV information
            hours_of_sun = forecast.get("hoursOfSun")
            if hours_of_sun is not None:
                article_parts.append(f"Hours of Sun: {hours_of_sun} hours")

            # Air Quality and UV Index
            air_pollen = forecast.get("airAndPollen", [])
            for item in air_pollen:
                if item.get("name") == "UVIndex":
                    article_parts.append(
                        f"UV Index: {item.get('value')} ({item.get('category', '')})"
                    )
                elif item.get("name") == "AirQuality":
                    article_parts.append(f"Air Quality: {item.get('category', '')}")

            # Day forecast
            day = forecast.get("day", {})
            if day:
                article_parts.append("\nDaytime:")
                article_parts.append(f"- Conditions: {day.get('longPhrase', '')}")

                # Precipitation details
                precip_prob = day.get("precipitationProbability")
                if precip_prob is not None:
                    article_parts.append(f"- Precipitation: {precip_prob}% chance")
                    if day.get("hasPrecipitation"):
                        rain = day.get("rain", {}).get("value")
                        if rain:
                            article_parts.append(f"- Expected rainfall: {rain}mm")

                # Wind details
                wind = day.get("wind", {})
                wind_gust = day.get("windGust", {})
                if wind:
                    direction = get_safe_value(
                        wind, "direction", "localizedDescription"
                    )
                    speed = get_safe_value(wind, "speed", "value", default=0)
                    gust_speed = get_safe_value(wind_gust, "speed", "value", default=0)
                    if direction and speed:
                        article_parts.append(f"- Wind: {direction} at {speed}km/h")
                        if gust_speed:
                            article_parts.append(f"- Wind gusts up to {gust_speed}km/h")

            # Night forecast
            night = forecast.get("night", {})
            if night:
                article_parts.append("\nNighttime:")
                article_parts.append(f"- Conditions: {night.get('longPhrase', '')}")

                # Precipitation details
                precip_prob = night.get("precipitationProbability")
                if precip_prob is not None:
                    article_parts.append(f"- Precipitation: {precip_prob}% chance")
                    if night.get("hasPrecipitation"):
                        rain = night.get("rain", {}).get("value")
                        if rain:
                            article_parts.append(f"- Expected rainfall: {rain}mm")

                # Cloud cover
                cloud_cover = night.get("cloudCover")
                if cloud_cover is not None:
                    article_parts.append(f"- Cloud cover: {cloud_cover}%")

        except Exception as e:
            logger.exception(e)
            continue  # Skip problematic forecasts

    return "\n".join(article_parts).strip()
