def get_a_secret_key(length: int = 32):
    import os
    import secrets
    API_KEY = secrets.token_urlsafe(32)
    return API_KEY

def get_df_from_dse(format: str = "json", server: str = "cloud"):
    
    import requests
    import pandas as pd
    from io import StringIO

    if server == "local":
        url = "http://127.0.0.1:5000/scrape" # web server is on local machine
    else:
        url = "https://dse-scraper.onrender.com/scrape" # web server is on cloud
    
    headers = {"x-api-key": "9ia86sVRUrWu1uIRZUfKxncrJWewjA_jdzp_B8vEtm0"}
    payload = {"format": "cs"}

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.ok:
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                df = pd.read_json(StringIO(response.text))
                print("Parsed as JSON")
                print(df.head())
            elif "text/csv" in content_type:
                df = pd.read_csv(StringIO(response.text))
                print("Parsed as CSV")
                df = pd.read_csv(StringIO(response.text))  # if CSV
                print(df.head())
            else:
                print("Unknown format:", content_type)
        else:
            print("Error:", response.status_code, response.text)
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g. 404, 500 errors
    
    except requests.exceptions.ConnectionError:
        print("ConnectionError occured: Failed to connect to the server.")
    
    except requests.exceptions.Timeout:
        print("The request timed out.")
    
    except requests.exceptions.RequestException as err:
        print(f"An unknown error occurred: {err}")

if __name__ == '__main__':
    # print(get_a_secret_key())
    get_df_from_dse(format="csv", server="local")