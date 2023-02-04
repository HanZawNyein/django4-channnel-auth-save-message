# django4-channnel-auth-save-message

### Enable a Channel Layer

#### Redis Channel Layer

    docker run -p 6379:6379 -d redis:5

    CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },

}

#### In-Memory Channel Layer

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
