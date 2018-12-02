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
url = u'{}/RPC2'.format(tmm_address)

tinyMediaManager = xmlrpc.client.ServerProxy(tmm_address)

tinyMediaManager.update() or sys.exit(POSTPROCESS_ERROR)
tinyMediaManager.scrape_unscraped() or sys.exit(POSTPROCESS_ERROR)
tinyMediaManager.rename() or sys.exit(POSTPROCESS_ERROR)
sys.exit(POSTPROCESS_SUCCESS)
