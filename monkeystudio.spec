%define Werror_cflags %nil

Name: monkeystudio

Version: 1.9.0.2
Release: 1
Summary: Free crossplatform Qt 4 IDE
Group: Development/KDE and Qt
License: GPLv3
URL: http://www.monkeystudio.org/
Source0: https://monkeystudio.googlecode.com/files/mks_%{version}-src.tar.gz

BuildRequires:  qt4-devel >= 4.4.0
BuildRequires:  desktop-file-utils
BuildRequires:  qscintilla-qt4-devel

%description
MonkeyStudio is a crossplatform Integrated Development Environment ( IDE )
aiming to become a Rapid Application Development ( RAD ) environment.
MonkeyStudio runs everywhere Qt 4.4.0 ( minimum required to build it )
is available as a shared library. It is extensible via a great and powerful
plugin system which help make it do nearly anything you want and support
virtually any kind of project type for which a plugin exists or is created.
The primary goal of MonkeyStudio was to manage Qt4 projects as best
as possible, it directly uses .pro files and does not create intrusive or
unsightly configuration files. MonkyStudio is also a multi language
code editor too ( javascript, xml, ... ).

%prep
%setup -q -n mks_%{version}-src
# Fix files permissions
find monkey/src -type f -exec chmod 0644 {} \;
find datas/templates/ -type f -exec chmod 0644 {} \;
find plugins/ -type f -exec chmod 0644 {} \;
chmod 0755 datas/apis/Tools/tags2api.py

# For the "hidden files" rpmlint warning
sed -i -e 's/\.ui/ui/' -e 's/\.moc/moc/' -e 's/\.rcc/rcc/' config.pri
sed -i -e 's/\.ui/ui/' -e 's/\.moc/moc/' -e 's/\.rcc/rcc/' plugins/plugins.pri

# End of file encoding
sed -i -e 's/\r//' dev-readme 'datas/templates/Python/Qt Form - Single Inheritance/$Class Name$.ui' 'datas/templates/C++/Qt Form - No Inheritance/$Class Name$.ui' 'datas/templates/Python/PyQt Gui/$Form File Name$.ui'

# UpdateChecker is removed because yum will take care of updates
sed -i -e 's/UpdateChecker//' plugins/base/base.pro

# Remove automatic doc install to let the spec file do it
sed -i -e 's/INSTALL.*monkey_docs$/INSTALLS = monkey_datas/' installs.pri


%build
%{qmake_qt4} prefix=%{_prefix} plugins=%{_libdir} system_qscintilla=1
%make

%install
rm -rf %{buildroot}
%{qmake_qt4} prefix=%{_prefix} plugins=%{_libdir} system_qscintilla=1
make install INSTALL_ROOT=%{buildroot}
desktop-file-install --vendor="" \
  --dir %{buildroot}%{_datadir}/applications/ \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc Doxyfile GPL-3 readme.txt dev-readme
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
