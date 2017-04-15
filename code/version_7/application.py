"""
This module exists to just multiple modules a chance to
import and use the app instance
"""

from flask import (
    Flask
)

# create the application instance
app = Flask(__name__,
            template_folder="templates")