from django.conf import settings

SANTACLARA_EMOTICONS_CONTEXT = getattr(settings, 'SANTACLARA_EMOTICONS_CONTEXT', settings.STATIC_URL+"images/emoticons")

