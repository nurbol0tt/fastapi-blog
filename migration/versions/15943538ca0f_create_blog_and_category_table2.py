"""create blog and category table2

Revision ID: 15943538ca0f
Revises: 699c7e0986d7
Create Date: 2023-08-10 23:22:04.009219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import FetchedValue

# revision identifiers, used by Alembic.
revision = '15943538ca0f'
down_revision = '699c7e0986d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('title', sa.String(length=55), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=FetchedValue(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=FetchedValue(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_title'), 'categories', ['title'], unique=False)
    op.create_table('blogs',
    sa.Column('phone', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('user', sa.String(length=255), nullable=False),
    sa.Column('fio', sa.String(length=255), nullable=False),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=FetchedValue(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=FetchedValue(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_blogs_email'), 'blogs', ['email'], unique=False)
    op.create_index(op.f('ix_blogs_fio'), 'blogs', ['fio'], unique=False)
    op.create_index(op.f('ix_blogs_id'), 'blogs', ['id'], unique=False)
    op.create_index(op.f('ix_blogs_phone'), 'blogs', ['phone'], unique=False)
    op.create_index(op.f('ix_blogs_user'), 'blogs', ['user'], unique=False)
    op.create_table('blog_category_association',
    sa.Column('blog_id', sa.UUID(), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_category_association')
    op.drop_index(op.f('ix_blogs_user'), table_name='blogs')
    op.drop_index(op.f('ix_blogs_phone'), table_name='blogs')
    op.drop_index(op.f('ix_blogs_id'), table_name='blogs')
    op.drop_index(op.f('ix_blogs_fio'), table_name='blogs')
    op.drop_index(op.f('ix_blogs_email'), table_name='blogs')
    op.drop_table('blogs')
    op.drop_index(op.f('ix_categories_title'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
