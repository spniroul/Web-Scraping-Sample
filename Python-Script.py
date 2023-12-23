from bs4 import BeautifulSoup
import requests
from csv import writer

#Web-Scraping AEA Website using Python
#Extracting Volume Number, Issue Page Links and Issue Dates
#For all available Issues on the website
#Importing webpage content
html_text = requests.get('https://www.aeaweb.org/journals/aer/issues').text
soup = BeautifulSoup(html_text, 'html.parser')
#Begin----Extracting webpage information
#Volume Number, Issue Page Links and Issue Dates
volumes = soup.find_all('section', class_='journal-issues-expandable')
for volume in volumes:
  volume_numbers = volume.find_all('div', class_='issue-item')
  #Creating a csv file to write information
  with open('aea.csv', 'w') as f:
    thewriter = writer(f)
    header = ['volume', 'link', 'issue_date']
    thewriter.writerow(header)
    #Scraping required data from HTML tags
    for volume_number in volume_numbers:
        # volume_nums = volume_number.find('span',class_='news-item news-type').text
        # volume_descriptions = volume_number.find_all('div')
        # for volume_description in volume_descriptions:
            volume_info = volume_number.find('a').text.split(" (")
            volume_link = volume_number.a['href'] \
              .replace('/issues','https://www.aeaweb.org/issues')
            volume_num = volume_info[0]
            volume_date = volume_info[1].replace(")","")
            print_info = [volume_num, volume_date, volume_link]
            print(print_info)
            thewriter.writerow(print_info)

#Web Scraping AEA website
#Obtaining Volume Info, Issued Dates, Article Titles, Authors, Page Info,
#Download Link, JEL Codes and JEL Description for all available articles in the website

#Requesting webpage content
html_text_issues = requests.get('https://www.aeaweb.org/journals/aer/issues').text
soup = BeautifulSoup(html_text_issues, 'html.parser')

#Extracting Information......
issues = soup.find_all('div', class_='issue-item')

#Creating a csv file to write data
with open('aea2.csv', 'w') as f:
  thewriter = writer(f)
  header = ['Volume-Issue_Number', 'Issue Date', 'Title', 'Authors', 'Page No.', 'Link',
            'JEL Code', 'JEL Code Description']
  thewriter.writerow(header)

  for issue in issues:
    # volume_numbers = issue.find_all('article')
    # for volume_number in volume_numbers:
    #     volume_description = volume_number.find_all('div')
    #     for subvolume in (volume_description):
    #       #Extracting Issue Page Link
          issue_link = issue.a['href'].replace('/issues','https://www.aeaweb.org/issues')
          #Begin----Extract from Specific Issue Pages
          html_text_articles = requests.get(issue_link).text
          soup2 = BeautifulSoup(html_text_articles, 'html.parser')
          #Locating Specific Articles
          articles = soup2.find("section", class_="journal-article-group").find_all('a')
          # for a1 in a1s:
          #   titles = a1.find_all('h3', class_= 'title')
          for article in articles:
                link_articles = article['href'] \
                  .replace('/articles','https://www.aeaweb.org/articles')
                article_page = requests.get(link_articles).text
                soup3 = BeautifulSoup(article_page, 'html.parser')
                #Extracting article info
                a2s = soup3.find_all('section', \
                                     class_ = "primary article-detail journal-article")
                for a2 in a2s:
                    #Extracting Article Title
                    title_name = (a2.find('h1', class_ = 'title').text)
                    if title_name == "Front Matter" \
                      or title_name == "Report of Independent Auditor" \
                      or title_name == "A Special Introduction":
                        break
                    #Extracting Author Name
                    attributions = a2.find_all('ul', class_ = 'attribution')
                    author_name= ""
                    for attribution in attributions:
                      a3s = attribution.find_all('li', class_ = "author")
                      for a3 in a3s:
                        a = (a3.text).strip()
                        author_name = author_name  + a + "\n"
                      author_name = (author_name.strip()).replace("\n",", ")
                      #Extracting Volume Info
                      volume_infos = soup3.find("div", class_="journal").find_next('div', class_="journal").text
                      volume_info, issue_number, date = volume_infos.rsplit(',')
                      volume_info = volume_info.strip() +","+ issue_number.strip()
                      date = date.strip()
                      #Extracting Page Numbers, Download Link
                      pages = soup3.find('div', class_="pages").text
                      download_link = a2.find('section', class_='download').a['href'].replace('/articles','https://www.aeaweb.org/articles')
                      #Extracting Jel Code and Description
                      jels = soup3.find_all('ul', class_='jel-codes')
                      code_list = []
                      description_list =[]
                      for jel in jels:
                        extract = jel.find("li").text
                        extract = extract.split("\n")
                        extract_filtered = []
                        for i in range(0,len(extract)):
                          if extract[i].strip() != "":
                            extract_filtered.append(extract[i])
                        for i in range(0,len(extract_filtered), 2):
                          code_list.append(extract_filtered[i].strip())
                          description_list.append(extract_filtered[i+1].strip())
                        code = ", ".join(code_list)
                        description = ",".join(description_list)
                      #Writing into csv file
                      print_info = [volume_info, date, title_name, author_name, pages,
                                    download_link, code, description]
                      print(print_info)
                      thewriter.writerow(print_info)
