
# config
dist := $(shell lsb_release -a 2>/dev/null | \
    awk '/Distributor/{print $$3}')

ifeq ($(dist),Ubuntu)
  exec = python
  host = $(shell ifconfig wlan0 | \
    awk '/inet/{print $$1}' | \
    sed -e '/inet6/d' | \
    awk -F: '{print $$2}')
else
  ifeq ($(dist),Raspbian)
    exec = python3
  else
    $(error)
  endif
endif

# version
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell $(exec) --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
python_version_patch := $(word 3,${python_version_full})


all:

run:all
ifeq ($(python_version_major),3)
	$(exec) main.py
else
	@echo "!!! python vesrion should be 3.x !!!"
endif

clean:
	rm -rf *.pyc *.ini
