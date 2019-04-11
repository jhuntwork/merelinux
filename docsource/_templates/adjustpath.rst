{% extends "instructions.rst" %}{% block stepname %}Adjust PATH
==========={% endblock %}{% block custom %}At this point, :file:`/mere` should contain everything that is needed to
successfully build the rest of the temporary tools. As a further protection
from utilities in the host system being discovered and referenced in
generated scripts, adjust the PATH environment variable to only contain
:file:`/mere/bin`.

{% endblock %}
