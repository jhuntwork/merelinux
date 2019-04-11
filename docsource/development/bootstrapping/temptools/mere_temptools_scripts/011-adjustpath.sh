#!/mere/bin/bash -e
sed -i '/^PATH=/s@=.*@=/mere/bin@' /mere/bin/clean_env
source /mere/bin/clean_env

# Verify that the current PATH is correct
test "/mere/bin" = "$(printf '%s' "$PATH")"