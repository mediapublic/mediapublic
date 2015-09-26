cors_policy = dict(
    enabled=True,
    origins=('*', ),
    max_age=1728000,
    headers=('Origin', 'Content-Type', 'Accept', 'Authorization'),
    credentials=True,
)
