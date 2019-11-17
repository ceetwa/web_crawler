```usage: crawler.py [-h] [-v] [-m MAX] [-l LIST] [-d DB] [-f] [-u USER_AGENT]

Gather stats about a list of URLs

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose mode (enables debug logging)
  -m MAX, --max MAX     Max number of URLs to process
  -l LIST, --list LIST  URL list file to use (realtive path from this script)
  -d DB, --db DB        Output database name (filename only, placed in the
                        'data' directory)
  -f, --follow          Follow redirects (creates secondary db with all
                        redirections performed)
  -u USER_AGENT, --user_agent USER_AGENT
                        User agent string (use 'random' to randomise)```
