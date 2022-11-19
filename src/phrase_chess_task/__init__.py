"""
Define here top level singletons, e.g. logging
"""

import logging

logging.basicConfig(
    format="%(process)d.%(thread)d %(name)s in %(funcName)s at %(filename)s:%(lineno)d %(levelname)s: %(message)s",
    level=logging.INFO,
)
