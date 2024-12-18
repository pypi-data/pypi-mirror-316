# scm_config_clone/commands/objects/application.py

import logging
from typing import List, Optional, Any, Dict

import typer
from scm.client import Scm
from scm.config.objects import Application
from scm.exceptions import (
    AuthenticationError,
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
)
from scm.models.objects.application import (
    ApplicationCreateModel,
    ApplicationResponseModel,
)
from tabulate import tabulate

from scm_config_clone.utilities import load_settings, parse_csv_option


def build_create_params(
    src_obj: ApplicationResponseModel,
    folder: str,
) -> Dict[str, Any]:
    """
    Construct the dictionary of parameters required to create a new application object.

    Given an existing ApplicationResponseModel (source object) and a target folder,
    this function builds a dictionary with all necessary fields for creating
    a new application in the destination tenant. It uses `model_dump` on a Pydantic model
    to ensure only valid, explicitly set fields are included.

    Args:
        src_obj: The ApplicationResponseModel representing the source application object.
        folder: The folder in the destination tenant where the object should be created.

    Returns:
        A dictionary containing the fields required for `Application.create()`.
        This dictionary is validated and pruned by ApplicationCreateModel.
    """
    data = {
        "name": src_obj.name,
        "folder": folder,
        "category": src_obj.category,
        "subcategory": src_obj.subcategory,
        "technology": src_obj.technology,
        "risk": src_obj.risk,
        "description": src_obj.description if src_obj.description is not None else None,
        "ports": src_obj.ports if src_obj.ports else None,
        "evasive": src_obj.evasive,
        "pervasive": src_obj.pervasive,
        "excessive_bandwidth_use": src_obj.excessive_bandwidth_use,
        "used_by_malware": src_obj.used_by_malware,
        "transfers_files": src_obj.transfers_files,
        "has_known_vulnerabilities": src_obj.has_known_vulnerabilities,
        "tunnels_other_apps": src_obj.tunnels_other_apps,
        "prone_to_misuse": src_obj.prone_to_misuse,
        "no_certifications": src_obj.no_certifications,
    }

    create_model = ApplicationCreateModel(**data)
    return create_model.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )


def applications(
    folder: Optional[str] = typer.Option(
        None,
        "--folder",
        prompt="Please enter the folder name",
        help="The folder to focus on when retrieving and cloning applications.",
    ),
    exclude_folders: str = typer.Option(
        None,
        "--exclude-folders",
        help="Comma-separated list of folders to exclude from the retrieval.",
    ),
    exclude_snippets: str = typer.Option(
        None,
        "--exclude-snippets",
        help="Comma-separated list of snippets to exclude from the retrieval.",
    ),
    commit_and_push: bool = typer.Option(
        False,
        "--commit-and-push",
        help="If set, commit the changes on the destination tenant after object creation.",
        is_flag=True,
    ),
    auto_approve: bool = typer.Option(
        None,
        "--auto-approve",
        "-A",
        help="If set, skip the confirmation prompt and automatically proceed with creation.",
        is_flag=True,
    ),
    create_report: bool = typer.Option(
        None,
        "--create-report",
        "-R",
        help="If set, create or append to a 'result.csv' file with the task results.",
        is_flag=True,
    ),
    dry_run: bool = typer.Option(
        None,
        "--dry-run",
        "-D",
        help="If set, perform a dry run without applying any changes.",
        is_flag=True,
    ),
    quiet_mode: bool = typer.Option(
        None,
        "--quiet-mode",
        "-Q",
        help="If set, hide all console output (except log messages).",
        is_flag=True,
    ),
    logging_level: str = typer.Option(
        None,
        "--logging-level",
        "-L",
        help="Override the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    ),
    settings_file: str = typer.Option(
        "settings.yaml",
        "--settings-file",
        "-s",
        help="Path to the YAML settings file containing tenant credentials and configuration.",
    ),
):
    """
    Clone application objects from a source SCM tenant to a destination SCM tenant.

    This Typer CLI command automates the process of retrieving application objects
    from a specified folder in a source tenant, optionally filters them out based
    on user-defined exclusion criteria, and then creates them in a destination tenant.

    The workflow is:
    1. Load authentication and configuration settings (e.g., credentials, logging) from the YAML file.
    2. If any runtime flags are provided, they override the corresponding settings from the file.
    3. Authenticate to the source tenant and retrieve application objects from the given folder.
    4. Display the retrieved source objects. If not auto-approved, prompt the user before proceeding.
    5. Authenticate to the destination tenant and create the retrieved objects there.
    6. If `--commit-and-push` is provided and objects were created successfully, commit the changes.
    7. Display the results, including successfully created objects and any errors.

    Args:
        folder: The source folder from which to retrieve application objects.
        exclude_folders: Comma-separated folder names to exclude from source retrieval.
        exclude_snippets: Comma-separated snippet names to exclude from source retrieval.
        commit_and_push: If True, commit changes in the destination tenant after creation.
        auto_approve: If True or set in settings, skip the confirmation prompt before creating objects.
        create_report: If True or set in settings, create/append a CSV file with task results.
        dry_run: If True or set in settings, perform a dry run without applying changes (logic TBD).
        quiet_mode: If True or set in settings, hide console output except log messages (logic TBD).
        logging_level: If provided, override the logging level from settings.yaml.
        settings_file: Path to the YAML settings file for loading authentication and configuration.

    Raises:
        typer.Exit: Exits if authentication fails, retrieval fails, or if the user opts not to proceed.
    """
    typer.echo("🚀 Starting application objects cloning...")

    # Load settings from file
    settings = load_settings(settings_file)

    # Apply fallback logic: if a flag wasn't provided at runtime, use settings.yaml values
    auto_approve = settings["auto_approve"] if auto_approve is None else auto_approve
    create_report = (
        settings["create_report"] if create_report is None else create_report
    )
    dry_run = settings["dry_run"] if dry_run is None else dry_run
    quiet_mode = settings["quiet"] if quiet_mode is None else quiet_mode

    # Logging level fallback
    if logging_level is None:
        logging_level = settings["logging"]
    logging_level = logging_level.upper()

    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, logging_level, logging.INFO))

    # Parse CSV options
    exclude_folders_list = parse_csv_option(exclude_folders)
    exclude_snippets_list = parse_csv_option(exclude_snippets)

    # Authenticate and retrieve from source
    try:
        source_creds = settings["source_scm"]
        source_client = Scm(
            client_id=source_creds["client_id"],
            client_secret=source_creds["client_secret"],
            tsg_id=source_creds["tenant"],
            log_level=logging_level,
        )
        logger.info(f"Authenticated with source SCM tenant: {source_creds['tenant']}")
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with source tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with source authentication: {e}")
        raise typer.Exit(code=1)

    # Retrieve application objects from source
    try:
        source_applications = Application(source_client, max_limit=5000)
        application_objects = source_applications.list(
            folder=folder,
            exact_match=True,
            exclude_folders=exclude_folders_list,
            exclude_snippets=exclude_snippets_list,
        )
        logger.info(
            f"Retrieved {len(application_objects)} application objects from source tenant folder '{folder}'."
        )
    except Exception as e:
        logger.error(f"Error retrieving application objects from source: {e}")
        raise typer.Exit(code=1)

    # Display retrieved applications if not quiet_mode
    if application_objects and not quiet_mode:
        app_table = [
            [
                app.name,
                app.folder,
                app.category,
                app.subcategory,
                app.technology,
                app.risk,
                app.description or "",
                ", ".join(app.ports) if app.ports else "",
            ]
            for app in application_objects
        ]
        typer.echo(
            tabulate(
                app_table,
                headers=[
                    "Name",
                    "Folder",
                    "Category",
                    "Subcategory",
                    "Technology",
                    "Risk",
                    "Description",
                    "Ports",
                ],
                tablefmt="fancy_grid",
            )
        )
    elif not application_objects:
        typer.echo("No application objects found in the source folder.")

    # Prompt if not auto-approved and objects exist
    if application_objects and not auto_approve:
        proceed = typer.confirm(
            "Do you want to proceed with creating these objects in the destination tenant?"
        )
        if not proceed:
            typer.echo("Aborting cloning operation.")
            raise typer.Exit(code=0)

    # Authenticate with destination tenant
    try:
        dest_creds = settings["destination_scm"]
        destination_client = Scm(
            client_id=dest_creds["client_id"],
            client_secret=dest_creds["client_secret"],
            tsg_id=dest_creds["tenant"],
            log_level=logging_level,
        )
        logger.info(
            f"Authenticated with destination SCM tenant: {dest_creds['tenant']}"
        )
    except (AuthenticationError, KeyError) as e:
        logger.error(f"Error authenticating with destination tenant: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error with destination authentication: {e}")
        raise typer.Exit(code=1)

    # Create application objects in destination
    destination_applications = Application(destination_client, max_limit=5000)
    created_objs: List[ApplicationResponseModel] = []
    error_objects: List[List[str]] = []

    for src_obj in application_objects:
        try:
            create_params = build_create_params(src_obj, folder)
        except ValueError as ve:
            error_objects.append([src_obj.name, str(ve)])
            continue

        try:
            new_obj = destination_applications.create(create_params)
            created_objs.append(new_obj)
            logger.info(f"Created application object in destination: {new_obj.name}")
        except (
            InvalidObjectError,
            MissingQueryParameterError,
            NameNotUniqueError,
            ObjectNotPresentError,
        ) as e:
            error_objects.append([src_obj.name, str(e)])
            continue
        except Exception as e:
            error_objects.append([src_obj.name, str(e)])
            continue

    # Display results if not quiet_mode
    if created_objs and not quiet_mode:
        typer.echo("\nSuccessfully created the following application objects:")
        created_table = [
            [
                obj.name,
                obj.folder,
                obj.category,
                obj.subcategory,
                obj.technology,
                obj.risk,
                obj.description or "",
                ", ".join(obj.ports) if obj.ports else "",
            ]
            for obj in created_objs
        ]

        typer.echo(
            tabulate(
                created_table,
                headers=[
                    "Name",
                    "Folder",
                    "Category",
                    "Subcategory",
                    "Technology",
                    "Risk",
                    "Description",
                    "Ports",
                ],
                tablefmt="fancy_grid",
            )
        )

    if error_objects and not quiet_mode:
        typer.echo("\nSome application objects failed to be created:")
        typer.echo(
            tabulate(
                error_objects,
                headers=["Object Name", "Error"],
                tablefmt="fancy_grid",
            )
        )

    # Commit changes if requested and objects were created
    if commit_and_push and created_objs:
        try:
            commit_params = {
                "folders": [folder],
                "description": "Cloned application objects",
                "sync": True,
            }
            result = destination_applications.commit(**commit_params)
            job_status = destination_applications.get_job_status(result.job_id)
            logger.info(
                f"Commit job ID {result.job_id} status: {job_status.data[0].status_str}"
            )
        except Exception as e:
            logger.error(f"Error committing application objects in destination: {e}")
            raise typer.Exit(code=1)
    else:
        if created_objs and not commit_and_push:
            logger.info(
                "Objects created, but --commit-and-push not specified, skipping commit."
            )
        else:
            logger.info("No new application objects were created, skipping commit.")

    typer.echo("🎉 Application objects cloning completed successfully! 🎉")
