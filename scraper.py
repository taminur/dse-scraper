import requests
import pandas as pd
from lxml import html

def fetch_latest_share_price_from_dsebd() -> pd.DataFrame:
    '''
    This function extracts data from "https://www.dsebd.org/latest_share_price_scroll_l.php" and returns a pandas dataframe if successfull.
    '''

    url = "https://www.dsebd.org/latest_share_price_scroll_l.php"
    # connect to dsebd.org
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        last_update = tree.xpath('//*[@id="RightBody"]/div[1]/div[1]/h2[1]')[0].text.strip().split('On')[-1].strip()
        dt = pd.to_datetime(last_update, format="%b %d, %Y at %I:%M %p")
        print(f'last update on: {last_update}')
        
        try:
            # Extract tables using pandas (it uses lxml under the hood)
            tables = pd.read_html(response.content)
            
            # select the target table
            df = tables[-2]
            df['date'] = dt.strftime('%Y-%m-%d %H:%M:%S')
            print('Date added successfully!')
        except:
            print('Date failed to add')
        return df
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g. 404, 500 errors
        return pd.DataFrame()
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server.")
        return pd.DataFrame()
    except requests.exceptions.Timeout:
        print("The request timed out.")
        return pd.DataFrame()
    except requests.exceptions.RequestException as err:
        print(f"An unknown error occurred: {err}")
        return pd.DataFrame()

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    '''
    to drop the unnessary columns. rename the columns and reorder the columns.
    '''
    # delete unnessary columns
    if df is not None:
        try:
            df.drop(['#', 'LTP*', 'CHANGE'], axis=1, inplace=True)
        except:
            print('columns not deleted, probably already deleted\n')

        df.rename(columns={'TRADING CODE':'symbol','CLOSEP*':'close' ,'YCP*':'open', 'VALUE (mn)':'value_in_mn'}, inplace=True)
        df.columns = df.columns.str.lower()
    # reorder the column data
        df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'trade', 'value_in_mn']]

    return df

def collect_from_dsebd() -> pd.DataFrame:
    '''
    collect latest share price from dsebd.org and return the cleaned the data as pandas dataframe
    '''
    return clean_data(fetch_latest_share_price_from_dsebd())

if __name__ == '__main__':
    '''
    this is used for testing purpose
    '''
    df = fetch_latest_share_price_from_dsebd()
    print(df.head())

    df1 = clean_data(df)
    print(df1.head())
    
    # df = pd.DataFrame()
    # print(df)
    # print('is empty')
    # print(df.empty)