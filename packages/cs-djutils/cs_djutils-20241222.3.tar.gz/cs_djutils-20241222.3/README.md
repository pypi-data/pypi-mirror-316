My collection of things for working with Django.

*Latest release 20241222.3*:
Autocall settings.configure() if required because Django's settings object is a royal PITA.

## <a name="BaseCommand"></a>Class `BaseCommand(cs.cmdutils.BaseCommand, django.core.management.base.BaseCommand)`

A drop in class for `django.core.management.base.BaseCommand`
which subclasses `cs.cmdutils.BaseCommand`.

This lets me write management commands more easily, particularly
if there are subcommands.

This is a drop in in the sense that you still make a management command
in nearly the same way:

    from cs.djutils import BaseCommand

    class Command(BaseCommand):

and `manage.py` will find it and run it as normal.
But from that point on the style is as for `cs.cmdutils.BaseCommand`:
- no `aegparse` setup
- direct support for subcommands as methods
- succinct option parsing, if you want command line options

A simple command looks like this:

    class Command(BaseCommand):

        def main(self, argv):
            ... do stuff based on the CLI args `argv` ...

A command with subcommands looks like this:

    class Command(BaseCommand):

        def cmd_this(self, argv):
            ... do the "this" subcommand ...

        def cmd_that(self, argv):
            ... do the "that" subcommand ...

If want some kind of app/client specific "overcommand" composed
from other management commands you can import them and make
them subcommands of the overcommand:

    from .other_command import Command as OtherCommand

    class Command(BaseCommand):

        # provide it as the "other" subcommand
        cmd_other = OtherCommand

Option parsing is inline in the command. `self` comes
presupplied with a `.options` attribute which is an instance
of `cs.cmdutils.BaseCommandOptions` (or some subclass).

Parsing options is simple:

    class Command(BaseCommand):

        def cmd_this(self, argv):
            options = self.options
            # parsing options:
            #
            # boolean -x option, makes options.x
            #
            # --thing-limit n option taking an int
            # makes options.thing_limit
            # help text is "Thing limit."
            #
            # a --mode foo option taking a string
            # makes options.mode
            # help text is "The run mode."
            options.popopts(
                argv,
                x=None,
                thing_limit_=int,
                mode_='The run mode.',
            )
            ... now consult options.x or whatever
            ... argv is now the remaining arguments after the options

Usage summary:

    Usage: base [common-options...] [options...]
      A drop in class for `django.core.management.base.BaseCommand`
      which subclasses `cs.cmdutils.BaseCommand`.
      Subcommands:
        help [common-options...] [-l] [-s] [subcommand-names...]
          Print help for subcommands.
          This outputs the full help for the named subcommands,
          or the short help for all subcommands if no names are specified.
          Options:
            -l  Long listing.
            -r  Recurse into subcommands.
            -s  Short listing.
        info [common-options...] [field-names...]
          Recite general information.
          Explicit field names may be provided to override the default listing.
        repl [common-options...]
          Run a REPL (Read Evaluate Print Loop), an interactive Python prompt.
          Options:
            --banner banner  Banner.
        shell [common-options...]
          Run a command prompt via cmd.Cmd using this command's subcommands.

*`BaseCommand.Options`*

*`BaseCommand.SubCommandClass`*

*`BaseCommand.add_arguments(self, parser)`*:
Add the `Options.COMMON_OPT_SPECS` to the `argparse` parser.
This is basicly to support the Django `call_command` function.

*`BaseCommand.handle(*, argv, **options)`*:
The Django `BaseComand.handle` method.
This creates another instance for `argv` and runs it.

*`BaseCommand.run_from_argv(argv)`*:
Intercept `django.core.management.base.BaseCommand.run_from_argv`.
Construct an instance of `cs.djutils.DjangoBaseCommand` and run it.

## <a name="DjangoSpecificSubCommand"></a>Class `DjangoSpecificSubCommand(cs.cmdutils.SubCommand)`

A subclass of `cs.cmdutils.SubCOmmand` with additional support
for Django's `BaseCommand`.

*`DjangoSpecificSubCommand.__call__(self, argv: List[str])`*:
Run this `SubCommand` with `argv`.
This calls Django's `BaseCommand.run_from_argv` for pure Django commands.

*`DjangoSpecificSubCommand.is_pure_django_command`*:
Whether this subcommand is a pure Django `BaseCommand`.

*`DjangoSpecificSubCommand.usage_text(self, *, cmd=None, **kw)`*:
Return the usage text for this subcommand.

# Release Log



*Release 20241222.3*:
Autocall settings.configure() if required because Django's settings object is a royal PITA.

*Release 20241222.2*:
BaseCommand.Options.settings: call settings.configure() on init if that has not already been done.

*Release 20241222.1*:
Placate the dataclass - upgrade BaseCommand.Options.settings to be a field() with a default_factory.

*Release 20241222*:
BaseCommand.Options: include .settings with the public django.conf.settings names, mostly for cmd_info and cmd_repl.

*Release 20241119*:
New DjangoSpecificSubCommand(CSBaseCommand.SubCommandClass) to include support for pure Django BaseCommands.

*Release 20241111*:
Rename DjangoBaseCommand to just BaseCommand so that we go `from cs.djutils import BaseCommand`. Less confusing.

*Release 20241110*:
Initial PyPI release with DjangoBaseCommand, cs.cmdutils.BaseCommand subclass suppplanting django.core.management.base.BaseCommand.
