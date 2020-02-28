"""This is the custom vcr filter."""
import json
import os

from vcr import VCR

# remove sensitive values from JSON response
BAD_FIELDS = [
    'checkInSessionToken',
    'first-name',
    'firstName',
    'last-name',
    'lastName',
    'name',
    'passengerInfo',
    'passengers',
    'recordLocator',
]

# pylint: disable=invalid-name


def redact(obj):
    """Redact bad fields."""
    if isinstance(obj, (''.__class__, u''.__class__)):
        return
    for k, v in list(obj.items()):
        if k in BAD_FIELDS:
            obj[k] = '[REDACTED]'
        elif isinstance(v, list) and not isinstance(v, str):
            for o in v:
                redact(o)
        elif isinstance(v, dict):
            redact(v)


def filter_payload(response):
    """Filter for before_record_response."""
    s = response['body']['string']
    if len(s) == 0:
        return response
    string_body = s.decode('utf8')
    try:
        body = json.loads(string_body)
        redact(body)
        response['body']['string'] = json.dumps(body).encode()
    finally:
        return response  # pylint: disable=lost-exception


def custom_vcr():
    """Redifines vcr test."""
    dirname = os.path.dirname(__file__)
    return VCR(
        decode_compressed_response=True,
        cassette_library_dir=os.path.join(
            dirname,
            'fixtures/cassettes',
        ),
        path_transformer=VCR.ensure_suffix('.yml'),
        filter_query_parameters=BAD_FIELDS,
        before_record_response=filter_payload,
        filter_post_data_parameters=BAD_FIELDS,
        match_on=['path', 'method'],
    )
