from flask import Flask, render_template_string, request
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

def load_data(file_path, num_rows=10):
    if os.path.exists(file_path):
        print("Using local file")
        df = pd.read_csv(file_path, nrows=num_rows)
        nRow, nCol = df.shape
        fake_accounts = df[df['fake'] == 1]['profile username'].unique()
        return df, f'There are {nRow} rows and {nCol} columns', fake_accounts, f'Number of Fake Accounts: {len(fake_accounts)}'
    else:
        return None, None, None, None

def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]]
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) // nGraphPerRow
    plt.figure(num=None, figsize=(6 * nGraphPerRow, 8 * nGraphRow), dpi=80, facecolor='w', edgecolor='k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columndf = df.iloc[:, i]
        if not np.issubdtype(type(columndf.iloc[0]), np.number):
            valueCounts = columndf.value_counts()
            valueCounts.plot.bar()
        else:
            columndf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation=90)
        plt.title(f"{columnNames[i]} (column {i})")
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.show()

@app.route('/')
def display_dataframe():
    file_path = request.args.get('file_path')
    num_rows = request.args.get('num_rows', type=int)
    if file_path and num_rows:
        df, rows_and_cols, fake_accounts, fake_accounts_count = load_data(file_path, num_rows)
        if df is not None:
            html_table = df.to_html()
            return render_template_string(
                """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Data Frame Display</title>
                    <style>
                        html, body {
                            height: 100%;
                            margin: 0;
                        }
                        body {
                            background-image: url('https://wallpapers.com/images/hd/720p-social-background-1280-x-720-ubk16q7k72ddmlyx.jpg'); /* Adjust the URL to the location of your image file */
                            background-size: cover; /* Ensure the background image covers the entire viewport */
                            background-position: center; /* Center the background image */
                            background-repeat: no-repeat; /* Do not repeat the background image */
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }
                        .content {
                            text-align: center;
                        }
                    </style>
                </head>
                <body>
                    <div class="content">
                        <h1>Data Frame Display</h1>
                        <p>{{ rows_and_cols }}</p>
                        <p>Fake Account IDs: {{ fake_accounts }}</p>
                        <p>{{ fake_accounts_count }}</p>
                        {{ table|safe }}
                    </div>
                </body>
                </html>
                """,
                table=html_table,
                rows_and_cols=rows_and_cols,
                fake_accounts=fake_accounts,
                fake_accounts_count=fake_accounts_count,
                file_path=file_path,
                num_rows=num_rows
            )
        else:
            return "File not found or unable to load data."
    else:
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Data Frame Display</title>
                <style>
                    html, body {
                        height: 100%;
                        margin: 0;
                    }
                    body {
                        background-image: url('https://wallpapers.com/images/hd/720p-social-background-1280-x-720-ubk16q7k72ddmlyx.jpg'); /* Adjust the URL to the location of your image file */
                        background-size: cover; /* Ensure the background image covers the entire viewport */
                        background-position: center; /* Center the background image */
                        background-repeat: no-repeat; /* Do not repeat the background image */
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }
                    .content {
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="content">
                    <h1>Data Frame Display</h1>
                    <form action="/" method="get">
                        <label for="file_path">File Path:</label>
                        <input type="text" id="file_path" name="file_path"><br><br>
                        <label for="num_rows">Number of Rows:</label>
                        <input type="number" id="num_rows" name="num_rows"><br><br>
                        <input type="submit" value="Submit">
                    </form>
                </div>
            </body>
            </html>
            """
        )



@app.route('/plot_distribution')
def plot_distribution():
    file_path = request.args.get('file_path')

    # Check if file_path is provided
    if file_path:
        # Render form to input number of graphs and number of graphs per row
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Plot Distribution</title>
                <style>
                    html, body {
                        height: 100%;
                        margin: 0;
                    }
                    body {
                        background-image: url('/static/background.jpg'); /* Adjust the URL to the location of your image file */
                        background-size: cover; /* Ensure the background image covers the entire viewport */
                        background-position: center; /* Center the background image */
                        background-repeat: no-repeat; /* Do not repeat the background image */
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }
                    .content {
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="content">
                    <h1>Plot Distribution</h1>
                    <form action="/generate_distribution_plots" method="get">
                        <input type="hidden" name="file_path" value="{{ file_path }}">
                        <label for="num_graphs">Number of Graphs:</label>
                        <input type="number" id="num_graphs" name="num_graphs"><br><br>
                        <label for="num_graphs_per_row">Number of Graphs Per Row:</label>
                        <input type="number" id="num_graphs_per_row" name="num_graphs_per_row"><br><br>
                        <input type="submit" value="Generate Distribution Plots">
                    </form>
                </div>
            </body>
            </html>
            """,
            file_path=file_path
        )
    else:
        return "Please provide file_path parameter."




if __name__ == '__main__':
    app.run(debug=True)
