
# config
dist := $(shell lsb_release -a 2>/dev/null | \
    awk '/Distributor/{print $$3}')
host := 192.168.2.105
port := 8080
has_controller := true
has_cammera := true
has_arduino := true

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

conf:
	@echo '[settings]' > config.ini
	@echo 'host = $(host)' >> config.ini
	@echo 'port = $(port)' >> config.ini
	@echo '[flags]' >> config.ini
	@echo 'has_controller = $(has_controller)' >> config.ini
	@echo 'has_cammera = $(has_cammera)' >> config.ini
	@echo 'has_arduino = $(has_arduino)' >> config.ini

clean:
	rm -rf *.pyc *.ini
