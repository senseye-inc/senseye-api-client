Introduction
============

The ``senseye-api-client`` repository makes it easy to connect to and interact with Senseye's Eucalyptus API.

Dependencies
============

``senseye-api-client`` requires FFMPEG for h264 streaming.

Install ``ffmpeg`` for:
- Windows:
  .. code-block:: console
    choco install ffmpeg
- Mac:
  .. code-block:: console
    brew install ffmpeg
- Linux:
  .. code-block:: console
    sudo apt-get install ffmpeg

Other Python dependencies, along with the client library, can be installed via:
.. code-block:: console
  pip install .

How to Get Started
===================

1. Clone the repository and navigate to its root directory:
  .. code-block:: console
    git clone git@github.com:senseyeinc/senseye-api-client.git

  .. code-block:: console
    cd senseye-api-client

2. Install the client library and its Python dependencies:
  .. code-block:: console
    pip install .

3. Get an API key.
  - Go to http://dev.senseye.co

  - Login / Sign Up

  - Create JWT Credentials
      - Navigate to the "API Credentials" section of your dashboard.

      - Click on [+CREATE API CREDENTIAL] > [CREATE API CREDENTIAL]

      - You should now have a **key** and **secret** pair.

  - Copy your key and secret into ``./examples/config.yml`` and save.

Now you can successfully make calls to our API using one of our examples:
- ``camera_stream.py``
- ``static_video.py``

For example, the following will open a bidirectional stream with our servers, sending live video frames from your camera while we send back cognitive load data in response:
.. code-block:: console
  python examples/camera_stream.py
