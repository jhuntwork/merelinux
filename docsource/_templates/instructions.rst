{% block stepname %}{{ name|capitalize() }}
{% for i in name|list() %}={% endfor %}{% endblock %}
{% block custom %}{% endblock %}
{%if pkgname %}
.. glossary::

    Description
        {{description}}

    Rationale
        {{rationale}}

{%if note %}
.. note::

    {{note}}

{% endif %}
{% endif %}

The following script [#f1]_ outlines the commands required to complete this step:

.. literalinclude:: mere_temptools_scripts/{{ buildorder }}-{{ name }}.sh
    :language: bash


.. [#f1] :download:`{{ buildorder }}-{{ name }}.sh <mere_temptools_scripts/{{ buildorder }}-{{ name }}.sh>`
{% block customend %}{% endblock %}
