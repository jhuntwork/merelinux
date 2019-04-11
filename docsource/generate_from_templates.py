import json
import os
import shutil
import subprocess

import jinja2


TEMPTOOLS = 'development/bootstrapping/temptools'


def url_basename(source):
    return sources[source].get('url').split('/')[-1]


# Grab the basic build order info
with open('resources/buildorder.json', 'r') as orderfd:
    order = json.load(orderfd)

# Grab a flattened, unique list of source infor required
source_list = [x['sources'] for x in order if 'sources' in x]
unique_flattened = set(x for lst in source_list for x in lst)

# Pull out from the PKGBUILD files the metadata about each
# source
sources = {}
for item in unique_flattened:
    sources[item] = json.loads(subprocess.check_output(
            ['./pull_source_info.sh', item]))

# Generate an the temptools buildorder index
with open('_templates/buildorder.rst', 'w') as toctree:
    output = """.. toctree::
   :hidden:
   :numbered:

"""
    toctree.write(output)
    for item in order:
        toctree.write('   temptools/{}\n'.format(item.get('name')))

# Delete any existing content in the temptools directory, and create
# an empty mere_temptools_scripts directory
shutil.rmtree(TEMPTOOLS, ignore_errors=True)
os.makedirs('{}/mere_temptools_scripts'.format(TEMPTOOLS))

env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('_templates'))

# Cycle through the build order and generate any content
i = 0
for item in order:
    i = i+1
    data = {}
    data['name'] = item.get('name')
    data['extra_filenames'] = []
    data['patches'] = []
    data['buildorder'] = '{:03d}'.format(i)
    patchlist = item.get('patches', [])

    if 'sources' in item:
        primary_source = item['sources'][0]
        data.update(sources[primary_source])
        data['filename'] = url_basename(primary_source)
        for source in item['sources'][1:]:
            extra_data = sources[source]
            extra_data['name'] = source
            extra_data['filename'] = url_basename(source)
            data['extra_filenames'].append(extra_data)
        for patch in patchlist:
            patch['filename'] = patch.get('url', '').split('/')[-1]
            data['patches'].append(patch)

    with open('{}/{}.rst'.format(TEMPTOOLS, data['name']), 'w') as inc:
        custom_template = '_templates/{}.rst'.format(data['name'])
        if os.path.exists(custom_template):
            template = env.get_template(os.path.basename(custom_template))
        else:
            template = env.get_template('instructions.rst')
        inc.write(template.render(**data))

    with open('{}/mere_temptools_scripts/{}-{}.sh'.format(
                TEMPTOOLS, data['buildorder'], data['name']),
              'w') as script:
        custom_template = '_templates/{}.sh'.format(data['name'])
        if os.path.exists(custom_template):
            template = env.get_template(os.path.basename(custom_template))
        else:
            template = env.get_template('buildpackage.sh')
        script.write(template.render(**data))
