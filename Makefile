CODE_DIR = ./sdmay23-14/tests/Phase5/

.PHONY: CAN_CMAC_test

CAN_CMAC_test:
	$(MAKE) -C $(CODE_DIR)

clean:
	$(MAKE) -C $(CODE_DIR) clean