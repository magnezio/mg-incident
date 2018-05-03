import click
from mg_incident import create_app, db

app = create_app()
app.config['SQLALCHEMY_ECHO'] = False


@app.cli.command()
def insert_roles():
    from mg_incident.models import AppRole

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
            role = AppRole(name=r[0], description=r[1], is_predefined=True)
            db.session.add(role)
            processed.append(role)
    try:
        db.session.commit()
        click.echo('Inserted roles: ' + str(processed))
    except:
        click.echo('Commit Failed')


@app.cli.command()
def insert_tickets_statuses():
    from mg_incident.models import TicketStatus

    tickets_statuses = [
        ('New', 'As soon as a customer opens a ticket, it has a status of New.'),
        ('In Progress', 'After a ticket is reviewed by support team, it moves to the In Progress status.'),
        ('Pending Customer',
         'If the support team needs more information from the customer to fix the issue, the ticket might move to the Pending Customer status.'),
        ('Pending Vendor',
         'If the ticket is waiting for an update or release from a vendor, the ticket might move to the Pending Vendor status.'),
        ('Pending Maintenance',
         'If the ticket is waiting for a maintenance window and is not being actively worked, the ticket might move to the Pending Maintenance status.'),
        ('Transferred', 'If a ticket moves to another member of the support team, it has a status of Transferred.'),
        ('Solved', 'When support team solved the issue, the status is changed to Solved.'),
        ('Closed', 'After a ticket has a status of Solved, a customer can move the ticket to Closed')
    ]

    statuses_names = [sn[0] for sn in tickets_statuses]
    exists_statuses = TicketStatus.query.filter(TicketStatus.name.in_(statuses_names)).all()
    exists_names = [s.name for s in exists_statuses]

    processed = []
    for s in tickets_statuses:
        if not s[0] in exists_names:
            ticket_status = TicketStatus(name=s[0], description=s[1], is_predefined=True)
            db.session.add(ticket_status)
            processed.append(ticket_status)
    try:
        db.session.commit()
        click.echo('Inserted tickets statuses: ' + str(processed))
    except Exception as ex:
        click.echo(str(ex))
        click.echo('Commit Failed')


@app.cli.command()
def setup_roles():
    from mg_incident.models import AppRole, TicketStatus

    available_statuses_for_user = []
    available_statuses_for_worker = ['In Progress', 'Pending Customer', 'Pending Vendor', 'Pending Maintenance',
                                     'Solved']
    available_statuses_for_manager = available_statuses_for_worker + ['Transferred', 'Closed', 'New']
    available_statuses_for_admin = available_statuses_for_manager

    roles_statuses_map = {
        'user': available_statuses_for_user,
        'worker': available_statuses_for_worker,
        'manager': available_statuses_for_manager,
        'admin': available_statuses_for_admin
    }

    for r, s in roles_statuses_map.items():
        approle = AppRole.query.filter(AppRole.name == r).first()
        _statuses = TicketStatus.query.filter(TicketStatus.name.in_(s)).all()
        approle.ticket_statuses = _statuses
        db.session.add(approle)

    try:
        db.session.commit()
        click.echo('Successfully mapped tickets statuses with users roles')
    except Exception as ex:
        click.echo(str(ex))
        click.echo('Error on mapping tickets statuses with users roles')
