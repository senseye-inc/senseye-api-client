# Senseye API

## How to ping the Senseye API:

### Clone repository
`git clone git@github.com:senseyeinc/senseye-api-client.git`

### Install client library
`pip install .`

### Install ffmpeg
Our client code relies on ffmpeg for h264 video streaming.

* Windows: `choco install ffmpeg`
* Mac: `brew install ffmpeg`
* Linux: `sudo apt-get install ffmpeg`

You can also install it manually by downloading the executable at https://www.ffmpeg.org/download.html, and then adding the file (ffmpeg) to your system path.

### Get an API Key
1. Go to http://dev.senseye.co

2. Sign Up / Login

3. Navigate to your Dashboard. In the 'API Credentials' section, click on '+CREATE API CREDENTIAL' > 'CREATE API CREDENTIAL' (no need to fill out the fields). You should now have a 'key' and 'secret' pair.

4. Copy your key/secret into ./scripts/setup-client.sh.

The key should be pasted after `SENSEYE_API_JWT_KEY`.

The secret should be pasted after `SENSEYE_API_JWT_SECRET`.

5. Run: `source ./scripts/setup-client.sh`

### Run sample client code
Now you can successfully connect to our API.

Example code can be found in the examples folder.
For example, a simple camera stream can be sent to our API via: `python examples/camera_stream.py`
