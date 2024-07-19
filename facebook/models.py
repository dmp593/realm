from django.db import models


FACEBOOK_ACCESS_TOKEN_SCOPE = (
    ("user-short-lived", "Facebook Short-Lived User Access Token"),
    ("user-long-lived", "Facebook Long-Lived User Access Token"),
    ("app", "Facebook App Access Token"),
    ("page", "Facebook Page Access Token"),
)


class FacebookAccessToken(models.Model):
	scope = models.CharField(choices=FACEBOOK_ACCESS_TOKEN_SCOPE, max_length=50)

	access_token = models.CharField(max_length=255)

	# this should be set according to the scope.
	
	# eg: user-long-lived token has 60 days until expires:
	# from django.utils.timezone import now
	# from datetime import timedelta
	#
	# Token(scope='user-long-lived', access_token='...', expiry=now() + timedelta(days=60))
	expiry = models.DateTimeField()

	class Meta:
		ordering = ('-expiry', )

	def __str__(self):
		return f"{self.scope} :: {self.access_token[:5]}...{self.access_token[-5:]} @ {self.expiry}"
