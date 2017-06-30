from wtforms import Form, TextField, validators

class PeerForm(Form):
    hostname = TextField('Hostname:', validators=[validators.DataRequired()])
    key_file = TextField('Keyfile:')
    pub_key_file = TextField('Pubkeyfile:')
    remoteadmlogin = TextField('radmlogin:')
    remotelogin = TextField('rlogin:')
    remotepassword = TextField('Password:', validators=[validators.DataRequired()])
