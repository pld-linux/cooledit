Summary:	Full featured multiple window programmer's text editor
Summary(pl):	Funkcjonalny edytor tekstowy dla programistów
Name:		cooledit
Version:	3.6.2
Release:	1
Copyright:	GPL
Group:		Applications/Editors
Group(pl):	Aplikacje/Edytory
Source:		sunsite.unc.edu/pub/Linux/apps/editors/X/cooledit-3.6.2.tar.gz
Patch:		cooledit.patch
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
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s \
./configure %{_target} \
	--prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
make install-strip

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*

%post
 check if the command is already present:
if test -z "`grep coolicon /usr/lib/X11/xinit/Xclients`" ; then
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
    cat temp.Xclients /usr/lib/X11/xinit/Xclients > temp2.Xclients
    cp temp2.Xclients /usr/lib/X11/xinit/Xclients
    chmod 0755 /usr/lib/X11/xinit/Xclients
    rm temp.Xclients temp2.Xclients
fi


%files
%defattr(644, root, root, 755)
%doc ABOUT-NLS AUTHORS BUGS COPYING FAQ INSTALL INTERNATIONAL
%doc MAILING_LIST NEWS PROGRAMMING README TODO VERSION ChangeLog
%doc cooledit.lsm coolicon.lsm coolman.lsm

%attr(755, root, root) /usr/lib/libCw.so*
%attr(755, root, root) /usr/bin/*

/usr/lib/libCw.la
/usr/lib/libCw.a

/usr/lib/coolicon/*

/%lang(cs)usr/share/locale/cs/LC_MESSAGES/cooledit.mo
/%lang(da)usr/share/locale/da/LC_MESSAGES/cooledit.mo
/%lang(de)usr/share/locale/de/LC_MESSAGES/cooledit.mo
/%lang(es)usr/share/locale/es/LC_MESSAGES/cooledit.mo
/%lang(fi)usr/share/locale/fi/LC_MESSAGES/cooledit.mo
/%lang(fr)usr/share/locale/fr/LC_MESSAGES/cooledit.mo
/%lang(it)usr/share/locale/it/LC_MESSAGES/cooledit.mo
/%lang(ja)usr/share/locale/ja/LC_MESSAGES/cooledit.mo
/%lang(ko)usr/share/locale/ko/LC_MESSAGES/cooledit.mo
/%lang(nl)usr/share/locale/nl/LC_MESSAGES/cooledit.mo
/%lang(no)usr/share/locale/no/LC_MESSAGES/cooledit.mo
/%lang(pl)usr/share/locale/pl/LC_MESSAGES/cooledit.mo
/%lang(pt)usr/share/locale/pt/LC_MESSAGES/cooledit.mo
/%lang(sl)usr/share/locale/sl/LC_MESSAGES/cooledit.mo
/%lang(sv)usr/share/locale/sv/LC_MESSAGES/cooledit.mo

%{_mandir}/man1/*

%changelog
- built for PLD based on spec by anonim
