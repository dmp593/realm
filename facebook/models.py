from django.db import models
from django.utils.translation import gettext_lazy as _


FACEBOOK_ACCESS_TOKEN_SCOPE = (
    ("user-short-lived", _("Facebook Short-Lived User Access Token")),
    ("user-long-lived", _("Facebook Long-Lived User Access Token")),
    ("app", _("Facebook App Access Token")),
    ("page", _("Facebook Page Access Token")),
)


class FacebookAccessToken(models.Model):
	scope = models.CharField(
		choices=FACEBOOK_ACCESS_TOKEN_SCOPE,
		max_length=50,
		verbose_name=_('scope')
	)

	access_token = models.CharField(
		max_length=255,
		verbose_name=_('access token')
	)

	expiry = models.DateTimeField(
		verbose_name=_('expiry'),
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = _('facebook access token')
		verbose_name_plural = _('facebook access tokens')
		ordering = ('-expiry', )

	def __str__(self):
		return f"{self.scope} :: {self.access_token[:5]}...{self.access_token[-5:]} @ {self.expiry}"
