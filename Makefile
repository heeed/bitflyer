ECHO = @echo
PYTHON = python

QSTR_DEFS = inc/py/qstrdefs.h inc/microbit/qstrdefsport.h

HEX_SRC = build/bbc-microbit-classic-gcc-nosd/source/microbit-micropython.hex
HEX_FINAL = build/firmware.hex

deploy: build/final.hex
	automator tools/deploy.workflow

build/final.hex: build/bitflyer.py
	tools/makecombinedhex.py $(HEX_FINAL) build/bitflyer.py > build/final.hex

build/bitflyer.py: yotta bitflyer/*.py
	cat bitflyer/*.py > build/bitflyer.py.full
	pyminifier build/bitflyer.py.full > build/bitflyer.py

#bitflyer/imgs.py: bitflyer/images/* tools/imgconvert.py
#	tools/imgconvert.py bitflyer/images > bitflyer/imgs.py

yotta: inc/genhdr/qstrdefs.generated.h
	@yt build
	@/bin/cp $(HEX_SRC) $(HEX_FINAL)

# Note: we need to protect the qstr names from the preprocessor, so we wrap
# the lines in "" and then unwrap after the preprocessor is finished.
inc/genhdr/qstrdefs.generated.h: $(QSTR_DEFS) tools/makeqstrdata.py inc/microbit/mpconfigport.h inc/py/mpconfig.h
	$(ECHO) "Generating $@"
	@cat $(QSTR_DEFS) | sed 's/^Q(.*)/"&"/' | $(CPP) -Iinc -Iinc/microbit - | sed 's/^"\(Q(.*)\)"/\1/' > build/qstrdefs.preprocessed.h
	@$(PYTHON) tools/makeqstrdata.py build/qstrdefs.preprocessed.h > $@

serial:
	@picocom /dev/ttyACM0 -b 115200
