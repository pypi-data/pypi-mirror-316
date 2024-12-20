# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textual_textarea']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.9.0,<2.0.0', 'textual[syntax]>=0.89.1,<2.0']

setup_kwargs = {
    'name': 'textual-textarea',
    'version': '0.15.0',
    'description': 'A text area (multi-line input) with syntax highlighting for Textual',
    'long_description': '# Textual Textarea\n![Textual Textarea Screenshot](textarea.svg)\n\n## Note: This is **NOT** the official TextArea widget!\n\nWith v0.38.0, Textual added a built-in TextArea widget. You probably want to use \nthat widget instead of this one. This project predated the official widget; versions < v0.8.0\nhad a completely separate implmentation.\n\nSince v0.8.0, this project uses the built-in TextArea widget, but adds the features outlined below.\n\n## Installation\n\n```\npip install textual-textarea\n```\n\n## Features\nFull-featured text editor experience with VS-Code-like bindings, in your Textual App:\n- Syntax highlighting and support for Pygments themes.\n- Move cursor and scroll with mouse or keys (including <kbd>ctrl+arrow</kbd>, <kbd>PgUp/Dn</kbd>,  <kbd>ctrl+Home/End</kbd>).\n- Open (<kbd>ctrl+o</kbd>) and save (<kbd>ctrl+s</kbd>) files.\n- Cut (<kbd>ctrl+x</kbd>), copy (<kbd>ctrl+c</kbd>), paste (<kbd>ctrl+u/v</kbd>), optionally using the system clipboard.\n- Comment selections with <kbd>ctrl+/</kbd>.\n- Indent and dedent (optionally for a multiline selection) to tab stops with <kbd>Tab</kbd> and <kbd>shift+Tab</kbd>.\n- Automatic completions of quotes and brackets.\n- Select text by double-, triple-, or quadruple-clicking.\n- Quit with <kbd>ctrl+q</kbd>.\n\n## Usage\n\n### Initializing the Widget\n\nThe TextArea is a Textual Widget. You can add it to a Textual\napp using `compose` or `mount`:\n\n```python\nfrom textual_textarea import TextEditor\nfrom textual.app import App, ComposeResult\n\nclass TextApp(App, inherit_bindings=False):\n    def compose(self) -> ComposeResult:\n        yield TextEditor(text="hi", language="python", theme="nord-darker", id="ta")\n\n    def on_mount(self) -> None:\n        editor = self.query_one("#id", expect_type=TextEditor)\n        editor.focus()\n\napp = TextApp()\napp.run()\n```\n\nIn addition to the standard Widget arguments, TextArea accepts three additional, optional arguments when initializing the widget:\n\n- language (str): Must be `None` or the short name of a [Pygments lexer](https://pygments.org/docs/lexers/), e.g., `python`, `sql`, `as3`. Defaults to `None`.\n- theme (str): Must be name of a [Pygments style](https://pygments.org/styles/), e.g., `bw`, `github-dark`, `solarized-light`. Defaults to `monokai`.\n- use_system_clipboard (bool): Set to `False` to make the TextArea\'s copy and paste operations ignore the system clipboard. Defaults to `True`. Some Linux users may need to apt-install `xclip` or `xsel` to enable the system clipboard features.\n\nThe TextArea supports many actions and key bindings. **For proper binding of `ctrl+c` to the COPY action,\nyou must initialize your App with `inherit_bindings=False`** (as shown above), so that `ctrl+c` does not quit the app. The TextArea implements `ctrl+q` as quit; you way wish to mimic that in your app so that other in-focus widgets use the same behavior.\n\n### Interacting with the Widget\n\n#### Getting and Setting Text\n\nThe TextArea exposes a `text` property that contains the full text contained in the widget. You can retrieve or set the text by interacting with this property:\n\n```python\neditor = self.query_one(TextEditor)\nold_text = editor.text\neditor.text = "New Text!\\n\\nMany Lines!"\n```\n\nSimilarly, the TextEditor exposes a `selected_text` property (read-only):\n```python\neditor = self.query_one(TextEditor)\nselection = editor.selected_text\n```\n\n#### Inserting Text\n\nYou can insert text at the current selection:\n```python\neditor = self.query_one(TextEditor)\neditor.text = "01234"\neditor.selection = Selection((0, 2), (0, 2))\neditor.insert_text_at_selection("\\nabc\\n")\nassert editor.text == "01\\nabc\\n234"\nassert editor.selection == Selection((2, 0), (2, 0))\n```\n\n#### Getting and Setting The Cursor Position\n\nThe TextEditor exposes a `selection` property that returns a textual.widgets.text_area.Selection:\n\n```python\neditor = self.query_one(TextEditor)\nold_selection = editor.selection\neditor.selection = Selection((999, 0),(999, 0))  # the cursor will move as close to line 999, pos 0 as possible\ncursor_line_number = editor.selection.end[0]\ncursor_x_position = editor.selection.end[1]\n```\n\n\n#### Getting and Setting The Language\n\nSyntax highlighting and comment insertion depends on the configured language for the TextEditor.\n\nThe TextArea exposes a `language` property that returns `None` or a string that is equal to the short name of an installed tree-sitter language:\n\n```python\neditor = self.query_one(TextEditor)\nold_language = editor.language\neditor.language = "python"\n```\n\n#### Getting Theme Colors\n\nIf you would like the rest of your app to match the colors from the TextArea\'s theme, they are exposed via the `theme_colors` property.\n\n```python\neditor = self.query_one(TextEditor)\ncolor = editor.theme_colors.contrast_text_color\nbgcolor = editor.theme_colors.bgcolor\nhighlight = editor.theme_colors.selection_bgcolor\n```\n\n\n#### Adding Bindings and other Behavior\n\nYou can subclass TextEditor to add your own behavior. This snippet adds an action that posts a Submitted message containing the text of the TextEditor when the user presses <kbd>ctrl+j</kbd>:\n\n```python\nfrom textual.message import Message\nfrom textual_textarea import TextEditor\n\n\nclass CodeEditor(TextEditor):\n    BINDINGS = [\n        ("ctrl+j", "submit", "Run Query"),\n    ]\n\n    class Submitted(Message, bubble=True):\n        def __init__(self, text: str) -> None:\n            super().__init__()\n            self.text = text\n\n    async def action_submit(self) -> None:\n        self.post_message(self.Submitted(self.text))\n```\n',
    'author': 'Ted Conbeer',
    'author_email': 'tconbeer@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tconbeer/textual-textarea',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.14',
}


setup(**setup_kwargs)
