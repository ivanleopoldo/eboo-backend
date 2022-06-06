from ebooklib import epub
from concurrent.futures import ThreadPoolExecutor
from core.assets import results_dir
import itertools
import re

chapterList = []
no_per_volume = 200
toc = []
filterFileName = "[#%<>&{{}}\/?*$:@+`|=;]"

# init
book = epub.EpubBook()
book.set_language("en")
_page_id = map('{:04}'.format, itertools.count(1))

# functions
def add_chapter(title, para):
    fileName = re.sub(filterFileName, "", title)
    fileName = fileName.replace("’", "'")

    c = epub.EpubHtml(
        file_name=f"chapter{next(_page_id)}.xhtml",
        title=fileName,
        lang="hr",
        content=f"<h2>{title}</h2>\n\n{para}",
        direction=book.direction,
    )
    book.add_item(c)
    chapterList.append(c)
    book.spine.append(c)

def make_intro_page(title: str, authors: list, url: str, coverimg=None):
    if len(authors) > 1:
        authors = ",".join(i for i in authors)
    elif len(authors) == 1:
        authors = authors[0]

    intro_html = '<div style="%s">' % ";".join(
        [
            "display: flex",
            "text-align: center",
            "flex-direction: column",
            "justify-content: space-between",
            "align-items: center",
        ]
    )

    intro_html += """
        <div>
            <h1>%s</h1>
            <h3>%s</h3>
        </div>
    """ % (
        title or "N/A",
        authors or "N/A",
    )

    if coverimg != None:
        intro_html += '<img id="cover" src="%s" style="%s">' % (
            "cover-img.jpg",
            "; ".join(
                [
                    "height: 30vh",
                    "object-fit: contain",
                    "object-position: center center",
                ]
            ),
        )

    intro_html += """
    <div>
        <br>
        <b>Source:</b> <a href="%s">%s</a><br>
        <i>Scraped by <b>Nove</b></i>
    </div>""" % (
        url,
        "novelfull",
    )

    intro_html += "</div>"

    return epub.EpubHtml(
        uid="intro", file_name="intro.xhtml", title="Intro", content=intro_html
    )

def create_book(title: str, authors: list, path: str, img: str, url: str):
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.set_title(title)
    # book.set_cover("cover-img.jpg", img, create_page=False)

    splitter = [
        chapterList[i: i + no_per_volume]
        for i in range(0, len(chapterList), no_per_volume)
    ]

    for i in splitter:
        volume_no = splitter.index(i)
        toc.append(
            (
                epub.Section(f"Volume {volume_no+1}"),
                tuple(splitter[volume_no]),
            )
        )

    if len(authors) > 1:
        for j in authors:
            book.add_author(j)
    elif len(authors) <= 1:
        book.add_author(authors[0])

    intro_page = make_intro_page(title, authors, url, img)

    book.add_item(intro_page)

    book.toc = tuple(toc)
    book.spine = [intro_page, "nav"] + chapterList

    epub_path = path + "\\" + title + ".epub"
    epub.write_epub(epub_path, book)

    return epub_path

def start_download(title: str, url: str = None):
    add_chapter("test", "hello")
    add_chapter("test1", "hello1")
    add_chapter("test2", "hello2")
    add_chapter("test3", "hello3")
    add_chapter("test4", "hello4")
    create_book(title, ["me"], results_dir, None, "youtube.com")