Summary:	Full featured multiple window programmer's text editor
Summary(pl):	Funkcjonalny edytor tekstu dla programistów
Name:		cooledit
Version:	3.17.7
Release:	1
License:	GPL
Group:		Applications/Editors
Source0:	http://cooledit.sourceforge.net/%{name}-%{version}.tar.gz
# Source0-md5:	06e16994ebc2108e04dc7c6bd29981de
URL:		http://cooledit.sourceforge.net/
BuildRequires:	XFree86-devel
Requires(post):	/sbin/ldconfig
Requires(post):	coreutils
Requires(post):	grep
Requires(post):	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Full-featured X Window text editor; multiple edit windows; 3D
Motif-ish look and feel; shift-arrow and mouse text highlighting;
column text highlighting and manipulation; key for key undo; macro
recording; regular expression search and replace; pull-down menus;
drag and drop; interactive man page browser; run make and other shell
commands with seamless shell interface; redefine keys with an easy
interactive key learner; syntax highlighting for various file types;
full support for proportional fonts.

%description -l pl
Cooledit to pe³nowarto¶ciowy edytor tekstowy dla systemu X Window.
Jego najistotniejsze cechy to: obs³uga wielu okien edycyjnych,
zaznaczanie tekstu za pomoc± strza³ek z shiftem i myszki, motifowy
wygl±d, kolumnowe zaznaczanie i modyfikacja tekstu, wielopoziomowe
undo, nagrywanie makr, wyszukiwanie i zamiana za pomoc± wyra¿eñ
regularnych, menu, "przeci±gnij i upu¶æ", interaktywna przegl±darka
stron podrêcznika systemowego (man), uruchamianie make oraz innych
poleceñ za pomoc± zintegrowanego interfejsu pow³oki, redefiniowanie
klawiszy za pomoc± interaktywnego narzêdzia, pod¶wietlanie sk³adni
rozmaitych typów plików, pe³na obs³uga fontów proporcjonalnych.

%prep
%setup -q

%build
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no -devel package, so useless
rm -f $RPM_BUILD_ROOT%{_libdir}/libCw.{so,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
# check if the command is already present:
if test -z "`grep coolicon %{_libdir}/X11/xinit/Xclients`" ; then
# estimate the speed of this machine:
	BOGOMIPS=`cat /proc/cpuinfo | grep bogomips | sed -e 's/^[^0-9]*//' -e 's/\..*$//'`
	BOGOMIPS="$BOGOMIPS"
	if test -z "$BOGOMIPS" ; then
		BOGOMIPS=50
	fi
	if test "$BOGOMIPS" -gt "500" ; then
		BOGOMIPS=500
	fi
# add use of shape extension if this is a fast machine:
	if test "$BOGOMIPS" -gt "80" ; then
		COOLICON_OPTIONS="-s -X $BOGOMIPS"
	else
		COOLICON_OPTIONS="-X $BOGOMIPS"
	fi

	cat > temp.Xclients <<EOF
#!/bin/sh

# coolicon needs an existing mail file, even if it is empty
MAILFILE=/var/mail/\$LOGNAME
if test -f \$MAILFILE ; then
	coolicon $COOLICON_OPTIONS -M \$MAILFILE 2>&1 | coolmessage &
fi
EOF
	cat temp.Xclients %{_libdir}/X11/xinit/Xclients > temp2.Xclients
	cp -f temp2.Xclients %{_libdir}/X11/xinit/Xclients
	chmod 0755 %{_libdir}/X11/xinit/Xclients
	rm -f temp.Xclients temp2.Xclients
fi

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS FAQ INTERNATIONAL
%doc MAILING_LIST NEWS PROGRAMMING README TODO VERSION ChangeLog
%doc cooledit.lsm coolicon.lsm coolman.lsm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libCw.so.*.*.*
%{_datadir}/coolicon
%{_datadir}/cooledit
%{_mandir}/man1/*
