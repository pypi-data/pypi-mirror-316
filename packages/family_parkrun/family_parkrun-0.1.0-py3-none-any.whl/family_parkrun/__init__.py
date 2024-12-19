"""Generate a summary of the Parkrun performances of a group of people."""

import argparse
import itertools
from pathlib import Path
from string import Template

from . import download
from . import html_construct as html
from .html_construct import a, td, th
from .runner import Runner

__version__ = "0.1.0"


def abs_path(path):
    return Path(__file__).parent / path


EVENTS = td("Events", class_="text")
COUNT = td("Count", class_="text")
PB = td("PB")


MAIN_SUBROWS = {
    td("Count", class_="text"): lambda r, runner: td(
        a(r.runs, href=f"{r.event.url}/parkrunner/{runner.primary_id}")
    ),
    td("PB"): lambda r, _: td(r.pb),
}
OVERALL_SUBROWS = {
    EVENTS: lambda r, j: td(len(r.parkrun_data)),
    COUNT: lambda r, j: (
        td(r.total_junior_parkruns, class_=f"b{r.band}" if r.band else None)
        if j
        else td(r.total_parkruns, class_=f"s{r.shirt}" if r.shirt else None)
    ),
    PB: lambda r, j: td(r.pb) if r else td(),
}
TOTAL_SUBROWS = {
    td("Count", class_="text"): lambda x: td(sum(i.runs for i in x), class_="total"),
    td("PB"): lambda x: td(min(i.pb for i in x), class_="total"),
}
TOTAL_OVERALL_SUBROWS = {
    EVENTS: lambda x: td(len({i.event for r in x for i in r.parkrun_data})),
    COUNT: lambda x: td(sum(j.runs for r in x for j in r.parkrun_data)),
    PB: lambda x: td(min(i.pb for i in x)),
}


def make_table(runners, junior=False):
    parkruns = set()
    for runner in runners:
        parkruns.update(x.event for x in runner.parkrun_data)
    parkruns = sorted(parkruns)
    maintable = [
        [
            th(h)
            for h in (
                ["Parkrun", ""]
                + [a(r.name.split(" ")[0], download.url(r.primary_id)) for r in runners]
                + ["Overall"]
            )
        ]
    ]
    # Make top "Overall" rows
    for subrow in OVERALL_SUBROWS:
        row = [td(), subrow]
        row += [OVERALL_SUBROWS[subrow](runner, junior) for runner in runners]
        row.append(TOTAL_OVERALL_SUBROWS[subrow](runners))
        maintable.append(
            f'<tr class="total{"" if subrow == PB else " count"}">{"".join(row)}</tr>'
        )

    # Make main table
    for parkrun in parkruns:
        for i, subrow in enumerate(MAIN_SUBROWS):
            initial = td(parkrun.html(), class_="text") if i == 0 else td()
            row = [initial, subrow]
            for r in runners:
                data = r.get_parkrun_data(parkrun)
                row.append(td() if data is None else MAIN_SUBROWS[subrow](data, r))
            row.append(
                TOTAL_SUBROWS[subrow](
                    r.get_parkrun_data(parkrun)
                    for r in runners
                    if r.get_parkrun_data(parkrun) is not None
                )
            )
            maintable.append(
                f'<tr class="count">{"".join(row)}</tr>'
                if subrow == td("Count", class_="text")
                else row
            )

    return html.create_html_table(maintable, "main")


def make_recents_table(runners):
    runs = sorted(
        itertools.chain.from_iterable(
            [(run, runner.name) for run in runner.recents] for runner in runners
        ),
        key=lambda r: (-r[0].run_date.date.toordinal(), r[0].event, r[0].overall_pos),
    )
    table = [
        [
            th(x)
            for x in (
                "Date",
                "Event",
                "Runner",
                "Gender Position",
                "Overall Position",
                "Time",
                "Age Grade",
            )
        ]
    ]
    previous_run = None
    had_dates = set()
    colour = 1
    for run, runner_name in runs:
        if (run.run_date.date, run.event) != previous_run:
            colour = 1 - colour
            previous_run = (run.run_date.date, run.event)

        overline = False
        if run.run_date.date not in had_dates:
            if had_dates:
                overline = True
            had_dates.add(run.run_date.date)
            if len(had_dates) > 10:
                break
        row = "".join(
            (
                td(run.run_date.html()),
                td(run.event.html(), class_="text"),
                td(runner_name.split(" ")[0], class_="text"),
                td(format(run.gender_pos, "\N{FIGURE SPACE}>3")),
                td(format(run.overall_pos, "\N{FIGURE SPACE}>3")),
                td(run.time),
                td(run.age_grade),
            )
        )
        classes = []
        if colour:
            classes.append("shaded")
        if overline:
            classes.append("overline")
        class_ = f' class="{" ".join(classes)}"' if classes else ""
        table.append(f"<tr{class_}>{row}</tr>")
    return html.create_html_table(table, class_="recent")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "runners", type=argparse.FileType("r"), help="file with list of runner IDs"
    )
    args = parser.parse_args()
    runners = [download.get_runner_stats(r.strip()) for r in args.runners]

    senior_runners = []
    junior_runners = []
    for runner in runners:
        senior_data = [r for r in runner.parkrun_data if not r.junior]
        junior_data = [r for r in runner.parkrun_data if r.junior]
        if senior_data:
            senior_runners.append(
                Runner(
                    runner.name, runner.runner_id, senior_data, [], bool(junior_data)
                )
            )
        if junior_data:
            junior_runners.append(
                Runner(runner.name, runner.runner_id, junior_data, [], True)
            )
    tab_buttons = ["Recent"]
    tabs = [("Recent", make_recents_table(runners))]
    if senior_runners:
        tab_buttons.append("Senior")
        tabs.append(("Senior", make_table(senior_runners)))
    if junior_runners:
        tab_buttons.append("Junior")
        tabs.append(("Junior", make_table(junior_runners, True)))
    content = html.nav_bar(tab_buttons) + "".join(html.tab(*t) for t in tabs)
    Path("summary.html").write_text(
        Template(abs_path("page.html").read_text()).substitute(
            {"css": abs_path("style.css").read_text(), "content": content}
        )
    )
