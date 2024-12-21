import json
import os
from json import JSONDecodeError
from pathlib import Path
from typing import List, Optional, Union

import click

from base.exceptions import ApiException
from dottxt.client import Dottxt


def _load_schema_from_json(schema_file: Path) -> str:
    """Load a schema source from JSON file."""
    try:
        with schema_file.open("r") as f:
            schema = json.load(f)
    except JSONDecodeError as e:
        click.echo(f"Error: Failed to decode JSON file '{schema_file}'. {e}", err=True)
        raise click.ClickException(f"Invalid JSON file: {schema_file}") from e
    return json.dumps(schema)


class DottxtCLI(click.Group):
    """
    Click group with custom invoke method to globally
    handle API exceptions and format JSON outputs.
    """

    def invoke(self, ctx):
        ctx.ensure_object(dict)

        try:
            response = super().invoke(ctx)

            # All subcommands return list of dicts or dicts
            click.echo(json.dumps(response, indent=4))
        except ApiException as error:
            # Handle API exceptions
            error_dict = {
                "error": error.__class__.__name__,
                "status": str(error.status),
                "reason": str(error.reason),
                "data": str(error.data),
            }
            click.echo(json.dumps(error_dict, indent=4), err=True)


@click.group(name="dottxt", cls=DottxtCLI)
@click.pass_context
@click.option(
    "--api-key",
    type=str,
    help=(
        "Dottxt API key. An `api_key` must be passed or set "
        "in the environment as `DOTTXT_API_KEY`."
    ),
    default=os.getenv("DOTTXT_API_KEY"),
)
@click.option(
    "--base-url",
    type=str,
    help=(
        "Dottxt API endpoint. If `base_url` is not passed or "
        "set in the environment as `DOTTXT_BASE_URL`, the client "
        "will use the default Dottxt API endpoint."
    ),
)
def dottxt_cli(ctx: click.Context, api_key: str | None, base_url: str | None) -> None:
    """CLI for the .txt API."""
    ctx.ensure_object(dict)
    ctx.obj["dottxt"] = Dottxt(api_key=api_key, base_url=base_url)


@dottxt_cli.command()
@click.pass_context
@click.option(
    "--schema-file",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="File containing JSON Schema",
)
@click.option("--name", type=str, help="JSON schema name")
@click.option("--wait", type=bool, default=True, help="Wait for the schema to compile")
def create_schema(
    ctx: click.Context, schema_file: Path, name: Optional[str] = None, wait: bool = True
) -> dict:
    """Create a JSON schema from a file."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    schema_str = _load_schema_from_json(schema_file)
    status = dottxt.create_schema(schema=schema_str, name=name, wait=wait)
    return status.model_dump()


@dottxt_cli.command()
@click.pass_context
@click.option("--name", type=str, help="JSON schema name")
@click.option("--js-id", type=str, help="JSON schema ID")
@click.option("--source", type=str, help="JSON schema source")
def get_schema_status(ctx: click.Context, name: str, js_id: str, source: str) -> dict:
    """Get schema status by name, js-id, or source."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    options = {"name": name, "js-id": js_id, "source": source}
    provided = [key for key, value in options.items() if value]

    if len(provided) != 1:
        raise click.UsageError(
            "Exactly one of --name, --js-id, or --source must be provided."
        )

    selected = provided[0]
    value = options[selected]
    if selected == "name":
        status = dottxt.get_schema_status_by_name(name=value)
    elif selected == "js-id":
        status = dottxt.get_schema_status(js_id=value)
    else:
        status = dottxt.get_schema_status_by_source(schema=value)

    if status:
        return status.model_dump()

    return {}


@dottxt_cli.command()
@click.pass_context
@click.option("--limit", type=int, help="Max number of JSON schemas to list")
def list_schemas(ctx: click.Context, limit: int) -> list:
    """List schemas."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    schema_list = []
    for i, schema in enumerate(dottxt.list_schemas()):
        if limit is not None and i >= limit:
            break
        schema_list.append(schema.model_dump())
    return schema_list


@dottxt_cli.command()
@click.pass_context
@click.argument("js_id", type=str, required=True)
def get_schema(ctx: click.Context, js_id: str) -> dict:
    """Get JSON schema source by JSON schema id."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    schema = dottxt.get_schema(js_id)
    return schema.model_dump()


@dottxt_cli.command()
@click.pass_context
@click.argument("js_id", type=str, required=True)
def delete_schema(ctx: click.Context, js_id: str) -> dict:
    """Delete a schema by JSON schema id."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    success = dottxt.delete_schema(js_id)
    return success.model_dump()


@dottxt_cli.command()
@click.pass_context
@click.option("--js-id", type=str, required=True, help="JSON schema ID")
@click.option(
    "--prompt", type=str, required=True, help="Prompt to use for structured generation"
)
@click.option("--max-tokens", type=int, help="Max tokens to generate")
@click.option(
    "--frequency-penalty", type=float, help="Frequency penalty sampling value"
)
@click.option("--presence-penalty", type=float, help="Presence penalty sampling value")
@click.option("--temperature", type=float, help="Value for sampling temperature")
@click.option("--seed", type=int, help="Seed for generation")
@click.option("--top_p", type=float, help="Value for top p sampling")
@click.option("--stop", type=str, multiple=True, help="List of stop strings")
def create_completion(
    ctx: click.Context,
    js_id: str,
    prompt: str,
    max_tokens: Optional[int] = None,
    frequency_penalty: Optional[float] = None,
    presence_penalty: Optional[float] = None,
    temperature: Optional[float] = None,
    seed: Optional[int] = None,
    top_p: Optional[float] = None,
    stop: Union[Optional[str], List[str]] = None,
) -> dict:
    """Generate structured JSON data using compiled schema."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    completion = dottxt.create_completion(
        prompt=prompt,
        js_id=js_id,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        temperature=temperature,
        seed=seed,
        top_p=top_p,
        stop=stop,
    )
    return completion.model_dump()


@dottxt_cli.command(name="json")
@click.pass_context
@click.option(
    "--schema-file",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="File containing JSON Schema",
)
@click.option(
    "--prompt", type=str, required=True, help="Prompt to use for structured generation"
)
@click.option("--max-tokens", type=int, help="Max tokens to generate")
@click.option(
    "--frequency-penalty", type=float, help="Frequency penalty sampling value"
)
@click.option("--presence-penalty", type=float, help="Presence penalty sampling value")
@click.option("--temperature", type=float, help="Value for sampling temperature")
@click.option("--seed", type=int, help="Seed for generation")
@click.option("--top_p", type=float, help="Value for top p sampling")
@click.option("--stop", type=str, multiple=True, help="List of stop strings")
def json_cli(
    ctx: click.Context,
    schema_file: Path,
    prompt: str,
    max_tokens: Optional[int] = None,
    frequency_penalty: Optional[float] = None,
    presence_penalty: Optional[float] = None,
    temperature: Optional[float] = None,
    seed: Optional[int] = None,
    top_p: Optional[float] = None,
    stop: Union[Optional[str], List[str]] = None,
) -> dict:
    """Generate structured JSON data using provided schema."""
    dottxt: Dottxt = ctx.obj["dottxt"]
    schema = _load_schema_from_json(schema_file)
    completion = dottxt.json(
        prompt=prompt,
        schema=schema,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        temperature=temperature,
        seed=seed,
        top_p=top_p,
        stop=stop,
    )
    return completion.model_dump()


if __name__ == "__main__":
    dottxt_cli()  # pragma: no cover
