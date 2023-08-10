import sqlalchemy as sa
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from internal.entity.mixin import TimestampMixin

from internal.entity.base import Base


blogs_category_association = Table(
    'blog_category_association',
    Base.metadata,
    sa.Column('blog_id', sa.UUID, sa.ForeignKey('blogs.id')),
    sa.Column('category_id', sa.UUID, sa.ForeignKey('categories.id'))
)


class Category(TimestampMixin, Base):
    __tablename__ = 'categories' # noqa

    title = sa.Column(sa.String(55), index=True)

    blogs = relationship(
        'Blog',
        secondary=blogs_category_association,
        back_populates='categories'
    )


class Blog(TimestampMixin, Base):
    __tablename__ = 'blogs'  # noqa

    __table_args__ = (
        sa.UniqueConstraint('phone'),
        sa.UniqueConstraint('email'),
    )

    phone = sa.Column(sa.String(255), index=True, nullable=False)
    email = sa.Column(sa.String(255), index=True, nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    user = sa.Column(sa.String(255), index=True, nullable=False)
    fio = sa.Column(sa.String(255), index=True, nullable=False)
    category_id = sa.Column(
        sa.UUID,
        sa.ForeignKey('categories.id', ondelete="NO ACTION")
    )

    categories = relationship(
        'Category',
        secondary=blogs_category_association,
        back_populates='blogs'
    )
