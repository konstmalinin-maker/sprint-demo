"""Export actual GitHub timestamps, Excel formulas/charts and a static figure."""

import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import xlsxwriter

REPO = "konstmalinin-maker/sprint-demo"
BASELINE = [1, 4, 6, 8, 9]
MOSCOW = timezone(timedelta(hours=3))


def api(resource):
    items = []
    page = 1
    while True:
        payload = subprocess.check_output(
            [
                "gh",
                "api",
                f"repos/{REPO}/{resource}?state=all&per_page=100&page={page}",
            ],
            text=True,
        )
        batch = json.loads(payload)
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def dt(value):
    return datetime.fromisoformat(value) if value else None


def export(root, offline=False):
    out = root / "docs" / "metrics"
    out.mkdir(parents=True, exist_ok=True)
    if offline:
        issues = json.loads((out / "issues.json").read_text())
        pulls = json.loads((out / "pulls.json").read_text())
    else:
        issues = [
            {
                key: issue[key]
                for key in [
                    "number",
                    "title",
                    "html_url",
                    "created_at",
                    "closed_at",
                    "state",
                ]
            }
            for issue in api("issues")
            if "pull_request" not in issue
        ]
        pulls = [
            {
                key: pr[key]
                for key in [
                    "number",
                    "title",
                    "html_url",
                    "created_at",
                    "merged_at",
                    "body",
                    "merge_commit_sha",
                ]
            }
            for pr in api("pulls")
        ]
        for name, items in [("issues", issues), ("pulls", pulls)]:
            (out / f"{name}.json").write_text(
                json.dumps(items, ensure_ascii=False, indent=2) + "\n"
            )

    rows = []
    for issue in sorted(issues, key=lambda i: i["number"]):
        related = [
            p
            for p in pulls
            if re.search(
                rf"\b(?:closes?|fix(?:es|ed)?|resolves?)\s+#({issue['number']})(?!\d)",
                p["body"] or "",
                re.IGNORECASE,
            )
            and p["merged_at"]
        ]
        pr = min(related, key=lambda p: p["merged_at"]) if related else None
        merged = dt(pr["merged_at"]) if pr else None
        opened = dt(pr["created_at"]) if pr else None
        created = dt(issue["created_at"])
        lead = (merged - created).total_seconds() / 60 if merged else None
        cycle = (merged - opened).total_seconds() / 60 if merged else None
        assert lead is None or lead >= 0
        assert cycle is None or cycle >= 0
        rows.append(
            {
                "issue": issue["number"],
                "title": issue["title"],
                "issue_url": issue["html_url"],
                "pr": pr["number"] if pr else None,
                "pr_url": pr["html_url"] if pr else None,
                "created": issue["created_at"],
                "opened": pr["created_at"] if pr else None,
                "merged": pr["merged_at"] if pr else None,
                "lead_minutes": lead,
                "cycle_minutes": cycle,
                "note": "Дубликат #1; отдельного PR нет"
                if issue["number"] == 3
                else ("До слияния: нет конечной метрики" if not pr else ""),
            }
        )
    (out / "metrics.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    )
    baseline = [r for r in rows if r["issue"] in BASELINE]
    assert len(baseline) == 5 and all(r["merged"] for r in baseline)
    workbook = xlsxwriter.Workbook(out / "sprint-metrics.xlsx")
    header = workbook.add_format(
        {"bold": True, "bg_color": "#17365D", "font_color": "white", "text_wrap": True}
    )
    dates = workbook.add_format({"num_format": "dd.mm.yyyy hh:mm:ss"})
    nums = workbook.add_format({"num_format": "0.00"})
    bold = workbook.add_format({"bold": True})
    wrap = workbook.add_format({"text_wrap": True, "valign": "top"})

    for name, data in [("Sprint 1", baseline), ("Все Issues", rows)]:
        sheet = workbook.add_worksheet(name)
        headings = [
            "Issue",
            "Задача",
            "PR",
            "Issue создана (Москва)",
            "PR открыт (Москва)",
            "PR объединён (Москва)",
            "Lead Time, мин",
            "Cycle Time, мин",
            "Примечание",
        ]
        sheet.write_row(0, 0, headings, header)
        sheet.set_row(0, 34)
        sheet.set_column(0, 0, 10)
        sheet.set_column(1, 1, 38)
        sheet.set_column(2, 2, 10)
        sheet.set_column(3, 5, 23)
        sheet.set_column(6, 7, 18)
        sheet.set_column(8, 8, 40)
        sheet.freeze_panes(1, 2)
        for index, row in enumerate(data, 1):
            excel_row = index + 1
            sheet.write_url(index, 0, row["issue_url"], string=f"#{row['issue']}")
            sheet.write(index, 1, row["title"], wrap)
            if row["pr"]:
                sheet.write_url(index, 2, row["pr_url"], string=f"#{row['pr']}")
            for col, key in [(3, "created"), (4, "opened"), (5, "merged")]:
                if row[key]:
                    sheet.write_datetime(
                        index,
                        col,
                        dt(row[key]).astimezone(MOSCOW).replace(tzinfo=None),
                        dates,
                    )
            for col, start, key in [
                (6, "D", "lead_minutes"),
                (7, "E", "cycle_minutes"),
            ]:
                formula = f'=IF(OR({start}{excel_row}="",F{excel_row}=""),"",(F{excel_row}-{start}{excel_row})*1440)'
                sheet.write_formula(
                    index, col, formula, nums, row[key] if row[key] is not None else ""
                )
            sheet.write(index, 8, row["note"], wrap)
        end = len(data) + 2
        sheet.write(end, 5, "Среднее", bold)
        for col, letter, key in [(6, "G", "lead_minutes"), (7, "H", "cycle_minutes")]:
            valid = [r[key] for r in data if r[key] is not None]
            sheet.write_formula(
                end,
                col,
                f"=AVERAGE({letter}2:{letter}{len(data) + 1})",
                nums,
                mean(valid),
            )
        sheet.autofilter(0, 0, len(data), 8)
        chart = workbook.add_chart({"type": "column"})
        for col, title in [(6, "Lead Time"), (7, "Cycle Time")]:
            chart.add_series(
                {
                    "name": title,
                    "categories": [name, 1, 0, len(data), 0],
                    "values": [name, 1, col, len(data), col],
                }
            )
        chart.set_title({"name": f"{name}: Lead Time и Cycle Time"})
        chart.set_y_axis({"name": "Минуты", "min": 0})
        chart.set_x_axis({"name": "Issue"})
        chart.set_legend({"position": "bottom"})
        chart.set_size({"width": 850, "height": 400})
        sheet.insert_chart(end + 3, 0, chart)
    info = workbook.add_worksheet("Методика")
    info.set_column(0, 0, 110)
    for i, text in enumerate(
        [
            "Исходные timestamps GitHub: UTC. Отображение в таблице: Москва, UTC+03:00.",
            "Lead Time = merged_at связанного PR − created_at Issue.",
            "Cycle Time = merged_at PR − created_at PR.",
            "Окончание метрики — слияние feature-PR в целевую ветку, а не закрытие Issue и не релиз.",
            "Лист Sprint 1: пять исходных функций. Лист Все Issues: также hotfix и задачи симуляции F.",
            "Issue #3 дублирует #1, отдельного PR нет: метрики не определены и в среднее не входят.",
            "В ячейках находятся формулы и сохранённые числовые результаты; диаграммы редактируются в Excel.",
            "Продолжительность включает ожидание и перерывы; она не равна времени активного программирования.",
            "Источник: https://github.com/konstmalinin-maker/sprint-demo; снимки API рядом с Excel.",
        ]
    ):
        info.write(i, 0, text, wrap)
        info.set_row(i, 30)
    workbook.close()

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(baseline))
    width = 0.36
    ax.bar(
        [i - width / 2 for i in x],
        [r["lead_minutes"] for r in baseline],
        width,
        label="Lead Time",
    )
    ax.bar(
        [i + width / 2 for i in x],
        [r["cycle_minutes"] for r in baseline],
        width,
        label="Cycle Time",
    )
    ax.set_xticks(list(x), [f"Issue #{r['issue']} / PR #{r['pr']}" for r in baseline])
    ax.set_ylabel("Минуты")
    ax.set_title("Sprint 1: фактические метрики GitHub")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / "sprint-metrics.png", dpi=180)
    plt.close(fig)
    longest = max(baseline, key=lambda r: r["cycle_minutes"])
    text = [
        "# Метрики Sprint 1",
        "",
        "Источник — timestamps Issues и PR GitHub; время в таблице московское (UTC+03:00).",
        "",
        "| Issue | PR | Создана Issue | Открыт PR | Слияние PR | Lead Time, мин | Cycle Time, мин |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in baseline:
        display = lambda key, r=r: (
            dt(r[key]).astimezone(MOSCOW).strftime("%d.%m.%Y %H:%M:%S")
        )
        text.append(
            f"| #{r['issue']} | #{r['pr']} | {display('created')} | {display('opened')} | {display('merged')} | {r['lead_minutes']:.2f} | {r['cycle_minutes']:.2f} |"
        )
    text.extend(
        [
            "",
            f"Средний Lead Time: **{mean(r['lead_minutes'] for r in baseline):.2f} мин**. Средний Cycle Time: **{mean(r['cycle_minutes'] for r in baseline):.2f} мин**.",
            "",
            f"Самый долгий цикл у Issue #{longest['issue']} / PR #{longest['pr']}: **{longest['cycle_minutes']:.2f} мин**. Авторизация открыта первой и объединена во время общей интеграции функций. В её обсуждении подтверждено исправление валидации email и добавление трёх тестов. Тimestamps не позволяют разложить весь интервал на активную работу и ожидание; утверждать, что всё это время заняло исправление, нельзя.",
            "",
            "Issue #3 — дубликат #1 без самостоятельного PR. Значения N/A, в среднее не включена. Все остальные Issues и дополнительные задачи приведены на листе «Все Issues».",
            "",
            "[Excel с формулами и редактируемыми диаграммами](sprint-metrics.xlsx).",
            "",
            "![Lead Time и Cycle Time](sprint-metrics.png)",
            "",
        ]
    )
    (out / "README.md").write_text("\n".join(text))
    print(
        "Exported",
        len(rows),
        "Issues; baseline averages:",
        mean(r["lead_minutes"] for r in baseline),
        mean(r["cycle_minutes"] for r in baseline),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    export(args.root, args.offline)
