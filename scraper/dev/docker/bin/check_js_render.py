import json
import os
import sys
import re

config_arg = os.environ['CONFIG']

if os.path.isfile(config_arg):
    with open(config_arg, 'r') as f:
        conf = f.read()
else:
  conf = config_arg

config = json.loads(conf)

group_regex = re.compile("\\(\?P<(.+?)>.+?\\)")
results = re.findall(group_regex, conf)

if ('js_render' in config and config['js_render']) or len(results) > 0:
        sys.exit(0)
else:
        sys.exit(1)
