# app_elements

Reusable desktop UI composition for applications built with app_framework,
gui_builder and wx_utils. app_framework owns application services; app_elements
exposes their common menus, actions and settings panels. Product-specific
document, feed, podcast and account settings remain in the consuming application.

## Application contract

The application must be importable as `application`. Bootstrap it with
`app_framework.bootstrap_application(application)` before showing these controls.
The framework initializes configuration and translations before importing the
main window; it initializes optional services before returning to the event loop.
Importing controls earlier can capture untranslated labels or incomplete feature
flags. Set manifest capabilities before importing menus or panels: their class
declarations select optional controls at import time.

`HelpMenu` from `app_elements.menu` supplies documentation (F1), About, and optional
website, issue reporting, activation and frozen-application update actions. It
uses the framework's manifest capability checks. The application supplies `name`,
`version`, `author`, `locale`, and any enabled services' required attributes.
About also uses `website`. Actions use the same application module as bootstrap.

## Settings panels

Embed panels in gui_builder/wx_utils forms as normal declarative children:

```python
from app_elements.i18n import LanguageSelectionPanel
from wx_utils.forms import AutoSizedDialog

class OptionsDialog(AutoSizedDialog):
    language = LanguageSelectionPanel(sizer_type="horizontal")

    def set_config_values(self):
        self.language.set_config_values()
```

The caller owns OK/Cancel: call `set_config_values()` only after OK, then save
the application's configuration using its normal persistence mechanism. Rendering
a panel must not save settings. These methods update configuration; they do not
apply audio changes or switch the running application's language.

| Panel | Application requirements | Saved setting |
| --- | --- | --- |
| `i18n.LanguageSelectionPanel` | `name`, resolved `locale`, `config`, registered application translations | `UI.language`; restart required |
| `audio.DeviceSelectionPanel` | initialized sound output, `config`; `record_sound` enables input selection | `audio.device`, `audio.input_device` |
| `startup.RunAtStartupPanel` | Windows, `name`, stable executable/script location | Current user's Windows Run registry value |

Startup registration changes the registry immediately when its save method runs;
it is not part of configuration-file persistence. Do not import `startup` on
other platforms. Keep portable applications in a stable location if enabling it.

## Documentation files

`interface.view_documentation()` expects `readme.html` under the embedded-data
directory in frozen applications, or under `../documentation` relative to the
application path in source runs. Locale subdirectories use identifiers such as
`fr_CA` or `fr`. Products own building and packaging those HTML files.

## Development and CI

Controlled composition tests use Python's standard-library unittest and Babel
2.17.0. They import the production modules and replace desktop-service boundaries
with doubles; they do not require wxPython, private repositories or credentials.
Run from the repository root:

```text
uv run --no-project --python 3.13 --with babel==2.17.0 python -m unittest discover -s tests -v
uv build
```

The test command deliberately uses `--no-project`: it does not resolve or change
the desktop application's dependency environment. `uv build` invokes the
existing Hatchling backend to produce source and wheel distributions without
installing runtime dependencies. There is no tracked project lock or type-check
authority here. CI runs these two commands on one Linux/Python 3.13 runner for
pull requests (including forks) and pushes to master. It needs no private token.

These checks establish controlled composition and package-build results. They
do not establish native wx behavior, Windows startup execution, frozen-product
integration, or live screen-reader output; those require consumer verification.
