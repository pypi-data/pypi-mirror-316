import rich
import rich_click as click
from rich import box
from rich.panel import Panel
from rich.status import Status

from codegen.analytics.decorators import track_command
from codegen.api.client import RestAPI
from codegen.auth.decorators import requires_auth
from codegen.auth.session import CodegenSession
from codegen.errors import ServerError
from codegen.utils.codemod_manager import CodemodManager
from codegen.utils.schema import CODEMOD_CONFIG_PATH
from codegen.workspace.decorators import requires_init


@click.command(name="create")
@track_command()
@requires_auth
@requires_init
@click.argument("name", type=str)
@click.option("--description", "-d", default=None, help="Description of what this codemod does")
def create_command(session: CodegenSession, name: str, description: str | None):
    """Create a new codemod in the codegen-sh/codemods directory."""
    with Status("[bold]Generating codemod...", spinner="dots", spinner_style="purple") as status:
        try:
            # Get code from API
            response = RestAPI(session.token).create(description if description else None)
            # Show the AI's explanation
            rich.print("\n[bold]🤖 AI Assistant:[/bold]")
            rich.print(
                Panel(
                    response.response,
                    title="[bold blue]Generated Codemod Explanation",
                    border_style="blue",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )

            # Create the codemod
            codemod = CodemodManager.create(
                session=session,
                name=name,
                code=response.code,
                codemod_id=response.codemod_id,
                description=description or f"AI-generated codemod for: {name}",
                author=session.profile.name,
            )

        except ServerError as e:
            status.stop()
            raise click.ClickException(str(e))
        except ValueError as e:
            status.stop()
            raise click.ClickException(str(e))

    # Success message
    rich.print("\n[bold green]✨ Created new codemod:[/bold green]")
    rich.print("─" * 40)
    rich.print(f"[cyan]Location:[/cyan] {codemod.path.parent}")
    rich.print(f"[cyan]Main file:[/cyan] {codemod.path}")
    if codemod.config:
        rich.print(f"[cyan]Config:[/cyan] {codemod.path.parent / CODEMOD_CONFIG_PATH}")
    rich.print("\n[bold yellow]💡 Next steps:[/bold yellow]")
    rich.print("1. Review and edit [cyan]run.py[/cyan] to customize the codemod")
    rich.print("2. Run it with: [green]codegen run[/green]")
    rich.print("─" * 40 + "\n")
