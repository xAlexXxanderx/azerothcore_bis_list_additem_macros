# azerothcore_bis_list_additem_macros

Creating .additem macros from [BIS list](https://gist.github.com/xAlexXxanderx/321bb4d379e24e83202b213ef2228b7e) for [AzerothCore](https://github.com/azerothcore/azerothcore-wotlk) (via [Super Duper Macro 1.8.3](https://github.com/hypehuman/super-duper-macro/tree/d25b5fe50add9f03185bc09327144d450ffc85e4))

## Quick Start

1. Clone repo and go to folder with script:

```git clone git@github.com:xAlexXxanderx/azerothcore_bis_list_additem_macros.git```

```cd azerothcore_bis_list_additem_macros```

2. Copy ``.env.dist`` as ``.env`` and fill it with your credentials for access to AzerothCore DB:

```cp .env.dist .env```

```editor .env```

3. Install requirements:

```pip install -r requirements.txt```

4. Start script:

```python3 main.py -f /path/to/bis.md```

without `-f` key, script use `bis.md` in script folder

5. Place `SuperDuperMacro.lua` in `<WoW Dir>/WTF/Account/<AccountName>/SavedVariables`
