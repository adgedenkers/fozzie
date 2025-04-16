import click
from fozzie.calendar.school_days import chorus_today, populate_school_day_letters

@click.group()
def chorus():
    """School-related utilities like chorus checks and day letter assignment."""
    pass

@chorus.command()
@click.argument('db_path')
def today(db_path):
    """Check if today is a chorus day."""
    if chorus_today(db_path):
        click.echo("🎶 Yes, today is a chorus day!")
    else:
        click.echo("❌ No chorus today.")

@chorus.command()
@click.argument('db_path')
@click.argument('start_date')
@click.argument('end_date')
def assign(db_path, start_date, end_date):
    """Add & assign school day letters from START_DATE to END_DATE."""
    populate_school_day_letters(db_path, start_date, end_date)
    click.echo(f"✅ Populated school day letters from {start_date} to {end_date}")
