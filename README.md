# Stock Image Semantic Search

Improve upon my previous design_describer repo attempt. Pick up an existing semantic search effort
and deploy it, applied to stock images.

Build a docker image that hosts a simple website.

- Hosts a jina querying application. Takes an input an image and returns the top-k similar images
from an S3 blob of pre-indexed photos.

## Next step

- Retrain the model on a specific subset of things
- Rather than use a static store of files connect to a pre-indexed set of images from unsplash/pexels/etc
- Work on finding similar movies based on audio/cinematography

# MVP steps

## Version 1 - DONE:

- terraform: an S3 bucket, an EC2 image that has docker installed.
- run a simple EC2 instance that has docker installed. Then insidne we can build
and run a simple docker image.
- Locally stored files on S3. Have a `download_files.sh` script to download images
and upload to aws.
- files are connected to S3. Which is added as a volume to docker image.
- docker image can then be ssh-ed into, where we run an index command (saved to S3).
- then from within docker image, we can call the query command

## Version 2:

__cleaning code __

- [X] package results as a package. local editable install.
- [X] include a top-level cli
- [X] add simple cli option with click.
    - cli exists in the src code. Which we can then source into the top level script.
    This would help simplify the top-level script to just be the cli and dotenv portions.
    - download images
    - index images to a folder
    - query images
- [ ] abstract away app code into a folder
    - don't have to worry about loading yaml files from right directory.
    - [ ] formalise env variables into a config.py file
- [ ] add testing of commands
    - tests for the image downloader that data ends up in the right form
- run the indexing just using a custom gap in the bytes. Will later leverage
the multi-modal search functionality that is fresh in jina.

__ui__

- [ ] return a simple webpage that takes a request for a webform and
returns the images as a result.
    - __can use streamlit__
    - can re-use code from the flasky web app.
    - investigate if there is a more elegant solution with existing javascript
    frameworks.

## Version 3:

- ui improvements
    - fancy heading and explanation
    - add in credit to Pexels
    - can add in details on the number of images and from what topics the results we have indexed.
    - add in credit and link back to github
    - improve printing of images. fit more on each page.
- attempt multi-modal searching
- attempt to wrap the computationally expensive parts (bert) in serverless application.
Then, try to host the rest of the application in a single EC2 t2.micro? Or maybe push for
everything to be either dockerised or severless.
    - Chalice?

## Nice to have:

- Have a custom encoder that has been trained upon our data images (if using design templates)

# Getting started

1. Install the package.

    ```bash
    pip install -e . 
    ```

1. Download the data that we will process. It will create the folder `data/`
and put a processed csv into `data/raw`

    ```bash
   design_search --verbosity=DEBUG download --output-csv=testing.csv football friends
    ```

1. Construct the AWS infrastructure. This will require that you have
set up the AWS cli on your system. You will need to pass in the name
of your desired AWS key pair as a variable.

    ```bash
    terraform apply
    ```

1. Copy the application code and data file to our EC2 instance.

    ```bash
    ssh -i ~/.ssh/personal ubuntu@$(terraform output public_dns) 'mkdir code'
    rsync -av -e "ssh -i ~/.ssh/personal" \
      --include='*.csv' --include='.env' --exclude-from=.gitignore \
      .env data src setup.py requirements.txt MANIFEST.in \
      ubuntu@$(terraform output public_dns):code
    ```

1. Install required dependencies

    ```bash
    ssh -i <path/to/your/private_key> ubuntu@$(terraform output public_dns)
    cd code
    conda create -n design_search python=3.7 pip
    source activate design_search
    pip install -r requirements.txt
    ```

1. While within the EC2 instance, run the indexing application:

    ```bash
    design_search index
    ```

1. After that you are free to run the search application:

    ```bash
    design_search search
    ```
