import requests
import csv
from bs4 import BeautifulSoup


def get_groups(url):
    found_groups = []

    page = requests.get(url)
    group_soup = BeautifulSoup(page.content, 'html.parser')

    all_details = group_soup.find_all('td', class_="details")
    for detail in all_details:
        found_groups.append(detail.find('a', href=True)['href'])

    return found_groups


if __name__ == '__main__':

    SITE = 'https://www.nami.org/'
    NAMI_CONNECTION = SITE + 'Find-Your-Local-NAMI/Affiliate/Programs?classkey=a1x36000003TN9TAAW'
    NAMI_FAMILY = SITE + 'Find-Your-Local-NAMI/Affiliate/Programs?classkey=a1x36000003TN9LAAW'

    output_rows = []
    emails = []

    groups = get_groups(NAMI_CONNECTION)
    groups = groups + get_groups(NAMI_FAMILY)

    for group in groups:
        group_page = requests.get(SITE + group)
        soup = BeautifulSoup(group_page.content, 'html.parser')

        email_div = soup.find('div', class_="contact-row-email")

        # Make sure page has an email section
        if email_div is None:
            continue

        email_node = email_div.find('a', href=True)

        # Make sure email section has an email
        if email_node is None:
            continue

        email = email_node['href']
        email = email.replace("mailto:", "")

        name_div = soup.find('div', class_="contact-row-name")
        name = ""

        if name_div is not None:
            name = name_div.text

        if email not in emails:
            print([name, email])
            output_rows.append([name, email])
            emails.append(email)

    with open('nami_contact_info.csv', 'w', newline='') as csvfile:
        header = ['Name', 'Email']
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in output_rows:
            writer.writerow(row)
