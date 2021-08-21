%global debug_package %{nil}

Name: operator-sdk
Epoch: 100
Version: 1.15.0
Release: 1%{?dist}
Summary: SDK for building Kubernetes applications
License: Apache-2.0
URL: https://github.com/operator-framework/operator-sdk/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.17
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
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.15.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.15.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=f6326e832a8a5e5453d0ad25e86714a0de2c0fc8 \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.21 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.15.0 \
        " \
        -o ./bin/operator-sdk ./cmd/operator-sdk && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.15.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.15.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=f6326e832a8a5e5453d0ad25e86714a0de2c0fc8 \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.21 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.15.0 \
        " \
        -o ./bin/ansible-operator ./cmd/ansible-operator && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.15.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.15.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=f6326e832a8a5e5453d0ad25e86714a0de2c0fc8 \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.21 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.15.0 \
        " \
        -o ./bin/helm-operator ./cmd/helm-operator

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/ansible-operator
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/helm-operator
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/operator-sdk
./bin/operator-sdk completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/operator-sdk

%files
%license LICENSE
%{_bindir}/ansible-operator
%{_bindir}/helm-operator
%{_bindir}/operator-sdk
%{_prefix}/share/bash-completion/completions/operator-sdk

%changelog
