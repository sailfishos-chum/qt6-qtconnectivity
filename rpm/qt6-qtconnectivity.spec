%global  qt_version 6.7.2

Summary: Qt6 - Connectivity components
Name:    qt6-qtconnectivity
Version: 6.7.2
Release: 0%{?dist}

# See LICENSE.GPL3, respectively, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt.io
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_qt6_archdatadir}/qml/.*\\.so$

BuildRequires: cmake
BuildRequires: clang
BuildRequires: ninja
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{vqt_ersion}
BuildRequires: qt6-qtbase-private-devel >= %{qt_version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel >= %{qt_version}
BuildRequires: pkgconfig(bluez)
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: openssl-devel

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt6_libexecdir}/sdpscanner
%{_qt6_libdir}/libQt6Bluetooth.so.6*
%{_qt6_libdir}/libQt6Nfc.so.6*

%files devel
%{_qt6_headerdir}/QtBluetooth/
%{_qt6_libdir}/libQt6Bluetooth.so
%{_qt6_libdir}/libQt6Bluetooth.prl
%{_qt6_headerdir}/QtNfc/
%{_qt6_libdir}/libQt6Nfc.so
%{_qt6_libdir}/libQt6Nfc.prl
%dir %{_qt6_libdir}/cmake/Qt6Bluetooth/
%dir %{_qt6_libdir}/cmake/Qt6Nfc/
%{_qt6_libdir}/cmake/Qt6/FindBlueZ.cmake
%{_qt6_libdir}/cmake/Qt6/FindPCSCLITE.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_qt6_libdir}/cmake/Qt6Bluetooth/*.cmake
%{_qt6_libdir}/cmake/Qt6Nfc/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_bluetooth*.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_nfc*.pri
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/pkgconfig/*.pc
