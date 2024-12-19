
This is for arranging multiple config files.



## config nest manifest

This is a file under the config nest subfolder, it has 3 fields: 

```
selection_mode: [one, all] # To include all names or select one of them
if_no_selection: [skip, deafult, error] #  if selection_mode is `one`, and not specified which to select in view file, skip this name, use the default name (next field value), or raise error when parsing
deafult_selection: [...] # if if_no_selection is `default`, this name will return
```

- The default selection_mode=all, which means, if no manifest file (should be named CONFIGNEST_MANIFEST) all names are included.
- The default if_no_selection=error, which means, if you do not select any of them in view file, this will raise error.

## demo
For a demo, see the repo: 0-1CxH/megatron-wrap