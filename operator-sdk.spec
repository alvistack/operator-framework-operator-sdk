# Copyright 2023 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: operator-sdk
Epoch: 100
Version: 1.27.0
Release: 1%{?dist}
Summary: SDK for building Kubernetes applications
License: Apache-2.0
URL: https://github.com/operator-framework/operator-sdk/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.20
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
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.27.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.27.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=5cbdad9209332043b7c730856b6302edc8996faf \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.25.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.27.0 \
        " \
        -o ./bin/operator-sdk ./cmd/operator-sdk && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.27.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.27.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=5cbdad9209332043b7c730856b6302edc8996faf \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.25.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.27.0 \
        " \
        -o ./bin/ansible-operator ./cmd/ansible-operator && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w \
            -X github.com/operator-framework/operator-sdk/internal/version.Version=v1.27.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitVersion=v1.27.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.GitCommit=5cbdad9209332043b7c730856b6302edc8996faf \
            -X github.com/operator-framework/operator-sdk/internal/version.KubernetesVersion=v1.25.0 \
            -X github.com/operator-framework/operator-sdk/internal/version.ImageVersion=v1.27.0 \
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