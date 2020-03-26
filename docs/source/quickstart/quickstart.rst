Introduction
============

The ``senseye-api-client`` repository makes it easy to connect to and interact with Senseye's Eucalyptus API.

Dependencies
============

``senseye-api-client`` requires FFMPEG for h264 streaming.

Install ``ffmpeg`` for:

- Windows::

   choco install ffmpeg

- Mac::

   brew install ffmpeg

- Linux::

   sudo apt-get install ffmpeg

Python dependencies are installed along with the client library.

Getting Started
===============

1. Clone the repository and navigate to its root directory::

   git clone git@github.com:senseyeinc/senseye-api-client.git && cd senseye-api-client

2. Install the client library and its Python dependencies::

   pip install .

3. Get an API key:

   a. Go to http://dev.senseye.co

   b. Login / Sign Up

   c. Create JWT Credentials:

      i. Navigate to the "API Credentials" section of your dashboard.

      ii. Click on [+CREATE API CREDENTIAL] > [CREATE API CREDENTIAL]

      iii. You should now have a **key** and **secret** pair.

   d. Copy your key and secret into ``./examples/config.yml`` and save.

Now you can successfully make calls to our API using one of our examples under ``./examples``.

For instance, the following will perform bidirectional streaming between your client and our servers, sending live video frames from your camera while we send back cognitive load data in response::

   python examples/camera_stream.py
