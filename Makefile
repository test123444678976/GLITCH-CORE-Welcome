PYTHON ?= python3
CC ?= cc
PREFIX ?= /usr
DESTDIR ?=
CFLAGS ?= -O2 -Wall -Wextra -Werror
BUILD_DIR := build
NATIVE_LIB := $(BUILD_DIR)/libglitch_system.so

.PHONY: all native run test check install clean
all: native

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

native: $(NATIVE_LIB)

$(NATIVE_LIB): src/core/system.c src/core/system.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -fPIC -shared -Isrc/core -o $@ src/core/system.c

run:
	$(PYTHON) src/main.py

test:
	$(PYTHON) -m unittest discover -s tests -v

check:
	$(PYTHON) -m py_compile src/main.py src/core/system_info.py
	$(PYTHON) src/main.py --version
	$(PYTHON) -m json.tool packaging/glitch-app.json > /dev/null

install: native
	install -d $(DESTDIR)$(PREFIX)/lib/glitch-welcome/src/core
	install -d $(DESTDIR)$(PREFIX)/lib/glitch-welcome/src/ui
	install -d $(DESTDIR)$(PREFIX)/bin
	install -d $(DESTDIR)$(PREFIX)/share/applications
	install -m 755 src/main.py $(DESTDIR)$(PREFIX)/lib/glitch-welcome/src/main.py
	install -m 644 src/core/system_info.py src/core/__init__.py $(DESTDIR)$(PREFIX)/lib/glitch-welcome/src/core/
	install -m 644 src/ui/style.css $(DESTDIR)$(PREFIX)/lib/glitch-welcome/src/ui/
	install -m 755 $(NATIVE_LIB) $(DESTDIR)$(PREFIX)/lib/glitch-welcome/libglitch_system.so
	printf '%s\\n' '#!/bin/sh' 'exec $(PYTHON) $(PREFIX)/lib/glitch-welcome/src/main.py "$$@"' > $(DESTDIR)$(PREFIX)/bin/glitch-welcome
	chmod 755 $(DESTDIR)$(PREFIX)/bin/glitch-welcome
	install -m 644 packaging/glitch-welcome.desktop $(DESTDIR)$(PREFIX)/share/applications/

clean:
	rm -rf $(BUILD_DIR) src/__pycache__ src/core/__pycache__ tests/__pycache__
