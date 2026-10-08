import json, os, urllib.request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

USER = os.environ.get("GH_USER", "meralamuralikrishna-cpu")
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
)
data = json.load(urllib.request.urlopen(req))
cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

dates, counts = [], []
for week in cal["weeks"]:
    days = week["contributionDays"]
    if not days:
        continue
    dates.append(datetime.strptime(days[0]["date"], "%Y-%m-%d"))
    counts.append(sum(d["contributionCount"] for d in days))

BG, LINE, TEXT, GRID = "#0d1117", "#58a6ff", "#c9d1d9", "#21262d"

fig, ax = plt.subplots(figsize=(11, 3.6), facecolor=BG)
ax.set_facecolor(BG)
ax.plot(dates, counts, color=LINE, linewidth=2.4, marker="o", markersize=4,
        markerfacecolor="#ffffff", markeredgecolor=LINE)
ax.fill_between(dates, counts, color=LINE, alpha=0.18)

ax.set_title(f"Contribution Graph  •  {cal['totalContributions']} contributions in the last year",
             color=TEXT, fontsize=13, loc="left", pad=12)
ax.set_ylabel("Weekly contributions", color=TEXT, fontsize=9)
ax.tick_params(colors=TEXT, labelsize=9)
ax.grid(axis="y", color=GRID, linewidth=0.8)
ax.set_ylim(bottom=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)

fig.tight_layout()
os.makedirs("assets", exist_ok=True)
fig.savefig("assets/contribution-graph.svg", facecolor=BG, format="svg")
print("saved assets/contribution-graph.svg")
