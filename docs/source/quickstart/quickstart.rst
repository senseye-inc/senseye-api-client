Introduction
============

The senseye-api-client repository makes it easy to connect to and interact with Senseye's Eucalyptus API.


Dependencies
============

senseye-api-client requires FFMPEG for h264 streaming.

Install ffmpeg via:

- Windows: ``choco install ffmpeg``
- Mac: ``brew install ffmpeg``
- Linux: ``sudo apt-get install ffmpeg``

Other Python dependencies (and the client library) can be installed via:

``pip install .``

Using senseye-api-client
=========================

1. Clone the repository

``git clone git@github.com:senseyeinc/senseye-api-client.git``
``cd senseye-api-client``

2. Install Client Library

Run: ``pip install .``

3. Get an API Key.

- Go to http://dev.senseye.co

- Login/Sign Up

- Create a JWT Key/Secret

    Navigate to the 'API Credentials' section.

    Click on '+CREATE API CREDENTIAL' > 'CREATE API CREDENTIAL' (no need to fill out the fields).

    You should now have a 'key' and 'secret' pair.

- Copy your key/secret into ./scripts/setup-client.sh.

    The key should be pasted after `SENSEYE_API_JWT_KEY`.

    The secret should be pasted after `SENSEYE_API_JWT_SECRET`.

- Set up environment variables.

Run: ``source ./scripts/setup-client.sh``

3. Run sample client code

Now you can successfully connect to our API.

Example code can be found in the examples folder.

For example, a simple camera stream can be sent to our API via:

``python examples/camera_stream.py``
