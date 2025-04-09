<%!
    import datetime
%>
"""${message}

Revision ID: ${up_revision}
Revises: ${repr(down_revision)}
Create Date: ${create_date if create_date else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

# revision identifiers, used by Alembic.
revision = '${up_revision}'
down_revision = ${repr(down_revision)}
branch_labels = None
depends_on = None

def upgrade():
    ${upgrades if upgrades else "pass"}

def downgrade():
    ${downgrades if downgrades else "pass"}
