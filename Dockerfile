# Start from the official Python base image.
FROM python:3.10
EXPOSE 80

# Set the current working directory to /code.
#
# This is where we'll put the requirements.txt file and the app directory.
WORKDIR /code
ENV PYTHONPATH /code/app

# Copy the file with the requirements to the /code directory.
#
# Copy only the file with the requirements first, not the rest of the code.
#
# As this file doesn't change often, Docker will detect it and use the cache for this step, enabling the cache for the next step too.
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
#
# The --no-cache-dir option tells pip to not save the downloaded packages locally, as that is only if pip was going to be run again to install the same packages, but that's not the case when working with containers.
#
# Note:
# The --no-cache-dir is only related to pip, it has nothing to do with Docker or containers.
#
# The --upgrade option tells pip to upgrade the packages if they are already installed.
#
# Because the previous step copying the file could be detected by the Docker cache, this step will also use the Docker cache when available.
#
# Using the cache in this step will save you a lot of time when building the image again and again during development, instead of downloading and installing all the dependencies every time.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
