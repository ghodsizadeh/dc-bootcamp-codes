import json
import requests
from bs4 import BeautifulSoup
from save_to_s3 import save_file
import logging
def lambda_handler(event, context)->dict:
    """lambda handler that crawls csv file http://insideairbnb.com/get-the-data
    and saves it to S3 bucket


    Args:
        event (_type_): from AWS Lambda
        context (_type_): from AWS Lambda

    Returns:
        dict: {
        'statusCode': 200,
        'airbnb_status_code': r.status_code,
        'total_links': number of links crawled,
        "total_downloads": total number of files downloaded,
        "total_skips": total number of files skipped because they already exist,
        "total_errors": total number of errors
    }
    """   
    main_url = 'http://insideairbnb.com/get-the-data/'
    
    
    r = requests.get(main_url)
    soup = BeautifulSoup(r.content)
    links = soup.select('.table-striped a')
    
    
    total_downloads = 0
    total_errors = 0
    total_skips = 0
    
    
    for link in links:
        href = link['href']
        try:
            new = save_file(href) 
            if new:
                total_downloads += 1
            else:
                total_skips += 1
            
        except Exception as e:
            total_errors += 1 
            logging.error(e)
        

    return {
        'statusCode': 200,
        'airbnb_status_code': r.status_code,
        'total_links': len(links),
        "total_downloads": total_downloads,
        "total_skips": total_skips,
        "total_errors": total_errors
    }
