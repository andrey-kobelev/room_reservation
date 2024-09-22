"""rename MeetingRom to MeetingRoomModel

Revision ID: e396934a519e
Revises: c95f8289bb3d
Create Date: 2024-09-10 17:57:42.400218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e396934a519e'
down_revision = 'c95f8289bb3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table(old_table_name='meetingroom', new_table_name='meetingroommodel')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table(old_table_name='meetingroommodel', new_table_name='meetingroom')
    # ### end Alembic commands ###