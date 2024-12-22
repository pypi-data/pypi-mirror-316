from setuptools import setup

name = "types-workalendar"
description = "Typing stubs for workalendar"
long_description = '''
## Typing stubs for workalendar

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`workalendar`](https://github.com/workalendar/workalendar) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `workalendar`. This version of
`types-workalendar` aims to provide accurate annotations for
`workalendar==17.0.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/workalendar`](https://github.com/python/typeshed/tree/main/stubs/workalendar)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`097581ea47d0fd77f097c88d80d5947e0218d9c4`](https://github.com/python/typeshed/commit/097581ea47d0fd77f097c88d80d5947e0218d9c4).
'''.lstrip()

setup(name=name,
      version="17.0.0.20241221",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/workalendar.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['workalendar-stubs'],
      package_data={'workalendar-stubs': ['__init__.pyi', 'africa/__init__.pyi', 'africa/algeria.pyi', 'africa/angola.pyi', 'africa/benin.pyi', 'africa/ivory_coast.pyi', 'africa/kenya.pyi', 'africa/madagascar.pyi', 'africa/mozambique.pyi', 'africa/nigeria.pyi', 'africa/sao_tome.pyi', 'africa/south_africa.pyi', 'africa/tunisia.pyi', 'america/__init__.pyi', 'america/argentina.pyi', 'america/barbados.pyi', 'america/brazil.pyi', 'america/canada.pyi', 'america/chile.pyi', 'america/colombia.pyi', 'america/el_salvador.pyi', 'america/mexico.pyi', 'america/panama.pyi', 'america/paraguay.pyi', 'asia/__init__.pyi', 'asia/china.pyi', 'asia/hong_kong.pyi', 'asia/israel.pyi', 'asia/japan.pyi', 'asia/kazakhstan.pyi', 'asia/malaysia.pyi', 'asia/philippines.pyi', 'asia/qatar.pyi', 'asia/singapore.pyi', 'asia/south_korea.pyi', 'asia/taiwan.pyi', 'astronomy.pyi', 'core.pyi', 'europe/__init__.pyi', 'europe/austria.pyi', 'europe/belarus.pyi', 'europe/belgium.pyi', 'europe/bulgaria.pyi', 'europe/cayman_islands.pyi', 'europe/croatia.pyi', 'europe/cyprus.pyi', 'europe/czech_republic.pyi', 'europe/denmark.pyi', 'europe/estonia.pyi', 'europe/european_central_bank.pyi', 'europe/finland.pyi', 'europe/france.pyi', 'europe/georgia.pyi', 'europe/germany.pyi', 'europe/greece.pyi', 'europe/guernsey.pyi', 'europe/hungary.pyi', 'europe/iceland.pyi', 'europe/ireland.pyi', 'europe/italy.pyi', 'europe/latvia.pyi', 'europe/lithuania.pyi', 'europe/luxembourg.pyi', 'europe/malta.pyi', 'europe/monaco.pyi', 'europe/netherlands.pyi', 'europe/norway.pyi', 'europe/poland.pyi', 'europe/portugal.pyi', 'europe/romania.pyi', 'europe/russia.pyi', 'europe/scotland/__init__.pyi', 'europe/scotland/mixins/__init__.pyi', 'europe/scotland/mixins/autumn_holiday.pyi', 'europe/scotland/mixins/fair_holiday.pyi', 'europe/scotland/mixins/spring_holiday.pyi', 'europe/scotland/mixins/victoria_day.pyi', 'europe/serbia.pyi', 'europe/slovakia.pyi', 'europe/slovenia.pyi', 'europe/spain.pyi', 'europe/sweden.pyi', 'europe/switzerland.pyi', 'europe/turkey.pyi', 'europe/ukraine.pyi', 'europe/united_kingdom.pyi', 'exceptions.pyi', 'oceania/__init__.pyi', 'oceania/australia.pyi', 'oceania/marshall_islands.pyi', 'oceania/new_zealand.pyi', 'precomputed_astronomy.pyi', 'registry.pyi', 'registry_tools.pyi', 'skyfield_astronomy.pyi', 'usa/__init__.pyi', 'usa/alabama.pyi', 'usa/alaska.pyi', 'usa/american_samoa.pyi', 'usa/arizona.pyi', 'usa/arkansas.pyi', 'usa/california.pyi', 'usa/colorado.pyi', 'usa/connecticut.pyi', 'usa/core.pyi', 'usa/delaware.pyi', 'usa/district_columbia.pyi', 'usa/florida.pyi', 'usa/georgia.pyi', 'usa/guam.pyi', 'usa/hawaii.pyi', 'usa/idaho.pyi', 'usa/illinois.pyi', 'usa/indiana.pyi', 'usa/iowa.pyi', 'usa/kansas.pyi', 'usa/kentucky.pyi', 'usa/louisiana.pyi', 'usa/maine.pyi', 'usa/maryland.pyi', 'usa/massachusetts.pyi', 'usa/michigan.pyi', 'usa/minnesota.pyi', 'usa/mississippi.pyi', 'usa/missouri.pyi', 'usa/montana.pyi', 'usa/nebraska.pyi', 'usa/nevada.pyi', 'usa/new_hampshire.pyi', 'usa/new_jersey.pyi', 'usa/new_mexico.pyi', 'usa/new_york.pyi', 'usa/north_carolina.pyi', 'usa/north_dakota.pyi', 'usa/ohio.pyi', 'usa/oklahoma.pyi', 'usa/oregon.pyi', 'usa/pennsylvania.pyi', 'usa/rhode_island.pyi', 'usa/south_carolina.pyi', 'usa/south_dakota.pyi', 'usa/tennessee.pyi', 'usa/texas.pyi', 'usa/utah.pyi', 'usa/vermont.pyi', 'usa/virginia.pyi', 'usa/washington.pyi', 'usa/west_virginia.pyi', 'usa/wisconsin.pyi', 'usa/wyoming.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
