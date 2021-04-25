import app

#def integration_test_echo():
#    filename = '/tmp/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
#    assert app.echo(filename) == True

def test_email_to_speech():
  bucket_name = 'mail.cloudmatica.com'
  key = 'echo/81nim74n8q0h8q70sg3inomd5v78lhgsd6njq0o1'
  message = app.email_to_speech(bucket_name, key)
  import os
  assert os.path.exists(message)