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
    body_text = msg.get_body('plain').get_payload()
    body_html = msg.get_body('html').get_payload()
    print(sender, subject, body_text, body_html)
    import boto3
    ses = boto3.client('ses')
    from email.message import EmailMessage
    response = EmailMessage(policy=policy.default)
    response['To'] = sender
    response['Subject'] = subject
    response['From'] = 'echo@cloudmatica.com'
    response.set_content(body_text, subtype='plain')
    response.add_alternative(body_html, subtype='html')
    for a in msg.iter_attachments():
        response.attach(a)
    ses.send_raw_email(RawMessage={'Data': response.as_bytes()})
    return True

@app.on_s3_event(bucket='mail.cloudmatica.com', events=['s3:ObjectCreated:*'])
def handle_s3_event(event):
    print(f"Received event for bucket: {event.bucket}, key: {event.key}")
    filename = download_file(event.bucket, event.key)
    echo(filename)



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
