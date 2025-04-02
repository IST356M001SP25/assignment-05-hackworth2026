from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    return 

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    return 

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    return


if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

