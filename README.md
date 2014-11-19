# hiyapyco

HiYaPyCo - A Hierarchical Yaml Python Config


## Description

A simple python lib allowing hierarchical config files in YAML syntax.


## Key Features

* hierarchical overlay of multiple YAML files
* multiple merge methods for hierarchical YAML files
* variable interpolation using jinja2


## Requirements

* PyYAML aka. python-yaml
* Jinja2 aka. python-jinja2


## Usage

A simple example:

    import hiyapyco
    conf = hiyapyco.load('yamlfile1' [,'yamlfile2' [,'yamlfile3' [...]]] [,kwargs])
    print(hiyapyco.dump(conf))

### args

All `args` are handled as file names. They may be strings or list of strings.

### kwargs

* `method`: bit (one of the listed below):

  * `hiyapyco.METHOD_SIMPLE`: replace values (except for lists a simple merge is performed) (default method)
  * `hiyapyco.METHOD_MERGE`: perform a deep merge

* `interpolate`: boolean : perform interpolation after the merge (default: False)

* `failonmissingfiles`: boolean : fail if a supplied YAML file can not be found (default: True)

* `loglevel`: int : loglevel for the hiyapyco logger; should be one of the valid levels from `logging`: 'WARN', 'ERROR', 'DEBUG', 'I    NFO', 'WARNING', 'CRITICAL', 'NOTSET' (default: default of `logging`)

* `loglevelmissingfiles`: int : one of the valid levels from `logging`: 'WARN', 'ERROR', 'DEBUG', 'INFO', 'WARNING', 'CRITICAL', 'NOTSET' (default: `logging.ERROR` if `failonmissingfiles = True`, else `logging.WARN`)


### interpolation

The default jinja2.Environment for the interpolation is

    hiyapyco.jinja2env = Environment(undefined=Undefined)

This means that undefined vars will be ignored and replaced with a empty string.
If you like to change the jinja2 Environment use dfor the interpolation, set `hiyapyco.jinja2env` **before** calling `hiyapyco.load`!

If you like to keep the undefined var as string but raise no error, use

    hiyapyco.jinja2env = Environment(undefined=DebugUndefined)

If you like to raise a error on undefined vars, use

    hiyapyco.jinja2env = Environment(undefined=StrictUndefined)

See: [jinja2.Environment](http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment)


## Install

### from source

Using python setuptools:

    git clone https://github.com/zerwes/hiyapyco
    cd hiyapyco
    sudo python setup.py install

### pip

    pip install HiYaPyCo

### debian packages

    echo "deb http://repo.zero-sys.net/hiyapyco/deb ./" > /etc/apt/sources.list.d/hiyapyco.list
    gpg --keyserver subkeys.pgp.net --recv-key ED7D414C
    gpg --armor --export ED7D414C | apt-key add -
    apt-get update
    apt-get install python3-hiyapyco python-hiyapyco

### rpm packages

use `http://repo.zero-sys.net/hiyapyco/rpm` as URL for the yum repo
and `http://jwhoisserver.net/key.asc` as the URL for the key.

## License

(c) 2014 Klaus Zerwes [zero-sys.net](http://zero-sys.net)  
This package is free software.  
This software is licensed under the terms of the
GNU LESSER GENERAL PUBLIC LICENSE version 3 or later,
as published by the Free Software Foundation.  
See [https://www.gnu.org/licenses/lgpl.html](https://www.gnu.org/licenses/lgpl.html)

