PYTHON ?= python3
CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -Werror
BUILD_DIR := build
NATIVE_LIB := $(BUILD_DIR)/libglitch_system.so

.PHONY: all native run test check clean
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

clean:
	rm -rf $(BUILD_DIR) src/__pycache__ src/core/__pycache__ tests/__pycache__
