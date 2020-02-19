# Eucalyptus

## How to ping the Eucalyptus server:

### Clone repository (master)
`git clone -b master git@github.com:senseyeinc/eucalyptus-client.git`

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

4. Using the Debugger at https://jwt.io and with the credentials you just created, fill out the 'Decoded' section like so:

    * Header:
    ```
    {
      "alg": "HS256",
      "typ": "JWT"
    }
    ```

    * Payload:
    ```
    {
      "iss": "<key>"
    }
    ```

    * Verify Signature:
    ```
    HMACSHA256(
      base64UrlEncode(header) + "." +
      base64UrlEncode(payload),
      <secret>
    )
    ```

5. Copy your token from the 'Encoded' section and paste it into ./scripts/setup-client.sh (next to `SENSEYE_API_AUTH_TOKEN=`).

6. Run: `source ./scripts/setup-client.sh`

### Run sample client code
Now you can successfully connect to our API.

Example code can be found in the examples folder.
For example, a simple camera stream can be sent to our API via: `python examples/camera_stream.py`
