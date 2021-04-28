# USAGE: pytest test_app.py --capture=no

import app

def setup_function(function):
    print("setting up", function)

def test_get_mail():
    bucket_name = 'mail.cloudmatica.com'
    key = 'echo/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    import os
    if os.path.exists(filename):
        os.remove(filename)
    filename = app.download_file(bucket_name, key)
    print(filename)
    assert os.path.exists(filename)

def test_parse_mail():
    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    email_parts = app.parse_email(filename)
    print(email_parts)
    assert email_parts['subject'] == 'Fwd: Test incoming email into S3'
    assert email_parts['sender'] == 'Vijay Balasubramaniam <vbalasu@gmail.com>'
    assert 'one more time' in email_parts['body_text']
    assert 'one more time' in email_parts['body_html']

def test_read_body_text():
    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    body_text = app.read_body_text(filename)
    print(body_text)
    assert type(body_text) == str
    assert 'one more time' in body_text

def test_tts():
    text = 'hello world'
    import os, hashlib
    expected_filename = '/tmp/' + hashlib.sha256(text.encode()).hexdigest() + '.mp3'
    actual_filename = app.tts(text)
    print(actual_filename)
    assert expected_filename == actual_filename
    assert os.path.exists(actual_filename)

def test_mp3_get_s3_url():
    filename = '/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.mp3'
    s3_url = app.mp3_get_s3_url(filename)
    print(s3_url)
    assert 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9' in s3_url

def test_url_works():
    import requests
    filename = '/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.mp3'
    response = requests.get(app.mp3_get_s3_url(filename))
    print(response.status_code)
    assert response.status_code == 200

def test_compose_response():
    filename = '/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.mp3'
    email_parts = {
        'subject': 'Fwd: Test incoming email into S3',
        'sender': 'Vijay Balasubramaniam <vbalasu@gmail.com>',
        'body_text': 'one more time\n'
    }
    s3_url = app.mp3_get_s3_url(filename)
    message = app.compose_response(s3_url, email_parts)
    assert message == filename.replace('.mp3', '.eml')
    import os
    print(message)
    assert os.path.exists(message)

def test_send_email():
    assert app.send_email('/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.eml') == True