# __eboo with plugin support__


A Flask Restful API that scrapes data from multiple websites in the form of plugins. 

## Project Tree
```bash
noveapi/
├── app.py
├── core/
│   ├── __init__.py
│   ├── assets/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── plug_base_class.py
│   │   └── scraper_obj.py
│   └── utils/
│       ├── __init__.py
│       ├── bookbinder.py
│       ├── handlers.py
│       └── load_plugins.py
├── dev/
│   └── dirtree.py
├── LICENSE
├── plugins/
│   └── default.scraper.py
├── plugins.db.json
├── README.md
├── requirements.txt
├── results/
├── settings.json
└── tests/
```

## __Usage__
Run Flask App and type ```localhost:81``` in your browser. Input novel title and email. 

## __TODO__
- **Features**
  - [x] exception handling
  - [x] clean and consistent format
  - [ ] threading
  - [ ] downloads handler
  - [ ] use models for post requests
  - [ ] more plugins
    - [ ] add threading

- **Testing**
  - [ ] app.exe file paths

- **Misc**
  - [ ] Add docstrings
  - [ ] readme documentation
  - [ ] automatic documentation using sphyinx

- **Ideas**
  - [ ] create fastapi email service hosted on heroku