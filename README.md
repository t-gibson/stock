# Stock

An ML-powered web app for stock image semantic search.

__Screencast goes here__

Powered by:

- [Terraform](https://www.terraform.io/) for the infrastructure
- [Pexels](https://www.pexels.com/api/) for the stock images
- [Jina](https://github.com/jina-ai/jina) for the search capabilities
- [Streamlit](https://github.com/streamlit/streamlit) for the web app

# Getting started

1. Optionally, construct the AWS infrastructure. This can also be run on your
local machine. This step will require that you have
set up the AWS cli on your system. You will need to pass in the name
of your desired AWS key pair as a variable.

    ```bash
    # clone the directory
    terraform apply
    ```

1. Either on your local or within the EC2 instance, install the `stock` cli app.
_Note:_ this app requires python>=3.7. I recommend using a virtual env or conda.

    ```bash
    # optionally ssh to EC2
    ssh -i <path/to/ssh_private_key> ubuntu@$(terraform output public_dns)
    # install the package
    pip install -r requirements.txt
    ```

1. Populate the `.env` template. __Fill more here__

1. Download the data that we will process. We abide by the limits of the Pexels API.
So, if you attempt to download too many things `stock` will throw an exception or else
the API will just return not as many images as you will expect.

    ```bash
    stock download -n 50 <space separated list of image categories to query>
    ```

1. Run the indexing application.

    ```bash
    stock index
    ```

1. After that you are free to run the search application. The streamlit app
will be running on port `8501`.

    ```bash
    stock search
    ```

# Improvements to make:

- ui improvements
    - can add in details on the number of images and from what topics the results we have indexed.
    - add in credit and link back to github
    - improve printing of images. fit more on each page.
- attempt multi-modal searching
- attempt to wrap the computationally expensive parts (bert) in serverless application.
Then, try to host the rest of the application in a single EC2 t2.micro? Or maybe push for
everything to be either dockerised or severless.
    - Chalice?
