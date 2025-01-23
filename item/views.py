from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from item.schemas import Item
from item import crud as item