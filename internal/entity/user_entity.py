import sqlalchemy as sa

from internal.entity.mixin import TimestampMixin

from internal.entity.base import Base


class User(TimestampMixin, Base):
    __tablename__ = 'users'  # noqa

    __table_args__ = (
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )

    username = sa.Column(sa.String(255), index=True, nullable=False)
    email = sa.Column(sa.String(255), index=True, nullable=False)
    hashed_password = sa.Column(sa.String(255), nullable=False)
    is_active = sa.Column(sa.Boolean(), default=True)
