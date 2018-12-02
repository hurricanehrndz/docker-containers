#!/usr/bin/env python3

##########################################
### NZBGET POST-PROCESSING SCRIPT      ####

# Script to send post-processing info
# to tinyMediaManager.

##########################################
### OPTIONS                            ###

# tmm address.
#Host=http://localhost:8000

### NZBGET POST-PROCESSING SCRIPT      ###
##########################################

import os
import sys
import xmlrpc.client

POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR = 94
POSTPROCESS_NONE = 95

tmm_address = os.environ['NZBPO_HOST']
url = u'{}'.format(tmm_address)

tinyMediaManager = xmlrpc.client.ServerProxy(tmm_address)

if not tinyMediaManager.update():
    sys.exit(POSTPROCESS_ERROR)
if not tinyMediaManager.scrape_unscraped():
    sys.exit(POSTPROCESS_ERROR)
if not tinyMediaManager.rename():
    sys.exit(POSTPROCESS_ERROR)
sys.exit(POSTPROCESS_SUCCESS)
