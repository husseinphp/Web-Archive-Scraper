import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse

print(r"""
  ___       _   _                    _       
 / _ \__  _| | | |_   _ ___ ___  ___(_)_ __  
| | | \ \/ / |_| | | | / __/ __|/ _ \ | '_ \ 
| |_| |>  <|  _  | |_| \__ \__ \  __/ | | | |
 \___//_/\_\_| |_|\__,_|___/___/\___|_|_| |_|
x.com/0xHussein
""")

parser = argparse.ArgumentParser(description="Fetch URLs and Titles from web.archive.org.")
parser.add_argument("-l", "--linkfile", type=str, help="File containing URLs to process.", default="er.txt")
parser.add_argument("-e", "--extensions", type=str, nargs='+', help="File extensions to filter by, separated by spaces.", default=["php", "html"])
args = parser.parse_args()

with open(args.linkfile, "r", encoding="utf-8") as file:
    input_urls = [line.strip() for line in file.readlines() if line.strip()]

extension_filter = "|".join(args.extensions)

with open("urls.txt", "w", encoding="utf-8") as output_file:
    for url in input_urls:
        params = {
            "url": url,
            "matchType": "domain",
            "collapse": "urlkey",
            "output": "text",
            "fl": "original",
            "filter": f"urlkey:.*\\.({extension_filter})$", 
            "limit": "1000"
        }
        response = requests.get("https://web.archive.org/cdx/search", params=params)
        found_urls = response.text.splitlines()
        for found_url in found_urls:
            output_file.write(f"{found_url}\n")

with open("urls.txt", "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]

with open("results.html", "w", encoding="utf-8") as html_file:
    html_file.write("""
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URLs and Titles</title>
    <!-- تضمين مكتبة jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <!-- تضمين مكتبة DataTables -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.1/css/jquery.dataTables.min.css">
    <script src="https://cdn.datatables.net/1.13.1/js/jquery.dataTables.min.js"></script>
    <!-- تنسيق مخصص -->
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h2>URLs and Titles</h2>
    <table id="example" class="display">
        <thead>
            <tr>
                <th>URL</th>
                <th>Title</th>
                <th>Status Code</th>
                <th>Content Length</th>
            </tr>
        </thead>
        <tbody>
""")

    for count, url in enumerate(tqdm(urls, desc="⠙ request count", unit=" requests", dynamic_ncols=True), 1):
        try:
            response = requests.get(url)
            status_code = response.status_code
            content_length = len(response.content)
            if response.ok:  
                content = response.text
                if "<html" in content.lower():
                    soup = BeautifulSoup(content, 'html.parser')
                    title = soup.title.string.strip() if soup.title else "No Title"
                else:
                    title = "Invalid HTML"

                display_url = url if len(url) <= 100 else url[:100] + '...'

                html_file.write(f"<tr><td><a target='_blank' href='{url}'>{display_url}</a></td>")
                html_file.write(f"<td>{title}</td>")
                html_file.write(f"<td>{status_code}</td>")
                html_file.write(f"<td>{content_length}</td></tr>\n")
            else:
                html_file.write(f"<tr><td><a target='_blank' href='{url}'>{url}</a></td>")
                html_file.write("<td>Failed to fetch</td>")
                html_file.write(f"<td>{status_code}</td>")
                html_file.write("<td>0</td></tr>\n")
        except Exception as e:
            html_file.write(f"<tr><td><a target='_blank' href='{url}'>{url}</a></td>")
            html_file.write(f"<td>Error: {str(e)}</td>")
            html_file.write("<td>Error</td><td>0</td></tr>\n")

    html_file.write("""
                </tbody>
            </table>

    <script>
        $(document).ready(function() {
            $('#example').DataTable();
        });
    </script>
</body>
</html>
""")

print("Results have been saved to results.html")
