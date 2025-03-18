import os
import requests
import dotenv
dotenv.load_dotenv()

def main():
  response = requests.get(os.getenv('DATE_ENDPOINT'))
  dates = response.json()
  if not dates or len(dates) != 1:
    raise ValueError('No dates found')
  
  start_year = dates[0]['start'].split("-")[0]
  end_year = dates[0]['end'].split("-")[0]

  text_out = f'export const START_YEAR = {start_year}\nexport const END_YEAR = {end_year}'
  with open('src/dates.ts', 'w') as file:
    file.write(text_out)

if __name__ == "__main__":
  main()