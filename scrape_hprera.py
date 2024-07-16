import requests
from bs4 import BeautifulSoup
import pandas as pd
import certifi

base_url = "https://hprera.nic.in/PublicDashboard"
details_base_url = "https://hprera.nic.in/"
ca_bundle_path = certifi.where()  # Use certifi's CA bundle

def get_project_links():
    response = requests.get(base_url, verify=ca_bundle_path)
    soup = BeautifulSoup(response.content, "html.parser")

    project_links = []
    projects = soup.find_all("a", class_="card-title", limit=6)
    for project in projects:
        link = project['href']
        project_links.append(details_base_url + link)
    
    return project_links

def get_project_details(url):
    response = requests.get(url, verify=ca_bundle_path)
    soup = BeautifulSoup(response.content, "html.parser")

    details = {}
    labels = ["GSTIN No", "PAN No", "Name", "Permanent Address"]

    for label in labels:
        label_tag = soup.find("td", text=label)
        if label_tag:
            value_tag = label_tag.find_next_sibling("td")
            details[label] = value_tag.text.strip() if value_tag else None
        else:
            details[label] = None
    
    return details

def main():
    project_links = get_project_links()
    project_details_list = []

    for link in project_links:
        details = get_project_details(link)
        project_details_list.append(details)

    df = pd.DataFrame(project_details_list)
    return df

if __name__ == "__main__":
    df = main()
    print(df)

