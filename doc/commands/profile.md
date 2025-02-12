# Profile

Add, delete, update or list profiles.

A profile contains the following data:

* name: A unique name by which the profile can be referenced. The name is not stored in the data files, but identifies the folder. (required)
* type: The type of the profile. Allowed values are 'jira', 'polarion' and 'superset', currently. (required)
* server: The URL to the server. (required)
* token: An API token to allow for easier access. (optional)
* user/password: The credentials to authenticate with the server in case no token is given. (optional)
* certificate: A certificate for the specified server instance. (optional)

When adding a profile, the server URL and token (or user/password) are required.
The certificate is optional and can also be added later on with the --update option.

```cmd
pyProfileMgr profile [-h] {add,list,remove,update} ...
```

Output:

```cmd
usage: pyProfileMgr profile add [-h] -pt <profile type> -s <server URL> [-t <token>] [-u <user>] [-p <password>] [--cert <certificate path>] <profile name>

positional arguments:
  <profile name>        The name of the profile.

options:
  -h, --help            show this help message and exit
  -pt <profile type>, --profile_type <profile type>
                        The type of the profile ('jira', 'polarion' or 'superset').
  -s <server URL>, --server <server URL>
                        The server URL to connect to.
  -t <token>, --token <token>
                        The token to authenticate at the server.
  -u <user>, --user <user>
                        The user to authenticate at the server.
  -p <password>, --password <password>
                        The password to authenticate at the server.
  --cert <certificate path>
                        The server SSL certificate.
```

Example:

```cmd
pyProfileMgr profile add -pt jira -s https://jira-instance.com -t exampleToken --cert C:\\Path\\To\\Certificate.crt testProfileName
```

This will create a new Jira profile with the name "testProfileName".
