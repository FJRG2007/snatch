# Command: settings

**Description**: Manage and configure settings.

**Arguments**:
* `option` (required): The specific setting to modify.
* `suboption` (optional): Additional parameters for certain settings.

Here you can see the sub-options available for each option.

| Options | Suboptions                   |
|---------|------------------------------|
| help    |                              |
| model   | models (default), advanced   |
| verify  |                              |

**Options**:
* `--help` (optional): Display help information for the command.

## Examples

In this case, the default sub-option is bypassed, so it is "models", and this command shows you the suppliers and models available in Snatch.
```bash
# Setting up an AI model.
$ snatch settings model
# Or (are equal, due to their default value).
$ snatch settings model models
```