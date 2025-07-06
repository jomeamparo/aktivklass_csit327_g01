from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class PatchedEmailBackend(DjangoEmailBackend):
    def _send(self, email_message):
        # Patch: Remove keyfile/certfile from starttls()
        if not self.connection:
            self.open()
        try:
            # Remove keyfile/certfile from connection if present
            if hasattr(self.connection, 'starttls'):
                orig_starttls = self.connection.starttls
                def safe_starttls(*args, **kwargs):
                    kwargs.pop('keyfile', None)
                    kwargs.pop('certfile', None)
                    return orig_starttls(*args, **kwargs)
                self.connection.starttls = safe_starttls
            return super()._send(email_message)
        finally:
            if not self.connection:
                self.close() 