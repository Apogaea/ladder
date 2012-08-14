from fusionbox.fabric_helpers import *

env.roledefs = {
        'dev': ['dev.fusionbox.com'],
        }

env.project_name = 'ladder'
env.short_name = 'ladder'

stage = roles('dev')(stage)
