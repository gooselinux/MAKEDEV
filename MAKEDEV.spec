Name: MAKEDEV
Version: 3.24
Release: 6%{?dist}
Group: System Environment/Base
License: GPLv2
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source: MAKEDEV-%{version}-1.tar.gz
Summary: A program used for creating device files in /dev
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libselinux-devel
URL: http://www.lanana.org/docs/device-list/
Requires(pre): shadow-utils, /usr/bin/getent

%description
This package contains the MAKEDEV program, which makes it easier to create
and maintain the files in the /dev directory.  /dev directory files
correspond to a particular device supported by Linux (serial or printer
ports, scanners, sound cards, tape drives, CD-ROM drives, hard drives,
etc.) and interface with the drivers in the kernel.

You should install the MAKEDEV package because the MAKEDEV utility makes
it easy to manage the /dev directory device files.

%prep
%setup -q

%build
make OPTFLAGS="$RPM_OPT_FLAGS" SELINUX=1

%install
make install DESTDIR=$RPM_BUILD_ROOT devdir=/dev makedevdir=/sbin
rm -f $RPM_BUILD_ROOT/dev/MAKEDEV

%clean
rm -fr $RPM_BUILD_ROOT

%pre
# Add the floopy group and the vcsa user.
getent group floppy >/dev/null || groupadd -g 19 -r -f floppy
getent group vcsa >/dev/null || groupadd -g 69 -r -f vcsa
getent passwd vcsa >/dev/null || \
	useradd -r -g vcsa -d /dev -s /sbin/nologin -u 69 \
	-c "virtual console memory owner" vcsa 2>/dev/null
exit 0

%files
%defattr(-,root,root)
%doc COPYING devices-2.6+.txt
%{_mandir}/man8/*
%{_sbindir}/mksock
/sbin/MAKEDEV
%config(noreplace) %{_sysconfdir}/makedev.d

%changelog
* Fri Jun 18 2010 Chris Lumens <clumens@redhat.com> 3.24-6
- Change user/group creation for new shadow-utils behavior.
  Resolves: rhbz#594092

* Tue Mar 30 2010 Chris Lumens <clumens@redhat.com> - 3.24-5
- Fix pkgwrangler warnings
  Related: rhbz#543948.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 08 2009 Robert Scheck <robert@fedoraproject.org> 3.24-3
- Hardcoded temporarily the release tag in package source tag

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Chris Lumens <clumens@redhat.com> 3.24-1
- Fix speed up patch (jakub, #466485).

* Thu Oct 09 2008 Dave Airlie <airlied@redhat.com> 3.23-7
- Add bootup speed up patch from Jakub

* Fri Sep 19 2008 Dave Airlie <airlied@redhat.com> 3.23-6
- make it boot faster by renaming a bunch of 00 files into a better order

* Mon Jun 16 2008 Jesse Keating <jkeating@redhat.com> - 3.23-5
- Make sure we have getent installed for our %%pre section.

* Mon Mar 03 2008 Chris Lumens <clumens@redhat.com> 3.23-4
- Change license to GPLv2 only.
- minor cleanups for merge review (Todd Zullinger <tmz@pobox.com>):
  - rpmlint warnings fixed:
    - buildprereq and prereq use
    - quoted macros in %%changelog
    - summary-ended-with-dot
  - create vcsa user and floppy group according to packaging guidelines
    (Packaging/UsersAndGroups)
  - note that we are upstream for MAKEDEV above the source tag
  - bring BuildRoot tag in line with the packaging guidelines
  - remove grep and mktemp from Require

* Mon Feb 25 2008 Jeremy Katz <katzj@redhat.com> - 3.23-3
- Add fix to build with gcc 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.23-2.2
- Autorebuild for GCC 4.3

* Mon Jul 17 2006 Nalin Dahyabhai <nalin@redhat.com> - 3.23-1.2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.23-1.1
- rebuild

* Tue Jun 20 2006 Nalin Dahyabhai <nalin@redhat.com> 3.23-1
- update to 15 May devices-2.6+.txt:
  - remove pktcdvd*
  - add ttyJ0
  - add ptlsec

* Thu May  4 2006 Nalin Dahyabhai <nalin@redhat.com> 3.22-1
- update to 1 March devices-2.6+.txt:
  - add ttyEQ*

* Mon Feb 13 2006 Nalin Dahyabhai <nalin@redhat.com> 3.21-3
- rebuild

* Tue Feb  7 2006 Nalin Dahyabhai <nalin@redhat.com> 3.21-2
- rebuild

* Thu Jan 26 2006 Nalin Dahyabhai <nalin@redhat.com> 3.21-1
- update to 4 January devices-2.6+.txt:
  - add ttyNX*
- document how conflicting rules are resolved
- batch rename configuration files to allow third-parties to override rules
  more dependably

* Thu Dec 22 2005 Nalin Dahyabhai <nalin@redhat.com> 3.20-3
- actually get the name of the file right

* Thu Dec 22 2005 Nalin Dahyabhai <nalin@redhat.com> 3.20-2
- actually include the devices.txt file which corresponds to the 2.6 kernel

* Fri Dec 16 2005 Nalin Dahyabhai <nalin@redhat.com> 3.20-1
- update to 28 November devices-2.6+.txt:
  - rename ttyUB* to rfcomm*
  - rename cuub* to curf*
  - add ttyPSC*
  - add ttyAT*
  - add rfd*

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- remove /dev/MAKEDEV to build with newest rpm

* Thu Jul 21 2005 Nalin Dahyabhai <nalin@redhat.com> 3.19-3
- rebuild

* Thu Jul 21 2005 Nalin Dahyabhai <nalin@redhat.com> 3.19-2
- move usb-specific config file out, go with the mainline devices-2.6+.txt file
- update to 12 May devices-2.6+.txt:
  - add usb/legousbtower
  - add xvd
  - rename ttyIOC4 to ttyIOC
  - add 32 more ttyIOC nodes
  - add ttySIOC

* Thu Mar 17 2005 Nalin Dahyabhai <nalin@redhat.com> 3.19-1
- skip over subdirectories in /etc/makedev.d (#150766) instead of spitting
  out an error (or warning, if -i was used) and quitting

* Tue Mar 15 2005 Nalin Dahyabhai <nalin@redhat.com> 3.18-1
- update to 10 February devices-2.6+.txt:
  - remove vtx
  - remove vttunner
  - add mga_vid
  - add infiniband
  - add biometrics
  - add ttyVR,cuvr
  - add ipath
- restruct symlink target creation to exact (-X) mode

* Thu Jan 20 2005 Nalin Dahyabhai <nalin@redhat.com> 3.17-1
- update to 7 January 2005 devices.txt:
  - add midishare
- move cpu/*/microcode to cpu/microcode to match udev's behavior (#144887)
- create targets of symlinks if they don't exist

* Tue Dec 21 2004 Nalin Dahyabhai <nalin@redhat.com> 3.16-3
- raise number of loop devices from 16 to 256 (Kenneth Lee)
- create 'vmware' alias for vnet,vmnet,vmmon devices
- change vmnet->vnet to vmnet0->vnet0, so that it isn't left dangling

* Wed Dec  8 2004 Nalin Dahyabhai <nalin@redhat.com> 3.16-2
- remove ataraid devices (#140175)

* Mon Nov 29 2004 Nalin Dahyabhai <nalin@redhat.com> 3.16-1
- allow devices to be specified either as "device" or "devdir"[/]"device"
- update to 22 November 2004 devices.txt:
  - add fuse
  - add ttyCPM,cucpm
  - add ttyIOC4,cuioc4
  - rename user-mode block devices to avoid conflict with ub block device

* Fri Nov 12 2004 Nalin Dahyabhai <nalin@redhat.com> 3.15-3
- rebuild

* Fri Nov 12 2004 Nalin Dahyabhai <nalin@redhat.com> 3.15-2
- rebuild

* Fri Nov 12 2004 Nalin Dahyabhai <nalin@redhat.com> 3.15-1
- set the file creation context for symlinks as well (#138897)
- verify the file context for symlinks as well
- use lgetfilecon instead of getfilecon so that we don't chase symlinks when
  determining the current context of a file (Dan Walsh)
- update to 27 October 2004 devices.txt:
  - remove msd* devices
  - add ub* devices
- comment out ubd* (98/0) devices for now, would conflict with a ub block
  device (180/24)
- handle symlink-already-exists errors

* Tue Oct 19 2004 Nalin Dahyabhai <nalin@redhat.com> 3.14-1
- update to 20 September 2004 devices.txt:
  - add ttyMM devices (no callout devices)
  - move inftl* devices from major 94 to major 96
  - move msd* devices from major 96 to major 95
  - move dasd* devices from major 95 to major 94
- drop the number of vnet nodes from 16 to 9
- make vmnet* a link to vnet*
- fix -n, -v

* Tue Sep 14 2004 Nalin Dahyabhai <nalin@redhat.com> 3.13-1
- excise all architecture-specific logic and configuration data -- udev knows
  no arch-specific details, so they should be irrelevant now
- remove build conflicts on older RPM, unnecessary now that dev is gone
- remove dev's %%post fstab munging
- add a short-circuit test for the common non-match cases

* Tue Sep 14 2004 Jeremy Katz <katzj@redhat.com> - 3.12.2-1
- add the vcsa user and floppy group in the MAKEDEV package now (#132595)

* Mon Sep 13 2004 Nalin Dahyabhai <nalin@redhat.com> 3.12.1-1
- nuke the "dev" subpackage

* Tue Sep  7 2004 Nalin Dahyabhai <nalin@redhat.com> 3.12-1
- add a -a (alwayscreate) flag, to skip checking if the device node is already
  present with the desired permissions/ownership/context
- add a -u (udev permissions) flag, to spit out udev-style permissions settings
  for whatever nodes we would be creating

* Mon Sep  6 2004 Nalin Dahyabhai <nalin@redhat.com>
- add a context-directory flag, for using contexts assigned to devices created
  in the -d directory look like they would if it was the -D directory
- create intermediate subdirectories in exact (-x) mode

* Sat Sep  4 2004 Nalin Dahyabhai <nalin@redhat.com>
- don't even try to reset the default file creation context if SELinux
  is disabled (#131776)

* Thu Sep  2 2004 Nalin Dahyabhai <nalin@redhat.com>
- add usb/lcd, usb/brlvgr* from current usb.devices.txt (#69729); drops the
  number of dabusb devices from 16 to 4

* Thu Sep  2 2004 Nalin Dahyabhai <nalin@redhat.com> 3.11-1
- add an exact (-x) flag, for creating exactly one device at a time

* Wed Sep  1 2004 Nalin Dahyabhai <nalin@redhat.com> 3.10-1
- set SELinux contexts when creating device nodes, sockets, and intermediate
  directories
- turn on SELinux support at build-time

* Tue Aug 31 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9.2-1
- remove the MAKEDEV symlink from /dev, which allows removal of the %%pre
  scriptlet (#131075)
- make storage devices group-read-only (#110197)

* Mon Aug 30 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 30 August 2004 devices.txt:
  - give ttySMX callout devices non-conflicting names
- point man page to /sbin instead of /dev

* Thu Aug 26 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9.1-1
- update to 04 August 2004 devices.txt:
  - rename xfs0 to nnpfs0
  - replace solnp*/solnpctl* with ica*
  - add emd, hpet, drbd, ttySMX
- fix ieee1394/dv/PAL/out

* Wed Aug 25 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9-1
- 3.8.4 should have been a major revision
- remove /dev/kmem (#117692)
- teach MAKEDEV about dv1394 stuff (#127061)
- make rfcomm0 and rfcomm1 symlinks to ttyUB0 and ttyUB1, respectively (#88802)
- mksock: print usage information in cases of unrecognized arguments (#105440)

* Wed Aug 25 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.4-1
- move MAKEDEV to /sbin with a symlink from /dev (#116009)
- don't bother looking up the owners of symlinks, we don't use them

* Thu Jul 29 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.3-1
- use the correct permissions on /dev/ttySG0 and /dev/cusg0

* Wed Jul 28 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.2-1
- create /dev/ttySG0 and /dev/cusg0 (Erik Jacobson)

* Thu Jun 24 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.1-1
- create sx8 device nodes

* Mon Jun 21 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8-1
- rename /dev/carmel to /dev/sx8 (Jeff Garzik)

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 3.7-3
- hvsi* should be on ppc/ppc64, not s390 (David Howells)

* Mon Jun 14 2004 Nalin Dahyabhai <nalin@redhat.com> 3.7-2
- add hvsi0 and hvsi1 devices on s390 (David Howells)

* Wed Jun 09 2004 Karsten Hopp <karsten@redhat.de> 3.7-1 
- sort devices for a better overview (s390)
- add scsi devices for zfcp disks (s390)

* Sun May 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- simplify the pre script for MAKEDEV/dev

* Wed May  5 2004 Nalin Dahyabhai <nalin@redhat.com> 3.6-1
- Cleanups: don't require that the owning user or group exist when invoked
  with -M, because we don't care.

* Wed May  5 2004 Nalin Dahyabhai <nalin@redhat.com> 3.5-1
- Fix crashes when users and groups specified as owners in configuration files
  don't exist (Jim Gifford).
- Create /dev/adb and /dev/pmu devices (#119265)

* Mon Mar 29 2004 Nalin Dahyabhai <nalin@redhat.com> 3.4-1
- Bump version for kernel 2.6.
- Create /dev/mce_log on x86_64.
- Create /dev/kmsg everywhere.
- Create /dev/carmel disk nodes.
- Make vsys a symlink to aio (was renamed to aio).

* Wed Mar 10 2004 Phil Knirsch <pknirsch@redhat.com> 3.3.14-1
- Rebuilt for RHEL3 U2.

* Mon Feb 23 2004 Nalin Dahyabhai <nalin@redhat.com> 3.3.13-1
- Make MAKEDEV use ":" to separate user and group names in output created when
  invoked with the -S flag (patch by Tim Waugh).

* Wed Jan 21 2004 Phil Knirsch <pknirsch@redhat.com> 3.3.12-1
- Added missing scsi devices for s390(x).

* Tue Jan 20 2004 Phil Knirsch <pknirsch@redhat.com> 3.3.11-1
- Added back the /dev/tty* files on s390(x), needed for expect.

* Mon Jan 12 2004 Nalin Dahyabhai <nalin@redhat.com> 3.3.10-1
- raise the default number of sg devices from 32 to 256 (kernel has no
  hard-coded limit) (#104816)

* Thu Dec 18 2003 Than Ngo <than@redhat.com> 3.3.9-2
- add the correct alsa device name 

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 3.3.9-1
- ALSA device nodes

* Mon Sep 15 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.8-2
- rebuild

* Mon Sep 15 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.8-1
- apply patch from Matt Wilson to raise the number of raw devices from 128
  to 255

* Fri Aug 22 2003 Bill Nottingham <notting@redhat.com> 3.3.7-1
- make /dev/hvc0 a real file

* Fri Aug 15 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.6-2
- rebuild

* Fri Aug 15 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.6-1
- apply patch from Matt Wilson to make /dev/hvc0 a link to iseries/vtty0
- include the nvram and hvc0 devices on ppc/ppc64

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.5-2
- rebuild

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.5-1
- finish update to latest devices.txt
  moves /dev/3270/tty* from major 228 to 227
  moves /dev/3270/tub* from major 227 to 228

* Tue May 13 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.4-1
- update to latest devices.txt (renames smapi to thinkpad/thinkpad, adds
  systrace, tpm, pps, etherd/, spi/, usb/usblcd, usb/cpad0)

* Mon Apr 28 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.3-1
- replace libraw1394 config file with newer information from
  www.linux1394.org (#88170)

* Sat Feb 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sanitize dev rpm scripts

* Thu Jan 30 2003 Phil Knirsch <pknirsch@redhat.com>  3.3.2-5
- Removed too many tty devices for s390(x). Fixed.
- Removed mdsp* and logicalco devices for s390(x).

* Wed Jan 29 2003 Phil Knirsch <pknirsch@redhat.com> 3.3.2-3
- Updated number of dasd devices we create for s390(x) (64 now).
- Removed all unecessary /dev/tty?.? entries for s390(x).

* Mon Jan 27 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.2-2
- rebuild

* Wed Jan  8 2003 Nalin Dahyabhai <nalin@redhat.com> 3.3.2-1
- update to latest devices.txt (renames intel_rng to hwrng and adds ttyB*)

* Tue Sep 17 2002 Guy Streeter <streeter@redhat.com>
- include the /dev/iseries devices on ppc64

* Fri Aug 30 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3.1-2
- build nosst devices (#72914)

* Tue Jul 09 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3.1-1
- build the tunnelling device (/dev/net/tun)
- add configuration for libraw1394 (#67203)

* Tue Jul 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix SPARC build, patch from Jakub Jelinek <jakub@redhat.com>

* Tue May 28 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-7
- rebuild

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-6
- build 32 scsi generic devices
- add cfs device used by coda

* Thu May  9 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-5
- resync with current LANANA updates, remove ibcs config file
- resync with usb device list

* Tue Apr 23 2002 Nalin Dahyabhai <nalin@redhat.com>
- resync with current LANANA updates, heads-up from John Cagle
- create kpoll and 16 scramdisk devices

* Thu Apr 11 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-4
- build the package the same way for the superuser as we did before,
  preventing problems when building as root when some of the device
  owners don't exist on the build host

* Thu Mar 28 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-3
- set the /dev/vcs* devices to be owned by the vcsa user, and create the
  vcsa user

* Tue Mar 19 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-2
- rebuild

* Tue Mar 19 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3-1
- handle a step of 0 when creating multiple nodes
- add /dev/cpu/*/microcode (perms 0600) to the dev package

* Thu Feb 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2-12
- rebuild

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2-11
- up the limit on ide devices (hda through hdt) back up from 17 to 33 -- I'm
  told it works now

* Mon Jan 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2-10
- build for Raw Hide

* Mon Jan 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2-9
- actually create the vsys device

* Mon Jan 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2-8
- build for Raw Hide

* Mon Jan 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2-7
- aio/vsys rename courtesy of Ben LaHaise

* Thu Aug 30 2001 Nalin Dahyabhai <nalin@redhat.com> 3.2-6
- fix markup errors in the man page (no bug ID, reported by
  esr@snark.thyrsus.com)

* Thu Aug 30 2001 Nalin Dahyabhai <nalin@redhat.com> 3.2-5
- char 10/208 is cpqphpc, not cpqphpcp (#52910)
- add compaq/ devices (#52898)
- add information about raw1394 and video1394 devices (#52736)

* Fri Aug 17 2001 Karsten Hopp <karsten@redhat.de>
- add tape390 devices

* Tue Aug 14 2001 Karsten Hopp <karsten@redhat.de>
- clean up all those ifnarch s390 clauses

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- bring in line with devices.txt from 3 June 2001
- create dri devices

* Wed Jul 18 2001 Tim Powers <timp@redhat.com>
- rebuilt using new rpm that actually does %%dev correctly

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak the manifest handling to also build when RPM doesn't know
  about them
- add a -S option to spit out shell script snippets
- only claim that we need to create a particular directory once
- fix descriptions for i2o/hdd[i-p], which were wrong
- break generic and architecture-specific sections apart in %%install

* Sun Jul 15 2001 Jeff Johnson <jbj@redhat.com>
- generate device manifest with MAKEDEV -M to build as non-root.

* Wed Jul 11 2001 Bill Nottingham <notting@redhat.com>
- add proper prereqs to dev package for %%post (#48769)

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- disable unneeded parts of post for s390,s390x

* Sun Jul 01 2001 Karsten Hopp <karsten@redhat.de>
- S390-only changes -- added missing devices

* Fri Jun 29 2001 Karsten Hopp <karsten@redhat.de>
- added missing /dev/null on S390

* Wed Jun 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- back out some changes, move documentation for dasd device numbers elsewhere

* Wed Jun 27 2001 Karsten Hopp <karsten@redhat.de>
- move 2 S390 patches into CVS, console-patch has to stay or it
  would break other archs

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- create the first four /dev/osst devices (#35833)
- only 7 partitions for DAC960 disks, not 8 (#31484)
- add ataraid device nodes (#44807)
- add a "raid" alias for all raid devices (#33117)
- update the man page

* Tue Jun 26 2001 Bill Nottingham <notting@redhat.com>
- add /dev/shm to fstab too

* Thu Jun 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- own %%{_sysconfdir}/makedev.d in addition to files it contains

* Wed Jun 21 2001 Karsten Hopp <karsten@redhat.de>
- correct device naming and major/minor numbers on S390

* Fri Jun  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix a bug in creation of leading directories when a format specifier is
  included in the directory's name
- zero-fill the buffer before we pass it to readlink()
- don't try to create /dev/ixj*; the device isn't present in 2.4
- limit number of each device in /dev/input to 32

* Thu May 31 2001 Nalin Dahyabhai <nalin@redhat.com>
- increase the number of lp and parport devices from 3 to 8

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- make apm devices (apm_bios)
- make fancy beeper device (beep)

* Wed Apr 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- only make devices for two floppy drives instead of eight
- limit the number of cui devices to 16 instead of 64
- limit the number isdn and ippp devices to 16
- limit the number of nb devices to 32 (matches md)
- limit the number of st and nst devices to 16

* Fri Mar 23 2001 Nalin Dahyabhai <nalin@redhat.com> 
- make all devices for all RAID controllers again

* Mon Mar 12 2001 Nalin Dahyabhai <nalin@redhat.com> 
- make aliases for ide5 through ide9
- limit the number of console and console-related devices to 32
- run pam_console_apply in the post, if it exists

* Mon Mar  5 2001 Nalin Dahyabhai <nalin@redhat.com> 
- use a file manifest

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com> 
- drop the number of hdX devices from 33 to 17, on advice from Andre Hedrick

* Thu Mar  1 2001 Nalin Dahyabhai <nalin@redhat.com> 
- make js0, js1, js2, js3 symlinks into /dev/input so that all programs use
  the new input-core joystick driver instead of the old one

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com> 
- detect devfs in the MAKEDEV %%pre, too (#26110)
- fix message in the dev %%pre (#26110)

* Fri Feb 16 2001 Nalin Dahyabhai <nalin@redhat.com> 
- build the netlink device (#15785)

* Sun Feb 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- merge in s390 s390x support

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- fail to install if %%pre detects devfs

* Thu Jan 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- create /dev in the %%pre script; installing the dev package should fixup
  the permissions, and we can't redirect to /dev/null without it (#24392)

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- make /dev/aio world-writable (info from Ben LeHaise)

* Wed Jan 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- add device nodes using the new devices.txt for Linux 2.4.0, and check that
  file into the source tree to make tracking further changes simpler
- change Copyright: GPL to License: GPL
- add a very simple substitution macro facility for specifying ownership and
  permissions in a single place
- add code for creating sockets natively
- remove conflicting data for where /dev/ftape should point to
- remove all raid controller device nodes for second and additional controllers
  (they can be created with MAKEDEV)

* Tue Jan  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- make 32 partition devices for IDE disks instead of 16

* Tue Dec 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- make some ppp devices

* Thu Oct 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- change vcs0 to vcs (ditto for vcsa0)

* Tue Sep 12 2000 Bill Nottingham <notting@redhat.com>
- fixes for some sparc devices that fell out

* Thu Aug 24 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- change some devices that could be used for dialing to root:uucp/0660 perms

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- up the number of SCSI CD-ROM devices we know about from 8 to 32, but only
  create 8 at build-time

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove both temp files generated in the %%post (#16325)

* Mon Aug 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- change the sense of sga/sg0 node/symlink stuff to match kernel docs (#16056)

* Wed Aug  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the netlink device, and mark it as undocumented (#15785)
- add /dev/log socket as a ghost using Erik's mksocket
- add in devices that start with "m"
- change /dev/i20 to /dev/i2o
- fix a parser bug

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- add cciss device nodes (#14878)

* Mon Aug  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- make the usb lp? devices group-owned by 'lp'

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- make floppy disk devices group-accessible by the floppy group

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- stop making bogus symlinks (#14225)
- add "console" alias for tty devices to match man page
- add "qic" alias for tape devices to match man page

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- change group of the "lp" devices to "lp"
- comment out the ACSI disks, which probably shouldn't have those names
- incorporate the release number into the tarball file name

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix symlink creation where both the link and a target are in a subdirectory
- add efirtc in its own "ia64" control file

* Wed Jul  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a -i flag so that I can test in a CVS checkout
- use correct IBCS compatibility device entries
- fix symlink creation so that it works as intended

* Tue Jul  4 2000 Matt Wilson <msw@redhat.com>
- moved the Prereq: /usr/sbin/groupadd from the MAKEDEV package to the
  dev package
- added the %%post script to the dev package to add devpts mounting

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- make the man page 644, not 755

* Mon Jun 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update from 8 to 16 loop devices

* Mon Jun 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- add input/mice and md devices to the dev package
- limit loop devices to 16 in config files (this is a hard-coded kernel limit)

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the "floppy" group to the system in the dev package's pre-install

* Mon Jun 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix a typo in the devices list
- move non-standard names from linux-2.2 list to redhat list

* Sat Jun 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS packaging for a shiny new version
