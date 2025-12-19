import winsound


class AudioNotesMixin:
    _page_not_found_path = "audio/page_not_found.wav"
    _access_restricted_path = "audio/access_restricted.wav"
    _bad_connection_path = "audio/bad_connection.wav"
    _complete = "audio/complete.wav"

    @classmethod
    def page_not_found_audio(cls):
        winsound.PlaySound(cls._page_not_found_path, winsound.SND_FILENAME)

    @classmethod
    def access_restricted_audio(cls):
        winsound.PlaySound(cls._access_restricted_path, winsound.SND_FILENAME)

    @classmethod
    def bad_connection_audio(cls):
        winsound.PlaySound(cls._bad_connection_path, winsound.SND_FILENAME)

    @classmethod
    def complete_audio(cls):
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
        winsound.PlaySound(cls._complete, winsound.SND_FILENAME)


