#!/bin/bash
set -Eeuxo pipefail

./pipeline.sh example_crawl
diff example_output/part-00000 output/part-00000
diff example_output/part-00001 output/part-00001
diff example_output/part-00002 output/part-00002
