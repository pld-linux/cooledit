Summary:	Full featured multiple window programmer's text editor
Summary(pl):	Funkcjonalny edytor tekstu dla programistów
Name:		cooledit
Version:	3.11.0
Release:	1
Copyright:	GPL
Group:		Applications/Editors
Group(pl):	Aplikacje/Edytory
Source:		ftp://sunsite.unc.edu/pub/Linux/apps/editors/X/%{name}-%{version}.tar.gz
#Patch:		cooledit.patch
Icon:		cooledit.gif
BuildRoot:	/tmp/%{name}-%{version}-root

%description 
Full-featured X Window text editor; multiple edit windows; 3D Motif-ish
look and feel; shift-arrow and mouse text highlighting; column text
highlighting and manipulation; key for key undo; macro recording;
regular expression search and replace; pull-down menus; drag and drop;
interactive man page browser; run make and other shell commands with
seamless shell interface; redefine keys with an easy interactive key
learner; syntax highlighting for various file types; full support for
proportional fonts.

%prep
%setup -q
#%patch -p1

%build
%GNUconfigure

make

%install
rm -rf $RPM_BUILD_ROOT
make install-strip

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*

%find_lang %{name}

%post
 check if the command is already present:
if test -z "`grep coolicon %{_libdir}/X11/xinit/Xclients`" ; then
 estimate the speed of this machine:
    BOGOMIPS=`cat /proc/cpuinfo | grep bogomips | sed -e 's/^[^0-9]*//' -e 's/\..*$//'`
    BOGOMIPS="$BOGOMIPS"
    if test -z "$BOGOMIPS" ; then
	BOGOMIPS=50
    fi
    if test "$BOGOMIPS" -gt "500" ; then
	BOGOMIPS=500
    fi
 add use of shape extension if this is a fast machine:
    if test "$BOGOMIPS" -gt "80" ; then
	COOLICON_OPTIONS="-s -X $BOGOMIPS"
    else
	COOLICON_OPTIONS="-X $BOGOMIPS"
    fi

    cat > temp.Xclients <<EOF
#!/bin/bash

 coolicon needs an existing mail file, even if it is empty
MAILFILE=/var/spool/mail/\$LOGNAME
if test -f \$MAILFILE ; then
    cat /dev/null
else
    cat /dev/null > \$MAILFILE
    chmod 0600 \$MAILFILE
fi
coolicon $COOLICON_OPTIONS -M \$MAILFILE 2>&1 | coolmessage &

EOF
    cat temp.Xclients %{_libdir}/X11/xinit/Xclients > temp2.Xclients
    cp temp2.Xclients %{_libdir}/X11/xinit/Xclients
    chmod 0755 %{_libdir}/X11/xinit/Xclients
    rm temp.Xclients temp2.Xclients
fi


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ABOUT-NLS AUTHORS BUGS COPYING FAQ INSTALL INTERNATIONAL
%doc MAILING_LIST NEWS PROGRAMMING README TODO VERSION ChangeLog
%doc cooledit.lsm coolicon.lsm coolman.lsm

%attr(755,root,root) %{_libdir}/libCw.so*
%attr(755,root,root) %{_bindir}/*

%{_libdir}/libCw.la
%{_libdir}/libCw.a

%{_libdir}/coolicon/*

%{_mandir}/man1/*
