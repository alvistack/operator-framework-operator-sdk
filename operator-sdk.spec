%global debug_package %{nil}

Name: operator-sdk
Epoch: 100
Version: 1.19.1
Release: 1%{?dist}
Summary: SDK for building Kubernetes applications
License: Apache-2.0
URL: https://github.com/operator-framework/operator-sdk/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: go >= 1.18
BuildRequires: glibc-static

%description
The Operator SDK is a framework that uses the controller-runtime library
to make writing operators easier by providing:
  - High level APIs and abstractions to write the operational logic more
    intuitively
  - Tools for scaffolding and code generation to bootstrap a new project
    fast
  - Extensions to cover common Operator use cases

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.19.1 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.19.1 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=079d8852ce5b42aa5306a1e33f7ca725ec48d0e3 \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.23 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.19.1 \
        " \
        -o ./bin/operator-sdk ./cmd/operator-sdk && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.19.1 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.19.1 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=079d8852ce5b42aa5306a1e33f7ca725ec48d0e3 \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.23 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.19.1 \
        " \
        -o ./bin/ansible-operator ./cmd/ansible-operator && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.19.1 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.19.1 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=079d8852ce5b42aa5306a1e33f7ca725ec48d0e3 \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.23 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.19.1 \
        " \
        -o ./bin/helm-operator ./cmd/helm-operator

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/*
./bin/ansible-operator completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/ansible-operator
./bin/helm-operator completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/helm-operator
./bin/operator-sdk completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/operator-sdk

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
