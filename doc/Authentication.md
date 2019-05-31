# Authentication

To validate a request, we have a decorator named `validate` in Services.Authentication.decorators

**Usage:**
```python
from Services.Authentication.decorators import validate

@validate
def foo(request, other_args):
    return HttpResponse("OK")

```

Every function **MUST** put `request` as their **first** argument.

Every request **MUST** have 3 GET parameters:
* token
* time
* sign

So the decorator can apply the algorithm by `arg[0].GET.get('token')` , etc.

Tips: You can refer to the `Services/Authentication/decorators.py` to understand the implementation.



**Algorithm:**

```python
param_list = sorted(get_param_list) + sorted(post_param_list)
sign = md5(param_list+secret_key)
```

(note: get_param_list does not contain parameter `sign` but `token` and `time`)

(`secret_key` is a key that hard-coded into the app and nobody else know that.)

(We just append `secret_key` to `param_list` and no need to consider whether it conforms to HTTP protocol)


