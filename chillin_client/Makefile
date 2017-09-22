# Makefile

.PHONY: all gen

KOALASC = koalasc
MESSAGE_SRC = "helpers/messages.ks"
GENERATED_PROG_LANG = python
GENERATED_MESSAGE_DIR = "helpers"


all: gen

gen:
	$(KOALASC) $(MESSAGE_SRC) $(GENERATED_PROG_LANG) $(GENERATED_MESSAGE_DIR)
