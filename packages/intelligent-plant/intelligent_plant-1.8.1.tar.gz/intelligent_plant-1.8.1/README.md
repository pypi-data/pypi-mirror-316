# Python App Store API Client
A python implmentation of the Intelligent Plant industrial appstore API client

See the example folder for example on how to use the library for authorization code and implicit OAuth grant flows.

## Getting started

### Installing using pip

`pip install intelligent-plant`

### Installing from Source

Using pip:

`pip install git+https://github.com/intelligentplant/py-app-store-api`

Alternatively clone the Git repo:

`git clone https://github.com/intelligentplant/py-app-store-api.git`

## Example Scripts

The 'example' folder contains a series of examples which demonstrate the available authentication methods and queries that you can make using this library.

To install dependencies used by the example scripts run

`pip install -r example-requirements.txt`

### Querying the Industrial App Store

In order to query the industrial app store you must register as a developer and create an app registration. Full instructions can be found here: [https://wiki.intelligentplant.com/doku.php?id=dev:app_store_developers](https://wiki.intelligentplant.com/doku.php?id=dev:app_store_developers)

Once you have created and app registration you will need to copy and rename `config-example.json` to `config.json` and populate the `id` and `secret` fields with you app ID and app secret.

To run the authorization code grant flow example run:

`python example/authorization_code_grant_flow.py`

To run the authorization code grant flow example with the PKCE extension run:

This is the recommended flow for web and native applications.

`python example/authorization_code_grant_flow_pkce.py`

To run the device code flow example run:

*The device code flow is disabled by default, you must enable it on the app registration*

This is the recommended flow for CLI apps and tools.

`python example/device_code_flow.py`

To run the implicit grant flow example run:

*The implicit grant flow is deprecated and is disabled by default*

`python example/implicit_grant_flow.py`

#### Saving your session to reduce number of logins

The `intelligent_plant.session_manager` module provides functionality to save your session to your operating systems keyvault using the library [keyring](https://pypi.org/project/keyring/). To use this module you must have keyring installed:

`pip install keyring`

With keyring installed you can now use it as shown in the stored session examples.

Running the stored session example will use the device code flow to authenticate the first time (or if your session expires) but will otherwise use the stored credentials:

`python example/stored_session/stored_session.py`

You can see the stored session values using:

`python example/stored_session/get_stored_session.py`

And you can clear the stored session using:

`python example/stored_session/clear_session.py`

You can also see this being used in a Jupyter notebook in `example/stored_session/jupyter.ipynb`.

### Querying a local App Store Connect or Data Core node

To run the NTLM (windows authentication) example you will need to have a data core node available on the local network.
If you have an App Store Connect (https://appstore.intelligentplant.com/Home/DataSources) installed locally you can run the example without modification. If you are trying to authenticate with a data core node you will need to change the `base_url` variable defined in the script to match the URL of the Data Core admin UI.

Run the example using:

`python example/ntlm_example.py`

## Example Notebooks

You can find examples of how to use the library to make queries in our Jupyer Hub demo notebooks (these notebooks expect a valid Industrial App Store access token to be present in the `ACCESS_TOKEN` environment variable).

[https://github.com/intelligentplant/jupyter-hub-demo/tree/master/Python](https://github.com/intelligentplant/jupyter-hub-demo/tree/master/Python)

To use this library as part of a Jupyter Notebook join the Jupyter Hub:

https://appstore.intelligentplant.com/Home/AppProfile?appId=40d7a49722f84be4986318bb5cc98cf3


