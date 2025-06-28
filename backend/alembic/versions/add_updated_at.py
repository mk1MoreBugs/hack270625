"""add updated_at column

Revision ID: add_updated_at
Revises: 
Create Date: 2024-03-17 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'add_updated_at'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add updated_at column to all tables that inherit from TimestampedModel
    tables = [
        'users', 'developers', 'projects', 'buildings', 'apartments',
        'price_history', 'views_log', 'bookings', 'promotions',
        'webhook_inbox', 'dynamic_pricing_config'
    ]
    
    for table in tables:
        op.add_column(
            table,
            sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()'))
        )


def downgrade() -> None:
    # Remove updated_at column from all tables
    tables = [
        'users', 'developers', 'projects', 'buildings', 'apartments',
        'price_history', 'views_log', 'bookings', 'promotions',
        'webhook_inbox', 'dynamic_pricing_config'
    ]
    
    for table in tables:
        op.drop_column(table, 'updated_at') 