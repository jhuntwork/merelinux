ARG VERSION

FROM mere/base:v${VERSION}

RUN mere install cmake curl git llvm make mimalloc-dev musl-dev openssh-client rsync zig && \
    rm -rf /mere/cache/packages/* /mere/cache/repos/*
