"""empty message

Revision ID: bd90541825a7
Revises: 97d71ccd951a
Create Date: 2024-03-27 16:59:25.877948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd90541825a7'
down_revision: Union[str, None] = '97d71ccd951a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('translation_wordname_translation_ukey', 'translation', ['wordname', 'translation'], schema='words')
    # op.drop_constraint('translation_wordname_fkey', 'translation', type_='foreignkey')
    # op.create_foreign_key(None, 'translation', 'words', ['wordname'], ['word'], source_schema='words', referent_schema='words', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('translation_wordname_translation_ukey', 'translation', schema='words', type_='foreignkey')
    # op.create_foreign_key('translation_wordname_fkey', 'translation', 'words', ['wordname'], ['word'], ondelete='CASCADE')
    # op.drop_constraint(None, 'translation', schema='words', type_='unique')
    # ### end Alembic commands ###