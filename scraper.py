import os
import requests
from bs4 import BeautifulSoup 


# download images from google search image
Google_Image = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

usr_agnt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
} 

Image_Folder = 'Pictures'

def main():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    download_images()

def download_images():
    data = input('What do you want to download ?: ')
    num_images = int(input('How many images do you want? : '))
    
    print('Start Searching....')
    
    search_url = Google_Image + 'q=' + data 
    
    
    response = requests.get(search_url, headers=usr_agnt)
    html = response.text 
   

    soup = BeautifulSoup(html, 'html.parser') 
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})
    
    count = 0
    imagelinks= []
    for result in results:
        try:
            link = result['data-src']
            imagelinks.append(link)
            count = count + 1
            if (count >= num_images):
                break
            
        except KeyError:
            continue
    
    print(f'Found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)
        
        imagename = Image_Folder + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Download Finished!!')
    

if __name__ == '__main__':
    main()