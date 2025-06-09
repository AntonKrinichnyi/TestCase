from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (Integer,
                        DateTime,
                        String,
                        func)

from database.sqlite import Base


class CarInfoModel(Base):
    __tablename__ = "carinfo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    price_usd: Mapped[int] = mapped_column(Integer, nullable=False)
    odometer: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(127), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    image_count: Mapped[int] = mapped_column(Integer, nullable=False)
    car_number: Mapped[str] = mapped_column(String(10), nullable=True)
    car_vin: Mapped[str] = mapped_column(String(50), nullable=False)
    datetime_found: Mapped[datetime] = mapped_column(DateTime,
                                                     server_default=func.now(),
                                                     nullable=False)
