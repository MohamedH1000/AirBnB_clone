#!/usr/bin/python3
"""
module in models to be initialized
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()