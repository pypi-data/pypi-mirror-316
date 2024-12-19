"""Get data from a runner's personal parkrun page."""

import itertools
import time
import urllib

from bs4 import BeautifulSoup

from .event import Date, Parkrun
from .runner import PersonParkrunStats, RecentRun, Runner
from .times import Time

# User-Agent must be changed to prevent blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def url(runner_id):
    return f"https://www.parkrun.org.uk/parkrunner/{runner_id}/"


def get_html(runner_id):
    """Get the html of a runner's page from the parkrun website."""
    # Delay to prevent blocking
    time.sleep(5)
    request = urllib.request.Request(url(runner_id), data=None, headers=HEADERS)
    return urllib.request.urlopen(request).read().decode("utf-8")


def table_content(table):
    for row in table.contents:
        yield [c.contents[0] for c in row.contents]


def get_runner_data(html):
    """Find a person's name, results and recents from their page."""
    soup = BeautifulSoup(html, "html.parser")
    # Find the person's name
    name = soup.find("h2").contents[0].strip().title()
    # Find their results
    maintable = soup.find_all("table", id="results")[1].find("tbody")
    # Process them
    results = []
    for row in table_content(maintable):
        event_url = row[0]["href"]
        event_text = row[0].contents[0]
        junior = "junior" in event_text
        if junior:
            event_text = event_text.replace("junior ", "")
        results.append(
            PersonParkrunStats(
                event=Parkrun.from_url_title(event_url, event_text),
                runs=int(row[1]),
                best_gender_pos=int(row[2]),
                best_pos=int(row[3]),
                pb=Time(row[4].contents[0]),
                junior=junior,
            )
        )

    recents_table = soup.find_all("table", id="results")[0].find("tbody")
    recents = [
        RecentRun(
            event=Parkrun.from_url_title(row[0]["href"], row[0].contents[0]),
            run_date=Date.from_link(row[1]),
            gender_pos=int(row[2]),
            overall_pos=int(row[3]),
            time=Time(row[4]),
            age_grade=row[5],
        )
        for row in table_content(recents_table)
    ]
    return name, results, recents


def get_runner_stats(runner_id):
    if "&" not in runner_id:
        name, results, recents = get_runner_data(get_html(runner_id))
        return Runner(name, runner_id, results, recents)
    # Deal with runners with multiple ids
    resultss = []
    recentss = []
    for r in reversed(runner_id.split("&")):
        # Just use last occurring name (from first ID)
        name, results, recents = get_runner_data(get_html(r))
        resultss.append(results)
        recentss.append(recents)
    results = []
    parkruns = list({x.event for y in resultss for x in y})
    for parkrun in parkruns:
        relevant_stats = [[x for x in r if x.event == parkrun] for r in resultss]
        relevant_stats = [x[0] for x in relevant_stats if x]
        if not relevant_stats:
            continue
        # Calculate the overall stats for this runner
        results.append(
            PersonParkrunStats(
                event=parkrun,
                runs=sum(r.runs for r in relevant_stats),
                best_gender_pos=min(r.best_gender_pos for r in relevant_stats),
                best_pos=min(r.best_pos for r in relevant_stats),
                pb=min(r.pb for r in relevant_stats),
                junior=relevant_stats[0].junior,
            )
        )
    return Runner(
        name, runner_id, results, list(itertools.chain.from_iterable(recentss))
    )
