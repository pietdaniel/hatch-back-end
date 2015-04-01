# Hatch Alembic Migrations

Hatch uses [Alembic](https://alembic.readthedocs.org/en/latest/) to manage
changes to the database schema.

When you make _any_ changes to the model, you must add an associated migration
script to the `migrations/versions/` directory.

## Creating New Migration Script

*this has been adapted from the
[Alembic docs](http://alembic.readthedocs.org/en/latest/tutorial.html)*

Lets say you want to add a new table "foo". The first step is to run:

`python manage.py db revision --message "create foo table"`

This will generate an empty revision script in `migrations/versions/`. You need
to edit this script in a few places to create the migration.

First, set the `down_revision` variable to the revision identifier of the
previous migration. This is so Alembic knows which order to apply the
migrations; the next migration script's `down_revision` would be set to the
revision id of this one.

Next, you'll need to fill in the `upgrade()` and `downgrade()` functions. In
our example of adding a "foo" table, this would look something like:

```python
def upgrade():
    op.create_table(
        'foo',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('bar', sa.String(42), nullable=False),
    )

def downgrade():
    op.drop_table('foo')
```

`create_table()` and `drop_table()` are Alembic functions. Alembic provides all
the basic database migration operations via these directives, which are designed
to be as simple and minimalistic as possible; there’s no reliance upon existing
table metadata for most of these directives.

A full list of provided functions is available
[here](http://alembic.readthedocs.org/en/latest/ops.html#ops)
