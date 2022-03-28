import binascii
import collections
import datetime
import hashlib
import logging
from typing import Any, Dict, Generator, Iterable, Tuple
from urllib.parse import quote

import boto3
from botocore.exceptions import ClientError
from flask import Response, redirect, stream_with_context
from google.oauth2 import service_account

from cyberpunk.config import get_config


def stream_audio_file(filename: str, chunk_size: int = 4096) -> Generator:
    with open(f"/tmp/{filename}", "rb") as faudio:
        data = faudio.read(chunk_size)
        while data:
            yield data
            data = faudio.read(chunk_size)


def build_local_stream(processed_file, file_type):
    return Response(
        stream_with_context(stream_audio_file(processed_file)),
        mimetype=file_type,
    )


def build_presigned_s3_url(key: str):
    """Generate a presigned URL to share an S3 object

    @param key: key to the audio file
    @return: Presigned URL as string. If error, returns None.
    """

    config = get_config()

    bucket_name = config.s3_storage_bucket
    object_name = f"{config.s3_storage_base_dir}{key}"
    expiration = 3600

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def build_presigned_gcs_url(key: str):
    config = get_config()

    assert (
        config.gcs_results_bucket is not None
        or config.gcs_storage_bucket is not None
    )

    bucket_name = (
        config.gcs_results_bucket
        if config.gcs_results_bucket is not None
        else config.gcs_storage_bucket
    )
    object_name = f"{config.gcs_results_base_dir if config.gcs_results_base_dir is not None else ''}{key}"
    expiration = 3600
    service_account_file = config.google_application_credentials

    escaped_object_name = quote(object_name, safe=b"/~")
    canonical_uri = "/{}".format(escaped_object_name)

    datetime_now = datetime.datetime.now(tz=datetime.timezone.utc)
    request_timestamp = datetime_now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = datetime_now.strftime("%Y%m%d")

    google_credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
    )
    client_email = google_credentials.service_account_email
    credential_scope = f"{datestamp}/auto/storage/goog4_request"
    credential = "{}/{}".format(client_email, credential_scope)

    host = f"{bucket_name}.storage.googleapis.com"
    headers = {"host": host}

    canonical_headers = ""
    for k, v in headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += "{}:{}\n".format(lower_k, strip_v)

    signed_headers = ""
    for k, _ in headers.items():
        lower_k = str(k).lower()
        signed_headers += "{};".format(lower_k)
    signed_headers = signed_headers[:-1]  # remove trailing ';'

    query_parameters: Dict = {
        "X-Goog-Algorithm": "GOOG4-RSA-SHA256",
        "X-Goog-Credential": credential,
        "X-Goog-Date": request_timestamp,
        "X-Goog-Expires": expiration,
        "X-Goog-SignedHeaders": signed_headers,
    }

    canonical_query_string = ""
    items: Iterable[Tuple[Any, Any]] = list(query_parameters.items())
    ordered_query_parameters: collections.OrderedDict = (
        collections.OrderedDict(
            sorted(items),
        )
    )
    for k, v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe="")
        encoded_v = quote(str(v), safe="")
        canonical_query_string += "{}={}&".format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1]  # remove trailing '&'

    canonical_request = "\n".join(
        [
            "GET",
            canonical_uri,
            canonical_query_string,
            canonical_headers,
            signed_headers,
            "UNSIGNED-PAYLOAD",
        ],
    )

    canonical_request_hash = hashlib.sha256(
        canonical_request.encode(),
    ).hexdigest()

    string_to_sign = "\n".join(
        [
            "GOOG4-RSA-SHA256",
            request_timestamp,
            credential_scope,
            canonical_request_hash,
        ],
    )

    # signer.sign() signs using RSA-SHA256 with PKCS1v15 padding
    signature = binascii.hexlify(
        google_credentials.signer.sign(string_to_sign),
    ).decode()

    scheme_and_host = "{}://{}".format("https", host)
    signed_url = "{}{}?{}&x-goog-signature={}".format(
        scheme_and_host,
        canonical_uri,
        canonical_query_string,
        signature,
    )

    logging.critical(
        f"generated gcs signed url scheme_host '{scheme_and_host}', canonical_uri '{canonical_uri}', canonical_query_string '{canonical_query_string}', "
        f"signature '{signature}'",
    )

    return signed_url


def build_response(processed_file, file_type):
    config = get_config()
    if config.gcs_results_bucket is None and config.s3_storage_bucket is None:
        return build_local_stream(processed_file, file_type)
    elif config.gcs_results_bucket is not None:
        url = build_presigned_gcs_url(processed_file)
        return redirect(url, 301)
    elif config.s3_storage_bucket is not None:
        url = build_presigned_s3_url(processed_file)
        return redirect(url, 301)
    else:
        logging.error("que?")
