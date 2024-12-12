import os
import time
import csv
import urllib.parse

def read_csv(directory_path):
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"The path '{directory_path}' is not a valid directory.")
    
    scheme_hosts = set()
    parameters = set()

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if not file_name.endswith('.csv'):
            print(f"Skipping non-CSV file: {file_name}")
            continue

        print(f"Reading CSV file: {file_path}")
        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('Scheme and Host'):
                        scheme_hosts.add(row['Scheme and Host'])
                    if row.get('Parameter'):
                        parameters.add(row['Parameter'])
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")

    return list(scheme_hosts), list(parameters)

def read_xss(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def redirect_test(deeplink, xss_payload):
    if not deeplink:
        print("Error: Empty deeplink, Skipping test!")
        return
    encoded_payload = urllib.parse.quote(xss_payload, safe='') #urlencoding 
    test_url = f"{deeplink}{encoded_payload}"
    cmd = f'adb shell am start -W -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "{test_url}"'
    print(f"Executing command: {cmd}")
    os.system(cmd)

    time.sleep(5) #You can Adjust delay time 

    os.system(f"adb shell input keyevent 3")

def main():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_DIR = os.path.join(CURRENT_DIR, '..', '..', 'data', 'csv')
    XSS_DIR = os.path.join(CURRENT_DIR, '..', '..', 'XSS_payload.txt')

    print(f"CSV Directory: {CSV_DIR}")
    print(f"XSS Payload File: {XSS_DIR}")

    try:
        scheme_hosts, parameters = read_csv(CSV_DIR)
        print(f"Found {len(scheme_hosts)} scheme hosts and {len(parameters)} parameters.")
    except FileNotFoundError as e:
        print(e)
        return
    
    scheme_hosts, parameters = read_csv(CSV_DIR)
    xss_payloads = read_xss(XSS_DIR)

    for scheme_host in scheme_hosts:
        for parameter in parameters:
            deeplink = f"{scheme_host}?{parameter}="
            print(f"\nCreated deeplink: {deeplink}")

            for xss_payload in xss_payloads:
                print(f"\nTesting deeplink: {deeplink}")
                print(f"Scheme and Host: {scheme_host}")
                print(f"Parameter: {parameter}")
                print(f"XSS Payload: {xss_payload}")
                
                redirect_test(deeplink, xss_payload)
                
                time.sleep(2)

if __name__ == "__main__":
    main()