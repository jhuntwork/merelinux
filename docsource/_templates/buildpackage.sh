{% block buildas %}#!/mere/bin/bash -e
{% endblock %}{% block workingdir %}
# Clean the environment
source /mere/bin/clean_env

# Ensure the required source files are present
cd /mere/sources
fetch \
    {{url}} \
    {{sha256sum}}
{%if extra_filenames %}{% for item in extra_filenames %}fetch \
    {{item.url}} \
    {{item.sha256sum}}
{% endfor %}{% endif %}
{%if patches %}{% for item in patches %}fetch \
    {{item.url}} \
    {{item.sha256sum}}
{% endfor %}{% endif %}# Unpack the main source file into a temporary directory
source_dir=$(unpack -T {{name}}.XXXXXX /mere/sources/{{filename}})
cd "${source_dir:?}"
{% if patches %}
# Apply patches
{% for item in patches %}patch -Np1 -i /mere/sources/{{item.filename}}
{% endfor %}{% endif %}{% endblock %}{% block build %}
# Configure the build
./configure --prefix=/mere

# Compile
make

# Install
make install

{% endblock %}{% block finish %}# Optionally, clean up the source_dir
cd /mere/sources
rm -rf "$source_dir"
{% endblock %}
