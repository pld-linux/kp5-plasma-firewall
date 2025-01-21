#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.27.12
%define		qtver		5.15.2
%define		kpname		plasma-firewall
%define		kf5ver		5.39.0

Summary:	plasma-firewall
Name:		kp5-%{kpname}
Version:	5.27.12
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	ce90288f17b4ac49f9fd6b16fc1cdcb2
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.0
BuildRequires:	Qt5DBus-devel >= 5.15.0
BuildRequires:	Qt5Gui-devel >= 5.15.0
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Qml-devel
BuildRequires:	Qt5Quick-devel >= 5.15.0
BuildRequires:	Qt5X11Extras-devel
BuildRequires:	Qt5Xml-devel >= 5.15.0
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	kf5-kauth-devel >= 5.82
BuildRequires:	kf5-kcmutils-devel
BuildRequires:	kf5-kconfig-devel >= 5.82
BuildRequires:	kf5-kcoreaddons-devel >= 5.85.0
BuildRequires:	kf5-kdeclarative-devel >= 5.82
BuildRequires:	kf5-ki18n-devel >= 5.82
BuildRequires:	kf5-plasma-framework-devel >= 5.82
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires:	python3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Plasma 5 Firewall KCM.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_libdir}/libkcm_firewall_core.so
%dir %{_libdir}/qt5/plugins/kf5/plasma_firewall
%{_libdir}/qt5/plugins/kf5/plasma_firewall/firewalldbackend.so
%{_libdir}/qt5/plugins/kf5/plasma_firewall/ufwbackend.so
%attr(755,root,root) %{_prefix}/libexec/kauth/kde_ufw_plugin_helper
%attr(755,root,root) %{_prefix}/libexec/kde_ufw_plugin_helper.py
%{_datadir}/dbus-1/system-services/org.kde.ufw.service
%{_datadir}/dbus-1/system.d/org.kde.ufw.conf
%dir %{_datadir}/kcm_ufw
%{_datadir}/kcm_ufw/defaults
%{_datadir}/kpackage/kcms/kcm_firewall
%{_datadir}/metainfo/org.kde.plasma.firewall.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.ufw.policy
%{_libdir}/qt5/plugins/plasma/kcms/systemsettings/kcm_firewall.so
%{_desktopdir}/kcm_firewall.desktop
