# Excel_to_GCP_example
Trying to use Python, Google-SDK and Google-API-Client to build and manage GCP resources. In this particular case, we are creating http servers and the code final returns the Ephemeral IPs

## Changes you need to make
1. Provide the path to the GCP IAM credential JSON file, which is necessary for the code to access GCP APIs
2. Provide the path to the startup scripts, that must by run while creating the instances, in the expected coulumn of the "Resources.xlsx" file.
