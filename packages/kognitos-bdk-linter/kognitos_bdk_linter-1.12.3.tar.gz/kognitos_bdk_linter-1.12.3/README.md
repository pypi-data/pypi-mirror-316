# Python Linter for Book Development Kit

This package provides an extension for Pylint that will test a book conformance to BCI 3.


## Usage

In order to configure the project as a dependency you must follow the following steps:

Add the repository to your project:

```shell
poetry source add --priority=supplemental bdk "https://kognitos-719468614044.d.codeartifact.us-west-2.amazonaws.com/pypi/bdk/simple/"
```

Authenticate the repository using your AWS credentials (notice the authentication will only last 12 hours):

```shell
poetry config http-basic.bdk aws $(aws codeartifact get-authorization-token --domain-owner 719468614044 --domain kognitos --query 'authorizationToken' --output text)
```

Add the dependency:

```shell
poetry add --source bdk kognitos-bdk-linter
```