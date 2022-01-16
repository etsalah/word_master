#!/usr/bin/env python
"""This module contains code to help in generation of ids (string based) for the
various models in the application."""
import uuid


def generate_id():
    """Generate id for use as primary key"""
    return str(uuid.uuid4()).replace('-', '')

