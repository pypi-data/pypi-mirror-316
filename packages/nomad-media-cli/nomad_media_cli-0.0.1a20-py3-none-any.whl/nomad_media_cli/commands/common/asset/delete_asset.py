import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The ID of the asset to be deleted.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to delete the asset for (bucket::object-key).")
@click.option("--object-key", help="Object-key of the Asset (file or folder) to delete the asset for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.pass_context
def delete_asset(ctx, id, url, object_key):
    """Delete asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if not id and not url and not object_key:
        click.echo(json.dumps({ "error": "Please provide an id, url or object-key" }))
        sys.exit(1)

    if url or object_key:
        if url and "::" not in url:
            click.echo(json.dumps({ "error": "Please provide a valid path or set the default bucket." }))               
            sys.exit(1)
        if object_key:
            if "bucket" in ctx.obj:
                url = f"{ctx.obj['bucket']}::{object_key}"
            else:
                click.echo(json.dumps({ "error": "Please set bucket using `set-bucket` or use url." }))
                sys.exit(1)
                
        url_search_results = nomad_sdk.search(None, None, None, [{
            "fieldName": "url",
            "operator": "equals",
            "values": url
        }], None, None, None, None, None, None, None, None, None)
        
        if not url_search_results or len(url_search_results["items"] == 0):
            click.echo(json.dumps({ "error": f"URL {url} not found." }))
            sys.exit(1)
            
        id = url_search_results["items"][0]["id"]
    try:
        result = nomad_sdk.delete_asset(id)
        click.echo("Asset deleted successfully.")
        click.echo(result)

    except Exception as e:
        click.echo(json.dumps({"error": f"Error deleting asset: {e}"}))
        sys.exit(1)