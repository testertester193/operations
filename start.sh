#!/bin/bash
gunicorn operation:server --bind 0.0.0.0:10000