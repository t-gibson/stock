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

## Version 1:

- terraform: an S3 bucket, an EC2 image that has docker installed.
- run a simple EC2 instance that has docker installed. Then inside we can build
and run a simple docker image.
- Locally stored files on S3. Have a `download_files.sh` script to download images
and upload to aws.
- files are connected to S3. Which is added as a volume to docker image.
- docker image can then be ssh-ed into, where we run an index command (saved to S3).
- then from within docker image, we can call the query command

## Version 2:

- Query the images with a stock image API. Do all the indexing in batch myself. And store the url to get the actual image. Then the getting the image can be done in the output function callback call.

## Version 3:

- Have a frontend UI for querying the images
- Wrap each step as a docker image.
- Be able to use natural language for searching the images. I.e. if we can store the chunk as the image
description instead.

## Version 4:

- Dockerise each step. S3 blob for any data. Terraform steps for creating the required elements.

## Nice to have:

- Have a custom encoder that has been trained upon our data images (if using design templates)
- Work on semantic text -> image search (use ImageBERT)

# Things I've learnt

- progressively calling index steps will append to existing indexed data, provided the configs are the same (i.e. workspace)
- protobuf is the preferred messaging between the pods. I need to read up on
how this works compared to REST.