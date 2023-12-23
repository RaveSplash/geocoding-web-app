import requests
import json
from bs4 import BeautifulSoup


def scrap_page(text):
    soup = BeautifulSoup(text, 'html.parser')

    
    return soup


def main():
    # extra multiple page data until none is available with a reasonable amount of page
    store_set = []
    for page_index in range(1,10):
        page_url = f"https://zuscoffee.com/category/store/melaka/page/{page_index}/"
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = scrap_page(response.text)
            parent_element = soup.find('div', class_='ecs-posts elementor-posts-container elementor-posts elementor-grid elementor-posts--skin-archive_custom')

            if parent_element:               
                # Find all elements with data-elementor-type="loop"
                elements = soup.find_all(attrs={'data-elementor-type': 'loop'})


                    #parse through parent element which is the grid every element to scrap it's name and address
                for element in elements:
                    current_object ={"name": None, "address": None}
                    containers = element.find_all('div', class_='elementor-widget-container')
                    for container in containers:
                        extra_hatom_div = container.find('div', class_='extra-hatom')
                        if extra_hatom_div:
                            address_p = container.find("p")
                            address = address_p.text.strip() if address_p else None
                            if address is not None:
                                current_object['address'] = address
                        else:
                            name_p = container.find('p', class_='elementor-heading-title elementor-size-default')
                            name = name_p.text.strip() if name_p else None
                            if name is not None:
                                current_object['name'] = name
                
                    
                    if current_object['name'] is not None and current_object['address'] is not None:
                        # Append the current object to the list
                        print("current object ",current_object)
                        store_set.append(current_object)
                    print('---')  # Separate entries for clarity

                
                print(f'Scraping of page {page_url} completed.')
        else: break
    


   
    json_data = json.dumps(store_set)

    print(json_data)

if __name__ == "__main__":
    main()

        # addresses = soup.select('elementor-widget-container')
        # Store the scraped data in your database (choose a suitable database library)
        # Example using SQLite:
        # import sqlite3

        # conn = sqlite3.connect('your_database.db')
        # cursor = conn.cursor()

        # for name, address in zip(names, addresses):
        #     # Insert data into your database
        #     cursor.execute('INSERT INTO your_table (name, address) VALUES (?, ?)', (name.text, address.text))

        # conn.commit()
        # conn.close()