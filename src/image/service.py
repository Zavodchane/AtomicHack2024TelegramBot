from sqlalchemy.ext.asyncio import AsyncSession

from src.image import schemas as image_schemas
from src.image.models import Image


async def create_image(
    image_schema: image_schemas.Image,
    session: AsyncSession,
) -> Image:
    image: Image = Image(**image_schema.model_dump())
    session.add(image)
    await session.commit()
    return image
