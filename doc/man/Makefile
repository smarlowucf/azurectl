header = AZURECTL User Manuals
buildroot = /
man_prefix = ${buildroot}/usr/share/man

all:
	for i in *.md; do \
		cat $$i | \
			pandoc -s -t man -f markdown_mmd |\
			sed -e 's@.TH ""@.TH "AZURECTL" "1" "" "${header}" ""@' |\
			gzip -f \
		> `echo $$i | sed -e s@.md@.1.gz@` ;\
	done

install:
	install -d -m 755 ${man_prefix}/man1
	for i in *.gz; do \
		install -m 644 $$i ${man_prefix}/man1 ;\
	done

clean:
	rm -f *.1.gz
