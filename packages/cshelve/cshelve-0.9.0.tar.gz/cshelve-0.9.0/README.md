# Cloud Shelve
`Cloud Shelve (cshelve)` is a Python package that provides a seamless way to store and manage data in the cloud using the familiar [Python Shelve interface](https://docs.python.org/3/library/shelve.html). It is designed for efficient and scalable storage solutions, allowing you to leverage cloud providers for persistent storage while keeping the simplicity of the `shelve` API.

## Features

- Supports large file storage in the cloud
- Secure data in-transit encryption when using cloud storage
- Fully compatible with Python's `shelve` API
- Cross-platform compatibility for local and remote storage

## Installation

Install `cshelve` via pip:

```bash
pip install cshelve
```

## Usage

The `cshelve` module strictly follows the official `shelve` API. Consequently, you can refer to the [Python official documentation](https://docs.python.org/3/library/shelve.html) for general usage examples. Simply replace the `shelve` import with `cshelve`, and you're good to go.

### Local Storage

Here is an example, adapted from the [official shelve documentation](https://docs.python.org/3/library/shelve.html#example), demonstrating local storage usage. Just replace `shelve` with `cshelve`:

```python
import cshelve

d = cshelve.open('local.db')  # Open the local database file

key = 'key'
data = 'data'

d[key] = data                 # Store data at the key (overwrites existing data)
data = d[key]                 # Retrieve a copy of data (raises KeyError if not found)
del d[key]                    # Delete data at the key (raises KeyError if not found)

flag = key in d               # Check if the key exists in the database
klist = list(d.keys())        # List all existing keys (could be slow for large datasets)

# Note: Since writeback=True is not used, handle data carefully:
d['xx'] = [0, 1, 2]           # Store a list
d['xx'].append(3)             # This won't persist since writeback=True is not used

# Correct approach:
temp = d['xx']                # Extract the stored list
temp.append(5)                # Modify the list
d['xx'] = temp                # Store it back to persist changes

d.close()                     # Close the database
```

### Debug/test Storage

For testing purposes, it is possible to use an in-memory provider that can:
- Persist the data during all the program execution.
- Remove the data object is deleted.

Here is a configuration example:
```bash
$ cat in-memory.ini
[default]
provider    = in-memory
# If set, open twice the same database during the program execution will lead to open twice the same database.
persist-key = standard
```

A common use case for this provider is to simplify mocking.

Example:
```bash
$ cat persist.ini
[default]
provider    = in-memory
# If set, open twice the same database during the program execution will lead to open twice the same database.
persist-key = my-db

$ cat do-not-persist.ini
[default]
provider = in-memory
```

```python
import cshelve

with cshelve.open('persist.ini') as db:
    db["Asterix"] = "Gaulois"

with cshelve.open('persist.ini') as db:
    assert db["Asterix"] == "Gaulois"

with cshelve.open('do-not-persist.ini') as db:
    db["Obelix"] = "Gaulois"

with cshelve.open('do-not-persist.ini') as db:
    assert "Obelix" not in db
```

### Remote Storage (e.g., Azure)

To configure remote cloud storage, you need to provide an INI file containing your cloud provider's configuration. The file should have a `.ini` extension. Remote storage also requires the installation of optional dependencies for the cloud provider you want to use.

#### Example Azure Blob Configuration

First, install the Azure Blob Storage provider:
```bash
pip install cshelve[azure-blob]
```

Then, create an INI file with the following configuration:
```bash
$ cat azure-blob.ini
[default]
provider        = azure-blob
account_url     = https://myaccount.blob.core.windows.net
# Note: The auth_type can be access_key, passwordless, connection_string, or anonymous.
# The passwordless authentication method is recommended, but the Azure CLI must be installed (https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
auth_type       = passwordless
container_name  = mycontainer
```

Once the INI file is ready, you can interact with remote storage the same way as with local storage. Here's an example using Azure:

```python
import cshelve

d = cshelve.open('azure-blob.ini')  # Open using the remote storage configuration

key = 'key'
data = 'data'

d[key] = data                  # Store data at the key on the remote storage
data = d[key]                  # Retrieve the data from the remote storage
del d[key]                     # Delete the data from the remote storage

flag = key in d                # Check if the key exists in the cloud storage
klist = list(d.keys())         # List all keys present in the remote storage

# Note: Since writeback=True is not used, handle data carefully:
d['xx'] = [0, 1, 2]            # Store a list on the remote storage
d['xx'].append(3)              # This won't persist since writeback=True is not used

# Correct approach:
temp = d['xx']                 # Extract the stored list from the remote storage
temp.append(5)                 # Modify the list locally
d['xx'] = temp                 # Store it back on the remote storage to persist changes

d.close()                      # Close the connection to the remote storage
```

More configuration examples for other cloud providers can be found [here](./tests/configurations/).

### Providers configuration

#### In Memory

Provider: `in-memory`
Installation: No additional installation required.

The In Memory provider uses an in-memory data structure to simulate storage. This is useful for testing and development purposes.

| Option         | Description                                                                  | Required | Default Value |
|----------------|------------------------------------------------------------------------------|----------|---------------|
| `persist-key`  | If set, its value will be conserved and reused during the program execution. | :x:      | None          |
| `exists`       | If True, the database exists; otherwise, it will be created.                 | :x:      | False         |


#### Azure Blob

Provider: `azure-blob`
Installation: `pip install cshelve[azure-blob]`

The Azure provider uses [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) as remote storage.
The module considers the provided container as dedicated to the application. The impact might be significant. For example, if the flag `n` is provided to the `open` function, the entire container will be purged, aligning with the [official interface](https://docs.python.org/3/library/shelve.html#shelve.open).

| Option                           | Description                                                                                                                                                  | Required           | Default Value |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|---------------|
| `account_url`                    | The URL of your Azure storage account.                                                                                                                       | :x:                |               |
| `auth_type`                      | The authentication method to use: `access_key`, `passwordless`, `connection_string` or `anonymous`.                                                                               | :white_check_mark:                |               |
| `container_name`                 | The name of the container in your Azure storage account.                                                                                                     | :white_check_mark:                |               |

Depending on the `open` flag, the permissions required by `cshelve` for blob storage vary.

| Flag | Description | Permissions Needed |
|------|-------------|--------------------|
| `r`  | Open an existing blob storage container for reading only. | [Storage Blob Data Reader](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-reader) |
| `w`  | Open an existing blob storage container for reading and writing. | [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor) |
| `c`  | Open a blob storage container for reading and writing, creating it if it doesn't exist. | [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor) |
| `n`  | Purge the blob storage container before using it. | [Storage Blob Data Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor) |


Authentication type supported:

| Auth Type         | Description                                                                                     | Advantage                                                                 | Disadvantage                          | Example Configuration |
|-------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------|-----------------------|
| Access Key       | Uses an Access Key or a Shared Access Signature for authentication. | Fast startup as no additional credential retrieval is needed. | Credentials need to be securely managed and provided. | [Example](./tests/configurations/azure-integration/access-key.ini) |
| Anonymous         | No authentication for anonymous access on public blob storage. | No configuration or credentials needed. | Read-only access. | [Example](./tests/configurations/azure-integration/anonymous.ini) |
| Connection String | Uses a connection string for authentication. Credentials are provided directly in the string. | Fast startup as no additional credential retrieval is needed. | Credentials need to be securely managed and provided. | [Example](./tests/configurations/azure-integration/connection-string.ini) |
| Passwordless      | Uses passwordless authentication methods such as Managed Identity. | Recommended for better security and easier credential management. | May impact startup time due to the need to retrieve authentication credentials. | [Example](./tests/configurations/azure-integration/standard.ini) |


## Contributing

We welcome contributions from the community! Have a look at our [issues](https://github.com/Standard-Cloud/cshelve/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions, issues, or feedback, feel free to [open an issue]https://github.com/Standard-Cloud/cshelve/issues).
