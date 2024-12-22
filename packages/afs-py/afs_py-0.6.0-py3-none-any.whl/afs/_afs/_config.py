from textwrap import dedent
from typing import Any, Callable, Coroutine, ParamSpec, Text, TypeVar

from pydantic import BaseModel, Field

R = TypeVar("R")
P = ParamSpec("P")


FunctionType = Callable[P, R]  # Regular function type
CoroutineType = Callable[P, Coroutine[Any, Any, R]]  # Coroutine function type


class AfsConfig(BaseModel):
    """
    A configuration class for Aiello-Functions (AFS) that defines function metadata and validation rules.

    This class serves as the core configuration component for AFS function tools, providing
    essential metadata such as function name, description, and path. It inherits from Pydantic's
    BaseModel to ensure type safety and validation.

    Notes
    -----
    The configuration requires three mandatory fields:
    - name: A function identifier that must match the pattern ^[a-zA-Z0-9_-]*$
    - description: A detailed explanation of the function's purpose
    - function: The import path to the callable function

    The class also provides validation methods to ensure configuration integrity and a method
    to import the configured function.

    Examples
    --------
    >>> config = AfsConfig(
    ...     name="get_weather",
    ...     description="Retrieves weather information for a location",
    ...     function="weather_module.get_weather"
    ... )
    >>> config.is_valid()
    True
    >>> func = config.get_function()
    """  # noqa: E501

    name: Text = Field(
        ...,
        description="The name of the function.",
        pattern=r"^[a-zA-Z0-9_-]*$",
    )
    description: Text = Field(
        ...,
        description="A description of the function.",
    )
    function: Text = Field(
        ...,
        description="The path of the callable function.",
    )
    error_content: Text = Field(
        default=dedent(
            """
            The service is currently unavailable. Please try again later.
            """
        ).strip(),
        description="The content of the error message.",
    )

    @classmethod
    def is_config_valid(cls, config: "AfsConfig") -> bool:
        """
        Validate the configuration by attempting to import the specified function.

        A configuration is considered valid if the function path can be successfully
        imported. Any import errors are logged and result in validation failure.

        Notes
        -----
        This method performs dynamic imports and should be used with trusted
        function paths only.

        Examples
        --------
        >>> config = AfsConfig(name="test_func", description="Test",
        ...                   function="module.path.func")
        >>> AfsConfig.is_config_valid(config)
        True
        """

        from afs.config import logger
        from afs.utils.import_ import import_function

        try:
            import_function(config.function)
            return True
        except Exception as e:
            logger.error(f"Invalid configuration of {config}: {e}")
        return False

    def is_valid(self) -> bool:
        """
        Check if the current configuration instance is valid.

        This is a convenience wrapper around is_config_valid() that passes
        the current instance as the configuration to validate.
        """

        return self.is_config_valid(self)

    def raise_if_invalid(self) -> None:
        """
        Validate the configuration and raise an exception if invalid.

        Raises
        ------
        ValueError
            If the configuration is invalid, with details about the invalid config.
        """

        if not self.is_valid():
            raise ValueError(f"Invalid configuration: {self}")

    def get_function(self) -> FunctionType | CoroutineType:
        """
        Import and return the configured function.

        Returns a callable that may be either a regular function or a coroutine,
        as specified by the function path in the configuration.

        Notes
        -----
        This method performs dynamic imports and should be used with trusted
        function paths only. The imported function is not cached.
        """

        from afs.utils.import_ import import_function

        return import_function(self.function)
