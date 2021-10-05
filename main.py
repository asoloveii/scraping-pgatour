import requests
import json
import csv
import time

from bs4 import BeautifulSoup


headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
  "Accept": "*/*"
}


def get_data():
  urls = ["https://www.pgatour.com/players.html", "https://www.pgatour.com/champions/players.html"] 

  data = []

  with open("data/data.csv", "w") as file:
    writer = csv.writer(file)

    writer.writerow(
      (
        "First name",
        "Last name",
        "Date of birth",
        "County of birth",
        "Place of birth"
      )
    )

  for url in urls:
    req = requests.get(url=url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(req.text, "lxml")

    letters = soup.find("div", class_="viewport").find("div", class_="overview").find_all("ul", class_="ul-inline items")
    for letter in letters[:1]:    # so as not to waste time

      items = letter.find_all("li", class_="player-card active")
      for item in items:
        item_url = "https://www.pgatour.com/" + item.find("a", class_="player-link").get("href")

        r = requests.get(url=item_url, headers=headers, allow_redirects=True)
        source = BeautifulSoup(r.text, "lxml")

        info = source.find("div", class_="player-section-profile-module").find_all("div", class_="s-col__row")

        try:
          item_firstname = item.find("span", class_="player-firstname").text
        except:
          item_firstname = "No first name"

        try:
          item_lastname = item.find("span", class_="player-surname").text
        except:
          item_lastname = "No last name"

        try:
          for i in info:
            if i.find("p", class_="s-bottom-text").text == "Birthday":
              item_dob = i.find("p", class_="s-top-text").text
        except:
          item_dob = "No date of birth"

        try:
          item_country_birth = item.find("div", class_="player-country-title").text 
        except:
          item_dob = "No county of birth"

        try:
          for i in info:
            if i.find("p", class_="s-bottom-text").text == "Birthplace":
              item_place_birth = i.find("p", class_="s-top-text").text
        except:
          item_place_birth = "No place birth"

        data.append(
          {
            "First name": item_firstname,
            "Last name": item_lastname,
            "DOB": item_dob,
            "Country of birth": item_country_birth,
            "Place of birth": item_place_birth
          }
        )

        with open("data/data.csv", "a") as file:
          writer = csv.writer(file)

          writer.writerow(
            (
              item_firstname,
              item_lastname,
              item_dob,
              item_country_birth,
              item_place_birth,
            )
          )

        time.sleep(1)
        print("[INFO] Another one!")

      time.sleep(1)
      print("[INFO] Letter completed!")

  with open("data/data.json", "a", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

  print("[INFO] Completed successfuly!")


def main():
  get_data()


if __name__ == "__main__":
  main()
