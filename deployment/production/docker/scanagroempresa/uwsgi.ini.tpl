[uwsgi]
master = true
http = :8000
http-keepalive = true
module = scanterra.wsgi:application
offload-threads = 1
static-map = /${URL_PREFIX}static=./static_prod

; set cheaper algorithm to use, if not set default will be used
cheaper-algo = spare
; minimum number of workers to keep at all times
cheaper = 2
; number of workers to spawn at startup
cheaper-initial = 2
; maximum number of workers that can be spawned
workers = 4
; how many workers should be spawned at a time
cheaper-step = 1

; reload worker after max-requests is reached
max-requests = 1000

; don't bubble write exceptions
; https://github.com/pypa/warehouse/issues/679
; https://github.com/getsentry/raven-python/issues/732
ignore-sigpipe = true
ignore-write-errors = true
disable-write-exception = true

; sometimes needed, for example Sentry
enable-threads = true
