import uuid

from photition_models.models.user.photition_session_model import PhotitionSession



def generate_token():
    token = uuid.uuid4().hex
    if PhotitionSession.objects.filter(session_token=token).first() is None:
        return token
    else:
        return generate_token()
