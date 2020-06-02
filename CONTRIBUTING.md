# Contributing

Thank you for contributing to PyPWA! With the help of people like you,
we can make PyPWA a great Python based Partial Wave Analysis and High
Energy Physics toolkit.

## Where to start?

You don't need to have any physics or programming experience to start
contributing to PyPWA. If you are a physists who has never written code,
a software developer with little physics background, or even a new
student with little experience in either, we have projects that you can
help us with.

If you want to help, or get help, lets us know in the Issues section!

## Filing issues, Feature Requests, or requesting help

If you have a feature request, discovered a bug, a flaw in the
documentation, or a use-case where the toolkit runs slowly, please let
us know in the Issue tracker on Github.

When you are making a new issue on Github, you'll have a choice between
filing a bug report, feature request, or help request. Select which one
you want, and we will get reply as quickly as we can.

## Developing for PyPWA

PyPWA follows the PEP standard, which if you're using PyCharm the IDE
should help you conform to the format if you're new to it. We also
write all our documenation in numpydoc. 

Any functions or objects that are meant to be used by the users should
be imported directly into PyPWA/__init__.py and should be thoroughly
documented including examples. If it's an internal function however, it
should be moreso documentated in the code itself.

### Forking and branching

If you are working directly with us, and have access to the repository,
you will be forking all your branches off of the `development` branch.
All your additions will happen on that branch, and after your branch
passes reviews, you're branch will be merged into the `development`
branch to be included in the next release.

If you are a contributor from outside Jefferson Lab, please fork PyPWA,
make your changes to the `development` branch, and then submit a pull
request. We'll review your pull request, suggest changes, and then
accept your pull request.

### Running the test suite

We use PyTest for our testing. All code contributed to PyPWA should have
tests included in the fork or branch before it's merged into
`development`. This is so that we can continue to deliver as stable of
an experience as possible. We have no strict rules on the tests, but
please do your best to keep them short and concise.

### Merging or combining branches (Core Devs Only)

When you are combining a feature, fix, or documentation branch into
PyPWA, you squash all commits into a single commit, and then merge into
`development` with complete patch notes. The command to do this from a
standard machine is `git merge --squash`. This is to prevent the git
log from being polluted with small uninformative commits, and to keep
tracking changes concise.

### Creating a release (Core Devs Only)

When preparing for a release, a release branch for the new release
should be forked off of master, and all it's documentation should be
updated for the new release version. This should also be used as a final
attempt to catch any bugs that may have yet to been patched. Once all
bugs are patched, documentation is updated, tests passing, that is when
you would merge the branch into both master and development without
squash. It is desirable to maintain the full git log from development
when merging into master.
