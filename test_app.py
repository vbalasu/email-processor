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

def test_echo():
    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
    assert app.echo(filename) == True
