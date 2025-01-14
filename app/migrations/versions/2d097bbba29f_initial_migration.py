"""Initial migration

<<<<<<<< HEAD:app/migrations/versions/2d097bbba29f_initial_migration.py
Revision ID: 2d097bbba29f
Revises: 
Create Date: 2025-01-13 18:14:48.305369
========
Revision ID: 50e6c1d4ab9d
Revises: 
Create Date: 2025-01-13 16:16:46.723526
>>>>>>>> 0012c0f391b8e15167aab5e9fba4060276a181e9:app/migrations/versions/50e6c1d4ab9d_initial_migration.py

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
<<<<<<<< HEAD:app/migrations/versions/2d097bbba29f_initial_migration.py
revision = '2d097bbba29f'
========
revision = '50e6c1d4ab9d'
>>>>>>>> 0012c0f391b8e15167aab5e9fba4060276a181e9:app/migrations/versions/50e6c1d4ab9d_initial_migration.py
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=155), nullable=False),
    sa.Column('slug', sa.String(length=155), nullable=False),
    sa.Column('permission_group', sa.String(length=155), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('slug', sa.String(length=150), nullable=False),
    sa.Column('secondary', sa.Boolean(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('userType', sa.String(length=155), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('role_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstName', sa.String(length=80), nullable=False),
    sa.Column('lastName', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('countryCode', sa.String(length=120), nullable=False),
    sa.Column('mobileNo', sa.BigInteger(), nullable=False),
    sa.Column('empID', sa.String(length=120), nullable=False),
    sa.Column('userType', sa.String(length=120), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deletedAt', sa.DateTime(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('empID'),
    sa.UniqueConstraint('mobileNo')
    )
    op.create_table('biddings',
    sa.Column('bidId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('projectName', sa.String(length=80), nullable=False),
    sa.Column('projectDescription', sa.String(length=300), nullable=True),
    sa.Column('currency', sa.String(length=80), nullable=True),
    sa.Column('bidAmount', sa.Integer(), nullable=True),
    sa.Column('platform', sa.String(length=80), nullable=False),
    sa.Column('bidDate', sa.Date(), nullable=False),
    sa.Column('status', sa.String(length=120), nullable=False),
    sa.Column('clientName', sa.String(length=80), nullable=False),
    sa.Column('clientEmail', sa.String(length=120), nullable=False),
    sa.Column('countryCode', sa.String(length=120), nullable=False),
    sa.Column('clientContact', sa.BigInteger(), nullable=False),
    sa.Column('clientCompany', sa.String(length=120), nullable=True),
    sa.Column('clientLocation', sa.String(length=120), nullable=True),
    sa.Column('remarks', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('projectId', sa.Integer(), nullable=True),
    sa.Column('commission', sa.Boolean(), nullable=False),
    sa.Column('approvedBy', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['approvedBy'], ['users.id'], ),
    sa.ForeignKeyConstraint(['projectId'], ['projects.projectId'], use_alter=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('bidId'),
    sa.UniqueConstraint('projectName')
    )
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity', sa.String(length=50), nullable=False),
    sa.Column('desc', sa.String(length=250), nullable=True),
    sa.Column('ipAddress', sa.String(length=80), nullable=True),
    sa.Column('userAgent', sa.String(length=250), nullable=True),
    sa.Column('device', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('module', sa.String(length=255), nullable=False),
    sa.Column('seen', sa.Boolean(), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('read_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tokens',
    sa.Column('tokenId', sa.Integer(), nullable=False),
    sa.Column('accessToken', sa.String(length=250), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expiryAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tokenId')
    )
    op.create_table('projects',
    sa.Column('projectId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('currency', sa.String(length=80), nullable=True),
    sa.Column('totalBudget', sa.Integer(), nullable=True),
    sa.Column('startDate', sa.Date(), nullable=True),
    sa.Column('deadlineDate', sa.Date(), nullable=True),
    sa.Column('endDate', sa.Date(), nullable=True),
    sa.Column('status', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('techLeadId', sa.Integer(), nullable=False),
    sa.Column('assignedById', sa.Integer(), nullable=False),
    sa.Column('bidId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignedById'], ['users.id'], ),
    sa.ForeignKeyConstraint(['bidId'], ['biddings.bidId'], ),
    sa.ForeignKeyConstraint(['techLeadId'], ['users.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('projectId')
    )
    op.create_table('assignments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('projectId', sa.Integer(), nullable=False),
    sa.Column('developerId', sa.Integer(), nullable=False),
    sa.Column('testerId', sa.Integer(), nullable=True),
    sa.Column('assignedById', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignedById'], ['users.id'], ),
    sa.ForeignKeyConstraint(['developerId'], ['users.id'], ),
    sa.ForeignKeyConstraint(['projectId'], ['projects.projectId'], ),
    sa.ForeignKeyConstraint(['testerId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_developers',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('developer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['developer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.projectId'], ),
    sa.PrimaryKeyConstraint('project_id', 'developer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_developers')
    op.drop_table('assignments')
    op.drop_table('projects')
    op.drop_table('tokens')
    op.drop_table('notifications')
    op.drop_table('logs')
    op.drop_table('biddings')
    op.drop_table('users')
    op.drop_table('role_permissions')
    op.drop_table('roles')
    op.drop_table('permissions')
    # ### end Alembic commands ###
