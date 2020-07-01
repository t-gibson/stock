# Stock

An ML-powered web app for stock image semantic search.

![In-use animation](./results.gif "In-use animation")

Powered by:

- [Terraform](https://www.terraform.io/) for the infrastructure
- [Pexels](https://www.pexels.com/api/) for the stock images
- [Jina](https://github.com/jina-ai/jina) for the search capabilities
- [Streamlit](https://github.com/streamlit/streamlit) for the web app

See the code [here](https://github.com/t-gibson/stock)

# Getting started

To start, clone the repo:

```bash
git clone https://github.com/t-gibson/stock.git
```

## Optional prelude: Setting up an AWS instance

This repo includes steps to construct AWS infrastructure for hosting this web app.
It can also be run on your local machine. The steps for setting up the AWS infra
are below. They will require that you have set up the AWS cli on your system
and have installed Terraform.

1. Construct the AWS infrastructure using Terraform. You will need to pass in the name
of your desired AWS key pair as a variable.

    ```bash
    terraform apply
    ```

1. SSH into your EC2 instance and clone the codebase there.

    ```bash
    ssh -i <path/to/ssh_private_key> ubuntu@$(terraform output public_dns)
    git clone https://github.com/t-gibson/stock.git
    ```
   
## Main steps

1. Install the `stock` cli app.
_Note:_ this app requires python>=3.7. I recommend using a virtual env or conda.

    ```bash
    pip install -r requirements.txt
    ```

1. Populate the `.env` template file. This will save you keystrokes at the command line.

1. Download the data that we will process. We abide by the limits of the Pexels API.
So, if you attempt to download too many things `stock` will throw an exception or else
the API will just return not as many images as you will expect.

    ```bash
    stock download --num-results 50 <space separated list of image categories to query>
    ```

    To have a search application that has half-decent results you will need to have
downloaded info on a meaningful number of photos. However, don't abuse the Pexels API.
I recommend running the below variant of the command and schedule it to re-run
regularly using a crontab.

    ```bash
    stock download \
      --num-results 50 \
      --query-page-logs <file-to-store-interim-results> \
      <space separate list of image categories>
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



# Where to next?

To dig deeper into the neural search path I could consider __multi-modal search capabilities__.
This should be a cinch with the multi-modal search capapabilities that are on their way for Jina.

I only dipped my toe into hosting an app on AWS.
There isn't many smarts applied to the infrastructure that I set up.
__Could I attempt to wrap up the search capability as a serverless application?__
