#!/usr/bin/env python

import pandas as pd
import csv

SOURCE = "source.csv"

# clean up the source file
with open(SOURCE, "r") as f:
    rows = [[item.strip() for item in row] for row in csv.reader(f) if row]
# check row lengths
for i, row in enumerate(rows):
    assert len(row) == 5, "Row {} has {} columns: {}".format(i, len(row), repr(row))
rows = [rows[0]] + sorted(rows[1:], key=lambda x: x[0].lower())
with open(SOURCE, "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)


# generate the html file
def make_threads_link(val):
    # target _blank to open new window
    return '<a target="_blank" href="https://www.threads.net/@{}">{}</a>'.format(val[1], val[0])


df = pd.read_csv("source.csv")
df = df.fillna("")  # replace all NaN values with ""
df["Name"] = df[["Name", "Threads"]].apply(make_threads_link, axis=1)
df["Threads"] = df[["Threads", "Threads"]].apply(make_threads_link, axis=1)
df = df[["Name", "Threads", "Twitter", "Affiliation", "Role"]]
html_table_data = df.to_html(index=False, classes="display", table_id="table_id", escape=False)

raw_html = (
    """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.4/css/jquery.dataTables.css">
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.4/js/jquery.dataTables.min.js"></script>
    <title>AI Accounts on Threads</title>
</head>
<body>
<h1>AI Accounts on Threads</h1>
"""
    + html_table_data
    + """
    <script>
    $(document).ready( function () {
        $('#table_id').DataTable( {
            "pageLength": 100
        });
    });
    </script>
</body>
</html>
"""
)

with open("ai_accounts_on_threads.html", "w") as f:
    f.write(raw_html)
