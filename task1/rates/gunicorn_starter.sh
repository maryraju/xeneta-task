#!/bin/sh

export DIP=$doc_ip
gunicorn -b :3000 wsgi