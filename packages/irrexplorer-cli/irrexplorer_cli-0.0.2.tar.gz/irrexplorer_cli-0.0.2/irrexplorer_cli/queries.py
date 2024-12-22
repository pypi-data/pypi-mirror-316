"""Query functions for the CLI tool."""

import json
from typing import Optional

import httpx

from irrexplorer_cli.helpers import (
    find_least_specific_prefix,
    format_as_sets,
    format_direct_origins,
    format_overlapping_prefixes,
    format_prefix_result,
)
from irrexplorer_cli.irrexplorer import IrrDisplay, IrrExplorer


async def process_overlaps(explorer: IrrExplorer, least_specific: str) -> None:
    """Process and print overlapping prefixes."""
    try:
        all_overlaps = await explorer.fetch_prefix_info(least_specific)
        for result in all_overlaps:
            print(format_prefix_result(result, "OVERLAP"))
    except (httpx.HTTPError, ValueError, RuntimeError):
        pass


async def async_prefix_query(pfx: str, output_format: Optional[str] = None) -> None:
    """Execute asynchronous prefix query and display results."""
    explorer = IrrExplorer()
    display = IrrDisplay()
    try:
        direct_overlaps = await explorer.fetch_prefix_info(pfx)

        if output_format == "json":
            json_data = [result.model_dump() for result in direct_overlaps]
            print(json.dumps(json_data, indent=2))
        elif output_format == "csv":
            print("Type,Prefix,Category,RIR,RPKI_Status,BGP_Origins,IRR_Routes,Messages")

            for result in direct_overlaps:
                print(format_prefix_result(result, "DIRECT"))

            least_specific = await find_least_specific_prefix(direct_overlaps)
            if least_specific:
                await process_overlaps(explorer, least_specific)
        else:
            await display.display_prefix_info(direct_overlaps)
    finally:
        await explorer.close()


async def async_asn_query(as_number: str, output_format: Optional[str] = None) -> None:
    """Execute asynchronous ASN query and display results."""
    explorer = IrrExplorer()
    display = IrrDisplay()
    try:
        results = await explorer.fetch_asn_info(as_number)
        sets_data = await explorer.fetch_asn_sets(as_number)

        if output_format == "json":
            combined_data = {"asn_info": results, "as_sets": sets_data}
            print(json.dumps(combined_data, indent=2), end="\n")
        elif output_format == "csv":
            print("Type,ASN,Prefix,Category,RIR,RPKI_Status,BGP_Origins,IRR_Routes,Messages", end="")
            format_direct_origins(as_number, results)
            format_overlapping_prefixes(as_number, results)
            format_as_sets(as_number, sets_data)
            print()
        else:
            await display.display_asn_info(results, as_number, sets_data)
    finally:
        await explorer.close()
