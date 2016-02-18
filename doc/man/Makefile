header = AZURECTL User Manuals
buildroot = /
man_prefix = ${buildroot}/usr/share/man

all:
	for i in *.md; do \
		out=`echo $$i | sed -e s@.md@.1@` ;\
		pandoc -s -t man -f markdown_mmd $$i > $$out && \
		sed -i -e 's@.TH ""@.TH "AZURECTL" "1" "" "${header}" ""@' $$out && \
		gzip -f $$out || exit 1 ;\
	done

install:
	install -d -m 755 ${man_prefix}/man1
	for i in *.gz; do \
		install -m 644 $$i ${man_prefix}/man1 ;\
	done

show:
	zcat *.gz | nroff -man | less

clean:
	rm -f *.1
	rm -f *.1.gz
