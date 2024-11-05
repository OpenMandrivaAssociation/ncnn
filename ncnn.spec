%global upstream Tencent
%global gitbase  https://github.com

%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

Summary: High-performance neural network inference framework
Name:    ncnn
Version: 20240820
Release: 1
License: BSD-3-Clause
#Group:   System/Libraries
URL:     %{gitbase}/%{upstream}/%{name}
Source0: %{gitbase}/%{upstream}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:  tools-cmake_cxx_standard_17.patch
Patch1:  tools-protobuf-shared-libs-workaround.patch

BuildRequires: cmake
BuildRequires: glslang
BuildRequires: ninja
BuildRequires: cmake(glslang)
BuildRequires: cmake(OpenMP)
BuildRequires: cmake(Protobuf)
BuildRequires: cmake(SPIRV-Tools)
BuildRequires: pkgconfig(vulkan)

%description
%{ncnn} is a high-performance neural network inference computing framework optimized for mobile platforms.

%package -n %{libname}
Summary:  %{summary}
#Group:    %{group}
Provides: %{name} = %{version}-%{release}

%description -n %{libname}
This package contains the %{name} runtime libraries.

%package -n %{devname}
Summary:  %{summary}
#Group:    %{group}
Requires: %{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the %{name} development headers and libraries.

%package -n %{name}-tools
Summary:  %{summary}
#Group:    %{group}
Requires: %{libname} = %{version}-%{release}

%description -n %{name}-tools
This package contains the %{name} tools.

%prep
%autosetup -p 1
%cmake -G Ninja \
       -DCMAKE_BUILD_TYPE=Release \
       -DNCNN_ENABLE_LTO=ON \
       -DNCNN_SHARED_LIB=ON \
       -DNCNN_SYSTEM_GLSLANG=ON \
       -DNCNN_VULKAN=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}*

%files -n %{devname}
%doc README.md
%license LICENSE.txt
%{_includedir}/%{name}
%{_libdir}/lib%{name}*.so
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}*

%files -n %{name}-tools
%{_bindir}/*%{name}*
