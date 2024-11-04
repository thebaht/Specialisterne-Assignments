import pandas as pd
from os import walk, makedirs
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

source_path = 'GRI_2017_2020.xlsx'
output_path = './pdf-files/'
makedirs('pdf-files', exist_ok=True)


df = pd.read_excel(source_path, index_col='BRnum')
df = df[df.Pdf_URL.notnull() == True]
df = df[['Pdf_URL', 'Report Html Address']] # removes irrelevant columns. Not necessary to do, but it only adds 0.01s and feels cleaner.

downloaded = set()
failed = set()
for (dirpath, dirnames, filenames) in walk(output_path):
    downloaded.update(map(lambda x: x[:-4], filenames))

def download(path, brnum, url, alt_url=pd.NA):
    try:
        with requests.get(url, timeout=20, stream=True) as response:
            response.raise_for_status()
            if not response.content[:4] == b'%PDF':
                raise Exception
            with open(path, 'wb') as pdf:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf.write(chunk)
                downloaded.add(brnum)
                print(f"{brnum}\t Downloaded")
    except Exception as e:
        if pd.isna(alt_url):
            failed.add(brnum)  
            print(f"{brnum}\t Failed")
        else:
            print(f"{brnum}\t Attempting alternative")
            download(path, brnum, alt_url)


with ThreadPoolExecutor() as executor:
    for i, row in df.head(9).iterrows():
        if i in downloaded:
            print(f"{i}\t Exists")
            continue
        path = output_path+i+'.pdf'
        executor.submit(download, path, i, row['Pdf_URL'], row['Report Html Address'])
   
    # ! use for updating ui as completed
    # futures = []
    # for i, row in df.head(9).iterrows():
    #     futures.append(executor.submit(download, path, row['Pdf_URL'], row['Report Html Address']))

    # for future in as_completed(futures):
    #     print(future.result())
    # 
        
        
print(f"\nDownloaded: \n{downloaded}")
print(f"\nFailed: \n{failed}")