# fozzie/cli/sports.py
import click
from datetime import date
from fozzie.sports.config import load_sports_config
from fozzie.sports.fetch import get_events_for_sport, get_cached_teams, find_sport_id, get_next_event
from fozzie.sports.notify import notify_event

@click.group()
def sports():
    """Get info on school sports events via ScheduleGalaxy."""
    pass

@sports.command("today")
@click.option('--sport-id', type=int, help="Override sport_id from config.")
@click.option('--notify/--no-notify', default=True, help="Show desktop notification if event found.")
def today(sport_id, notify):
    """Show today's event (game, meet, or practice) for the configured team."""
    cfg = load_sports_config()
    sid = sport_id or cfg.get("sport_id")
    school_id = cfg.get("school_id")

    if not sid or not school_id:
        click.secho("Missing sport_id or school_id in config or CLI.", fg="red")
        return

    today_str = date.today().isoformat()
    events = get_events_for_sport(school_id, sid, today_str, today_str)

    if not events:
        click.echo("📅 No event scheduled today.")
    else:
        for ev in events:
            summary = f"{ev['title']} at {ev['location']} ({ev['start_time']})"
            click.secho(f"📣 {summary}", fg="green")
            if notify:
                notify_event(summary)

@sports.command("next")
@click.option('--sport-id', type=int, help="Override sport_id from config.")
@click.option('--notify/--no-notify', default=True, help="Show desktop notification if event found.")
def next_event(sport_id, notify):
    """Show the next upcoming event (game, meet, or practice) for the configured team."""
    cfg = load_sports_config()
    sid = sport_id or cfg.get("sport_id")
    school_id = cfg.get("school_id")

    if not sid or not school_id:
        click.secho("Missing sport_id or school_id in config or CLI.", fg="red")
        return

    ev = get_next_event(school_id, sid)
    if ev:
        summary = f"Next: {ev['title']} at {ev['location']} on {ev['date']} ({ev['start_time']})"
        click.secho(f"📅 {summary}", fg="blue")
        if notify:
            notify_event(summary)
    else:
        click.echo("🔍 No upcoming events found.")

@sports.command("list")
def list_teams():
    """List all sports teams for the configured school."""
    cfg = load_sports_config()
    school_id = cfg.get("school_id")
    if not school_id:
        click.secho("Missing school_id in config.", fg="red")
        return

    teams = get_cached_teams(school_id)
    for t in teams:
        click.echo(f"[{t['id']}] {t['title']}")

@sports.command("find")
@click.option('--level', required=True, help="Team level (e.g. 7/8TH, JV, V)")
@click.option('--sport', required=True, help="Sport name (e.g. Outdoor Track, Baseball)")
def find_team(level, sport):
    """Find sport ID by level and sport name."""
    cfg = load_sports_config()
    school_id = cfg.get("school_id")
    if not school_id:
        click.secho("Missing school_id in config.", fg="red")
        return

    sport_id = find_sport_id(school_id, level, sport)
    if sport_id:
        click.secho(f"✅ Sport ID for {level} {sport}: {sport_id}", fg="green")
    else:
        click.secho("❌ No match found.", fg="red")

# # fozzie/cli/sports.py
# import click
# from datetime import date
# from fozzie.sports.config import load_sports_config
# from fozzie.sports.fetch import get_events_for_sport, get_cached_teams, find_sport_id
# from fozzie.sports.notify import notify_event

# @click.group()
# def sports():
#     """Get info on school sports events via ScheduleGalaxy."""
#     pass

# @sports.command("today")
# @click.option('--sport-id', type=int, help="Override sport_id from config.")
# @click.option('--notify/--no-notify', default=True, help="Show desktop notification if event found.")
# def today(sport_id, notify):
#     """Show today's event (game, meet, or practice) for the configured team."""
#     cfg = load_sports_config()
#     sid = sport_id or cfg.get("sport_id")
#     school_id = cfg.get("school_id")

#     if not sid or not school_id:
#         click.secho("Missing sport_id or school_id in config or CLI.", fg="red")
#         return

#     today_str = date.today().isoformat()
#     events = get_events_for_sport(school_id, sid, today_str, today_str)

#     if not events:
#         click.echo("📅 No event scheduled today.")
#     else:
#         for ev in events:
#             summary = f"{ev['title']} at {ev['location']} ({ev['start_time']})"
#             click.secho(f"📣 {summary}", fg="green")
#             if notify:
#                 notify_event(summary)

# @sports.command("list")
# def list_teams():
#     """List all sports teams for the configured school."""
#     cfg = load_sports_config()
#     school_id = cfg.get("school_id")
#     if not school_id:
#         click.secho("Missing school_id in config.", fg="red")
#         return

#     teams = get_cached_teams(school_id)
#     for t in teams:
#         click.echo(f"[{t['id']}] {t['title']}")

# @sports.command("find")
# @click.option('--level', required=True, help="Team level (e.g. 7/8TH, JV, V)")
# @click.option('--sport', required=True, help="Sport name (e.g. Outdoor Track, Baseball)")
# def find_team(level, sport):
#     """Find sport ID by level and sport name."""
#     cfg = load_sports_config()
#     school_id = cfg.get("school_id")
#     if not school_id:
#         click.secho("Missing school_id in config.", fg="red")
#         return

#     sport_id = find_sport_id(school_id, level, sport)
#     if sport_id:
#         click.secho(f"✅ Sport ID for {level} {sport}: {sport_id}", fg="green")
#     else:
#         click.secho("❌ No match found.", fg="red")