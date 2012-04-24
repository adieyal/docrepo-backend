docrepo-backend
===============

A django application that abstracts access to document repositories

overview
========

This project provides an abstract interface to multiple document repository backends using a simple REST interface. Backends are developed as separate modules. Files and other resources are accessed through a simple REST interface. 

Resources are queried using a tag based mechanism. Backends that don''t natively support tags have tags imposed on them.

example
=======

As an example, let''s use a simple file system backend to describe how this works. Say we have the following file structure::

    - var
        - log
            - http
                - log1
                - log2
            - smtp
                - log3
                - jeff
                    - log4

using the file system backend we can define one or more ``source`` paths. In our case, we are interested in providing access to the log directory. In the admin suite we create a new file system source that points to ``/var/log`` and we call it ``log_files``. It is now possible to access resources under the ``/var/log`` directory through the ``log_files`` source. Note, a user is never exposed to the underlying path. 

A simple query pointing at ``log_files`` will return all files in all directories witihn that source in a flat list. For example the following query::

    http://docrepo/list/log_files/

will return the following json string::

    [{
        'name' : 'log1',
        'resource_id' : '6732433',
        .
        .
        .
    },
    {
        'name' : 'log2',
        'resource_id' : '4364332',
        .
        .
        .
    }
    .
    .
    .
    {
        'name' : 'log4',
        'resource_id' : '3512133',
        .
        .
        .
    }]

where the elipses refer to other resource metadata that might be available. The resource_id attribute is a unique identifier to the resource which is generated by a specific backend.

One of the metadata fields not show above is the tags fields. Tags are defined differently by each backend. Some document repositories natively store tags as part of their metadata. Filesystems do not. In this case, this basic backend will induce tags by splitting the path to the resource. For instance, log4 will have the following tags: smtp jeff. 

Filtering based on tags can be achieved as follows::

    http://docrepo/list/log_files/smtp+jeff

This will return only those documents that contain the tag smtp as well as the tag jeff.

The rationale behind ignoring the underlying hierarchical representation is to allow for manipulation of the structure visualisation by the end-user.

It is also possible to request the resource using the following request::

    http://docrepo/get/log_files/?resource_id=3512133

This will return the following::

    {"contents": "ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKCmNsYXNzIEJhY2tlbmQ6CiAgICAiIiIKICAgICAgICBCYWNrZW5kIGFic3RyYWN0aW9uIGNsYXNzIGZvciBkb2NyZXBvIGFwcGxpY2F0aW9uCiAgICAiIiIKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBiYWNrZW5kX2lkKToKICAgICAgICAgICAgc2VsZi5fY2xhc3MgPSBldmFsKHNldHRpbmdzLkJBQ0tFTkRfSURfTUFQW2JhY2tlbmRfaWRdKQoKICAgIGRlZiBsaXN0X3Jlc291cmNlcyhzZWxmLCBzb3VyY2UsICp0YWdzKToKICAgICAgICByZXR1cm4gc2VsZi5fY2xhc3MubGlzdF9yZXNvdXJjZXMoc291cmNlLCAqdGFncykKCiAgICBkZWYgZ2V0X3Jlc291cmNlKHNlbGYsIHNvdXJjZSwgcmVzb3VyY2VfaWQpOgogICAgICAgIHJldHVybiBzZWxmLl9jbGFzcy5nZXRfcmVzb3VyY2Uoc291cmNlLCByZXNvdXJjZV9pZCkKCg=="}

Note that the contents of the file are base64 encoded.

Addtional backends will be developed as needed.


