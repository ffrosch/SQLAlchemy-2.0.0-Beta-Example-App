# flake8: noqa
# mypy: disable-error-code=import
import sqlalchemy

# Monkey-Patch version "2.0.0b3" to avoid sqlalchemy_utils init-error
sqlalchemy.__version__ = "2.0.0"

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    Session,
    column_property,
    mapped_column,
    relationship,
)
from sqlalchemy_utils import create_database, database_exists, drop_database

engine = create_engine("sqlite+pysqlite:///test.db", echo=True)


class Base(MappedAsDataclass, DeclarativeBase):
    """Model base class."""


class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = column_property(
        firstname + " " + lastname,  # type: ignore[operator]
        init=False,
    )

    addresses: Mapped[List["Address"]] = relationship(
        default_factory=list, back_populates="user"
    )
    timestamp = mapped_column(DateTime, nullable=False)

    __mapper_args__ = {
        "version_id_col": timestamp,
        "version_id_generator": lambda v: datetime.now(),
    }


class Address(Base):

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    email_address: Mapped[str] = mapped_column(String)
    address_statistics: Mapped[Optional[str]] = mapped_column(
        Text,
        deferred=True,
        init=False,
    )

    user: Mapped["User"] = relationship(back_populates="addresses")


def create():
    db_url = engine.url
    if database_exists(db_url):
        drop_database((db_url))

    create_database(db_url)
    Base.metadata.create_all(engine)


def test():
    with Session(engine) as session:
        u = User(firstname="Peter", lastname="Mustermann")
        a = Address(user=u, email_address="peter@example.com")
        session.add(u)
        session.commit()

        result = session.execute(select(User))

        print(result.all())
        print("User.timestamp:", u.timestamp)


def destroy():
    drop_database((engine.url))


if __name__ == "__main__":
    """Demonstrate that this is a working example.

    python app.py
    """
    create()
    test()
    destroy()
