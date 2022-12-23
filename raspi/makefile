# config
DIR :="$(HOME)/workspace/mjpg-streamer/mjpg-streamer-experimental/"
DIST := $(shell lsb_release -a 2>/dev/null | awk '/Distributor/{print $$3}')

ifeq ($(DIST),Ubuntu)
  EXEC = python
else
  ifeq ($(DIST),Raspbian)
    EXEC = python3
  else
    $(error)
  endif
endif

# version
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell $(EXEC) --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
python_version_patch := $(word 3,${python_version_full})


all:

run:all
ifeq ($(python_version_major),3)
	$(EXEC) main.py
else
	@echo "!!! python vesrion should be 3.x !!!"
endif

clean:
	rm -rf *.pyc *.ini

stream:
	LD_LIBRARY_PATH=$(DIR) $(DIR)/mjpg_streamer -i "input_raspicam.so -fps 10 -q 20 -x 640 -y 480" -o "output_http.so -w $(DIR)/www -p 9000"