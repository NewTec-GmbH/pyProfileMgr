# Profile <!-- omit in toc -->

- [Add](#add)
- [List](#list)
- [Remove](#remove)
- [Update](#update)
- [Show](#show)

Add, list, remove, update or show profiles.

A profile contains the following data:

- name: A unique name by which the profile can be referenced. The name is not stored in the data files, but identifies the folder. (required)
- type: The type of the profile. Allowed values are 'jira', 'polarion', 'superset', 'conaktiv' and 'stages', currently. (required)
- server: The URL to the server. (required)
- token: An API token to allow for easier access. (optional)
- user/password: The credentials to authenticate with the server in case no token is given. (optional)
- certificate: A certificate for the specified server instance. (optional)

When adding a profile, the server URL and token (or user/password) are required.
The certificate is optional and can also be added later on with the `update` subcommand.

```cmd
pyProfileMgr profile [-h] {add,list,remove,update,show} ...
```

## Add

Add a new profile to the profile store.

```cmd
pyProfileMgr profile add [-h] -pt <profile type> -s <server URL> [-t <token>] [-u <user>] [-p <password>] [--cert <certificate path>] <profile name>
```

Output:

```cmd
usage: pyProfileMgr profile add [-h] -pt <profile type> -s <server URL> [-t <token>] [-u <user>] [-p <password>] [--cert <certificate path>] <profile name>

positional arguments:
  <profile name>        The name of the profile.

options:
  -h, --help            show this help message and exit
  -pt <profile type>, --profile_type <profile type>
                        The type of the profile ('jira', 'polarion', 'superset', 'conaktiv' or 'stages').
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

This will create a new Jira profile with the name "testProfileName":

```cmd
Successfully created profile 'testProfileName'.
```

## List

List the names of all stored profiles.

```cmd
pyProfileMgr profile list [-h]
```

Output:

```cmd
usage: pyProfileMgr profile list [-h]

options:
  -h, --help  show this help message and exit
```

Example:

```cmd
pyProfileMgr profile list
```

This will print the names of all stored profiles:

```cmd
Profiles:
    testProfileName
```

## Remove

Remove an existing profile from the profile store.

```cmd
pyProfileMgr profile remove [-h] <profile name>
```

Output:

```cmd
usage: pyProfileMgr profile remove [-h] <profile name>

positional arguments:
  <profile name>  The name of the profile.

options:
  -h, --help      show this help message and exit
```

Example:

```cmd
pyProfileMgr profile remove testProfileName
```

This will remove the profile "testProfileName":

```cmd
Successfully removed profile 'testProfileName'.
```

## Update

Update the certificate of an existing profile.

```cmd
pyProfileMgr profile update [-h] [-c <certificate path>] <profile name>
```

Output:

```cmd
usage: pyProfileMgr profile update [-h] [-c <certificate path>] <profile name>

positional arguments:
  <profile name>        The name of the profile.

options:
  -h, --help            show this help message and exit
  -c <certificate path>, --cert <certificate path>
                        The server SSL certificate.
```

Example:

```cmd
pyProfileMgr profile update -c C:\\Path\\To\\Certificate.crt testProfileName
```

This will add or replace the certificate of the profile "testProfileName":

```cmd
Successfully added certificate to profile 'testProfileName'.
```

## Show

Print all stored data of an existing profile.

```cmd
pyProfileMgr profile show [-h] <profile name>
```

Output:

```cmd
usage: pyProfileMgr profile show [-h] <profile name>

positional arguments:
  <profile name>  The name of the profile.

options:
  -h, --help      show this help message and exit
```

Example:

```cmd
pyProfileMgr profile show testProfileName
```

This will print the details of the profile "testProfileName":

```cmd
Profile name: testProfileName
Profile type: jira
Server URL:   https://jira-instance.com
Token:        exampleToken
Certificate:  C:\Path\To\Certificate.crt
```
