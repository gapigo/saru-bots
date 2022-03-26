from os import path
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from .convert import romajiToJapanese
from urllib.parse import quote
from html2image import Html2Image

hti = Html2Image()
hti.output_path = path.join(Path(__file__).parent.absolute(), f'images')

def get_html_from_url(url: str):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')


def download_image(url: str):
    with open(path.join(Path(__file__).parent.absolute(), f'images/nihongoichiban.gif'), "wb") as f:
        f.write(requests.get(url).content)


def search_on_nihongoichiban(searched_kanji: str, jlpt='n5') -> dict:
    # n5, n4 and n3
    url_dict = {
        "n5": "https://nihongoichiban.com/2011/04/10/complete-list-of-kanji-for-jlpt-n5/",
        "n4": "https://nihongoichiban.com/2011/05/22/complete-list-of-kanji-for-the-jlpt-n4/",
        "n3": "https://nihongoichiban.com/2014/07/22/complete-list-of-kanji-for-jlpt-n3/"
    }
    soup = get_html_from_url(url_dict[jlpt])
    rows = soup.find_all("tr")
    rows.pop(0)
    rom_katakana = ''
    for row in rows:
        kanji_column = row.findChildren()[1]
        kanji_link = kanji_column.findChildren()[0]
        if kanji_link.getText() == searched_kanji:
            code = row.findChildren()[0].getText().strip()
            # https://nihongoichiban.com/2011/04/11/%e6%82%aa/
            # ['2011', '04', '11', '%e6%82%aa', '']
            link = kanji_link['href']
            soup = get_html_from_url(link)
            try:
                table = soup.find_all("tbody")[0]
                rom_rows = table.find_all("td")
                meaning = rom_rows[1].getText()
                rom_katakana = rom_rows[3].getText()
                rom_hiragana = rom_rows[5].getText()
            except IndexError:
                div = soup.find_all("div", class_="entry-content")[0]
                paragraphs = div.find_all("p")
                meaning = ''
                rom_katakana = ''
                rom_hiragana = ''

                def get_only_alpha(text: str):
                    res = ''
                    for char in text:
                        if char.isalpha():
                            res += char
                    return res

                for p in paragraphs:
                    if len(strong := p.findChildren('strong')) != 0:
                        strong = strong[0].getText()
                        strong = get_only_alpha(strong)
                        if strong.lower() == "meaning":
                            meaning = p.getText().split(':')[1].strip()
                            continue
                        if strong.lower() == "onyomi":
                            rom_katakana = p.getText().split(':')[1].strip()
                            continue
                        if strong.lower() == "kunyomi":
                            rom_hiragana = p.getText().split(':')[1].strip()
                            break
            finally:
                rom_katakana = rom_katakana.replace('(', '•').replace(')', '').replace(',', '、')
                rom_hiragana = rom_hiragana.replace('(', '•').replace(')', '').replace(',', '、')
                rom_katakana = romajiToJapanese(rom_katakana, use_hiragana=False)
                rom_hiragana = romajiToJapanese(rom_hiragana, use_hiragana=True)
                meaning = meaning.lower()

            link_info = link.split('nihongoichiban.com/')[1].split('/')
            year = link_info[0]
            month = link_info[1]
            img_url = f'https://nihongoichibandotcom.files.wordpress.com/{year}/{month}/{code.lower()}.gif'
            download_image(img_url)
            return {
                'kanji': searched_kanji,
                'plataform': 'nihongoichiban',
                'onyomi': rom_katakana,
                'kunyomi': rom_hiragana,
                'meaning': meaning,
                'link': link
            }
    return None


def search_on_romajidesu(searched_kanji: str) -> dict:
    url = f"http://www.romajidesu.com/kanji/{quote(searched_kanji)}"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    div_kanji_info = soup.find_all("div", class_="kanji_meaning")[0]
    meaning = div_kanji_info.findChildren()[0].findChildren()[1].getText()
    meaning = meaning.strip().replace(';', ',').lower()

    onyomis = div_kanji_info.find_all("div", class_="on_yomi")[0]
    kunyomis = div_kanji_info.find_all("div", class_="kun_yomi")[0]

    def get_kana(kanas):
        def get_rid_of_romanji(text):
            final = ''
            for char in text:
                if not char.isascii() and char not in 'kō':
                    final += char
            return final

        kana = ''
        for k in kanas:
            text: str = k.getText().replace(" ", "").replace("\n", "").replace(".", "•").replace("·", "")
            if text != "":
                kana += f'{get_rid_of_romanji(text)}、'
        return kana[:-1]

    onyomi = get_kana(onyomis)
    kunyomi = get_kana(kunyomis)

    str_file = '<html>'
    for script in soup.find_all("script"):
        content = str(script)
        if 'uniconsent' not in content:
            str_file += content + '\n\n'
    str_file += str(soup.find_all("div", class_="kanji_strokes_order")[0])
    str_file += '</html>'

    html_path = str(path.join(Path(__file__).parent.absolute(), f'html/kanji_page.html'))
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(str_file)

    div_kanji_info = soup.find_all("div", class_="kanji_info")[0]
    stroke_count = int(div_kanji_info.findChildren("a")[0].findChildren("b")[0].getText())
    width = 10 if stroke_count >= 10 else stroke_count
    height = 1 if stroke_count <= 10 else (2 if stroke_count <= 20 else 3)
    hti.screenshot(
        html_file=html_path, save_as='romajidesu.png', size=(width * 58 + 20, height * 58 + 20)
    )
    return {
        'kanji': searched_kanji,
        'plataform': 'romajidesu',
        'onyomi': onyomi,
        'kunyomi': kunyomi,
        'meaning': meaning,
        'link': url
    }


def search_kanji(kanji: str):
    # kanji = str(input('Enter with kanji: ')).strip()
    jlpts = ['n5', 'n4', 'n3']
    for jlpt in jlpts:
        yield f'Searching on {jlpt} nihongoichiban...'
        r = search_on_nihongoichiban(kanji, jlpt)
        if r:
            yield r
            return

    yield f'Searching on romajidesu...'
    yield search_on_romajidesu(searched_kanji=kanji)
    return
