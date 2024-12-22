# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

RUN apt update -y && apt install -y libcairo2

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD pyproject.toml /app
ADD uv.lock /app
ADD tests/ /app
ADD src/ /app
ADD LICENSE /app
ADD *.md /app
ADD .python-version /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Uncomment for debugging
# RUN apt install -y curl jq libxml2-utils gnupg2 procps less nano iputils-ping

# When running the container, start the Starbridge MCP server
# But feel free to add arguments and options as needed when doing a docker run
ENTRYPOINT ["uv", "run", "--no-dev", "starbridge"]