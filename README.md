# Web Archive Scraper

## Overview :computer:	

**Web Archive Scraper** is a Python script designed to fetch archived web pages from the [Wayback Machine](https://web.archive.org/). The script allows users to extract titles and other relevant metadata of archived web pages based on specified file extensions.

## Features :cowboy_hat_face:

- Fetch archived URLs from the Wayback Machine.
- Filter results based on file extensions (e.g., `.php`, `.html`).
- Extract and display the title, status code, and content length of each archived page.
- Save the results in both `.txt` and `.html` formats.

## Usage :boom:
To run the script, use the following command:

``python was.py -l <linkfile> -e <extensions>``

``python was.py -l liveurls.txt -e php html ``

## Output :floppy_disk:	
> Text File: All fetched URLs are saved in a urls.txt file.

> HTML File: The script generates a results.html file containing a table with the following columns:
` URL`
` Title`
` Status Code`
` Content Length`

## Installation :cd:	

Clone the repository :

```bash
git clone https://github.com/husseinphp/web-archive-scraper.git
cd web-archive-scraper
