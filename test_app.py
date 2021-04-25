import app

def test_get_mail():
    bucket_name = 'mail.cloudmatica.com'
    key = 'echo/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    import os
    if os.path.exists(filename):
        os.remove(filename)
    app.download_file(bucket_name, key)
    assert os.path.exists(filename)

#def integration_test_echo():
#    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
#    assert app.echo(filename) == True

def test_read_body_text():
    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    body_text = app.read_body_text(filename)
    assert type(body_text) == str
    assert 'one more time' in body_text

def test_tts():
    text = 'hello world'
    import os, hashlib
    expected_filename = '/tmp/' + hashlib.sha256(text.encode()).hexdigest() + '.mp3'
    actual_filename = app.tts(text)
    assert expected_filename == actual_filename
    assert os.path.exists(actual_filename)

def test_mp3_get_s3_url():
    filename = '/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.mp3'
    s3_url = app.mp3_get_s3_url(filename)
    assert 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9' in s3_url

def test_url_works():
    import requests
    filename = '/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.mp3'
    response = requests.get(app.mp3_get_s3_url(filename))
    assert response.status_code == 200

def test_compose_response():
    filename = '/tmp/b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9.mp3'
    s3_url = app.mp3_get_s3_url(filename)
    message = app.compose_response(s3_url)
    assert message == filename.replace('.mp3', '.eml')
    import os
    assert os.path.exists(message)