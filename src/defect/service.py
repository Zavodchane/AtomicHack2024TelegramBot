from sqlalchemy.ext.asyncio import AsyncSession

from src.defect import schemas as defect_schemas
from src.defect.models import Defect


async def create_defect(
    defect_schema: defect_schemas.Defect,
    session: AsyncSession,
) -> Defect:
    defect: Defect = Defect(**defect_schema.model_dump())
    session.add(defect)
    await session.commit()
    return defect
