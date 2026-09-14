from django.core.mail.backends.smtp import EmailBackend
import smtplib


class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        try:
            self.connection = smtplib.SMTP(
                self.host,
                self.port,
                local_hostname="1723consultinggroup.com",
                timeout=self.timeout,
            )

            if self.use_tls:
                self.connection.starttls(context=self.ssl_context)

            if self.username and self.password:
                self.connection.login(
                    self.username,
                    self.password
                )

            return True

        except Exception:
            if not self.fail_silently:
                raise
            return False