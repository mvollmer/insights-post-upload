all:

install:
	install insights-post-upload /usr/libexec/
	install -m 644 insights-post-upload.service insights-post-upload.path /usr/lib/systemd/system
