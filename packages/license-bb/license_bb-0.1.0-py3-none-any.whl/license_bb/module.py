import os
import json
import platform
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding
import requests
import base64
from tzlocal import get_localzone
from .AES_utils import generate_aes_key
from .AES_utils import Aencrypt, Adecrypt
import schedule
import time
from datetime import datetime
from dateutil import parser

# Constants
CLIENT_CONFIG_DIRECTORY = "bbLicenseUtils"
LICENSE_DIRECTORY = "license"


def get_org_ids(base_directory):
    """
    Retrieves all folder names (org_id) in the specified base directory.

    Args:
        base_directory (str): The path to the base directory containing organization folders.

    Returns:
        list: A list of organization IDs (folder names).
    """
    try:
        org_ids = [name for name in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, name))]
        return org_ids
    except Exception as e:
        print(f"Error retrieving org IDs: {e}")
        return []


def schedule_sync():
    """
    Schedules the sync function to run for each org_id every 20 minutes.
    """
    org_ids = get_org_ids(CLIENT_CONFIG_DIRECTORY)
    for org_id in org_ids:
        schedule.every(20).minutes.do(sync, org_id=org_id)


def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_key(key, filepath, is_private=False):
    if is_private:
        encoding = serialization.Encoding.PEM
        format = serialization.PrivateFormat.PKCS8
        encryption_algorithm = serialization.NoEncryption()
    else:
        encoding = serialization.Encoding.PEM
        format = serialization.PublicFormat.SubjectPublicKeyInfo
        encryption_algorithm = serialization.NoEncryption()

    with open(filepath, 'wb') as f:
        f.write(
            key.private_bytes(
                encoding=encoding,
                format=format,
                encryption_algorithm=encryption_algorithm
            ) if is_private else key.public_bytes(
                encoding=encoding,
                format=format
            )
        )


def aes_encrypt(data, key):
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data


def rsa_encrypt(data, public_key):
    encrypted_data = public_key.encrypt(
        data.encode('utf-8'),
        padding.PKCS1v15()
    )
    return base64.b64encode(encrypted_data).decode('utf-8')


def checkValidKey(license_key, base_url):
    """
    Checks if the provided license key is valid by communicating with the license server.

    Args:
        license_key (str): The license key to validate.
        base_url (str): The base URL of the license server.

    Returns:
        dict: The response from the license server indicating the validity of the license key.

    Raises:
        ValueError: If the provided parameters are invalid.
        requests.RequestException: If there is an issue with the HTTP request.
        KeyError: If the response from the server is not as expected.
    """
    if not license_key or not isinstance(license_key, str):
        raise ValueError("Invalid LICENSE_KEY provided. It must be a non-empty string.")

    if not base_url or not isinstance(base_url, str):
        raise ValueError("Invalid BASE_URL provided. It must be a non-empty string.")

    # Endpoint for validating the license key
    validate_key_endpoint = f"/sdk/api/keyCheck/{license_key}"

    try:
        # Make the request to the license server
        response = requests.get(base_url + validate_key_endpoint)

        # Parse the response JSON
        response_data = response.json()
        if "message" not in response_data:
            raise KeyError("Unexpected response format from license server.")
        if "resultCode" not in response_data:
            raise KeyError("Unexpected response format from license server.")

        return response_data

    except requests.RequestException as e:
        raise requests.RequestException(f"HTTP request to license server failed: {str(e)}")


def init(base_url, license_key, client_details):
    """
    Initializes the client's configuration by creating the init file and generating necessary keys.

    Args:
        license_key (str): License key received by the user on requesting or subscribing.
        client_details (dict): Dictionary containing 'licenseKey', 'email', 'orgId', 'phone', 'userName', 'orgName', 'baseUrl (License server API base URL without the API endpoints)', 'assignType', and 'serverNameAlias' (optional).

    Returns:
        dict: Combined information including client and system details.
    """
    required_fields = ['email', 'orgId', 'phone', 'userName', 'orgName', 'serverNameAlias',
                       'assignType']
    for field in required_fields:
        if field not in client_details:
            raise ValueError(f"Missing required client detail: {field}")

    if not base_url or not isinstance(base_url, str):
        raise ValueError("Invalid BASE_URL provided. It must be a non-empty string.")

    if not license_key or not isinstance(license_key, str):
        raise ValueError("Invalid LICENSE_KEY provided. It must be a non-empty string.")

    license_valid = checkValidKey(license_key, base_url)
    if license_valid["resultCode"] != 1:
        raise ValueError("Invalid LICENSE_KEY provided.")

    device_type = ""
    # Type of Device Start
    if os.path.exists("/proc/1/cgroup"):
        try:
            with open("/proc/1/cgroup", "r") as file:
                data = file.read()
                if "/docker/" in data:
                    device_type = "Docker"
                elif "/machine.slice/machine-qemu" in data:
                    device_type = "Virtual Machine"
                elif "/machine.slice/machine-vmware" in data:
                    device_type = "Virtual Machine"
                else:
                    device_type = "Server"
        except Exception as err:
            raise Exception("Error reading /proc/1/cgroup to identify MACHINE")
    else:
        device_type = "Server"

    system_details = {
        "osType": platform.system(),
        "machine": platform.machine(),
        "deviceId": hex(uuid.getnode()),
        "deviceType": device_type,
        "browser": ""
    }
    combined_details = client_details.copy()
    combined_details["licenseKey"] = license_key
    combined_details["baseUrl"] = base_url
    combined_details["device"] = system_details

    # Generate AES key
    aes_key = generate_aes_key()
    combined_details["secretId"] = aes_key
    # Get the local timezone
    local_timezone = get_localzone()

    # Get the current time in the local timezone
    current_time = datetime.now(local_timezone)

    # Format the datetime string
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
    combined_details["dateTime"] = formatted_time
    try:
        combined_details["timeZone"] = str(local_timezone)
    except:
        combined_details["timeZone"] = ""
        # Generate RSA keys
    private_key, public_key = generate_rsa_keys()
    org_path = os.path.join(CLIENT_CONFIG_DIRECTORY, client_details['orgId'])
    if not os.path.exists(org_path):
        os.makedirs(org_path)
    save_key(private_key, os.path.join(org_path, 'private.pem'), is_private=True)
    save_key(public_key, os.path.join(org_path, 'public.pem'))

    # Save combined details to init file
    init_filepath = os.path.join(org_path, 'init.json')
    # os.makedirs(CLIENT_CONFIG_DIRECTORY, exist_ok=True)
    with open(init_filepath, 'w') as f:
        json.dump(combined_details, f, indent=4)

    do_exchange(combined_details)
    return combined_details


def do_exchange(combined_details):
    """
    Exchanges the client's public key with the license server and retrieves the server's public key.

    Args:
        org_id (str): Unique ID for each organization.
        client_details (dict): Full configuration from the init() function.

    Returns:
        dict: Response from the licensing server.
    """
    org_path = os.path.join(CLIENT_CONFIG_DIRECTORY, combined_details['orgId'])
    public_key_path = os.path.join(org_path, 'public.pem')
    with open(public_key_path, 'rb') as f:
        public_key_data = f.read()

    c_d_exchange = {
        "licenseKey": combined_details['licenseKey'],
        "email": combined_details['email'],
        "orgId": combined_details['orgId'],
        "assignType": combined_details['assignType']
    }

    c_d_exchange['key'] = public_key_data.decode('utf-8')

    response = requests.post(
        f"{combined_details['baseUrl']}/sdk/api/doExchange",
        json=c_d_exchange
    )

    if response.status_code == 200:
        server_public_key = response.json()['data']
        server_public_key_path = os.path.join(org_path, 'server.pem')
        with open(server_public_key_path, 'w') as f:
            f.write(server_public_key)
        get_license(combined_details)
    else:
        raise Exception("Failed to exchange keys with the license server.")


def get_license(client_details):
    """
    Retrieves the available/assigned license for the client from the license server.

    Args:
        org_id (str): Unique ID for each organization.
        client_details (dict): Full configuration from the init() function.

    Returns:
        dict: Response from the licensing server.
    """
    license_valid = checkValidKey(client_details["licenseKey"], client_details["baseUrl"])
    if license_valid["resultCode"] != 1:
        raise ValueError("Invalid LICENSE_KEY provided.")

    aes_key = client_details["secretId"]
    # Encrypt client details with AES
    client_details_data = json.dumps(client_details)
    encrypted_client_details = Aencrypt(client_details_data, aes_key)
    org_path = os.path.join(CLIENT_CONFIG_DIRECTORY, client_details['orgId'])
    # Read server's public key
    with open(os.path.join(org_path, 'server.pem'), 'rb') as f:
        server_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    # Encrypt AES key with server's public key
    encrypted_aes_key = rsa_encrypt(aes_key, server_public_key)
    response = requests.post(
        f"{client_details['baseUrl']}/sdk/api/generateLicense",
        json={
            "licenseKey": client_details["licenseKey"],
            "client": encrypted_client_details,
            "key": encrypted_aes_key
        }
    )

    if response.status_code == 200:
        license_data = response.json()['data']
        org_license_path = os.path.join(LICENSE_DIRECTORY, client_details['orgId'])
        if not os.path.exists(org_license_path):
            os.makedirs(org_license_path)
        license_filepath = os.path.join(org_license_path, 'license.pem')  #add in org id

        with open(license_filepath, 'w') as f:
            f.write(license_data)
        return response.json()
    else:
        raise Exception("Failed to retrieve license from the license server.")


def extract_license(org_id):
    """
    Extracts the license information for a given organization ID by decrypting the license file.

    Args:
        org_id (str): Unique ID for each organization.

    Returns:
        dict: Decrypted license information.
    """
    org_license_path = os.path.join(LICENSE_DIRECTORY, org_id)
    license_filepath = os.path.join(org_license_path, 'license.pem')
    try:
        if not os.path.exists(license_filepath):
            raise FileNotFoundError("License file not found. Please run get_license() first.")

        with open(license_filepath, 'rb') as f:
            encrypted_license_data = f.read()

        json_encrypted_license_data = json.loads(encrypted_license_data)
        # Check if 'sign' and 'enc' fields exist
        if 'sign' not in json_encrypted_license_data or 'enc' not in json_encrypted_license_data:
            raise ValueError("Invalid license file format. Missing required fields.")

        org_path = os.path.join(CLIENT_CONFIG_DIRECTORY, org_id)
        # Read the client's private key
        private_key_path = os.path.join(org_path, 'private.pem')
        with open(private_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

        # Decode the base64 encoded license data
        encrypted_license_data = base64.b64decode(json_encrypted_license_data['sign'])
        # Decrypt the license data with RSA
        decrypted_aes_key = private_key.decrypt(
            encrypted_license_data,
            padding.PKCS1v15()
        )
        # Use the decrypted AES key to decrypt the rest of the license data
        decrypted_data = Adecrypt(json_encrypted_license_data['enc'], decrypted_aes_key.decode('utf-8'))
        license_info = json.loads(decrypted_data)
        return license_info
    except FileNotFoundError as fnf_error:
        raise fnf_error

    except json.JSONDecodeError as json_error:
        raise ValueError("Error decoding JSON data in license file.") from json_error

    except KeyError as key_error:
        raise ValueError(f"KeyError: Missing required key '{key_error}' in license file.") from key_error

    except (ValueError, TypeError) as decrypt_error:
        raise ValueError("Error decrypting license data.") from decrypt_error

    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred: {str(e)}") from e


def is_product_expired(expiry_date_str):
    """
    Check if the product is expired based on the expiry date.

    Args:
        expiry_date_str (str): Expiry date in ISO format (e.g., "2024-08-21T11:46:06.961Z").

    Returns:
        bool: True if the product is expired, False otherwise.

    Raises:
        ValueError: If the expiry_date_str is not a valid date string.
        Exception: For any other errors.
    """
    try:
        # Parse the expiry date string to a datetime object
        expiry_date = parser.isoparse(expiry_date_str)
        # Get the local timezone
        local_timezone = get_localzone()

        # Get the current time in the local timezone
        current_date = datetime.now(local_timezone)

        # Get the timezone of the expiry date
        expiry_timezone = expiry_date.tzinfo

        # Convert the current date to the expiry date's timezone
        current_date_in_expiry_tz = current_date.astimezone(expiry_timezone)

        # # Format the datetime string
        # formatted_current_date_in_expiry_tz = current_date_in_expiry_tz.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

        is_expired = current_date_in_expiry_tz > expiry_date
        return is_expired
    except ValueError as ve:
        raise ValueError("The expiry date string is not in valid format.") from ve
    except Exception as e:
        raise Exception("An error occurred while checking the product expiry.") from e


def get_license_details(org_id):
    """
        Extracts the license information for a given organization ID by decrypting the license file.

        Args:
            org_id (str): Unique ID for each organization.

        Returns:
            dict: license information.
        """
    if not org_id or not isinstance(org_id, str):
        raise ValueError("Invalid ORG_ID provided. It must be a non-empty string.")
    decrypted_data = extract_license(org_id)

    response = {
        "code": 1,
        "data": decrypted_data,
        "result": "License Details",
        "meta": {
            "isExpired": is_product_expired(decrypted_data['meta']['expiry']),
            "issueDate": decrypted_data['meta']['issued'],
            "expiryDate": decrypted_data['meta']['expiry'],
            "package_id": decrypted_data['include']['package']['_id']
        }
    }
    return response


def update_license(license_key, org_id, assign_type):
    """
    Updates the client's license key and assigns type in the init() configuration.

    Args:
        license_key (str): New license key.
        org_id (str): Unique ID for each organization.
        assign_type (str): Assign type, either 'update' or 'default'.

    Returns:
        dict: Response from the licensing server.
    """
    if not org_id or not isinstance(org_id, str):
        raise ValueError("Invalid ORG_ID provided. It must be a non-empty string.")
    if not license_key or not isinstance(license_key, str):
        raise ValueError("Invalid LICENSE_KEY provided. It must be a non-empty string.")
    if not assign_type or not isinstance(assign_type, str):
        raise ValueError("Invalid ASSIGN_TYPE provided. It must be a non-empty string.")
    org_path = os.path.join(CLIENT_CONFIG_DIRECTORY, org_id)
    init_filepath = os.path.join(org_path, 'init.json')
    if not os.path.exists(init_filepath):
        raise FileNotFoundError("Init file not found. Please run init() first.")

    with open(init_filepath, 'r') as f:
        client_details = json.load(f)

    client_details['licenseKey'] = license_key
    client_details['assignType'] = assign_type

    response = init(client_details["baseUrl"], license_key, client_details)
    return response


def convert_data(item):
    """
    Convert the data in the dictionary based on its type.

    Args:
        item (dict): Dictionary containing the 'type' and 'data' keys.

    Returns:
        dict: Updated dictionary with converted 'data'.
    """
    if item['type'] == 'number':
        try:
            item['data'] = float(item['data']) if '.' in item['data'] else int(item['data'])
        except ValueError:
            raise ValueError(f"Error converting {item['data']} to number")
    elif item['type'] == 'boolean':
        item['data'] = item['data'].lower() == 'true'
    elif item['type'] == 'date':
        try:
            item['data'] = datetime.strptime(item['data'], '%Y-%m-%d').isoformat()
        except ValueError:
            raise ValueError(f"Error converting {item['data']} to date")
    elif item['type'] == 'text':
        item['data'] = str(item['data'])
    else:
        raise ValueError(f"Unknown type: {item['type']}")
    return item


def get_element_by_name(data_list, name):
    """
    Retrieves the first element in the list with the specified name.

    Args:
        data_list (list): List of dictionaries containing the data.
        name (str): The name to search for in the list.

    Returns:
        dict or None: The dictionary with the specified name or None if not found.
    """
    for item in data_list:
        if item['name'] == name:
            return item
    return False


def get_feature(org_id, feature_name):
    """
    Retrieves the specified feature details from the license file.

    Args:
        org_id (str): Unique ID for each organization.
        feature_name (str or list): Specific feature name or 'all' for all features. To get more than one features send as a list ["feature1", "feature2"]

    Returns:
        dict: Feature details.
    """
    if not org_id or not isinstance(org_id, str):
        raise ValueError("Invalid ORG_ID provided. It must be a non-empty string.")
    if not feature_name:
        raise ValueError("Invalid FEATURE_NAME provided. It must be a non-empty string.")
    full_license_data = extract_license(org_id)

    meta = {
        "isExpired": is_product_expired(full_license_data['meta']['expiry']),
        "issueDate": full_license_data['meta']['issued'],
        "expiryDate": full_license_data['meta']['expiry'],
        "package_id": full_license_data['include']['package']['_id']
    }
    convert_list = []
    if isinstance(feature_name, list):
        feature_details = full_license_data['include']['package']['featuresList']
        sorted_data = [item for item in feature_details if item['name'] in feature_name]
        for i in sorted_data:
            convert_list.append(convert_data(i))
        response = {
            "data": convert_list,
            "meta": meta
        }
        return response

    if feature_name == 'all':
        features_list = full_license_data['include']['package']['featuresList']
        for i in features_list:
            convert_list.append(convert_data(i))
        response = {
            "data": convert_list,
            "meta": meta
        }
        return response

    feature_details = full_license_data['include']['package']['featuresList']
    for item in feature_details:
        if item['name'] == feature_name:
            response = {
                "data": convert_data(item),
                "meta": meta
            }
            return response
    else:
        raise ValueError(f"Feature {feature_name} not found in the license data.")


def sync(org_id):
    """
    Synchronizes the license information for a given organization ID using the provided license key.

    Args:
        org_id (str): Unique ID for each organization.
    Returns:
        dict: License server response and updated license information.

    Raises:
        FileNotFoundError: If the init file or license file is not found.
        ValueError: If the provided parameters are invalid.
        IOError: If there is an issue reading or writing files.
    """
    if not org_id or not isinstance(org_id, str):
        raise ValueError("Invalid ORG_ID provided. It must be a non-empty string.")

    org_path = os.path.join(CLIENT_CONFIG_DIRECTORY, org_id)
    init_filepath = os.path.join(org_path, 'init.json')

    if not os.path.exists(init_filepath):
        raise FileNotFoundError(f"Init file not found for ORG_ID '{org_id}'. Please run init() first.")

    try:
        with open(init_filepath, 'r') as f:
            init_data = json.load(f)
    except json.JSONDecodeError:
        raise IOError(f"Failed to read or parse init file for ORG_ID '{org_id}'. The file may be corrupted.")

    # Call get_license() with the required parameters
    license_server_response = get_license(init_data)
    return license_server_response


def main():
    """
    Main function to set up the scheduler and run it.
    """
    schedule_sync()  # Initial scheduling

    while True:
        schedule.run_pending()
        time.sleep(1)


# Example Usage
if __name__ == "__main__":
    main()
