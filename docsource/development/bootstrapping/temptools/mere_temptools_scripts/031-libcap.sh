#!/mere/bin/bash -e

# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-2.25.tar.xz \
    693c8ac51e983ee678205571ef272439d83afe62dd8e424ea14ad9790bc35162

# Unpack the main source file into a temporary directory
source_dir=$(unpack -T libcap.XXXXXX /mere/sources/libcap-2.25.tar.xz)
cd "${source_dir:?}"

# Compile and Install
make RAISE_SETFCAP=no prefix=/mere lib=lib install

# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
