import click

from mg_incident import create_app


app = create_app()


@app.cli.command()
def insert_predefined_roles_for_users():
    from mg_incident.models.account import AppRole
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


# def insert_predefined_ticket_statuses():
#     from mg_incident.ticket.models import Status
#     from mg_incident import db

#     new = Status(name='New', description='As soon as a customer opens a ticket, it has a status of New.',
#                  predefined=True)

#     in_progress = Status(name='In Progress',
#                          description='After a ticket is reviewed by support team, it moves to the In Progress status.',
#                          predefined=True)

#     pending_customer = Status(name='Pending Customer',
#                               description='If the support team needs more information from the customer to fix the issue, the ticket might move to the Pending Customer status.',
#                               predefined=True)

#     pending_vendor = Status(name='Pending Vendor',
#                             description='If the ticket is waiting for an update or release from a vendor, the ticket might move to the Pending Vendor status.',
#                             predefined=True)

#     pending_maintenance = Status(name='Pending Maintenance',
#                                  description='If the ticket is waiting for a maintenance window and is not being actively worked, the ticket might move to the Pending Maintenance status.',
#                                  predefined=True)

#     transferred = Status(name='Transferred',
#                          description='If a ticket moves to another member of the support team, it has a status of Transferred.',
#                          predefined=True)

#     solved = Status(name='Solved', description='When support team solved the issue, the status is changed to Solved.',
#                     predefined=True)

#     closed = Status(name='Closed',
#                     description='After a ticket has a status of Solved, a customer can move the ticket to Closed',
#                     predefined=True)

#     statuses = [new, in_progress, pending_customer, pending_vendor, pending_maintenance, transferred, solved, closed]

#     report = []
#     with app.app_context():
#         for s in statuses:
#             _s = Status.query.filter(Status.name == s.name).first()
#             if not _s:
#                 db.session.add(s)
#                 report.append(s.name)
#         db.session.commit()

#     click.echo('Insert statuses: ' + str(report))

    # FLASK_APP=run.py flask run
 