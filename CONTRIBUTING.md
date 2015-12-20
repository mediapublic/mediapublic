# Contributing

Mediapublic is an Open Source project, and feedback, code, documentation, and
other contributions are all welcome. These are guidelines for new (and
existing) contributors who want to help.

## Contributing code

We work on the "develop" branch, and update master to the latest stable
version every so often. When you make changes and file pull requests, please
submit them against "develop."

1. You'll need to [fork this repository][fork] to your own GitHub account
1. Once you've forked the repo, clone it
   `git clone git@github.com:YOURNAME/mediapublic.git`
1. Make your change and commit it
1. File a [pull request][pull] and wait!

After filing a pull request, it may take some time for us to review it. If
there are problems, or something isn't clear we may ask some questions.

#### How to get a pull request accepted

In short:

1. Don't break existing tests or functionality
1. Write tests for the new code (see Testing)
1. Write a [good commit message][commit]
1. Tell us why you made this change

### Testing

We have automated tests that are run on every pull request, and as a rule we
don't merge code that breaks the tests. For the Python backend, we use
[tox][tox] which enforces code style, runs our API tests, and tests on multiple
Python versions.

You can run all the tests before you push code by typing `tox` in the `server`
directory and it will run all the tests.

We test the Python server using [gabbi][gabbi], which takes YAML definitions of
requests and runs them to confirm they succeed. For mediapublic, this is
important because the HTTP API is how the web application communicates with the
backend server, so it *has* to work all the time. Look [here][gabbitests] to
see examples of those tests.

## Development Schedule

The development team works in two-week sprints, and track what we're working on
with [GitHub milestones][milestones]. As issues come in, we tag them as "next
sprint" if we plan to do them soon (but not immediately). Each sprint has a due
date associated, and what doesn't get done will be moved to the following
sprint.

At the beginning of each sprint, we tag issues we plan to work on and
self-assign tasks. If you'd like to join us, let us know!

## Contributing Ideas

Do you have an idea for a feature, or a direction the project needs to go? We
want to hear from you! Write a spec and put it on the wiki. Here's an
[example](https://github.com/mediapublic/mediapublic/wiki/Example-Spec) that
you can copy over to a new page. When filling it out, make sure you include
enough information for developers and other users to understand what you want
and why it's important.

You don't need to write the whole spec at once, feel free to post a draft then
reach out to the team on [gitter.im](https://gitter.im) for feedback.

The mediapublic team is available on [gitter.im](https://gitter.im) if you have
any questions on how to write a spec. You can always post a draft to get
earlier feedback on your idea.

## Issue Tags

We have a few tags to help us navigate the issues page:

- "bug" - Bugs that need squashing because something isn't working right.
- "coding" - Tasks that involve programming, either frontend or backend.
- "design" - This means feedback is desired. When an issue has this tag, it's
    often about a future feature or a change to the project.
- "documentation" - All things documentation. Developer docs, user docs,
    installation docs, you name it.
- "duplicate" - Exactly what it says on the tin.
- "enhancement" - New features, or improvements to existing ones.
- "help wanted" - We need you! For whatever reason we can't do this ourselves,
    or it would be a good place for a new contributor to cut their teeth.
- "next sprint" - If an issue has this tag, we're hoping to get to it soon and
    will talk about it at the beginning of the next sprint.
- "nice to have" - Exactly what it says, it would be great but isn't a major
    priority right now.
- "question" - If you don't know how to do it, or something is unclear, ask a
    question.
- "wontfix" - An issue has been determined not to be a bug, or not to be
    fixable.

[fork]: https://help.github.com/articles/fork-a-repo/
[pull]: https://help.github.com/articles/using-pull-requests/
[commit]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
[tox]: https://tox.readthedocs.org/en/latest/
[gabbi]: https://gabbi.readthedocs.org/en/latest/
[gabbitests]: https://github.com/mediapublic/mediapublic/tree/develop/server/mediapublic/tests/gabbits
[milestones]: https://github.com/mediapublic/mediapublic/milestones
