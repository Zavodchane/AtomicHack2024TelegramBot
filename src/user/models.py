from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.image.models import Image


class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(primary_key=True)

    images: Mapped[list["Image"]] = relationship(back_populates="user")
