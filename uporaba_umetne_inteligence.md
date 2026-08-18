# Uporaba umetne inteligence

## Ideja za projekt

Idejo za projekt sem dobil s pomočjo ChatGPT-ja, ki mi je dal seznam potencialnih spletnih strani.  Med njimi je bila tudi spletna stran s podatki iz lige NBA. Sicer je pa ChatGPT še vedno nezanesljiv, saj je za veliko strani trdil, da se da iz njih zlahka pridobiti podatke, kar ni bilo res.

## Koda

Za nekatere dele kode, še posebej tiste, ki uporabljajo knjižnico BeautifulSoup, sem uporabil ChatGPT za pomoč. Pogovori so v angleščini.

### Pogovor 1

**Jaz:**  
how to get html data from inside a comment with beautiful soup?

**ChatGPT:**  

>Beautiful Soup treats HTML comments as `Comment` objects, so you can search for them specifically.
>For example, if your HTML contains:
>
>```html
><!--
><div class="player">
>    <p>LeBron James</p>
></div>
>-->
>```
>
>you can do:
>
>```python
>from bs4 import BeautifulSoup, Comment
>
>comments = soup.find_all(string=lambda text: isinstance(text, Comment))
>
>for comment in comments:
>    print(comment)
>```
>
>Now `comment` contains the **HTML inside the comment as a string**.
>
>### Then parse that HTML again
>
>If you want Beautiful Soup to treat the commented HTML as actual HTML:
>
>```python
>comment_soup = BeautifulSoup(comment, "html.parser")
>
>div = comment_soup.find("div", class_="player")
>print(div)
>```
>
>So the process is:
>
>**HTML → find comment → extract comment text → parse that text as HTML → search it**
>
>This is actually fairly common on websites that put content inside HTML comments, sometimes to defer loading or hide unused markup.
>
**Jaz:**  
is there a way to get a specific comment block?

**ChatGPT:**  
>Yes. You can search comments just like other Beautiful Soup elements.
>
>### If you know something inside the comment
>
>For example, if you have:
>
>```html
><!--
><table class="standings">
>    ...
></table>
>-->
>```
>
>you can do:
>
>```python
>from bs4 import Comment
>
>comment = soup.find(
>    string=lambda text: isinstance(text, Comment) and "standings" in text
>)
>
>print(comment)
>```
>
>Now `comment` is that specific comment block.
>
>### If you want the nth comment
>
>You can get all comments first:
>
>```python
>comments = soup.find_all(string=lambda text: isinstance(text, Comment))
>
>comment = comments[3]  # fourth comment
>```
>
>Then, if the comment contains HTML:
>
>```python
>comment_soup = BeautifulSoup(comment, "html.parser")
>
>tables = comment_soup.find_all("table")
>```
>
>### If you know the exact beginning/end
>
>You can also inspect them:
>
>```python
>for i, comment in enumerate(comments):
>    print(i, comment[:100])
>```
>
>That can be really useful in your case. You could find **which of the comments contains your missing two tables**, then parse only that comment instead of parsing every comment on the page.
>


### Pogovor 2

**Jaz:**  
how to get tag attributes with beautiful soup?

**ChatGPT:**  
>If you have a Beautiful Soup tag like:
>
>```python
>tag = soup.find("a")
>```
>
>you can get its attributes in several ways.
>
>### Get one specific attribute
>
>```python
>tag["href"]
>```
>
>For example, if the HTML is:
>
>```html
><a href="/players/lebron" class="player">LeBron James</a>
>```
>
>then:
>
>```python
>print(tag["href"])
># /players/lebron
>
>print(tag["class"])
># ['player']
>```
>
>You can also use `.get()`:
>
>```python
>tag.get("href")
>```
>
>The advantage is that `.get()` returns `None` if the attribute doesn't exist, whereas `tag["href"]` raises a `KeyError`.
>
>### Get all attributes
>
>Use:
>
>```python
>tag.attrs
>```
>
>For the example above:
>
>```python
>print(tag.attrs)
>```
>
>gives something like:
>
>```python
>{'href': '/players/lebron', 'class': ['player']}
>```
>
>So you can iterate over them:
>
>```python
>for name, value in tag.attrs.items():
    >print(name, value)
>```
>
>### Quick summary
>
>```python
>tag["href"]       # one attribute
>tag.get("href")   # one attribute, safely
>tag.attrs         # all attributes as a dictionary
>```
>
>One slightly surprising thing: attributes such as `class` can be returned as a **list**, because >HTML elements can have multiple classes.

### Pogovor 3

**Jaz:**  
an HTML table i'm taking data out of has a data-stat attribute for each td tag, how do i specify this attribute to beautiful soup?

**ChatGPT:**  
>Yep. Beautiful Soup lets you specify an attribute directly.
>
>For example, if your HTML is:
>
>```html
><td data-stat="player">Luka Dončić</td>
><td data-stat="age">27</td>
>```
>
>You can find the `<td>` with a specific `data-stat` like this:
>
>```python
>soup.find("td", attrs={"data-stat": "player"})
>```
>
>Or, more conveniently:
>
>```python
>soup.find("td", {"data-stat": "player"})
>```
>
>Then:
>
>```python
>cell = soup.find("td", {"data-stat": "player"})
>print(cell.text)
>```
>
>would give:
>
>```text
>Luka Dončić
>```
>
>### If you want all cells with that attribute
>
>```python
>cells = soup.find_all("td", {"data-stat": "player"})
>```
>
>### CSS selector alternative
>
>You can also use:
>
>```python
>soup.select('td[data-stat="player"]')
>```
>
>For your scraping project, I'd probably use the `data-stat` approach because it's very useful for tables: **the attribute effectively tells you what each column contains**, so you don't have to rely on column position.


### Pogovor 4

**Jaz:**  
translate all NBA division names into slovene and give them to me in the form of a python dictionary, where the keys are the english names and the values are slovene translations. Make sure that you also cover divisions throughout history, if any changed

**ChatGPT:**  
>Yes. If you want to cover **all NBA division names that have existed**, there are **10 distinct names** worth accounting for.
>
>The important historical change was in **1970–71**, when the old Eastern and Western *Divisions* became *Conferences*, each with two divisions. Then in **2004–05**, the NBA expanded from four divisions to six: the old Midwest Division was replaced by the Northwest and Southwest Divisions, while Southeast was added in the East. ([NBA][1])
>
>Here is the dictionary:
>
>```python
>nba_divisions = {
    ># Current divisions
    >"Atlantic Division": "Atlantska divizija",
    >"Central Division": "Centralna divizija",
    >"Southeast Division": "Jugovzhodna divizija",
    >"Northwest Division": "Severozahodna divizija",
    >"Pacific Division": "Pacifiška divizija",
    >"Southwest Division": "Jugozahodna divizija",
>
    ># Historical divisions
    >"Eastern Division": "Vzhodna divizija",
    >"Western Division": "Zahodna divizija",
    >"Midwest Division": "Srednjezahodna divizija",
>}
>```
>
>Actually, there is one nuance: **Eastern Division** and **Western Division** were used before 1970, while **Atlantic, Central, Midwest and Pacific** began in 1970–71. ([Wikipedia][2])
>
>So the complete set is **9 distinct division names**, not 10.
>
>### Chronology
>
>| English            | Slovenian               | Period       |
>| ------------------ | ----------------------- | ------------ |
>| Eastern Division   | Vzhodna divizija        | 1946–1970    |
>| Western Division   | Zahodna divizija        | 1946–1970    |
>| Atlantic Division  | Atlantska divizija      | 1970–present |
>| Central Division   | Centralna divizija      | 1970–present |
>| Midwest Division   | Srednjezahodna divizija | 1970–2004    |
>| Pacific Division   | Pacifiška divizija      | 1970–present |
>| Southeast Division | Jugovzhodna divizija    | 2004–present |
>| Northwest Division | Severozahodna divizija  | 2004–present |
>| Southwest Division | Jugozahodna divizija    | 2004–present |
>
>One thing I'd recommend for your project: **keep the English names as the canonical values in your scraped data and use this dictionary only for display/translation**. That way historical data such as `"Midwest Division"` doesn't get confused with the modern `"Northwest Division"` or `"Southwest Division"`. The NBA's current six divisions are Atlantic, Central, Southeast, Northwest, Pacific and Southwest. ([NBA][3])
>
>[1]: https://www.nba.com/news/history-season-review-1970-71?utm_source=chatgpt.com "Season Review: 1970-71 | NBA.com"
>[2]: https://en.wikipedia.org/wiki/Timeline_of_the_NBA?utm_source=chatgpt.com "Timeline of the NBA"
>[3]: https://www.nba.com/news/about?utm_source=chatgpt.com "About The NBA | NBA.com"
>

### Pogovor 5

**Jaz:**  
how do i save to CSV using dictwriter in python?

**ChatGPT:**  
>You use `csv.DictWriter` by:
>
>1. Opening the CSV file in write mode.
>2. Creating a `DictWriter` with the column names (`fieldnames`).
>3. Writing the header.
>4. Writing dictionaries as rows.
>
>For example:
>
>```python
>import csv
>
>dati = [
>    {"id": 1, "ime": "Lakers", "leto": 2025},
>    {"id": 2, "ime": "Celtics", "leto": 2025}
>]
>
>with open("podatki.csv", "w", newline="", encoding="utf-8") as datoteka:
>    writer = csv.DictWriter(
>        datoteka,
>        fieldnames=["id", "ime", "leto"]
>    )
>
>    writer.writeheader()
>    writer.writerows(dati)
>```
>
>This produces:
>
>```text
>id,ime,leto
>1,Lakers,2025
>2,Celtics,2025
>```
>
>### If you're writing one row at a time
>
>This is probably more relevant to your scraping project:
>
>```python
>with open("podatki.csv", "w", newline="", encoding="utf-8") as datoteka:
>    writer = csv.DictWriter(
>        datoteka,
>        fieldnames=["id", "ime", "leto"]
>    )
>
>    writer.writeheader()
>
>    for vrstica in podatki:
>        writer.writerow(vrstica)
>```
>
>Where each `vrstica` is a dictionary such as:
>
>```python
>{
>    "id": "LAL",
>    "ime": "Los Angeles Lakers",
>    "leto": 2025
>}
>```
>
>**Important:** the dictionary keys should correspond to your `fieldnames`. This makes `DictWriter` particularly convenient for your project because your scraping functions can return dictionaries with named columns, rather than having to worry about the exact column position.

**Jaz:**  
is there a way to add rows for each year i'm processing instead of overwriting the file every time?

**ChatGPT:**  
>Yes. Open the file in **append mode** (`"a"`) instead of write mode (`"w"`).
>
>The main thing to watch out for is the header: you only want to write `writeheader()` when the file is new/empty.
>
>For your project, you could do:
>
>```python
>import csv
>import os
>
>with open("podatki.csv", "a", newline="", encoding="utf-8") as datoteka:
>    writer = csv.DictWriter(
>        datoteka,
>        fieldnames=["id", "ime", "leto"]
>    )
>
>    if os.path.getsize("podatki.csv") == 0:
>        writer.writeheader()
>
>    writer.writerows(podatki)
>```
>
>Then you can process your years one after another:
>
>```python
>for leto in leta:
>    podatki = izlusci_podatke(soup, leto)
>
>    with open("podatki.csv", "a", newline="", encoding="utf-8") as datoteka:
>        writer = csv.DictWriter(
>            datoteka,
>            fieldnames=["id", "ime", "leto"]
>        )
>
>        if os.path.getsize("podatki.csv") == 0:
>            writer.writeheader()
>
>        writer.writerows(podatki)
>```
>
>So if you process **2020, 2021, 2022**, the rows for each year are simply added underneath the previous ones rather than replacing them.
>
>### An even cleaner approach
>
>Since you're scraping all the years in one run, I'd actually recommend opening the CSV **once** and then adding all the years:
>
>```python
>with open("podatki.csv", "w", newline="", encoding="utf-8") as datoteka:
>    writer = csv.DictWriter(
>        datoteka,
>        fieldnames=["id", "ime", "leto"]
>    )
>
>    writer.writeheader()
>
>    for leto in leta:
>        podatki = izlusci_podatke(soup, leto)
>        writer.writerows(podatki)
>```
>
>This gives you one clean CSV containing all years, and you don't need append mode at all.
>
>If you're running the scraper **separately for each year**, then `"a"` is the appropriate choice.


### Pogovor 6

**Jaz:**  
i will be using a jupyter notebook, are there any auxillary files that would be good to put in my gitignore?

**ChatGPT:**  
>Yes. For a Jupyter Notebook project, there are a few **generic auxiliary files/folders** that are usually worth ignoring in Git.
>
>A good general-purpose Python/Jupyter `.gitignore` would include:
>
>```gitignore
># Jupyter
>.ipynb_checkpoints/
>
># Python cache
>__pycache__/
>*.py[cod]
>*$py.class
>
># Virtual environments
>.venv/
>venv/
>env/
>ENV/
>
># Environment / secrets
>.env
>.env.*
>
># IDE/editor files
>.vscode/
>.idea/
>
># OS files
>.DS_Store
>Thumbs.db
>
># Python packaging
>*.egg-info/
>dist/
>build/
>
># Test / coverage caches
>.pytest_cache/
>.coverage
>htmlcov/
>
># Temporary files
>*.tmp
>*.temp
>```
>
>### For Jupyter specifically
>
>The most important one is:
>
>```gitignore
>.ipynb_checkpoints/
>```
>
>Jupyter automatically creates folders like:
>
>```text
>.ipynb_checkpoints/
>    my_notebook-checkpoint.ipynb
>```
>
>They're just autosave/checkpoint copies, so you normally **don't want them in Git**.
>
>### What you generally should NOT ignore
>
>Your actual notebook:
>
>```text
>analysis.ipynb
>```
>
>should usually be committed. That's the main source code/documentation of your work.
>
>Likewise, things such as:
>
>```text
>.py
>.csv
>requirements.txt
>README.md
>```
>
>should generally be committed **if they're part of the project and reproducibility matters**.
>
>One thing to think about separately is **generated data**. If your notebook produces large CSVs, images, models, etc., you may want to ignore those depending on whether they're source data or generated output.
