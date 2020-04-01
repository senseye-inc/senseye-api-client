Introduction
============

The Senseye API Client package makes it easy to connect to and interact with Senseye's Eucalyptus API.

Requirements
============

- Python 3.6+

- FFmpeg (required for h264 streaming):

  - Windows::

      choco install ffmpeg

  - Mac::

      brew install ffmpeg

  - Linux::

      sudo apt-get install ffmpeg

Getting Started
===============

1. Clone the ``senseye-api-client`` repository and navigate to its root directory::

      git clone git@github.com:senseyeinc/senseye-api-client.git && cd senseye-api-client

2. Install the client library along with its Python dependencies::

      pip install grpcio && pip install grpcio-tools && pip install .

3. Get an API key:

   a. Go to http://dev.senseye.co

   b. Login / Sign Up

   c. Create JWT Credentials:

      - Navigate to the "API Credentials" section of your dashboard.

      - Click on [+CREATE API CREDENTIAL] > [CREATE API CREDENTIAL]

      - You should now have a **key** and **secret** pair.

   d. Copy your key and secret into ``./examples/config.yml`` and save.

Now you can successfully make calls to Senseye's API server using any of the examples provided under ``./examples``.

Examples
========

.. literalinclude:: ../../examples/camera_stream.py
    :language: python

This will send a gRPC request to Senseye's API server and initiate a bidirectional stream. If successful, the client will begin sending video frames from your camera feed (provided your permissions), and the API server will in turn respond with cognitive load data for every batch of frames it receives and analyzes.
