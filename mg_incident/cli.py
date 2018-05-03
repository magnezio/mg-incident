import click
from mg_incident import create_app, db


app = create_app()
app.config['SQLALCHEMY_ECHO'] = False


@app.cli.command()
def insert_roles():
    from mg_incident.models.account import AppRole

    roles = [
        ('user', 'Can set status only for his ticket.'),
        ('worker', 'Can set status only for tickets assigned to it.'),
        ('manager', 'Can set status for all type of tickets.'),
        ('admin', 'Full access.'),
    ]
    names = [r[0] for r in roles]
    exists_roles = AppRole.query.filter(AppRole.name.in_(names)).all()
    exists_names = [r.name for r in exists_roles]
    processed = []
    for r in roles:
        if not r[0] in exists_names:
            role = AppRole(name=r[0], description=r[1], is_predefined=False)
            db.session.add(role)
            processed.append(role)
    try:
        db.session.commit()
        click.echo('Inserted roles: ' + str(processed))
    except:
        click.echo('Commit Failed')
