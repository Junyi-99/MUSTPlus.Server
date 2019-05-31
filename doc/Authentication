# Authentication

Every request **MUST** have 3 GET parameters:
* token
* time
* sign

Algorithm:

```Python
param_list = sorted(get_param_list) + sorted(post_param_list)
sign = md5(param_list+secret_key)
```

(note: get_param_list does not contain parameter `sign` but `token` and `time`)

(`secret_key` is a key that hard-coded into the app and nobody else know that.)

(We just append `secret_key` to `param_list` and no need to consider whether it conforms to HTTP protocol)


