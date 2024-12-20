"""Module for downloading files from object stores."""

import logging
import os
import tarfile
import time
from functools import wraps
from tempfile import TemporaryDirectory
from typing import List, Tuple
from urllib.parse import urlparse

import obstore

FILES_TAR_FILE_NAME = "include-files.tar.gz"
INTERNAL_APP_ENDPOINT_PATTERN = os.getenv("INTERNAL_APP_ENDPOINT_PATTERN")

logger = logging.getLogger(__name__)


def _generate_url_query_name(app_name: str, pattern: str = INTERNAL_APP_ENDPOINT_PATTERN) -> str:
    return pattern.replace("{app_fqdn}", app_name)


def _extract_bucket_and_path(uri: str) -> Tuple[str, str]:
    parsed_uri = urlparse(uri)
    bucket_name = parsed_uri.netloc
    path_name = parsed_uri.path.lstrip("/")

    return bucket_name, path_name


def retry(retries, delay):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= retries:
                if attempt > 0:
                    logger.debug(f"Retrying [{attempt}/{retries}] {func.__name__} with {args}, {kwargs}")
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempt += 1
                    if attempt > retries:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


@retry(retries=10, delay=2)
def _download_file(store, path_name: str, dest: str):
    resp = obstore.get(store, path_name)
    stream = resp.stream()

    with open(dest, "wb") as f:
        for buf in stream:
            f.write(buf)


def get_store(uri: str, bucket: str):
    if uri.startswith("s3://") or uri.startswith("s3a://"):
        from obstore.store import S3Store

        return S3Store.from_env(bucket=bucket)
    elif uri.startswith("gs://"):
        from obstore.store import GCSStore

        return GCSStore.from_env(bucket=bucket)
    else:
        raise RuntimeError(f"protocol in {uri} does not work")


def download_code(uri: str, dest: str):
    logger.debug(f"Downloading code from {uri} to {dest}")
    bucket, path_name = _extract_bucket_and_path(uri)

    store = get_store(uri, bucket)

    # Simplify when Python 3.12+ only, by always setting the `extract_kwargs`
    # https://docs.python.org/3.12/library/tarfile.html#extraction-filters
    extract_kwargs = {}
    if hasattr(tarfile, "data_filter"):
        extract_kwargs["filter"] = "data"

    with TemporaryDirectory() as temp_dir:
        temp_dest = os.path.join(temp_dir, FILES_TAR_FILE_NAME)
        _download_file(store, path_name, temp_dest)

        with tarfile.open(temp_dest, "r:gz") as tar:
            tar.extractall(path=dest, **extract_kwargs)


def download_single_file(uri: str, dest: str) -> str:
    logger.info(f"Downloading file from {uri} to {dest}")
    bucket, path_name = _extract_bucket_and_path(uri)

    dest_path = os.path.join(dest, path_name)
    parent_dest = os.path.dirname(dest_path)
    if not os.path.exists(parent_dest):
        os.makedirs(parent_dest)

    # TODO: Support other object stores
    store = get_store(uri, bucket)

    _download_file(store, path_name, dest_path)
    return dest_path


def download_directory(uri: str, dest: str) -> str:
    logger.info(f"Downloading directory from {uri} to {dest}")
    bucket, path_name = _extract_bucket_and_path(uri)

    store = get_store(uri, bucket)
    all_records = obstore.list(store, prefix=path_name)
    for records in all_records:
        for record in records:
            src = record["path"]
            rel_dest_path = os.path.relpath(src, path_name)
            dest_path = os.path.join(dest, rel_dest_path)

            dirname = os.path.dirname(dest_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            logger.info(f"Downloading file from {bucket}/{src} to {dest_path}")
            _download_file(store, src, dest_path)

    return dest


def download_inputs(user_inputs: List[dict], dest: str) -> Tuple[dict, dict]:
    logger.debug(f"Downloading inputs for {user_inputs}")

    output = {}
    env_vars = {}
    for user_input in user_inputs:
        if user_input["auto_download"]:
            user_dest = user_input["dest"] or dest
            if user_input["type"] == "file":
                value = download_single_file(user_input["value"], user_dest)
            elif user_input["type"] == "directory":
                value = download_directory(user_input["value"], user_dest)
            else:
                raise ValueError("Can only download files or directories")
        else:
            # Resolve url query
            value = user_input["value"]
            if user_input["type"] == "url_query":
                value = _generate_url_query_name(value)

        output[user_input["name"]] = value

        if user_input["env_name"] is not None:
            env_vars[user_input["env_name"]] = value

    return output, env_vars
