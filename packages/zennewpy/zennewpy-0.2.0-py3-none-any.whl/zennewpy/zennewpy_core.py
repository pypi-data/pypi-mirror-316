import json
import os
from pathlib import Path
import re
import requests
import warnings
import tarfile
import zipfile
from tabulate import tabulate
import time

def validate_url(url):
    """validates if URL is formatted correctly

    Returns:
        bool: True is URL is acceptable False if not acceptable
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def make_tarfile(output_file, source_dir):
    """tar a directory
    args
    -----
    output_file: path to output file
    source_dir: path to source directory

    returns
    -----
    tarred directory will be in output_file
    """
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def make_zipfile(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def prepare_zip(source_dir=None, output_file=None):
    """Prepare a zip dir.

    This will: 
        1. zip the directory, 
    Args:
        source_dir (str): path to directory to tar
        output_file (str): name of output file (optional)
            defaults to using the source_dir name as output_file
    """
    # make sure source directory exists
    source_dir = os.path.expanduser(source_dir)
    source_obj = Path(source_dir)
    if not source_obj.exists():
        raise FileNotFoundError(f"{source_dir} does not exist")
    # acceptable extensions for output file
    acceptable_extensions = ['.zip']
    # use name of source_dir for output_file if none is included
    if not output_file:
        output_file = f"{source_obj.stem}.zip"
        output_obj = Path(output_file)
    else:
        output_file = os.path.expanduser(output_file)
        output_obj = Path(output_file)
        extension = ''.join(output_obj.suffixes)  # gets extension like .tar.gz
        # make sure extension is acceptable
        if extension not in acceptable_extensions:
            raise Exception(f"Extension must be in {acceptable_extensions}")
        # add an extension if not included
        if not extension:
            output_file = os.path.expanduser(output_file + '.zip')
            output_obj = Path(output_file)

    # check to make sure output file doesn't already exist
    if output_obj.exists():
        raise Exception(f"{output_obj} already exists. Please chance the name")
    # create tar directory if does not exist
    if output_obj.parent.exists():
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            make_zipfile(source_dir, zipf)
    else:
        os.makedirs(output_obj.parent)
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            make_zipfile(source_dir, zipf)

    return output_file


class BearerAuth(requests.auth.AuthBase):
    """Bearer Authentication"""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Client(object):
    """Zenodo Client object

    Use this class to instantiate a zenodopy object
    to interact with your Zenodo account

        ```
        import zenodopy
        zeno = zenodopy.Client()
        zeno.help()
        ```

    Setup instructions:
        ```
        zeno.setup_instructions
        ```
    """

    def __init__(self, title=None, bucket=None, deposition_id=None, sandbox=None, token=None):
        """initialization method"""
        if sandbox:
            self._endpoint = "https://sandbox.zenodo.org/api"
            self._doi_pattern = r'^10\.5072/zenodo\.\d+$'
        else:
            self._endpoint = "https://zenodo.org/api"
            self._doi_pattern = r'^10\.5281/zenodo\.\d+$'

        self.title = title
        self.bucket = bucket
        self.deposition_id = deposition_id
        self.sandbox = sandbox
        self._token = self._read_from_config if token is None else token
        self._bearer_auth = BearerAuth(self._token)
        self.concept_id = None
        self.associated = False
        # 'metadata/prereservation_doi/doi'

    def __repr__(self):
        return f"zenodoapi('{self.title}','{self.bucket}','{self.deposition_id}')"

    def __str__(self):
        return f"{self.title} --- {self.deposition_id}"


    # ---------------------------------------------
    # hidden functions
    # ---------------------------------------------
    @staticmethod
    def _get_upload_types():
        """Acceptable upload types

        Returns:
            list: contains acceptable upload_types
        """
        return [
            "publication",
            "poster",
            "presentation",
            "dataset",
            "image",
            "video",
            "software",
            "lesson",
            "physicalobject",
            "other"
        ]


    @staticmethod
    def _read_config(path=None):
        """reads the configuration file

        Configuration file should be ~/.zenodo_token

        Args:
            path (str): location of the file with ACCESS_TOKEN

        Returns:
            dict: dictionary with API ACCESS_TOKEN
        """

        if path is None:
            print("You need to supply a path")

        full_path = os.path.expanduser(path)
        if not Path(full_path).exists():
            print(f"{path} does not exist. Please check you entered the correct path")

        config = {}
        with open(path) as file:
            for line in file.readlines():
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    if key in ("ACCESS_TOKEN", "ACCESS_TOKEN-sandbox"):
                        config[key] = value.strip()
        return config

    @property
    def _read_from_config(self):
        """reads the web3.storage token from configuration file
        configuration file is ~/.web3_storage_token
        Returns:
            str: ACCESS_TOKEN to connect to web3 storage
        """
        if self.sandbox:
            dotrc = os.environ.get("ACCESS_TOKEN-sandbox", os.path.expanduser("~/.zenodo_token"))
        else:
            dotrc = os.environ.get("ACCESS_TOKEN", os.path.expanduser("~/.zenodo_token"))

        if os.path.exists(dotrc):
            config = self._read_config(dotrc)
            key = config.get("ACCESS_TOKEN-sandbox") if self.sandbox else config.get("ACCESS_TOKEN")
            return key
        else:
            print(' ** No token was found, check your ~/.zenodo_token file ** ')


    def get_all_depositions(self):
        """
        Retrieves all depositions for the client, but only the last version with all metadata.

        Returns:
            list: A list of dictionaries containing the latest version of each deposition with full metadata.
        """
        url = f"{self._endpoint}/deposit/depositions"
        params = {
            "size": 1000,  # Adjust this value based on your needs
            "sort": "mostrecent",
            "all_versions": True
        }

        all_depositions = []
        concept_ids_processed = set()

        while True:
            response = requests.get(url, auth=self._bearer_auth,params=params)
            response.raise_for_status()
            depositions = response.json()

            if not depositions:
                break

            for deposition in depositions:
                concept_id = deposition['conceptrecid']
                if concept_id not in concept_ids_processed:
                    # This is the latest version of this deposition
                    all_depositions.append(deposition)
                    concept_ids_processed.add(concept_id)

            # Check if there are more pages
            links = response.links
            if 'next' not in links:
                break
            url = links['next']['url']

        return all_depositions



    def find_community_identifier(self,community_name):
        """Find a community id from community name"""
        params = {
            "q": community_name,
            "size": 100  # Adjust as needed
        }

        response = requests.get(self._endpoint+'/communities', params=params)

        if response.status_code == 200:
            data = response.json()
            for community in data['hits']['hits']:
                if community['metadata']['title'].lower() == community_name.lower():
                    return community['id']

        return None


    def set_deposition(self, id_value):
        """
        Sets the client to a specific deposition's latest version using a given deposition_id or concept_id.

        Args:
            id_value (int): The ID of the deposition or the concept ID to set.
            
        Raises:
            ValueError: If no valid deposition is found for the given ID.
        """
        if not id_value:
            raise ValueError("You must provide an ID.")

        # First, try to retrieve the deposition directly
        try:
            deposition = self.get_deposition_by_id(id_value)
            concept_id = deposition.get('conceptrecid')
        except requests.exceptions.HTTPError:
            # If that fails, assume it's a concept ID
            concept_id = id_value

        # Retrieve the latest version of the deposition using concept ID
        url = f"{self._endpoint}/deposit/depositions"
        params = {
            "q": f"conceptrecid:{concept_id}",
            "sort": "mostrecent",
            "size": 1,
        }
        
        # hack to the problem that the deposition_id is not created instantaneously on the server
        n_try = 8
        delta=1
        response = requests.get(url, auth=self._bearer_auth, params=params)
        depositions = response.json()
        while not depositions and n_try > 0:
            response = requests.get(url, auth=self._bearer_auth, params=params)
            depositions = response.json()  
            time.sleep(delta)
            n_try -=1
            delta+=0.5
        response.raise_for_status()
            
        if not depositions:
            raise ValueError(f"No depositions found for ID {id_value}.")
        
        latest_deposition = depositions[0]

        # Set class variables based on the latest version of the deposition
        self.title = latest_deposition['metadata'].get('title', None)
        self.bucket = latest_deposition['links'].get('bucket', 'N/A')
        
        self.deposition_id = latest_deposition['id']
        self.concept_id = latest_deposition['conceptrecid']
        self.associated = True


   
    def unset_deposition(self):
        """
        Unset the current deposition settings, resetting related attributes.
        """
        self.title = None
        self.bucket = None
        self.deposition_id = None
        self.concept_id = None
        self.associated = False

    def get_deposition_by_id(self, deposition_id=None):
        """
        Retrieves a specific deposition by its ID.

        Args:
            deposition_id (int): The ID of the deposition to retrieve.

        Returns:
            dict: A dictionary containing the full metadata of the deposition.
        """
        if deposition_id is None and self.associated :
            deposition_id = self.deposition_id
        url = f"{self._endpoint}/deposit/depositions/{deposition_id}"
 
        response = requests.get(url,auth=self._bearer_auth)
        response.raise_for_status()
        return response.json()
    
    @property
    def deposition(self):
        return self.get_deposition_by_id()


    def pretty_print_depositions(self, depositions=None):
        """
        Pretty prints all depositions with their metadata in a table format.

        Args:
            depositions (list): A list of deposition dictionaries to print.
        """
        if depositions is None: depositions = self.get_all_depositions()

        table_data = []

        for deposition in depositions:
            title = deposition['metadata'].get('title',None)
            cid = deposition['conceptrecid']
            dep_id = deposition['id']
            published = 'Yes' if deposition['submitted'] else 'No'
            doi = deposition.get('doi', 'N/A')
            
            # Check if this is the currently set deposition
            flag = '*' if self.deposition_id == dep_id else ''
            
            table_data.append([title, cid, dep_id, published, doi, flag])

        headers = ["Title", "CID", "ID", "Published", "DOI", "Set"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))


    def create_new_deposition(self):
        """
        Creates a new deposition.

        Returns:
            int: The ID of the newly created deposition.
        """
        url = f"{self._endpoint}/deposit/depositions"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, auth=self._bearer_auth, json={}, headers=headers)
        response.raise_for_status()

        deposition_data = response.json()
        return deposition_data['id']

    def delete_deposition(self, deposition_id=None):
        """
        Deletes a deposition.

        Args:
            deposition_id (int): The ID of the deposition to delete.
        """

        if deposition_id is None : deposition_id = self.deposition_id

        if not type(deposition_id)==list :
            deposition_id = [deposition_id]
        
        for ii in deposition_id:
            url = f"{self._endpoint}/deposit/depositions/{ii}"
            response = requests.delete(url, auth=self._bearer_auth)
            #response.raise_for_status()
            if(ii==self.deposition_id) : self.unset_deposition()
            if response.status_code < 400:
                print(f"Deposition {ii} deleted")

    
    def upload_file(self,file_path, remote_filename=None, file_id=None):
        """
        Uploads a file to a Zenodo deposition using PUT (if file_id is provided) or POST (for new files).

        Args:
            file_path (str): The local path of the file to upload.
            remote_filename (str, optional): The filename to use on Zenodo. If None, uses the local filename.
            file_id (str, optional): The ID of an existing file to update. If None, a new file will be created.

        Returns:
            dict: The uploaded file data, including the file_id.
        """
        deposition_id = self.deposition_id

        if remote_filename is None:
            remote_filename = os.path.basename(file_path)


        r = requests.get(f"{self._endpoint}/deposit/depositions/{deposition_id}", 
                      auth=self._bearer_auth)
        
        self.bucket = r.json()['links']['bucket']
        

        if file_id:
            print("this functionality does not work at moment on Zenodo!!")
            # Update existing file using PUT
            url = f"{self._endpoint}/deposit/depositions/{deposition_id}/files/{file_id}"
            with open(file_path, "rb") as file:
                response = requests.put(url, auth=self._bearer_auth, data=file)
        else:
            with open(file_path, 'rb') as file:
                response = requests.put(f"{self.bucket}/{remote_filename}", 
                         data=file, 
                         auth=self._bearer_auth)
            # Upload new file using POST
            # url = f"{self._endpoint}/deposit/depositions/{deposition_id}/files"
            # with open(file_path, "rb") as file:
            #     data = {"name": remote_filename}
            #     files = {"file": file}
            #     response = requests.post(url, auth=self._bearer_auth, data=data, files=files)

        response.raise_for_status()
        file_data = response.json()

        return file_data

    def get_file_ids(self, deposition_id=None):
        """
        Retrieves the file IDs for all files in a deposition.

        Args:
            deposition_id (int): The ID of the deposition.

        Returns:
            dict: A dictionary mapping filenames to their file IDs.
        """
        if deposition_id is None and self.associated :
            deposition_id = self.deposition_id
        deposition = self.get_deposition_by_id(deposition_id)
        return {file['filename']: file['id'] for file in deposition.get('files', [])}   


    def get_doi(self,deposition_id=None):
        if deposition_id is None and self.associated :
            deposition_id = self.deposition_id
        deposition = self.get_deposition_by_id(deposition_id)
        return deposition.get('doi',None)


    def publish_deposition(self):
        """
        Publishes a deposition.

        Args:
            deposition_id (int): The ID of the deposition to publish.

        Returns:
            dict: The published deposition data.
        """
        url = f"{self._endpoint}/deposit/depositions/{self.deposition_id}/actions/publish"

    
        try:
            response = requests.post(url, auth=self._bearer_auth)
            response.raise_for_status()
            return True  # If we get here, the request was successful
        except requests.exceptions.RequestException as e:
            # Log the error for debugging purposes
            print(f"Error publishing deposition: {str(e)}")
            return False  # Return False if any exception occurs
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            print(f"Response: {response.text}")  # For more detailed error information
        except KeyError:
            print("KeyError: Failed to retrieve 'publish' link. Check if the deposition is ready for publication.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @property 
    def is_published(self):
        return self.get_deposition_by_id()['submitted']

    def create_new_version(self):
        """
        Creates a new version of an existing deposition.
        
        
        Returns:
            dict: The new deposition data.
        """
        url = f"{self._endpoint}/deposit/depositions/{self.deposition_id}/actions/newversion"
        
        try:
            response = requests.post(url, auth=self._bearer_auth)
            response.raise_for_status()
                    
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.content}")

        new_id = response.json()['id']
        self.set_deposition(new_id)

        if self.deposition_id != new_id:
            print(f"Warning : association new deposition_id is not done! Deleting version :{new_id}")
            self.delete_deposition(new_id)
            return None
                
        return new_id

    def push_metadata(self, metadata):
        """
        Creates or updates metadata for a deposition.

        Args:
            deposition_id (int): The ID of the deposition.
            metadata (dict): The metadata to set.

        Returns:
            dict: The updated deposition data.
        """
        if not self.associated: 
            print("push_metadata: deposition is not associated.")
            return 
        

        url = f"{self._endpoint}/deposit/depositions/{self.deposition_id}"
        headers = {"Content-Type": "application/json"}
        data = {"metadata": metadata}

        response = requests.put(url, auth=self._bearer_auth, data=json.dumps(data), headers=headers)
        if response.status_code >= 500:
            self.delete_deposition()
        response.raise_for_status()

        return response.json()

    def update_metadata(self, metadata_updates):
        """
        Modifies metadata of a deposition (published or not).

        Args:
            metadata_updates (dict): The metadata fields to update.

        Returns:
            dict: The updated deposition data.
        """
        if not self.associated:
            print(f'Error in "modify_update" Deposition is not associated!')
            return None

        # Check if the deposition is published
        current_deposition = self.deposition
        current_metadata = current_deposition['metadata']

        if self.is_published:
            new_id = self.create_new_version()
            print(f"New deposition_id {new_id} was created for concept_id {self.concept_id}")
            current_deposition = self.deposition

        # Update the metadata
        for key, value in metadata_updates.items():
            if isinstance(value, list) and key in current_metadata:
                # If the value is a list and the key already exists, extend the list
                if isinstance(current_metadata[key], list):
                    current_metadata[key].extend(value)
                else:
                    # If the existing value is not a list, convert it to a list and extend
                    current_metadata[key] = [current_metadata[key]] + value
            else:
                # For non-list values or new keys, simply update/add the value
                current_metadata[key] = value

        # Use the push_metadata method to update
        return self.push_metadata(current_metadata)

    def update_file(self, file_path,remote_filename=None):
        """
        Updates a file in a deposition (published or not).

        Args:
            file_path (str): The path to the new file.
            remote_filename (str) : The remote name.

        Returns:
            dict: The updated file data.
        """

        if self.is_published : 
            print("Deposition is published. Before to update file please create a new version")
            return 


        # Check if the new file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Check if the new file is readable
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"No permission to read the file {file_path}.")

        # First, try to delete the existing file
        file_id = self.get_file_ids().get(remote_filename,None)
        if file_id :            
            delete_url = f"{self._endpoint}/deposit/depositions/{self.deposition_id}/files/{file_id}"


            try:
                delete_response = requests.delete(delete_url, auth=self._bearer_auth)
                delete_response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    # File not found, log a warning and continue with upload
                    print(f"Warning: File {file_id} not found. Proceeding with upload.")
                else:
                    raise Exception(f"Failed to delete existing file: {str(e)}")

        # Then, upload the new file
        try:
            return self.upload_file(file_path=file_path,remote_filename=remote_filename)
        except Exception as e:
            raise Exception(f"Failed to upload new file: {str(e)}")
   

    def get_file_ids(self):
        """
        Retrieves the file IDs for all files in a deposition.

        Args:
            deposition_id (int): The ID of the deposition.

        Returns:
            dict: A dictionary mapping filenames to their file IDs.
        """

        deposition = self.get_deposition_by_id(self.deposition_id)
        return {file['filename']: file['id'] for file in deposition.get('files', [])}


    def title_exists(self, title):
        """
        Check if depositions with the given title exist in Zenodo,
        and return their IDs if found.
        
        Args:
        title (str): The title to search for.
        
        Returns:
        dict: A dictionary containing 'exists' (bool) and 'ids' (list of str)
        """
        result = {
            'exists': False,
            'ids': []
        }

        search_url = f"{self._endpoint}/deposit/depositions"
        params = {
            'size': 9999  # Adjust this value based on your needs
        }
       
        try:
            response = requests.get(search_url, params=params, auth=self._bearer_auth)
            response.raise_for_status()
            
            depositions = response.json()
            for deposition in depositions:
                if deposition.get('metadata', {}).get('title', '').lower() == title.lower():
                    result['exists'] = True
                    deposition_id = deposition.get('id')
                    result['ids'].append(deposition_id)
                    status = "published" if deposition.get('submitted', False) else "draft"
                    print(f"Found {status} deposition with title: {title}, ID: {deposition_id}")
            
            if not result['exists']:
                print(f"No deposition found with title: {title}")
            elif len(result['ids']) > 1:
                print(f"Warning: Multiple depositions found with title: {title}")

        except requests.exceptions.RequestException as e:
            print(f"Error searching depositions: {e}")
            print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
            print(f"Response content: {e.response.text if e.response else 'N/A'}")

        return result
    
    def get_metadata(self,dep_id: str=None):
        """
        Retrieves the current metadata of a deposition on Zenodo.

        Args:
            dep_id (str): The ID of the deposition.

        Returns:
            response (dict): The current metadata from the Zenodo API.
        """
        if dep_id is None :
            dep_id = self.deposition_id
        url = f"{self._endpoint}/deposit/depositions/{dep_id}"

        # Fetch the existing metadata
        response = requests.get(url, auth=self._bearer_auth)

        if response.status_code == 200:
            return response.json()["metadata"]
        else:
            print(f"Failed to fetch metadata. Status code: {response.status_code}")
            return None



if __name__ == '__main__':
    zcd = Client(sandbox=True)

    # Create a new deposition
    deposition_id = zcd.create_new_deposition()
    
    # Create metadata
    metadata = {
        'title': 'My New Dataset',
        'description': 'This is a test dataset',
        'upload_type': 'dataset',
        'creators': [{'name': 'Doe, John', 'affiliation': 'zcddo'}]
    }


    zcd.set_deposition(deposition_id)

    zcd.push_metadata(metadata)

    # Upload a file
    zcd.upload_file('/tmp/eos.zip', 'remote_filename.zip')

    # Publish the deposition
    #zcd.publish_deposition()

    # Modify metadata (even after publishing)
    zcd.update_metadata({'title': 'Updated Dataset Title'})

    zcd.update_file('/tmp/eos2.zip',remote_filename='remote_filename.zip')

    
    # Delete a deposition (only works for unpublished depositions)
    #zcd.delete_deposition(deposition_id)
