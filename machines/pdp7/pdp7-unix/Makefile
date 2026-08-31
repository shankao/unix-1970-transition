
include build/os.mk

DOCKER?=docker
SIMH_CONTAINERFILE=Containerfile.simh

all: buildit

.PHONY: emulator FORCE
emulator: build/pdp7

FORCE:

build/pdp7: $(SIMH_CONTAINERFILE) FORCE
	@set -eu; \
	export_dir=$$(mktemp -d); \
	staged_binary=; \
	image_tag=pdp7-unix-simh-artifact:build-$$$$; \
	trap 'rm -rf "$$export_dir"; \
		if test -n "$$staged_binary"; then rm -f "$$staged_binary"; fi; \
		if test -n "$$image_tag"; then $(DOCKER) image rm -f "$$image_tag" >/dev/null 2>&1 || true; fi' EXIT; \
	$(DOCKER) build --file $(SIMH_CONTAINERFILE) --target builder --tag "$$image_tag" .; \
	$(DOCKER) run --rm --volume "$$export_dir:/out" "$$image_tag" \
		/bin/sh -c 'cat /opt/pdp7.b64 >/out/pdp7.b64; cat /opt/pdp7.sha256 >/out/pdp7.sha256'; \
	$(DOCKER) image rm "$$image_tag" >/dev/null; \
	image_tag=; \
	staged_binary=$$(mktemp build/.pdp7.XXXXXX); \
	base64 --decode "$$export_dir/pdp7.b64" >"$$staged_binary"; \
	test "$$(sha256sum "$$staged_binary" | cut -d ' ' -f 1)" = "$$(cat "$$export_dir/pdp7.sha256")"; \
	chmod 0755 "$$staged_binary"; \
	test -x "$$staged_binary"; \
	file "$$staged_binary" | grep -q 'ELF 64-bit LSB'; \
	readelf -h "$$staged_binary" >/dev/null; \
	readelf -d "$$staged_binary" >"$$export_dir/pdp7.dynamic"; \
	! grep -q 'libpcre\.so' "$$export_dir/pdp7.dynamic"; \
	ldd "$$staged_binary" >"$$export_dir/pdp7.ldd"; \
	! grep -q 'not found' "$$export_dir/pdp7.ldd"; \
	strings "$$staged_binary" | grep -qx 'G2IN'; \
	strings "$$staged_binary" | grep -qx 'G2OUT'; \
	printf 'exit\n' >"$$export_dir/smoke.simh"; \
	"$$staged_binary" "$$export_dir/smoke.simh" >/dev/null; \
	mv -f "$$staged_binary" build/pdp7

buildit:
	cd build && $(MAKE) all

run:
	cd build && $(MAKE) run PDP7=./pdp7

alt:
	cd build && $(MAKE) alt

altrun:
	cd build && $(MAKE) altrun PDP7=./pdp7

clean:
	cd build && $(MAKE) clean

binaries: buildit
	mkdir -p binaries
	cp build/image.fs binaries/
	cp build/boot.rim binaries/
	cp build/unixv0.simh binaries/
