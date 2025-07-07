from django.core.mail.backends.smtp import EmailBackend

class PatchedEmailBackend(EmailBackend):
    def open(self):
        """
        Open a network connection. Override to avoid passing keyfile/certfile to starttls().
        Fixes the Python 3.12 + Django 4.1 incompatibility.
        """
        if self.connection:
            return False

        connection_params = {
            'host': self.host,
            'port': self.port,
            'local_hostname': self.local_hostname,
            'timeout': self.timeout,
        }

        self.connection = self.connection_class(**connection_params)

        if self.use_tls:
            self.connection.ehlo()
            self.connection.starttls()  # <- this is the line that avoids keyfile/certfile
            self.connection.ehlo()

        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return True
