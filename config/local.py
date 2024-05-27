SECRET_KEY = "-47u^b24464!bpl2vse2*l!=+qzgy1cg9qr&z2(*rsa5)-56i!"
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://redis:6379/0")],
        },
    },
}
