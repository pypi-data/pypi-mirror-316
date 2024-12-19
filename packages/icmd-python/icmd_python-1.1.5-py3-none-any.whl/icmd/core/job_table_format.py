"""Format strings in the job table."""


def make_clickable(url):
    """Make a URL clickable."""
    url = url.lstrip("/")
    return f'<a href="https://server.questek.com/icmd/{url}">Link</a>'


def beautify_job_status(status: str):
    """Beautify job status."""
    if status == "successful":
        return (
            '<span style="color:white; display:inline-block; padding:5px; '
            'background-color:rgb(46, 125, 50)">Successful</span>'
        )
    if status == "failed":
        return (
            '<span style="color:white; display:inline-block; padding:5px; '
            'background-color:rgb(211, 47, 47)">Failed</span>'
        )
    if status == "running":
        return (
            '<span style="color:white; display:inline-block; padding:5px; '
            'background-color:rgb(237, 108, 2)">Running</span>'
        )
    if status == "submitted":
        return (
            '<span style="color:white; display:inline-block; padding:5px; '
            'background-color:rgb(55, 111, 208)">Submitted</span>'
        )
    return status


def beautify_datetime(value: str) -> str:
    """Beautify datetime string."""
    if isinstance(value, str):
        return value.split(".")[0].replace("T", " ")
    return str(value)


qt_job_table_style = {
    "icmd": make_clickable,
    "job_status": beautify_job_status,
    "job_started_at": beautify_datetime,
    "job_finished_at": beautify_datetime,
    "created_at": beautify_datetime,
}
