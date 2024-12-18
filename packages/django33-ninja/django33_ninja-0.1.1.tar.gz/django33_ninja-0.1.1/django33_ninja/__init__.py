"""Django Ninja - Fast Django REST framework"""

__version__ = "1.3.0"


from pydantic import Field

from django33_ninja.files import UploadedFile
from django33_ninja.filter_schema import FilterSchema
from django33_ninja.main import NinjaAPI
from django33_ninja.openapi.docs import Redoc, Swagger
from django33_ninja.orm import ModelSchema
from django33_ninja.params import (
    Body,
    BodyEx,
    Cookie,
    CookieEx,
    File,
    FileEx,
    Form,
    FormEx,
    Header,
    HeaderEx,
    P,
    Path,
    PathEx,
    Query,
    QueryEx,
)
from django33_ninja.patch_dict import PatchDict
from django33_ninja.router import Router
from django33_ninja.schema import Schema

__all__ = [
    "Field",
    "UploadedFile",
    "NinjaAPI",
    "Body",
    "Cookie",
    "File",
    "Form",
    "Header",
    "Path",
    "Query",
    "BodyEx",
    "CookieEx",
    "FileEx",
    "FormEx",
    "HeaderEx",
    "PathEx",
    "QueryEx",
    "Router",
    "P",
    "Schema",
    "ModelSchema",
    "FilterSchema",
    "Swagger",
    "Redoc",
    "PatchDict",
]
