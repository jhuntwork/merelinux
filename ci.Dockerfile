ARG VERSION

FROM mere/base:v${VERSION}

RUN mere install cmake curl git llvm make mimalloc-dev musl-dev jq zig=0.16.0 && \
    rm -rf /mere/cache/packages/* /mere/cache/repos/*
