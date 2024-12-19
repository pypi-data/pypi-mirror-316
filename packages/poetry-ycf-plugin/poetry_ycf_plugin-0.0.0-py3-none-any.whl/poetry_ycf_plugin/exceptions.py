from collections.abc import Callable
from typing import Any

import requests

from poetry_ycf_plugin import config


class PluginException(RuntimeError):
    def __str__(self) -> str:
        message = ''

        for arg in self.args:
            if isinstance(arg, requests.exceptions.RequestException):
                if arg.response is None:
                    message += f'{type(arg).__name__} - {arg};'

                else:
                    message += f'{type(arg).__name__} - {arg} - {arg.response.text};'

            elif isinstance(arg, BaseException):
                message += f'{type(arg).__name__} - {arg}; '

            else:
                message += f'{arg}; '

        return f'<b>{config.PLUGIN_NAME}</b>: {message}'


def plugin_exception_wrapper(func: Callable[..., Any]):
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)

        except PluginException as ex:
            raise ex

        except BaseException as ex:
            raise PluginException(ex) from ex

    return wrapper
