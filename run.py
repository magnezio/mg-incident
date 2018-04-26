import click

from mg_incident import create_app

app = create_app()


@app.cli.command()
def insert_predefined_roles_for_users():
    from mg_incident.account.models import AppRole
    from mg_incident import db

    user = AppRole(name='user',
                   description='Can set status only for his ticket.',
                   predefined=True)

    worker = AppRole(name='worker',
                     description='Can set status only for tickets assigned to it.',
                     predefined=True)

    manager = AppRole(name='manager',
                      description='Can set status for all type of tickets.',
                      predefined=True)

    admin = AppRole(name='admin',
                    description='Full access.',
                    predefined=True)

    roles = [user, worker, manager, admin]

    report = []
    with app.app_context():
        for r in roles:
            _r = AppRole.query.filter(AppRole.name == r.name).first()
            if not _r:
                db.session.add(r)
                report.append(r.name)
        db.session.commit()

    click.echo('Insert roles: ' + str(report))

# FLASK_APP=run.py flask run
