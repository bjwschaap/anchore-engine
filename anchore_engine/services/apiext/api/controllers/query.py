import copy
import json
import time
import datetime

from anchore_engine.clients import catalog
from anchore_engine.subsys import logger
from flask import request

import anchore_engine.services.common

def query_vulnerabilities(id=None, page=1, limit=None, affected_package=None, affected_package_version=None):
    request_inputs = anchore_engine.services.common.do_request_prep(request, default_params={'id': id, 'page': page, 'limit': limit, 'affected_pacakge': affected_package, 'affected_package_version': None})
    user_auth = request_inputs['auth']
    method = request_inputs['method']
    bodycontent = request_inputs['bodycontent']
    params = request_inputs['params']

    return_object = {}
    httpcode = 500
    userId, pw = user_auth    

    try:
        if affected_package_version and not affected_package:
            httpcode = 400
            raise Exception("if affected_package_version is specified, affected_package must also be specified")

        catalog_call_time = 0.0
        try:
            result = anchore_engine.services.common.get_cached_pagination(query_digest=request_inputs['pagination_query_digest'])
        except Exception as err:
            timer = time.time()
            result = catalog.query_vulnerabilities(user_auth, id=id, affected_package=affected_package, affected_package_version=affected_package_version)
            catalog_call_time = time.time() - timer

        return_object = anchore_engine.services.common.make_response_paginated_envelope(result, envelope_key='vulnerabilities', page=page, limit=limit, dosort=True, sortfunc=lambda x: json.dumps(x), pagination_func=anchore_engine.services.common.do_cached_pagination, query_digest=request_inputs['pagination_query_digest'], ttl=max(30.0, catalog_call_time))
        httpcode = 200
    except Exception as err:
        return_object = anchore_engine.services.common.make_response_error(err, in_httpcode=httpcode)
        httpcode = return_object['httpcode']

    return (return_object, httpcode)

def query_images_by_vulnerability(vulnerability_id=None, severity=None, namespace=None, affected_package=None, page=1, limit=None, vendor_only=True):
    request_inputs = anchore_engine.services.common.do_request_prep(request, default_params={'vulnerability_id': vulnerability_id, 'severity': severity, 'namespace': namespace, 'affected_package': affected_package, 'page': page, 'limit': limit, 'vendor_only': vendor_only})
    user_auth = request_inputs['auth']
    method = request_inputs['method']
    bodycontent = request_inputs['bodycontent']
    params = request_inputs['params']

    return_object = {}
    httpcode = 500
    userId, pw = user_auth

    try:
        catalog_call_time = 0.0
        try:
            result = anchore_engine.services.common.get_cached_pagination(query_digest=request_inputs['pagination_query_digest'])
        except Exception as err:
            timer = time.time()
            catalog_result = catalog.query_images_by_vulnerability(user_auth, vulnerability_id=vulnerability_id, severity=severity, namespace=namespace, affected_package=affected_package, page=page, limit=limit, vendor_only=vendor_only)
            catalog_call_time = time.time() - timer
            result = catalog_result.get('vulnerable_images', [])

        return_object = anchore_engine.services.common.make_response_paginated_envelope(result, envelope_key='images', page=page, limit=limit, dosort=True, sortfunc=lambda x: x['image']['imageDigest'], pagination_func=anchore_engine.services.common.do_cached_pagination, query_digest=request_inputs['pagination_query_digest'], ttl=max(30.0, catalog_call_time))

        httpcode = 200
    except Exception as err:
        return_object = anchore_engine.services.common.make_response_error(err, in_httpcode=httpcode)
        httpcode = return_object['httpcode']

    return (return_object, httpcode)

def query_images_by_package(name=None, version=None, package_type=None, page=1, limit=None):
    request_inputs = anchore_engine.services.common.do_request_prep(request, default_params={'name': name, 'version': version, 'package_type': package_type, 'page': page, 'limit': limit})
    user_auth = request_inputs['auth']
    method = request_inputs['method']
    bodycontent = request_inputs['bodycontent']
    params = request_inputs['params']

    return_object = {}
    httpcode = 500
    userId, pw = user_auth

    try:
        catalog_call_time = 0.0
        try:
            result = anchore_engine.services.common.get_cached_pagination(query_digest=request_inputs['pagination_query_digest'])
        except Exception as err:
            timer = time.time()
            #catalog_result = catalog.query_images_by_vulnerability(user_auth, vulnerability_id=vulnerability_id, severity=severity, namespace=namespace, affected_package=affected_package, page=page, limit=limit, vendor_only=vendor_only)
            catalog_result = catalog.query_images_by_package(user_auth, name=name, version=version, package_type=package_type, page=page, limit=limit)
            catalog_call_time = time.time() - timer
            result = catalog_result.get('matched_images', [])

        return_object = anchore_engine.services.common.make_response_paginated_envelope(result, envelope_key='images', page=page, limit=limit, dosort=True, sortfunc=lambda x: x['image']['imageDigest'], pagination_func=anchore_engine.services.common.do_cached_pagination, query_digest=request_inputs['pagination_query_digest'], ttl=max(30.0, catalog_call_time))

        httpcode = 200
    except Exception as err:
        return_object = anchore_engine.services.common.make_response_error(err, in_httpcode=httpcode)
        httpcode = return_object['httpcode']

    return (return_object, httpcode)


