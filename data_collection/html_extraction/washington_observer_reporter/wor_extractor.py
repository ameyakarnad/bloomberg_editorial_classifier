import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import pandas as pd 


def get_article(url):
    """
    Gets article content from URL
    Input : URL of article
    Output : Content in BeautifulSoup format
    """
    r = requests.get(url) 
    html_soup = BeautifulSoup(r.content, 'lxml')
    return html_soup


def extract_date(html_soup):
    """
    Extracts date of the article from content
    Input : Content in BeautifulSoup format
    Output : Date of the article
    """
    if html_soup.find('time', attrs = {'class':'asset-date'}) is not None:
        html_date = html_soup.find('time', attrs = {'class':'asset-date'}).text.strip()
        html_date = datetime.datetime.strptime(html_date, '%b %d, %Y')
    elif html_soup.find('time', attrs = {'class':'tnt-date'}) is not None:
        html_date = html_soup.find('time', attrs = {'class':'tnt-date'}).text.strip()
        html_date = datetime.datetime.strptime(html_date, '%b %d, %Y')
    elif html_soup.find('time', attrs = {'class':'text-muted'}) is not None:
        html_date = html_soup.find('time', attrs = {'class':'text-muted'}).text.strip()
        html_date = datetime.datetime.strptime(html_date, '%b %d, %Y')
    else:
        print("Whopop[s]")
        html_date = datetime.datetime.today()
    return html_date


def extract_heading(html_soup):
    """
    Extracts title of the article from content
    Input : Content in BeautifulSoup format
    Output : Title of the article
    """
    if html_soup.find('meta', attrs = {"name" : "title"}) is not None:
        return html_soup.find('meta', attrs = {"name" : "title"})["content"].strip()
    elif html_soup.find('title') is not None:
        main_title = html_soup.find('title').text.split("|")
        title =  main_title[0].strip()
    return title


def extract_keywords(html_soup):
    """
    Extracts keywords of the article from content
    Input : Content in BeautifulSoup format
    Output : Comma seperated keywords of the article
    """
    if html_soup.find('meta', attrs = {"name" : "news_keywords"}) is not None:
        return html_soup.find('meta', attrs = {"name" : "news_keywords"})["content"].strip()


def extract_content(html_soup):
    """
    Extracts text content of the article from content
    Input : Content in BeautifulSoup format
    Output : Text content of the article
    """
    list_pre = ["subscriber-preview", "subscriber-only"]
    text = ''
    if html_soup.findAll('div', attrs = {"itemprop" : "articleBody"}) is not None:
        temp_soup = html_soup.find('div', attrs = {"itemprop" : "articleBody"})
        for l in list_pre:
            if temp_soup.findAll('div', attrs = {'class':l}) is not None:
                soup = temp_soup.findAll('div', attrs = {'class':l})
                for s in soup:
                    text = text + ' ' + s.text
        if text == "" :
            soup = temp_soup.findAll('p')
            for s in soup:
                text = text + ' ' + s.text
    return text.strip()


def extract_author(html_soup):
    """
    Extracts Author of the article from content
    Input : Content in BeautifulSoup format
    Output : Author of the article
    """
    if html_soup.find('meta', attrs = {"name" : "author"}) is not None:
        author = html_soup.find('meta', attrs = {"name" : "author"})["content"].strip()
        if author: return author
    if html_soup.find('meta', attrs = {"name" : "twt-author-name"}) is not None:
        return html_soup.find('meta', attrs = {"name" : "twt-author-name"})["content"].strip()
    return ""


def main():
    """
    Reads the data file from the data/tagged/ directory from the path and returns saves content 
    for Washington Observer Reporter in csv format in the data/collected/ directory from the path
    """
    csv_data = pd.read_excel("data/tagged/sample-data.xlsx")
    wor_csv = pd.DataFrame(columns = ["URL","date","title","content","tag", "Editorial", "author"])
    for i, row in csv_data.iterrows():
        if row["Source"] == "Washington Observer Reporter":
            url = row["URL"]
            html_soup = get_article(url)
            art_date = extract_date(html_soup)
            title = extract_heading(html_soup)
            tag = extract_keywords(html_soup)
            text = extract_content(html_soup)
            author = extract_author(html_soup)
            wor_csv = wor_csv.append({"URL": url, "date": art_date, "title": title,"content": text,"tag": tag, "Editorial": row["Editorial"], "author": author}, ignore_index = True)
    wor_csv.to_csv("data/collected/washington_observer_reporter.csv", index=False)


if __name__ == "__main__":
    main()
