from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.image.models import Image


class Defect(Base):
    __tablename__ = "defect"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    rel_x: Mapped[float] = mapped_column(nullable=False)
    rel_y: Mapped[float] = mapped_column(nullable=False)
    width: Mapped[float] = mapped_column(nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)

    image_id: Mapped[UUID] = mapped_column(ForeignKey("image.id"))
    image: Mapped["Image"] = relationship(back_populates="defects")
