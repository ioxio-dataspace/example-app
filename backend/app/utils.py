from yarl import URL


def make_dsi(dataspace_base_domain: str, definition_path: str, source: str) -> str:
    """
    Construct a Data Source Identifier from the information on the request and token

    DSIs are URIs in the format: dpp://<source>@<dataspace_base_domain>/<data_definition>
    """

    # Data sources are identified on dataspaces as <group> or <group>:<variant>, which on the DSI URI correspond to a
    # "user" and an optional "password"
    user, _, password = source.partition(":")  # Extract group:source to URL properties

    if not password:
        # Passing the value None will not append it to the URL, whereas an empty string would be
        password = None

    # Use a URL builder to build the URI correctly
    #
    # Our expectation is that all the values are suitable for doing this with just string concatenation, however for
    # future proofing we want to do this a bit more carefully here.

    dsi_url = URL.build(
        scheme="dpp",
        host=dataspace_base_domain,
        path=definition_path,
        user=user,
        password=password,
    )

    return str(dsi_url)
