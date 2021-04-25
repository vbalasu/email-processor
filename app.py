from chalice import Chalice

app = Chalice(app_name='email-processor')

def download_file(bucket_name, key):
    import boto3
    s3 = boto3.client('s3')
    filename = '/tmp/' + key.replace('echo/', '')
    s3.download_file(bucket_name, key, filename)
    return filename

def echo(filename):
    import email
    from email import policy
    with open(filename) as f:
        msg = email.message_from_file(f, policy=policy.default)
    sender = msg.get('From')
    subject = msg.get('Subject')
    body_text = msg.get_body('plain').get_payload(decode=True)
    try:
        body_html = msg.get_body('html').get_payload(decode=True)
    except AttributeError:
        body_html = ''
    print(sender, subject, body_text, body_html)
    import boto3
    ses = boto3.client('ses')
    from email.message import EmailMessage
    response = EmailMessage(policy=policy.default)
    response['To'] = sender
    response['Subject'] = subject
    response['From'] = 'echo@cloudmatica.com'
    response.set_content(body_text, maintype='text', subtype='plain')
    response.add_alternative(body_html, maintype='text', subtype='html')
    for a in msg.iter_attachments():
        response.attach(a)
    ses.send_raw_email(RawMessage={'Data': response.as_bytes()})
    return True

def read_body_text(filename):
    import email
    from email import policy
    with open(filename) as f:
        msg = email.message_from_file(f, policy=policy.default)
    body_text = msg.get_body('plain').get_payload(decode=True)
    return str(body_text)

def tts(text, language='en', slow=False):
    from gtts import gTTS
    import hashlib
    myobj = gTTS(text=text, lang=language, slow=slow)
    filename = '/tmp/' + hashlib.sha256(text.encode('utf8')).hexdigest() + '.mp3'
    myobj.save(filename)
    return filename

def mp3_get_s3_url(filename):
    import boto3
    s3 = boto3.client('s3')
    s3_bucket = 'cloudmatica'
    s3_key = filename.replace('/tmp/', '1d/')
    s3.upload_file(filename, s3_bucket, s3_key)
    s3_url = s3.generate_presigned_url('get_object', {'Bucket': s3_bucket, 'Key': s3_key}, ExpiresIn=86400)
    with open('/tmp/url.txt', 'w') as f:
        f.write(s3_url)
    return s3_url

def compose_response(s3_url, recipient='vbalasu@gmail.com', sender='listen@cloudmatica.com', subject='Your audio is ready'):
    import boto3, re
    message = '/tmp/' + re.search('1d/(.*?).mp3', s3_url).group(1) + '.eml'
    ses = boto3.client('ses')
    from email.message import EmailMessage
    from email import policy
    response = EmailMessage(policy=policy.default)
    response['To'] = recipient
    response['Subject'] = subject
    response['From'] = sender
    body_text = s3_url
    response.set_content(body_text, subtype='plain')
    with open(message, 'wb') as f:
        f.write(response.as_bytes())
    ses.send_raw_email(RawMessage={'Data': response.as_bytes()})
    return message

def send_email(message):
    import boto3
    ses = boto3.client('ses')
    with open(message, 'rb') as f:
        email_bytes = f.read()
    ses.send_raw_email(RawMessage={'Data': email_bytes})
    return True

# Integration
def email_to_speech(bucket_name, key):
    filename = download_file(bucket_name, key)
    body_text = read_body_text(filename)
    audio_filename = tts(body_text)
    s3_url = mp3_get_s3_url(audio_filename)
    message = compose_response(s3_url)
    return send_email(message)

@app.on_s3_event(bucket='mail.cloudmatica.com', events=['s3:ObjectCreated:*'])
def handle_s3_event(event):
    print(f"Received event for bucket: {event.bucket}, key: {event.key}")
    #filename = download_file(event.bucket, event.key)
    #echo(filename)
    email_to_speech(event.bucket, event.key)



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
