import rich_click as click
from rich.traceback import install

from codegen.commands.create import create_command
from codegen.commands.docs_search import docs_search_command
from codegen.commands.expert import expert_command
from codegen.commands.init import init_command
from codegen.commands.login import login_command
from codegen.commands.logout import logout_command
from codegen.commands.profile import profile_command
from codegen.commands.run import run_command
from codegen.commands.set_active import set_active_command

click.rich_click.USE_RICH_MARKUP = True
install(show_locals=True)


@click.group()
def main():
    """Codegen CLI - Transform your code with AI."""


# Wrap commands with error handler
main.add_command(init_command)
main.add_command(logout_command)
main.add_command(login_command)
main.add_command(run_command)
main.add_command(docs_search_command)
main.add_command(profile_command)
main.add_command(create_command)
main.add_command(expert_command)
main.add_command(set_active_command)

if __name__ == "__main__":
    main()
