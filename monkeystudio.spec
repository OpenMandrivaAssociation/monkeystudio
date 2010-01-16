%define beta b2
%define svn svn3482

Name: monkeystudio
Version: 1.8.4.0
Release: %mkrel -c %beta %{svn}.1
Summary: Free crossplatform Qt 4 IDE
Group: Development/KDE and Qt
License: GPLv3
URL: http://www.monkeystudio.org/
Source0: http://monkeystudio.googlecode.com/files/mks_%{version}%{beta}-%{svn}-src.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

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
%setup -q -n mks_%{version}%{beta}-%{svn}
chmod 0644 datas/templates/Python/PyQt\ Gui/{\$Form\ File\ Name\$.ui,template.ini,\$Project\ Name\$.xpyqt}
chmod 0644 datas/templates/Python/Qt\ Form/{\$Class\ Name\$.ui,template.ini}
chmod 0644 datas/templates/Python/PyQt\ Console/{template.ini,\$Project\ Name\$.xpyqt}
chmod 0644 datas/templates/Python/QObject\ Herited\ Class/template.ini
chmod 0644 plugins/interpreter/Python/src/*.{cpp,h}
chmod 0644 plugins/xup/PyQt/src/PyQt.{cpp,h}
chmod 0755 datas/apis/tags2api.py

sed -i -e 's/UpdateChecker//' plugins/base/base.pro

sed -i -e 's/\r//' 'datas/templates/Python/Qt Form/template.ini' 'datas/templates/Python/Qt Form/$Class Name$.ui' readme.txt 'datas/templates/Python/PyQt Gui/$Form File Name$.ui' dev-readme 'datas/apis/tags2api.py'
sed -i -e 's/\.ui/ui/' -e 's/\.moc/moc/' -e 's/\.rcc/rcc/' config.pri
sed -i -e 's/\.moc/moc/' plugins/plugins.pri

%build
%{qmake_qt4} prefix=%{_prefix} plugins=%{_libdir} system_qscintilla=1
%make

%install
rm -rf $RPM_BUILD_ROOT
%{qmake_qt4} prefix=%{_prefix} plugins=%{_libdir} system_qscintilla=1
make install INSTALL_ROOT=$RPM_BUILD_ROOT
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Doxyfile GPL-3 readme.txt dev-readme
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
