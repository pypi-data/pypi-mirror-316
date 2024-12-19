import base64
import os
import csv
from pathlib import Path
import click
import yaml
import tableauserverclient as TSC
import psycopg
from psycopg import sql

CONFIG_FILE = str(Path.home().joinpath(".tableau_toolkit", "tableau.yaml"))


def get_default_config_path():
    return str(Path.home() / CONFIG_FILE)


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def decode_secret(encoded_secret):
    decoded_bytes = base64.b64decode(encoded_secret.split(":")[0])
    return decoded_bytes.decode("utf-8")


def authenticate(config):
    server_url = config["tableau_server"]["url"]
    site_content_url = config["site"]["content_url"]
    api_version = config["api"]["version"]

    if config["authentication"]["type"] == "personal_access_token":
        token_name = config["personal_access_token"]["name"]
        token_secret = decode_secret(config["personal_access_token"]["secret"])
        tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name, token_secret, site_id=site_content_url
        )
    else:
        username = config["tableau_auth"]["username"]
        password = decode_secret(config["tableau_auth"]["password"])
        tableau_auth = TSC.TableauAuth(username, password, site_id=site_content_url)

    server = TSC.Server(server_url, use_server_version=False)
    server.add_http_options({"verify": False})
    server.version = api_version
    server.auth.sign_in(tableau_auth)
    return server


@click.group()
@click.option(
    "--config", default=get_default_config_path(), help="Path to the configuration file"
)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["config"] = config


@cli.command()
def init():
    """Initialize the tableau_toolkit configuration."""
    home_dir = Path.home()
    config_dir = home_dir / ".tableau_toolkit"
    config_file = config_dir / "tableau.yaml"

    if config_file.exists():
        click.echo("Configuration file already exists. Do you want to overwrite it?")
        if not click.confirm("Overwrite?"):
            click.echo("Initialization cancelled.")
            return

    config_dir.mkdir(exist_ok=True)

    default_config = {
        "tableau_server": {"url": "https://hostname"},
        "authentication": {"type": "tableau_auth"},
        "personal_access_token": {"name": "name", "secret": "secret"},
        "tableau_auth": {"username": "username", "password": "password"},
        "site": {"content_url": ""},
        "api": {"version": "3.24"},
        "postgres": {
            "host": "host",
            "port": 8060,
            "database": "workgroup",
            "user": "readonly",
            "password": "password",
        },
    }

    with config_file.open("w") as f:
        yaml.dump(default_config, f, default_flow_style=False)

    click.echo(f"Configuration file created at {config_file}")


@cli.command()
@click.argument("string")
def encode(string):
    """Encode a string using Base64 encoding."""
    encoded_bytes = base64.b64encode(string.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    click.echo(encoded_str)


@cli.command()
@click.argument("encoded_string")
def decode(encoded_string):
    """Decode a Base64 encoded string."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_str = decoded_bytes.decode("utf-8")
        click.echo(decoded_str)
    except UnicodeDecodeError as e:
        click.echo(f"Error decoding string: {e}")


def execute_query(config, query, params=None):
    # pylint: disable=not-context-manager
    with psycopg.connect(
        host=config["postgres"]["host"],
        port=config["postgres"]["port"],
        dbname=config["postgres"]["database"],
        user=config["postgres"]["user"],
        password=decode_secret(config["postgres"]["password"]),
    ) as conn:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            results = cur.fetchall()
    return results


@cli.group()
def find():
    """Find various Tableau resources"""

@find.command()
@click.option("--limit", default=10, help="Number of results to return")
@click.option("--min_date", default=None, help="Minimum date in yyyy-mm-dd format")
@click.option("--max_date", default=None, help="Maximum date in yyyy-mm-dd format")
@click.option("--headers/--no-headers", default=True, help="Display headers (default: on)")
@click.option("--sort_by", default="view_name", help="Column to sort by")
@click.option("--sort_order", default="asc", type=click.Choice(['asc', 'desc']), help="Sort order")
@click.option("--owner_id", default=None, help="Filter by owner ID")
@click.option("--site_name", default=None, help="Filter by site name")
@click.pass_context
def views(ctx, limit, min_date, max_date, headers, sort_by, sort_order, owner_id, site_name):
    """Find views with performance data"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        with
        perf as (
with perf as (
SELECT
    h.site_id,
    -- The point of this nasty CASE statement is to try and extract a valid repository URL for views, workbooks, or data sources that requests are executed against.
    CASE
        WHEN COALESCE(h.currentsheet, '') = '' OR h.currentsheet LIKE '%% %%' OR currentsheet LIKE '%%/null'
          THEN
            -- wrap all this to remove periods in URLs, e.g. "SDOR/TFSDefectsSinceRelease.pdf"
            SPLIT_PART (
                CASE SPLIT_PART(http_request_uri, '/', 2)
                    WHEN 'views'
                        THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                    WHEN 't'  -- string is heading with the site id
                        THEN SPLIT_PART(http_request_uri, '/', 5) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 6), '?', 1)
                    WHEN 'trusted'
                        THEN SPLIT_PART(http_request_uri, '/', 5) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 6), '?', 1)
                    WHEN 'vizql'
                        THEN
                            CASE SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 3)  -- trim off any site names for consistency
                                WHEN 'w'
                                    THEN
                                        CASE
                                            LEFT(
                                                REPLACE(
                                                    http_request_uri,
                                                    ('/vizql/t/' || COALESCE(s.url_namespace, '')),
                                                    '/vizql'
                                                ),
                                                12
                                            )
                                            WHEN '/vizql/w/ds:'
                                                THEN 
                                                    REPLACE(
                                                        SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 4),
                                                        'ds:',
                                                        ''
                                                    ) 
                                            ELSE
                                                -- strip data source indicator off the front of the string
                                                SPLIT_PART(
                                                    REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'),
                                                    '/',
                                                    4
                                                )                                                                                               -- workbook name
                                                || 
                                                CASE
                                                  SPLIT_PART(
                                                      REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'),
                                                      '/',
                                                      6
                                                  )
                                                  WHEN 'null'       -- sometimes in ostensiby web-edit scenarios, the sheet name is "null", so strip it out
                                                    THEN ''
                                                  ELSE '/' ||
                                                    SPLIT_PART(
                                                        REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'),
                                                        '/',
                                                        6
                                                    )
                                                END                                                                                             -- sheet name
                                        END
                                WHEN 'authoring'
                                    THEN ''
                                ELSE ''
                            END
                    WHEN 'askData'
                        THEN SPLIT_PART(http_request_uri, '/', 3)
                    WHEN 'authoringNewWorkbook'
                        THEN SPLIT_PART(http_request_uri, '/', 4)
                    WHEN 'authoring'
                        THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                    WHEN 'startAskData'
                        THEN SPLIT_PART(SPLIT_PART(http_request_uri, '/', 3), '?', 1)
                    WHEN 'offline_views'
                        THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)

                    --  these are useless at present
                    --WHEN 'newWorkbook'
                    --    THEN ''

                    --WHEN 'admin'
                    --    THEN ''

                    ELSE NULL
                END,
                '.',
                1
            )
          ELSE
        -- we can use the currentsheet field
        CASE WHEN ( LEFT(currentsheet, 3) = 'ds:' OR LEFT(http_request_uri, 22) = '/authoringNewWorkbook/' OR LEFT(http_request_uri, 12) = '/vizql/w/ds:')
            THEN
                -- this is a web edit on a data source or workbook, so strip out the "ds" for data sources and build the repository url
                SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 1)
            ELSE
                SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 1)
                || '/' ||
                SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 2)
        END
    END                 AS item_repository_url ,

    CASE
        WHEN currentsheet LIKE 'ds:%%' OR LEFT(http_request_uri, 12) = '/vizql/w/ds:' OR LEFT(http_request_uri, 9) = '/askData/'
            THEN 'Data Source'
        WHEN http_request_uri LIKE '/authoringNewWorkbook/%%'
            OR
                (
                -- this logic is to trap the right type of item for certain web-edit scenarios that seem to come up
                SPLIT_PART(
                    REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'),
                    '/',
                    6
                    ) = 'null'
                AND
                currentsheet NOT LIKE '%%/%%'
                )
            THEN 'Workbook'
        ELSE 'View'   -- this, like cake, is a lie. many of these records may not really be referring to a view. but for our LEFT join, it will make sense and be less complicated.
    END                 AS item_type ,
    AVG(EXTRACT(EPOCH FROM (h.completed_at - h.created_at))) AS avg_duration

FROM http_requests AS h
    LEFT JOIN sites AS s
        ON h.site_id = s.id
where action = 'bootstrapSession'
  and LEFT(CAST(h.status AS TEXT), 1) = '2' -- Success
    and (%s::date IS NULL OR h.created_at::date >= %s::date)
    and (%s::date IS NULL OR h.created_at::date <= %s::date)
    AND (%s::text IS NULL OR s.name = %s::text)
group by 1,2,3
)
select 
site_id,
replace(item_repository_url, '/', '/sheets/') repository_url,
avg_duration
from perf
where item_type = 'View'
        ),
        project_path AS (
            WITH RECURSIVE project_hierarchy AS (
                SELECT
                    pc.site_id,
                    pc.content_id,
                    p.id AS project_id,
                    p.name AS project_name,
                    p.parent_project_id,
                    1 AS level,
                    p.name::character varying AS path
                FROM projects_contents pc
                JOIN projects p ON pc.project_id = p.id
                WHERE pc.content_type = 'workbook'
                UNION ALL
                SELECT
                    ph.site_id,
                    ph.content_id,
                    p.id,
                    p.name,
                    p.parent_project_id,
                    ph.level + 1,
                    (p.name || ' >> ' || ph.path)::character varying
                FROM project_hierarchy ph
                JOIN projects p ON ph.parent_project_id = p.id
                    AND ph.site_id = p.site_id
            )
            SELECT
                site_id,
                content_id,
                path AS full_project_path
            FROM project_hierarchy
            WHERE parent_project_id IS NULL
        ),
        view_usage as (
            select
                view_id,
                site_id,
                sum(nviews) total_views,
                count(distinct user_id) unique_users
            from views_stats
            where (%s::date IS NULL OR time::date >= %s::date)
              AND (%s::date IS NULL OR time::date <= %s::date)
            group by 1,2
        )
        select
            s.name as site_name,
            s.luid as site_luid,
            v.luid view_luid,
            v.name view_name,
            w.name as workbook_name,
            pp.full_project_path,
            p.avg_duration,
            vu.total_views,
            vu.unique_users,
            su.name owner_id,
            su.email owner_email,
            su.friendly_name owner_name
        from views v
        join sites s on v.site_id = s.id
        join workbooks w
            on w.id = v.workbook_id
            and w.site_id = v.site_id
        join users u
            on u.id = w.owner_id
            and u.site_id = w.site_id
        join system_users su
            on su.id = u.system_user_id
        left outer join perf p
            on p.site_id = v.site_id
            and p.repository_url = v.repository_url
        left outer join project_path pp
            on pp.site_id = v.site_id
            and pp.content_id = v.workbook_id
        left outer join view_usage vu
            on vu.view_id = v.id
            and vu.site_id = v.site_id
        WHERE 
            (%s::text IS NULL OR su.name = %s::text)
            AND (%s::text IS NULL OR s.name = %s::text)
        ORDER BY 
            CASE 
                WHEN {sort_column} IS NULL THEN 1 
                ELSE 0 
            END,
            {sort_column} {sort_direction}
        LIMIT %s
        """
    )

    sort_column = sql.Identifier(sort_by)
    sort_direction = sql.SQL(sort_order.upper())

    formatted_query = query.format(
        sort_column=sort_column,
        sort_direction=sort_direction
    )

    results = execute_query(config, formatted_query, (min_date, min_date, site_name, site_name,
                                                      max_date, max_date, 
                                                      min_date, min_date, max_date, max_date, 
                                                      owner_id, owner_id,
                                                      site_name, site_name, limit))

    if headers:
        click.echo(
            "Site Name\tSite LUID\tView LUID\tView Name\tWorkbook Name\tProject Path\tAvg Duration (s)\t"
            "Total Views\tUnique Users\tOwner ID\tOwner Email\tOwner Name"
        )


    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t{row[2] or 'Unknown'}\t{row[3] or 'Unknown'}\t{row[4] or 'Unknown'}\t"
            f"{row[5] or 'Unknown'}\t{row[6] or 'N/A'}\t{row[7] or 0}\t{row[8] or 0}\t"
            f"{row[9] or 'Unknown'}\t{row[10] or 'Unknown'}\t{row[11] or 'Unknown'}"
        )


@find.command()
@click.option("--limit", default=10, help="Number of results to return")
@click.option("--min_usage_date", default=None, help="Minimum usage date in yyyy-mm-dd format")
@click.option("--max_usage_date", default=None, help="Maximum usage date in yyyy-mm-dd format")
@click.option("--min_update_date", default=None, help="Minimum update date in yyyy-mm-dd format")
@click.option("--max_update_date", default=None, help="Maximum update date in yyyy-mm-dd format")
@click.option("--headers/--no-headers", default=True, help="Display headers (default: on)")
@click.option("--owner_email", default=None, help="Filter by owner email")
@click.option("--min_size", default=None, type=float, help="Minimum size in MB")
@click.option("--max_size", default=None, type=float, help="Maximum size in MB")
@click.option("--min_views", default=None, type=int, help="Minimum number of views")
@click.option("--max_views", default=None, type=int, help="Maximum number of views")
@click.option("--min_users", default=None, type=int, help="Minimum number of unique users")
@click.option("--max_users", default=None, type=int, help="Maximum number of unique users")
@click.option("--sort_by", default="size_mb", help="Column to sort by")
@click.option("--sort_order", default="desc", type=click.Choice(['asc', 'desc']), help="Sort order")
@click.pass_context
def workbooks(
    ctx,
    limit,
    min_usage_date,
    max_usage_date,
    min_update_date,
    max_update_date,
    headers,
    owner_email,
    min_size,
    max_size,
    min_views,
    max_views,
    min_users,
    max_users,
    sort_by,
    sort_order,
):
    """Find workbooks with usage data"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT COALESCE(%s::date, MIN(time)::date) AS min_usage_date,
                   COALESCE(%s::date, MAX(time)::date) AS max_usage_date
            FROM views_stats
        ),
        workbook_usage AS (
            SELECT
                v.workbook_id,
                v.site_id,
                COUNT(DISTINCT d.user_id) AS unique_users,
                sum(nviews) AS total_views,
                max(time) last_accessed_at
            FROM views_stats d
            join views v
                on v.id = d.view_id
                and v.site_id = d.site_id
            cross join date_range dr
            WHERE d.time::date BETWEEN dr.min_usage_date AND dr.max_usage_date
            GROUP BY v.workbook_id, v.site_id
        ),
        project_path AS (
            WITH RECURSIVE project_hierarchy AS (
                SELECT
                    pc.site_id,
                    pc.content_id,
                    p.id AS project_id,
                    p.name AS project_name,
                    p.parent_project_id,
                    1 AS level,
                    p.name::character varying AS path
                FROM projects_contents pc
                JOIN projects p ON pc.project_id = p.id
                WHERE pc.content_type = 'workbook'
                UNION ALL
                SELECT
                    ph.site_id,
                    ph.content_id,
                    p.id,
                    p.name,
                    p.parent_project_id,
                    ph.level + 1,
                    (p.name || ' >> ' || ph.path)::character varying
                FROM project_hierarchy ph
                JOIN projects p ON ph.parent_project_id = p.id
                    AND ph.site_id = p.site_id
            )
            SELECT
                site_id,
                content_id,
                path AS full_project_path
            FROM project_hierarchy
            WHERE parent_project_id IS NULL
        )
        SELECT
            s.name AS site_name,
            s.luid as site_luid,
            w.name AS workbook_name,
            w.luid as workbook_luid,
            w.size / 1048576.0 AS size_mb,
            COALESCE(wu.unique_users, 0) AS unique_users,
            COALESCE(wu.total_views, 0) AS total_views,
            w.created_at,
            w.updated_at,
            COALESCE(pp.full_project_path, 'Top Level') AS project_path,
            su.name AS owner_id,
            su.friendly_name owner_name,
            su.email owner_email,
            dr.min_usage_date,
            dr.max_usage_date,
            wu.last_accessed_at
        FROM workbooks w
        JOIN sites s ON w.site_id = s.id
        left JOIN workbook_usage wu ON w.id = wu.workbook_id and w.site_id = wu.site_id
        LEFT JOIN project_path pp ON w.id = pp.content_id AND w.site_id = pp.site_id
        LEFT JOIN users o ON w.owner_id = o.id
        left join system_users su on su.id = o.system_user_id
        cross join date_range dr
        WHERE (%s::text IS NULL OR su.email = %s::text)
        AND (%s::float IS NULL OR w.size / 1048576.0 >= %s::float)
        AND (%s::float IS NULL OR w.size / 1048576.0 <= %s::float)
        AND (%s::int IS NULL OR COALESCE(wu.total_views, 0) >= %s::int)
        AND (%s::int IS NULL OR COALESCE(wu.total_views, 0) <= %s::int)
        AND (%s::int IS NULL OR COALESCE(wu.unique_users, 0) >= %s::int)
        AND (%s::int IS NULL OR COALESCE(wu.unique_users, 0) <= %s::int)
        AND (%s::date IS NULL OR w.updated_at::date >= %s::date)
        AND (%s::date IS NULL OR w.updated_at::date <= %s::date)
        ORDER BY 
            CASE 
                WHEN {sort_column} IS NULL THEN 1 
                ELSE 0 
            END,
            {sort_column} {sort_direction}
        LIMIT %s
        """
    )

    sort_column = sql.Identifier(sort_by)
    sort_direction = sql.SQL(sort_order.upper())

    formatted_query = query.format(
        sort_column=sort_column,
        sort_direction=sort_direction
    )

    results = execute_query(
        config,
        formatted_query,
        (
            min_usage_date,
            max_usage_date,
            owner_email,
            owner_email,
            min_size,
            min_size,
            max_size,
            max_size,
            min_views,
            min_views,
            max_views,
            max_views,
            min_users,
            min_users,
            max_users,
            max_users,
            min_update_date,
            min_update_date,
            max_update_date,
            max_update_date,
            limit,
        ),
    )

    if headers:
        click.echo(
            "Site Name\tSite ID\t"
            "Workbook Name\tWorkbook ID\t"
            "Size (MB)\tUnique Users\t"
            "Total Views\tCreated At\t"
            "Updated At\tProject Path\t"
            "Owner ID\tOwner Name\t"
            "Owner Email\tUsage Start Date\t"
            "Usage End Date\tLast Accessed At"
        )

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t"
            f"{row[2] or 'Unknown'}\t{row[3] or 'Unknown'}\t"
            f"{row[4]:.2f}\t{row[5]}\t"
            f"{row[6]}\t{row[7]}\t"
            f"{row[8]}\t{row[9] or 'Top Level'}\t"
            f"{row[10] or 'Unknown'}\t{row[11] or 'Unknown'}\t"
            f"{row[12] or 'Unknown'}\t{row[13] or 'Unknown'}\t"
            f"{row[14] or 'Unknown'}\t{row[15] or 'Unknown'}"
        )


@find.command()
@click.option("--limit", default=10, help="Number of results to return")
@click.option("--min_usage_date", default=None, help="Minimum usage date in yyyy-mm-dd format")
@click.option("--max_usage_date", default=None, help="Maximum usage date in yyyy-mm-dd format")
@click.option("--min_update_date", default=None, help="Minimum update date in yyyy-mm-dd format")
@click.option("--max_update_date", default=None, help="Maximum update date in yyyy-mm-dd format")
@click.option("--headers/--no-headers", default=True, help="Display headers (default: on)")
@click.option("--owner_email", default=None, help="Filter by owner email")
@click.option("--owner_id", default=None, help="Filter by owner ID")
@click.option("--min_size", default=None, type=float, help="Minimum size in MB")
@click.option("--max_size", default=None, type=float, help="Maximum size in MB")
@click.option("--min_views", default=None, type=int, help="Minimum number of views")
@click.option("--max_views", default=None, type=int, help="Maximum number of views")
@click.option("--sort_by", default="size_mb", help="Column to sort by")
@click.option("--sort_order", default="desc", type=click.Choice(['asc', 'desc']), help="Sort order")
@click.pass_context
def datasources(
    ctx,
    limit,
    min_usage_date,
    max_usage_date,
    min_update_date,
    max_update_date,
    headers,
    owner_email,
    owner_id,
    min_size,
    max_size,
    min_views,
    max_views,
    sort_by,
    sort_order,
):
    """Find datasources with usage data"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT COALESCE(%s::date, MIN(last_access_time)::date) AS min_usage_date,
                   COALESCE(%s::date, MAX(last_access_time)::date) AS max_usage_date
            FROM _datasources_stats
        ),
        datasource_usage AS (
            SELECT
                d.datasource_id,
                d.site_id,
                sum(nviews) AS total_views,
                max(last_access_time) last_accessed_at
            FROM _datasources_stats d
            join datasources v
                on v.id = d.datasource_id
                and v.site_id = d.site_id
            cross join date_range dr
            WHERE
                v.connectable
                and
                d.last_access_time::date BETWEEN dr.min_usage_date AND dr.max_usage_date
            GROUP BY d.datasource_id, d.site_id
        ),
        project_path AS (
            WITH RECURSIVE project_hierarchy AS (
                SELECT
                    pc.site_id,
                    pc.content_id,
                    p.id AS project_id,
                    p.name AS project_name,
                    p.parent_project_id,
                    1 AS level,
                    p.name::character varying AS path
                FROM projects_contents pc
                JOIN projects p ON pc.project_id = p.id
                WHERE pc.content_type = 'datasource'
                UNION ALL
                SELECT
                    ph.site_id,
                    ph.content_id,
                    p.id,
                    p.name,
                    p.parent_project_id,
                    ph.level + 1,
                    (p.name || ' >> ' || ph.path)::character varying
                FROM project_hierarchy ph
                JOIN projects p ON ph.parent_project_id = p.id
                    AND ph.site_id = p.site_id
            )
            SELECT
                site_id,
                content_id,
                path AS full_project_path
            FROM project_hierarchy
            WHERE parent_project_id IS NULL
        )
        SELECT
            s.name AS site_name,
            s.luid as site_luid,
            d.name AS datasource_name,
            d.luid as datasource_luid,
            d.size / 1048576.0 AS size_mb,
            COALESCE(du.total_views, 0) AS total_views,
            d.created_at,
            d.updated_at,
            COALESCE(pp.full_project_path, 'Top Level') AS project_path,
            su.name AS owner_id,
            su.friendly_name owner_name,
            su.email owner_email,
            dr.min_usage_date,
            dr.max_usage_date,
            du.last_accessed_at
        FROM datasources d
        JOIN sites s ON d.site_id = s.id
        left JOIN datasource_usage du
            ON d.id = du.datasource_id and d.site_id = du.site_id
        LEFT JOIN project_path pp ON d.id = pp.content_id AND d.site_id = pp.site_id
        LEFT JOIN users o ON d.owner_id = o.id
        left join system_users su on su.id = o.system_user_id
        cross join date_range dr
        WHERE (%s::text IS NULL OR su.email = %s::text)
        AND (%s::text IS NULL OR su.name = %s::text)
        AND (%s::float IS NULL OR d.size / 1048576.0 >= %s::float)
        AND (%s::float IS NULL OR d.size / 1048576.0 <= %s::float)
        AND (%s::int IS NULL OR COALESCE(du.total_views, 0) >= %s::int)
        AND (%s::int IS NULL OR COALESCE(du.total_views, 0) <= %s::int)
        AND (%s::date IS NULL OR d.updated_at::date >= %s::date)
        AND (%s::date IS NULL OR d.updated_at::date <= %s::date)
        AND d.connectable
        ORDER BY 
            CASE 
                WHEN {sort_column} IS NULL THEN 1 
                ELSE 0 
            END,
            {sort_column} {sort_direction}
        LIMIT %s
        """
    )

    sort_column = sql.Identifier(sort_by)
    sort_direction = sql.SQL(sort_order.upper())

    formatted_query = query.format(
        sort_column=sort_column,
        sort_direction=sort_direction
    )

    results = execute_query(
        config,
        formatted_query,
        (
            min_usage_date,
            max_usage_date,
            owner_email,
            owner_email,
            owner_id,
            owner_id,
            min_size,
            min_size,
            max_size,
            max_size,
            min_views,
            min_views,
            max_views,
            max_views,
            min_update_date,
            min_update_date,
            max_update_date,
            max_update_date,
            limit,
        ),
    )

    if headers:
        click.echo(
            "Site Name\tSite ID\t"
            "Datasource Name\tDatasource ID\t"
            "Size (MB)\t"
            "Total Views\tCreated At\t"
            "Updated At\tProject Path\t"
            "Owner ID\tOwner Name\t"
            "Owner Email\tUsage Start Date\t"
            "Usage End Date\tLast Accessed At"
        )

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t"
            f"{row[2] or 'Unknown'}\t{row[3] or 'Unknown'}\t"
            f"{row[4]:.2f}\t"
            f"{row[5]}\t{row[6]}\t"
            f"{row[7]}\t{row[8] or 'Top Level'}\t"
            f"{row[9] or 'Unknown'}\t{row[10] or 'Unknown'}\t"
            f"{row[11] or 'Unknown'}\t{row[12] or 'Unknown'}\t"
            f"{row[13] or 'Unknown'}\t{row[14] or 'Unknown'}"
        )



@cli.group()
def delete():
    """Delete various Tableau resources"""


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site LUID", help="Column name for Site LUID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option("--task-id-col", default="Task LUID", help="Column name for Task LUID")
@click.option("--task-name-col", default="Schedule Name", help="Column name for Task Name")
@click.option("--content-type-col", default="Content Type", help="Column name for Content Type")
@click.option("--content-name-col", default="Content Name", help="Column name for Content Name")
@click.option("--owner-name-col", default="Owner Name", help="Column name for Owner Name")
@click.pass_context
def tasks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    task_id_col,
    task_name_col,
    content_type_col,
    content_name_col,
    owner_name_col,
):
    """Delete Tableau tasks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        import sys
        csv_data = sys.stdin
    elif file:
        csv_data = open(file, "r", encoding="utf-8", newline="")
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        task_id = row[task_id_col]
        task_name = row[task_name_col]
        site_name = row[site_name_col]
        content_type = row[content_type_col]
        content_name = row[content_name_col]
        owner_name = row[owner_name_col]

        try:
            server.auth.switch_site(site)
            server.tasks.delete(task_id)
            click.echo(
                f"Successfully deleted task: {task_name} "
                f"(ID: {task_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Content: {content_type} - {content_name}")
            click.echo(f"Owner: {owner_name}")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting task {task_name} "
                f"(ID: {task_id}): {str(e)}",
                err=True,
            )
        except Exception as e:
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()



@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--workbook-id-col", default="Workbook ID", help="Column name for Workbook ID"
)
@click.option(
    "--workbook-name-col", default="Workbook Name", help="Column name for Workbook Name"
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def workbooks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    workbook_id_col,
    workbook_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau workbooks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        import sys

        csv_data = sys.stdin
    elif file:
        csv_data = open(file, "r", encoding="utf-8", newline="")
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        workbook_id = row[workbook_id_col]
        workbook_name = row[workbook_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.workbooks.delete(workbook_id)
            click.echo(
                f"Successfully deleted workbook: {workbook_name} "
                f"(ID: {workbook_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting workbook {workbook_name} "
                f"(ID: {workbook_id}): {str(e)}",
                err=True,
            )
        except Exception as e:
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--datasource-id-col", default="Datasource ID", help="Column name for Datasource ID"
)
@click.option(
    "--datasource-name-col",
    default="Datasource Name",
    help="Column name for Datasource Name",
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def datasources(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    datasource_id_col,
    datasource_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau datasources specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        import sys

        csv_data = sys.stdin
    elif file:
        csv_data = open(file, "r", encoding="utf-8", newline="")
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        datasource_id = row[datasource_id_col]
        datasource_name = row[datasource_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.datasources.delete(datasource_id)
            click.echo(
                f"Successfully deleted datasource: {datasource_name} "
                f"(ID: {datasource_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting datasource {datasource_name} "
                f"(ID: {datasource_id}): {str(e)}",
                err=True,
            )
        except Exception as e:
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()

@find.command()
@click.option("--limit", default=10, help="Number of results to return")
@click.option("--site", default=None, help="Filter by site name")
@click.option("--min-duration", default=None, type=float, help="Minimum average duration in minutes")
@click.option("--content-type", default=None, type=click.Choice(['Datasource', 'Workbook']), help="Filter by content type")
@click.option("--headers/--no-headers", default=True, help="Display headers (default: on)")
@click.pass_context
def tasks(ctx, limit, site, min_duration, content_type, headers):
    """Find slowest extract refresh tasks"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
WITH parsed_jobs AS (
    SELECT
        id,
        job_name,
        title,
        created_at,
        started_at,
        completed_at,
        progress,
        site_id,
        args,
        notes,
        finish_code,
        CASE
            WHEN args LIKE '%%- Datasource%%' THEN 'Datasource'
            WHEN args LIKE '%%- Workbook%%' THEN 'Workbook'
            ELSE 'Unknown'
        END AS content_type,
        (regexp_match(args, '- (?:Datasource|Workbook)\n- (\\d+)\n'))[1]::integer AS content_id,
        (regexp_match(args, '- \\d+\n- (.+)\n- \\d+\n'))[1] AS content_name,
        (regexp_match(args, '- \\d+\n- .+\n- (\\d+)\n'))[1]::integer AS task_id,
        run_now
    FROM background_jobs
    WHERE job_name = 'Refresh Extracts'
    AND progress = 100
    AND notes NOT LIKE '%%Suspended: skipped%%'
    AND finish_code = 0
),
job_stats AS (
    SELECT
        task_id,
        AVG(EXTRACT(EPOCH FROM (completed_at - started_at)) / 60) AS avg_duration_minutes
    FROM parsed_jobs
    GROUP BY task_id
)
SELECT
    t.luid task_luid,
    CASE
        WHEN t.state = 0 THEN 'Active'
        WHEN t.state = 1 THEN 'Suspended'
        WHEN t.state = 2 THEN 'Disabled'
        ELSE 'Unknown'
    END AS task_state,
    sch.name AS schedule_name,
    t.consecutive_failure_count,
    s.luid AS site_luid,
    s.name AS site_name,
    COALESCE(d.luid, w.luid) AS content_luid,
    COALESCE(d.name, w.name, 'Unknown') AS content_name,
    CASE
        WHEN t.obj_type = 'Datasource' THEN 'Datasource'
        WHEN t.obj_type = 'Workbook' THEN 'Workbook'
        ELSE 'Unknown'
    END AS content_type,
    COUNT(pj.id) AS job_count,
    AVG(EXTRACT(EPOCH FROM (pj.completed_at - pj.started_at)) / 60) AS avg_duration_minutes,
    AVG(EXTRACT(EPOCH FROM (pj.started_at - pj.created_at)) / 60) AS avg_queue_duration_minutes,
    MIN(pj.created_at) AS first_created_at,
    MAX(pj.created_at) AS last_run_timestamp,
    SUM(CASE WHEN pj.run_now = true THEN 1 ELSE 0 END) AS run_now_count,
    su_owner.name AS owner_name
FROM tasks t
JOIN sites s ON t.site_id = s.id
LEFT JOIN datasources d ON t.obj_id = d.id AND t.obj_type = 'Datasource'
LEFT JOIN workbooks w ON t.obj_id = w.id AND t.obj_type = 'Workbook'
LEFT JOIN users u ON COALESCE(d.owner_id, w.owner_id) = u.id AND COALESCE(d.site_id, w.site_id) = u.site_id
LEFT JOIN system_users su_owner ON u.system_user_id = su_owner.id
JOIN schedules sch ON t.schedule_id = sch.id
LEFT JOIN parsed_jobs pj ON t.id = pj.task_id
LEFT JOIN job_stats js ON t.id = js.task_id
WHERE t.type = 'RefreshExtractTask'
AND (%s::text IS NULL OR s.name = %s::text)
AND (%s::float IS NULL OR js.avg_duration_minutes >= %s::float)
AND (%s::text IS NULL OR t.obj_type = %s::text)
GROUP BY
    t.luid, t.state, t.consecutive_failure_count, s.luid, s.name, d.luid, w.luid, d.name,
    w.name, t.obj_type, su_owner.name, sch.name, js.avg_duration_minutes
ORDER BY js.avg_duration_minutes DESC
LIMIT %s
        """
    )

    results = execute_query(
        config,
        query,
        (site, site, min_duration, min_duration, content_type, content_type, limit),
    )

    if headers:
        click.echo(
            "Task LUID\tTask State\tSchedule Name\tConsecutive Failures\tSite LUID\tSite Name\t"
            "Content LUID\tContent Name\tContent Type\tJob Count\tAvg Duration (min)\t"
            "Avg Queue Duration (min)\tFirst Created At\tLast Run Timestamp\tRun Now Count\tOwner Name"
        )

    for row in results:
        # Handle None values explicitly before formatting.
        avg_duration_minutes = f"{row[10]:.2f}" if row[10] is not None else ""
        avg_queue_duration_minutes = f"{row[11]:.2f}" if row[11] is not None else ""
        
        click.echo(
            f"{row[0] or ''}\t{row[1] or ''}\t{row[2] or ''}\t{row[3] or ''}\t{row[4] or ''}\t{row[5] or ''}\t"
            f"{row[6] or ''}\t{row[7] or ''}\t{row[8] or ''}\t{row[9] or ''}\t"
            f"{avg_duration_minutes}\t"
            f"{avg_queue_duration_minutes}\t"
            f"{row[12] or ''}\t{row[13] or ''}\t{row[14] or ''}\t{row[15] or ''}"
        )

@cli.group()
def download():
    """Download various Tableau resources"""

@download.command()
@click.option("--site-name", default="Default", help="Name of the site containing the workbook")
@click.option("--project-name", default="Default", help="Name of the project containing the workbook")
@click.option("--workbook-name", required=True, help="Name of the workbook to download")
@click.option("--output-path", default=".", help="Path to save the downloaded workbook")
@click.pass_context
def workbook(ctx, site_name, project_name, workbook_name, output_path):
    """Download a Tableau workbook"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        # Switch to the specified site
        site = next((site for site in TSC.Pager(server.sites) if site.name == site_name), None)
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return
        server.auth.switch_site(site)

        # Find the workbook
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                         TSC.RequestOptions.Operator.Equals,
                                         workbook_name))
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.ProjectName,
                                         TSC.RequestOptions.Operator.Equals,
                                         project_name))
        matching_workbooks = list(TSC.Pager(server.workbooks, req_option))

        if not matching_workbooks:
            click.echo(f"Workbook '{workbook_name}' not found in project '{project_name}'", err=True)
            return

        workbook = matching_workbooks[0]

        # Download the workbook
        output_filename = f"{workbook_name}.twbx"
        output_path = os.path.join(output_path, output_filename)
        server.workbooks.download(workbook.id, output_path)
        click.echo(f"Workbook downloaded successfully: {output_path}")

    except Exception as e:
        click.echo(f"Error downloading workbook: {str(e)}", err=True)
    finally:
        server.auth.sign_out()


@download.command()
@click.option("--site-name", default="Default", help="Name of the site containing the flow")
@click.option("--project-name", default="Default", help="Name of the project containing the flow")
@click.option("--flow-name", required=True, help="Name of the flow to download")
@click.option("--output-path", default=".", help="Path to save the downloaded flow")
@click.pass_context
def flow(ctx, site_name, project_name, flow_name, output_path):
    """Download a Tableau flow"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        site = next((site for site in TSC.Pager(server.sites) if site.name == site_name), None)
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return
        server.auth.switch_site(site)

        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                         TSC.RequestOptions.Operator.Equals,
                                         flow_name))
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.ProjectName,
                                         TSC.RequestOptions.Operator.Equals,
                                         project_name))
        matching_flows = list(TSC.Pager(server.flows, req_option))

        if not matching_flows:
            click.echo(f"Flow '{flow_name}' not found in project '{project_name}'", err=True)
            return

        flow = matching_flows[0]

        output_filename = f"{flow_name}.tfl"
        output_path = os.path.join(output_path, output_filename)
        server.flows.download(flow.id, output_path)
        click.echo(f"Flow downloaded successfully: {output_path}")

    except Exception as e:
        click.echo(f"Error downloading flow: {str(e)}", err=True)
    finally:
        server.auth.sign_out()

## Download Datasource Command

@download.command()
@click.option("--site-name", default="Default", help="Name of the site containing the datasource")
@click.option("--project-name", default="Default", help="Name of the project containing the datasource")
@click.option("--datasource-name", required=True, help="Name of the datasource to download")
@click.option("--output-path", default=".", help="Path to save the downloaded datasource")
@click.pass_context
def datasource(ctx, site_name, project_name, datasource_name, output_path):
    """Download a Tableau datasource"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        site = next((site for site in TSC.Pager(server.sites) if site.name == site_name), None)
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return
        server.auth.switch_site(site)

        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                         TSC.RequestOptions.Operator.Equals,
                                         datasource_name))
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.ProjectName,
                                         TSC.RequestOptions.Operator.Equals,
                                         project_name))
        matching_datasources = list(TSC.Pager(server.datasources, req_option))

        if not matching_datasources:
            click.echo(f"Datasource '{datasource_name}' not found in project '{project_name}'", err=True)
            return

        datasource = matching_datasources[0]

        output_filename = f"{datasource_name}.tdsx"
        output_path = os.path.join(output_path, output_filename)
        server.datasources.download(datasource.id, output_path)
        click.echo(f"Datasource downloaded successfully: {output_path}")

    except Exception as e:
        click.echo(f"Error downloading datasource: {str(e)}", err=True)
    finally:
        server.auth.sign_out()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
