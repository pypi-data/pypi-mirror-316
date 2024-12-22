import json
import textwrap
import typing

import httpx
import pydantic
import pydantic_core

from afs import AfsBaseModel, AfsConfig
from afs.config import logger

type CurrencySymbol = typing.Literal[
    "AUD",
    "BGN",
    "BRL",
    "CAD",
    "CHF",
    "CNY",
    "CZK",
    "DKK",
    "EUR",
    "GBP",
    "HKD",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JPY",
    "KRW",
    "MXN",
    "MYR",
    "NOK",
    "NZD",
    "PHP",
    "PLN",
    "RON",
    "SEK",
    "SGD",
    "THB",
    "TRY",
    "USD",
    "ZAR",
]
currency_symbols_to_names: typing.Dict[CurrencySymbol, typing.Text] = {
    "AUD": "Australian Dollar",
    "BGN": "Bulgarian Lev",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Renminbi Yuan",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "EUR": "Euro",
    "GBP": "British Pound",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Sheqel",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Króna",
    "JPY": "Japanese Yen",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PHP": "Philippine Peso",
    "PLN": "Polish Złoty",
    "RON": "Romanian Leu",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "USD": "United States Dollar",
    "ZAR": "South African Rand",
}

GET_CURRENCIES_CONFIG = AfsConfig.model_validate(
    {
        "name": "get_currencies",
        "description": textwrap.dedent(
            """
            This function retrieves a list of supported currencies, including their symbols and full names. It provides standardized currency information for applications requiring financial data or currency conversions.
            """  # noqa: E501
        ).strip(),
        "function": "afs.functions.assorted.currencies:get_currencies",  # noqa: E501
    }
)


async def get_currencies(request: "GetCurrencies") -> "GetCurrenciesResponse":
    url = httpx.URL("https://api.frankfurter.dev/v1/latest")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, params=json.loads(request.model_dump_json(exclude_none=True))
        )
        try:
            return GetCurrenciesResponse.model_validate(response.json())
        except pydantic_core.ValidationError as e:
            logger.error(
                f"Can not cast response to GetCurrenciesResponse: {response.json()}",
            )
            raise e


class GetCurrencies(AfsBaseModel):
    # Function metadata
    afs_config = GET_CURRENCIES_CONFIG
    # Function arguments
    base: CurrencySymbol = pydantic.Field(
        default="USD", description="The base currency to convert from"
    )
    symbols: typing.Optional[typing.List[CurrencySymbol]] = pydantic.Field(
        default=None, description="The currencies to convert to"
    )

    @classmethod
    def parse_content(cls, response: "GetCurrenciesResponse") -> typing.Text:
        if not response:
            logger.warning("Got empty function response content")
            return cls.afs_config.error_content
        if not isinstance(response, GetCurrenciesResponse):
            logger.warning(f"Invalid response type: {type(response)}")
            return cls.afs_config.error_content
        try:
            formatted_rates = "\n".join(
                [f"{symbol}: {rate}" for symbol, rate in response.rates.items()]
            )
            return (
                f"The base currency is {response.base} on {response.date}. "
                f"Exchange rates:\n{formatted_rates}"
            )
        except Exception as e:
            logger.exception(e)
            return cls.afs_config.error_content


class GetCurrenciesResponse(pydantic.BaseModel):
    amount: float = pydantic.Field(
        ..., description="The amount of the base currency used for the conversion."
    )
    base: CurrencySymbol = pydantic.Field(
        ..., description="The base currency symbol from which conversions are made."
    )
    date: typing.Text = pydantic.Field(
        ..., description="The date of the currency rates."
    )
    rates: typing.Dict[CurrencySymbol, float] = pydantic.Field(
        ...,
        description="A dictionary mapping currency symbols to their exchange rates relative to the base currency.",  # noqa: E501
    )
