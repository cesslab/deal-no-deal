from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
       'name': 'dnd_with_probabilities',
       'display_name': "Deal or No Deal",
       'num_demo_participants': 1,
       'app_sequence': ['exp'],
       'probability_treatment': True,
       'prize': 100,
       'envelope_1': 90,
       'envelope_2': 10,
       'envelope_3': 80,
       'envelope_4': 20,
       'envelope_5': 60,
       'envelope_6': 100,
       'envelope_7': 30,
       'envelope_8': 70,
       'envelope_9': 50,
       'envelope_10': 40,
       'buyout_min': 0,
       'buyout_max': 100,
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'd_5^fsi(l&z6seqpx2kfxiy9-_zpqxeq^29xpeocj9t_p997px'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
