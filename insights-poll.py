# Poll until /var/lib/insights/insights-details.json is 5 minutes
# older than /etc/insights-client/.lastupload, then exit.

# Calling "insights-details --check-results" only returns results
# corresponding to the most recent upload some time after the upload,
# but we don't know when exactly.  We assume that it will not take
# more than 5 minutes.  However, we also want the results as soon as
# they are available so we poll a couple of time before the 5 minutes
# are up.

# We poll fast for the first minute, and then slow down.  Also, there
# is a absolute limit on how often we poll, in case something is wrong
# with the time stamps (such as .lastupload being from 5 years in
# future).

import os
import sys
import subprocess
import time

def details_out_of_date():
    if not os.access("/etc/insights-client/.lastupload", os.F_OK):
        return False
    if not os.access("/var/lib/insights/insights-details.json", os.F_OK):
        return True
    last_upload = os.stat("/etc/insights-client/.lastupload")
    details = os.stat("/var/lib/insights/insights-details.json")
    return details.st_mtime < last_upload.st_mtime + 5*60

tries = 0
while tries < 20 and details_out_of_date():
    subprocess.call([ "insights-client", "--check-results" ])
    if tries < 5:
        time.sleep(10)
    else:
        time.sleep(60)
    tries += 1
